"""
Quiz Generation Service using the modern Google GenAI SDK.
Interfaces with Google Gemini 3.5 Flash to generate structured quiz JSON.
"""

import os
import json
import uuid
from typing import List, Dict, Any
from google import genai
from google.genai import types

from models.schemas import Quiz, Question, PageChunk
from services.prompt_templates import SYSTEM_PROMPT, QUIZ_GENERATION_PROMPT

def get_gemini_client() -> genai.Client:
    """Initialize and return the modern Google GenAI Client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise ValueError("GEMINI_API_KEY is not configured in environment variables.")
    return genai.Client(api_key=api_key)

def parse_and_validate_quiz(raw_json: str, filename: str, difficulty: str) -> Dict[str, Any]:
    """
    Parses clean JSON string and validates/standardizes the quiz structure.
    """
    data = json.loads(raw_json)
    
    # Standardize basic root keys
    if "questions" not in data or not isinstance(data["questions"], list):
        raise ValueError("JSON missing 'questions' list at root level.")
        
    # Standardize individual questions
    for idx, q in enumerate(data["questions"]):
        if not isinstance(q, dict):
            raise ValueError(f"Question at index {idx} is not a valid dictionary.")
            
        # Check required fields
        required_fields = ["type", "question", "correct_answer", "explanation"]
        for field in required_fields:
            if field not in q:
                raise ValueError(f"Question at index {idx} missing required field '{field}'.")
                
        # Generate ID if missing or duplicate
        if "id" not in q or not q["id"]:
            q["id"] = f"q_{idx + 1}_{str(uuid.uuid4())[:4]}"
            
        # Ensure options field exists for multiple choice and true_false
        q_type = q.get("type")
        if q_type == "multiple_choice":
            if "options" not in q or not isinstance(q["options"], list) or len(q["options"]) < 2:
                q["options"] = ["A", "B", "C", "D"]  # Fallback
        elif q_type == "true_false":
            q["options"] = ["True", "False"]
        else:
            q["options"] = None
            
        # Ensure source reference exists
        if "source_reference" not in q or not q["source_reference"]:
            q["source_reference"] = "Unknown Page"
            
    # Standardize main level
    if "id" not in data or not data["id"]:
        data["id"] = str(uuid.uuid4())
    if "title" not in data or not data["title"]:
        data["title"] = f"Quiz on {filename}"
        
    data["source_filename"] = filename
    data["difficulty"] = difficulty
    
    return data

def generate_quiz_from_chunks(
    filename: str,
    chunks: List[PageChunk],
    num_questions: int,
    difficulty: str
) -> Quiz:
    """
    Generates a full Quiz from document chunks using Google Gemini 3.5 Flash.
    Always merges the content to run in 1 API call to prevent rate limiting (429).
    """
    client = get_gemini_client()
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
    
    # Merge all chunk texts. Gemini 3.5 Flash has a 1M token context limit,
    # so we can easily fit the whole document in 1 call, avoiding multiple rapid 429 requests.
    merged_text = "\n\n".join([c.text for c in chunks])
    
    prompt = QUIZ_GENERATION_PROMPT.format(
        document_text=merged_text,
        num_questions=num_questions,
        difficulty=difficulty,
        source_filename=filename
    )
    
    print(f"Generating {num_questions} {difficulty} questions using {model_name}...")
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    
    quiz_data = parse_and_validate_quiz(response.text, filename, difficulty)
    
    # Map questions to pydantic Question list
    questions_list = []
    for q in quiz_data.get("questions", []):
        questions_list.append(Question(**q))
        
    return Quiz(
        id=quiz_data.get("id", str(uuid.uuid4())),
        title=quiz_data.get("title", f"Quiz: {filename.replace('.pdf', '')}"),
        source_filename=filename,
        questions=questions_list,
        difficulty=difficulty,
        num_questions=len(questions_list)
    )
