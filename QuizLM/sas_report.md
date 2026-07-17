# System Architecture Specification (SAS)
## For AI Quiz Generator (QuizLM)

---

## 1. Architectural Representation

The QuizLM application employs a **three-tier architecture** featuring a decoupled React Single-Page Application (SPA) client, an asynchronous FastAPI service layer, and an in-memory session data layer combined with Google's Gemini LLM.

```
┌────────────────────────────────────────────────────────┐
│                   React SPA Frontend                   │  (Client Layer)
│   (UploadPanel, ConfigPanel, QuizView, ResultsView)    │
└───────────────────────────┬────────────────────────────┘
                             │
                             │  HTTP REST (JSON / Multipart)
                             ▼
┌────────────────────────────────────────────────────────┐
│                 FastAPI REST Backend                   │  (Service Layer)
│  (PyMuPDF Parser, Gemini Client, PDF Export Compiler)   │
└─────────────┬─────────────────────────────┬────────────┘
              │                             │
              │  Local Dictionary Cache     │  Google GenAI Protocol
              ▼                             ▼
┌───────────────────────────┐ ┌──────────────────────────┐
│     In-Memory Stores      │ │      Google Gemini       │  (External / Data Layer)
│ (documents_store, quizzes)│ │     Flash Lite LLM       │
└───────────────────────────┘ └──────────────────────────┘
```

---

## 2. Component Design

### 2.1 React Frontend Components
*   **`App.jsx`**: Coordinates global state machine (e.g., active screen: upload -> config -> quiz -> results) and stores document/quiz metadata in state.
*   **`Header.jsx`**: Sticky navbar component featuring logo styling, system health state indicator, and layout titles.
*   **`UploadPanel.jsx`**: Multi-region drag-and-drop file dashboard. Collects file drops, executes validation, calls the upload API, and displays document metrics.
*   **`ConfigPanel.jsx`**: Configures quiz specifications (size count, difficulty rating). Triggers compilation and displays a loading skeleton with status alerts.
*   **`QuizView.jsx`**: Multi-layout quiz assessment player. Offers a step-by-step stepper navigation or full vertical scrolling list view.
*   **`ResultsView.jsx`**: Detailed score summary sheet. Features visual charts, color-coded answers, citation links, explanations, and download buttons.
*   **`api.js`**: Centrally coordinates all Fetch API REST network requests.

### 2.2 FastAPI Backend Components
*   **`main.py`**: Entry point that loads configuration, handles exception logs, initiates CORS permissions, setups IP rate limit filters, and launches routers.
*   **`routers/upload.py`**: Ingests files, runs extension filters, coordinates parser extractions, chunks strings, and caches documents.
*   **`routers/quiz.py`**: Handles generating quizzes, grading student keys, and routing file export compilations.
*   **`services/pdf_parser.py`**: Extracts text from PDF byte buffers using PyMuPDF and slices text into page-based groupings.
*   **`services/quiz_generator.py`**: Constructs custom instructions, queries Gemini API, and enforces structured schema parameters.
*   **`services/prompt_templates.py`**: Core prompt engineering catalog outlining instructions for question construction, difficulty constraints, and citation requirements.
*   **`services/export_service.py`**: Serializes datasets into JSON formats, composes clean Markdown summaries, and structures printable PDFs using `fpdf2`.

---

## 3. Data Flow Diagrams (DFD)

### 3.1 Document Ingestion Flow
```
[User Drop File] ───(PDF Upload)───► [FastAPI /upload]
                                            │
                                            ▼ (Parse Bytes)
                                      [PyMuPDF Parser]
                                            │
                                            ▼ (Extract Text Pages)
                                      [Chunking Algorithm]
                                            │
                                            ▼ (Store Chunks)
[Client Dashboard] ◄──(Doc Info JSON)─── [Cache in documents_store]
```

### 3.2 Quiz Generation & Grading Flow
```
[Client Config] ──(POST /quiz/generate)──► [FastAPI Quiz Router]
                                                  │
                                                  ▼ (Construct Prompt)
                                            [LLM Orchestrator]
                                                  │
                                                  ▼ (Enforce JSON Schema)
                                            [Google Gemini API]
                                                  │
                                                  ▼ (Validate & Store)
[Quiz View Dashboard] ◄───(Quiz JSON)◄─── [Cache in quizzes_store]
                                                  │
                               (Answer Submissions)
                                                  │
                                                  ▼ (Score MCQs/TF/SA)
[Review Panel] ◄───(QuizResult JSON)◄───── [Grading Service Engine]
```

---

## 4. Data Design (In-Memory Schemas)

Since QuizLM operates as an ephemeral session utility, data is managed using server-side in-memory dictionaries:
1.  **`documents_store`**: Mapping of `document_id` (UUID) to extracted metadata and text chunks.
2.  **`quizzes_store`**: Mapping of `quiz_id` (UUID) to generated `Quiz` objects.

### Pydantic Data Structures

#### 4.1 Page Chunk Schema
```python
class PageChunk(BaseModel):
    text: str
    page_start: int
    page_end: int
    chunk_index: int
```

#### 4.2 Quiz Question Schema
```python
class Question(BaseModel):
    id: str
    type: Literal["multiple_choice", "true_false", "short_answer"]
    question: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    source_reference: str
```

#### 4.3 Quiz Response Schema
```python
class Quiz(BaseModel):
    id: str
    title: str
    source_filename: str
    questions: List[Question]
    difficulty: Literal["easy", "medium", "hard"]
    created_at: datetime
    num_questions: int
```

---

## 5. Interface Design (API Endpoints)

The API comprises clean, RESTful JSON endpoints protected by rate limiting:

| Method | Endpoint | Description | Request / Payload | Response Body |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/upload` | Ingests PDF file, extracts and chunks text, returns ID | `multipart/form-data` | `DocumentInfo` |
| **POST** | `/quiz/generate` | Generates quiz questions from document chunks via Gemini | `QuizGenerationRequest` | `Quiz` |
| **POST** | `/quiz/{quiz_id}/submit` | Graded evaluation feedback for user answers | `AnswerSubmission` | `QuizResult` |
| **GET** | `/quiz/{quiz_id}/export` | Downloads the quiz structure in requested formats | Query `format` (json, markdown, pdf) | File Attachment |
| **GET** | `/health` | Server health and configuration status report | None | `{"status": "healthy", ...}` |
