"""
Pydantic models for the AI Quiz Generator.
Defines all request/response schemas.
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ─── Document Models ─────────────────────────────────────────────

class PageChunk(BaseModel):
    """A chunk of text extracted from one or more PDF pages."""
    text: str
    page_start: int
    page_end: int
    chunk_index: int

    @property
    def source_reference(self) -> str:
        if self.page_start == self.page_end:
            return f"Page {self.page_start}"
        return f"Pages {self.page_start}-{self.page_end}"


class DocumentInfo(BaseModel):
    """Response after successful PDF upload."""
    document_id: str
    filename: str
    page_count: int
    chunk_count: int
    total_characters: int
    status: str = "extracted"


# ─── Quiz Models ─────────────────────────────────────────────────

class Question(BaseModel):
    """A single quiz question."""
    id: str
    type: Literal["multiple_choice", "true_false", "short_answer"]
    question: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    source_reference: str  # e.g. "Page 4, Section 2.1"


class Quiz(BaseModel):
    """A complete quiz with metadata."""
    id: str
    title: str
    source_filename: str
    questions: List[Question]
    difficulty: Literal["easy", "medium", "hard"]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    num_questions: int = 0

    def model_post_init(self, __context):
        if self.num_questions == 0:
            self.num_questions = len(self.questions)


# ─── Request Models ──────────────────────────────────────────────

class QuizGenerationRequest(BaseModel):
    """Request to generate a quiz from an uploaded document."""
    document_id: str
    num_questions: Literal[5, 10, 20] = 10
    difficulty: Literal["easy", "medium", "hard"] = "medium"


class AnswerSubmission(BaseModel):
    """User's submitted answers for scoring."""
    answers: Dict[str, str]  # question_id → user_answer


# ─── Response Models ─────────────────────────────────────────────

class QuestionResult(BaseModel):
    """Result for a single question after scoring."""
    question_id: str
    question_text: str
    question_type: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    source_reference: str
    options: Optional[List[str]] = None


class QuizResult(BaseModel):
    """Complete quiz scoring result."""
    quiz_id: str
    score: int
    total: int
    percentage: float
    grade: str
    results: List[QuestionResult]


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    details: Optional[str] = None
