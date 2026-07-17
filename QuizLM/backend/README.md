# ⚙️ QuizLM — Backend API Documentation

This directory contains the asynchronous **FastAPI** backend codebase that powers the **QuizLM AI Quiz Generator**. It processes PDF documents, chunk-extracts text, coordinates with Google's Gemini models for quiz synthesis, grades submissions, and compiles multiple format exports.

---

## 🛠️ Technology Stack & Services

*   **FastAPI**: Asynchronous web framework for high-performance Python microservices.
*   **PyMuPDF (`fitz`)**: Robust PDF parsing engine for layout-aware text extraction.
*   **Google GenAI SDK**: Integrates directly with the `gemini-flash-lite-latest` model for structured JSON generation.
*   **FPDF2**: Clean vector-graphics compiler to compile downloadable quiz PDF sheets.
*   **Slowapi**: Token-bucket client IP rate-limiting protection.

---

## 📁 Directory Structure

```text
backend/
├── main.py                 # FastAPI application setup, rate limiter, and routes inclusion
├── requirements.txt        # Backend python packages list
├── .env.example            # Environment variables configuration template
├── models/
│   └── schemas.py          # Pydantic data schemas for requests and responses
├── routers/
│   ├── upload.py           # Endpoint handling file uploads, validation, and parsing
│   └── quiz.py             # Endpoints for quiz generation, grading, and multi-format exports
└── services/
    ├── pdf_parser.py       # Extract text from PDF buffers and split into overlapping chunks
    ├── quiz_generator.py   # Prompts Gemini model using Pydantic structured output mode
    ├── prompt_templates.py # Stores specialized prompt system instructions
    └── export_service.py   # Formats and returns downloadable JSON, MD, and PDF documents
```

---

## ⚙️ Setup & Local Execution

### 1. Configure Environment Variables
Copy `.env.example` to a new file named `.env`:
```bash
cp .env.example .env
```
Open `.env` and configure your **Google Gemini API Key**:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key...
```

### 2. Manual Installation
From this directory, run:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Server
Start the development server with Hot Module Reload (HMR):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
*   **API Root URL**: `http://localhost:8000`
*   **Swagger API Docs**: `http://localhost:8000/docs`
*   **ReDoc Docs**: `http://localhost:8000/redoc`

---

## 📡 API Endpoints Reference

### 1. Document Upload
*   **POST** `/upload`
*   **Content-Type**: `multipart/form-data`
*   **Payload**: `file` (PDF file)
*   **Action**: Extracts, chunks text, and registers document session in memory.
*   **Success Response** (`200 OK`):
    ```json
    {
      "document_id": "8f30730d-ef0f-4882-959c-70335e3be1ff",
      "filename": "chapter1.pdf",
      "page_count": 12,
      "chunk_count": 3,
      "total_characters": 24890,
      "status": "extracted"
    }
    ```

### 2. Quiz Generation
*   **POST** `/quiz/generate`
*   **Payload**:
    ```json
    {
      "document_id": "8f30730d-ef0f-4882-959c-70335e3be1ff",
      "num_questions": 10,
      "difficulty": "medium"
    }
    ```
*   **Success Response** (`200 OK`):
    ```json
    {
      "id": "quiz_a2b3c4...",
      "title": "Quiz on chapter1.pdf",
      "source_filename": "chapter1.pdf",
      "questions": [
        {
          "id": "q1",
          "type": "multiple_choice",
          "question": "What is the primary theme of Chapter 1?",
          "options": ["A) Choice A", "B) Choice B", "C) Choice C", "D) Choice D"],
          "correct_answer": "A) Choice A",
          "explanation": "Gemini reasoning explaining the correct option.",
          "source_reference": "Page 3"
        }
      ],
      "difficulty": "medium",
      "created_at": "2026-07-17T10:00:00Z",
      "num_questions": 1
    }
    ```

### 3. Grading Submission
*   **POST** `/quiz/{quiz_id}/submit`
*   **Payload**:
    ```json
    {
      "answers": {
        "q1": "A) Choice A"
      }
    }
    ```
*   **Success Response** (`200 OK`):
    ```json
    {
      "quiz_id": "quiz_a2b3c4...",
      "score": 1,
      "total": 1,
      "percentage": 100.0,
      "grade": "A",
      "results": [
        {
          "question_id": "q1",
          "question_text": "What is the primary theme of Chapter 1?",
          "question_type": "multiple_choice",
          "user_answer": "A) Choice A",
          "correct_answer": "A) Choice A",
          "is_correct": true,
          "explanation": "Gemini reasoning explaining the correct option.",
          "source_reference": "Page 3",
          "options": ["A) Choice A", "B) Choice B", "C) Choice C", "D) Choice D"]
        }
      ]
    }
    ```

### 4. File Exports
*   **GET** `/quiz/{quiz_id}/export?format={json|markdown|pdf}`
*   **Action**: Generates download payloads for the given format.
*   **Returns**: Attachment stream with appropriate MIME type.

### 5. Health Monitor
*   **GET** `/health`
*   **Action**: Verifies server health and status of active API configuration values.

---

## 🔒 Rate Limiting details
The API integrates a rate limiter to protect Gemini token usage:
*   IP rate-limiting configurations are managed via `slowapi`.
*   Users exceeding safe call volumes will receive a standard `429 Too Many Requests` response.
