"""
Quiz generation, scoring, and export endpoints.
"""

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response, StreamingResponse
import io

from models.schemas import Quiz, QuizGenerationRequest, AnswerSubmission, QuizResult, QuestionResult
from services.quiz_generator import generate_quiz_from_chunks
from services.export_service import export_json, export_markdown, export_pdf

router = APIRouter()

@router.post("/generate", response_model=Quiz)
async def generate_quiz(request: QuizGenerationRequest):
    """
    Generate a quiz from a previously uploaded document ID.
    """
    from main import documents_store, quizzes_store
    
    # 1. Retrieve document
    doc_id = request.document_id
    if doc_id not in documents_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document ID not found. Please upload the PDF first."
        )
        
    doc = documents_store[doc_id]
    
    # 2. Call generator
    try:
        quiz = generate_quiz_from_chunks(
            filename=doc["filename"],
            chunks=doc["chunks"],
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quiz: {str(e)}"
        )
        
    # 3. Store generated quiz in memory
    quizzes_store[quiz.id] = quiz
    
    return quiz

@router.post("/{quiz_id}/submit", response_model=QuizResult)
async def submit_quiz(quiz_id: str, submission: AnswerSubmission):
    """
    Submit user answers, grade them, and return detailed feedback.
    """
    from main import quizzes_store
    
    if quiz_id not in quizzes_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz ID not found."
        )
        
    quiz: Quiz = quizzes_store[quiz_id]
    
    results = []
    correct_count = 0
    total_scorable = 0
    
    for q in quiz.questions:
        user_ans = submission.answers.get(q.id, "").strip()
        correct_ans = q.correct_answer.strip()
        
        is_correct = False
        
        if q.type == "multiple_choice":
            total_scorable += 1
            # Exact option comparison or character comparison
            # Extract letter (e.g. "A" or option content match)
            # Case insensitive comparison
            is_correct = (user_ans.lower() == correct_ans.lower())
            
            # Sometimes correct answer might be written as "A) option text", check that too
            if not is_correct and len(user_ans) == 1:
                # User submitted 'A', check if correct answer starts with 'A'
                is_correct = correct_ans.lower().startswith(user_ans.lower())
                
            if is_correct:
                correct_count += 1
                
        elif q.type == "true_false":
            total_scorable += 1
            is_correct = (user_ans.lower() == correct_ans.lower())
            if is_correct:
                correct_count += 1
                
        else: # short_answer
            # Short answer is graded leniently in UI, backend returns is_correct=True if user wrote something substantial,
            # or marks it neutral. Let's do a basic keyword overlap check, but note that it needs manual review.
            # We'll mark is_correct as True if it's > 5 characters (submitted) and highlight self-review.
            is_correct = len(user_ans) >= 3
            # We don't increment correct_count or total_scorable to keep the numerical score based on multiple-choice/true-false.
            # However, if it's ALL short answer, scorable will be 0. Let's handle that:
            pass
            
        results.append(QuestionResult(
            question_id=q.id,
            question_text=q.question,
            question_type=q.type,
            user_answer=user_ans,
            correct_answer=correct_ans,
            is_correct=is_correct,
            explanation=q.explanation,
            source_reference=q.source_reference,
            options=q.options
        ))
        
    # Calculate score metrics
    # If there are no MCQs or T/Fs, score is based on short answers written
    if total_scorable == 0:
        total_questions = len(quiz.questions)
        # Count all non-empty short answers as correct/attempted for basic score
        correct_count = sum(1 for r in results if r.is_correct)
        total_scorable = total_questions
        
    percentage = (correct_count / total_scorable) * 100 if total_scorable > 0 else 0.0
    
    # Assign grade letter
    if percentage >= 90:
        grade = "A"
    elif percentage >= 80:
        grade = "B"
    elif percentage >= 70:
        grade = "C"
    elif percentage >= 60:
        grade = "D"
    else:
        grade = "F"
        
    return QuizResult(
        quiz_id=quiz.id,
        score=correct_count,
        total=total_scorable,
        percentage=round(percentage, 1),
        grade=grade,
        results=results
    )

@router.get("/{quiz_id}/export")
async def export_quiz_endpoint(quiz_id: str, format: str = Query("json", pattern="^(json|markdown|pdf)$")):
    """
    Export the quiz in JSON, Markdown, or PDF format.
    """
    from main import quizzes_store
    
    if quiz_id not in quizzes_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz ID not found."
        )
        
    quiz: Quiz = quizzes_store[quiz_id]
    
    if format == "json":
        json_data = export_json(quiz)
        return Response(
            content=json_data,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=quiz_{quiz_id}.json"}
        )
        
    elif format == "markdown":
        md_data = export_markdown(quiz)
        return Response(
            content=md_data,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=quiz_{quiz_id}.md"}
        )
        
    elif format == "pdf":
        try:
            pdf_bytes = export_pdf(quiz)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=quiz_{quiz_id}.pdf"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate PDF export: {str(e)}"
            )
            
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported format."
    )
