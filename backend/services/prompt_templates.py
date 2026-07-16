"""
System and User Prompt templates for Anthropic Claude to generate a quiz from PDF text chunks.
"""

SYSTEM_PROMPT = """You are an expert educator and quiz builder. Your task is to analyze the provided document content and generate high-quality, pedagogically sound quiz questions.

You must output ONLY valid JSON matching the specified JSON schema. Do not include any explanation, conversational text, markdown formatting (do NOT use ```json or ```), or extra symbols outside the raw JSON object. If you violate this rule, the parser will fail.
"""

QUIZ_GENERATION_PROMPT = """Generate a quiz based on the following document text.

DOCUMENT CONTENT:
{document_text}

---

PARAMETERS:
- Number of questions: {num_questions}
- Difficulty level: {difficulty} (Ensure the language, complexity of options, and depth of knowledge required matches this difficulty)
- Mix of Question Types:
  * multiple_choice (4 options, exactly one correct option)
  * true_false (options should be ["True", "False"], correct_answer must be either "True" or "False")
  * short_answer (open-ended question; correct_answer should be a concise exemplar answer)

Each question MUST include:
1. A unique, short ID (e.g. "q1", "q2", "q3", etc.)
2. The question type
3. The question text
4. Options (only for multiple_choice and true_false, null/omitted for short_answer)
5. The correct answer
6. A brief explanation of why the answer is correct and why other options are incorrect (if applicable)
7. A source page/section reference (e.g. "Page 4", "Pages 2-3") based on the page markers in the document.

You MUST respond with a JSON object matching this schema structure:
{{
  "id": "generated_quiz_id",
  "title": "A fitting title for the quiz based on the content",
  "source_filename": "{source_filename}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "id": "q1",
      "type": "multiple_choice",
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option B",
      "explanation": "Explanation here.",
      "source_reference": "Page 5"
    }},
    {{
      "id": "q2",
      "type": "true_false",
      "question": "Question text here?",
      "options": ["True", "False"],
      "correct_answer": "True",
      "explanation": "Explanation here.",
      "source_reference": "Page 6"
    }},
    {{
      "id": "q3",
      "type": "short_answer",
      "question": "Question text here?",
      "options": null,
      "correct_answer": "Exemplar correct answer here.",
      "explanation": "Explanation here.",
      "source_reference": "Page 7"
    }}
  ]
}}

Ensure all JSON string values containing double quotes are properly escaped with backslashes. Do not wrap the JSON output in markdown code blocks. Start directly with {{ and end with }}.
"""

JSON_CORRECTION_PROMPT = """The JSON output you previously generated failed to parse or did not match the required schema.
Parsing Error details:
{error_details}

Here is the malformed output you provided:
{malformed_output}

Please fix the formatting and output only the corrected JSON. Ensure all keys match the schema, all double quotes inside JSON string values are properly escaped, and no markdown formatting (like ```json) is used.
"""
