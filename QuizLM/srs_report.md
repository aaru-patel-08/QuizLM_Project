# Software Requirements Specification (SRS)
## For AI Quiz Generator (QuizLM)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for the **AI Quiz Generator (QuizLM)**. It defines the core capabilities, user interfaces, functional operations, and performance and security boundaries. This specification serves as a reference for developers, quality assurance teams, and project evaluators.

### 1.2 Scope
QuizLM is a full-stack, AI-powered educational tool designed to streamline quiz creation and assessment. Users upload textbook, research, or note PDFs. The application extracts page text, chunks it appropriately, prompts Google Gemini (via Gemini Flash Lite) to synthesize formatted questions (Multiple Choice, True/False, and Short Answer) with inline citations and explanation keys, and renders an interactive quiz dashboard. Users can complete quizzes online, receive immediate feedback, and export their generated assessments as JSON, Markdown, or styled printable PDFs.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **SRS**: Software Requirements Specification
*   **SAS**: System Architecture Specification
*   **LLM**: Large Language Model (e.g., Google Gemini)
*   **JSON**: JavaScript Object Notation (structured data interchange format)
*   **SPA**: Single Page Application (React-based client)
*   **API**: Application Programming Interface
*   **MCQ**: Multiple Choice Question
*   **TF**: True / False Question
*   **SA**: Short Answer Question

---

## 2. Overall Description

### 2.1 Product Perspective
QuizLM is designed as a standalone, lightweight, full-stack web application. The backend runs on FastAPI, utilizing memory-based session caches for PDF parsing and generated quizzes. The frontend is built on React (via Vite) and styled using custom Vanilla CSS variables to achieve a premium dark glassmorphism aesthetic. It connects directly with Google’s Gemini API using the official Google GenAI SDK.

### 2.2 Product Functions
*   **PDF Document Parsing**: Accepts PDF files up to standard document page counts, extracts clean layouts, and performs validation to verify text content.
*   **Text Chunking**: Dynamically segments extracted text to prevent LLM context-window exhaustion and focus query parameters.
*   **Structured Quiz Generation**: Sends chunks to Gemini, enforcing a structured JSON response schema mapping to questions, options, correct answers, reasoning, and source page citations.
*   **Interactive Test Stepper**: Enables takers to navigate questions step-by-step or scroll through a full dashboard.
*   **Grading and Explanations**: Scores MCQs and TF answers instantly. Displays feedback detailing correctness, explanation context, and source pages.
*   **Multi-Format Export**: Generates printable PDF documents (including Answer Keys), clean markdown files, and raw JSON configurations for download.

### 2.3 User Classes and Characteristics
*   **Students / Self-Learners**: Use the tool to upload lecture notes or study guides, testing their comprehension and checking explanations or source pages for review.
*   **Educators / Teachers**: Generate structured question pools from custom reading assignments, exporting clean PDFs or Markdown quizzes for classroom tests.

### 2.4 Operating Environment
*   **Operating System**: Cross-platform (Windows, macOS, Linux).
*   **Web Browsers**: Modern HTML5 browsers (Chrome, Edge, Safari, Firefox).
*   **Runtime Environment**: Python 3.10+ and Node.js v18+.
*   **External Service dependency**: Google AI Studio API access key.

---

## 3. Specific Requirements

### 3.1 External Interface Requirements

#### 3.1.1 User Interfaces
*   **Upload Zone**: A drag-and-drop region accepting PDF files with visual file info logs (filename, character counts, page sizes).
*   **Configuration Panel**: Input options to select the number of questions (5, 10, or 20) and difficulty levels (Easy, Medium, Hard).
*   **Quiz Stepper Board**: Viewport displaying one question at a time with previous/next controls, status bubbles, and radio option selection.
*   **Results Dashboard**: Breakdown showing summary stats, progress bars, correct/incorrect badges, and accordion expansion for explanations.

#### 3.1.2 Hardware Interfaces
*   Standard network card interfacing with local ports and external web gateways.

#### 3.1.3 Software Interfaces
*   **FastAPI REST Engine**: Serves API endpoints, parses JSON requests, and manages in-memory data tables.
*   **PyMuPDF (`fitz`)**: Interlocks with file uploads to perform high-fidelity text extraction.
*   **Google GenAI SDK**: Transmits prompt tokens and pulls structured JSON schemas from Gemini models.
*   **FPDF2 Compiler**: Compiles vector styling and text blocks into binary PDF blobs.

---

## 4. Functional Requirements

### 4.1 Document Ingestion and Parsing
*   **FR-1.1**: The system shall only accept PDF uploads. Any other file types must trigger a `400 Bad Request` error.
*   **FR-1.2**: The parser shall check for character lengths. If a PDF yields zero readable text (image-only or scanned documents without OCR), the system shall return a `422 Unprocessable Entity` error.
*   **FR-1.3**: The system shall chunk extracted text using a sliding page-grouping window to maintain semantic continuity.

### 4.2 AI Quiz Generation
*   **FR-2.1**: The system shall generate a structured instruction prompt based on user-selected question counts and difficulty tiers.
*   **FR-2.2**: The backend shall require a valid `GEMINI_API_KEY` to query Google Gemini. If missing, a clear setup warning must be displayed.
*   **FR-2.3**: The LLM integration must strictly output JSON matching the application's schema (containing IDs, question strings, option arrays, correct answers, detailed reasoning, and specific source page citations).
*   **FR-2.4**: Quizzes shall be stored in memory on the server with a unique UUID for session access.

### 4.3 Evaluation and Grading
*   **FR-3.1**: The frontend shall compile user answers as key-value pairs (Question ID → Answer Text).
*   **FR-3.2**: The backend shall evaluate MCQ and TF choices using case-insensitive comparisons, handling both exact matches and matching prefix options (e.g., comparing "A" to "A) Option text").
*   **FR-3.3**: Short answers shall be graded using length checks to verify effort, returning explanatory answers for self-review.
*   **FR-3.4**: The system shall compute a total numerical score, percentage correct, and a corresponding letter grade (A, B, C, D, F).

### 4.4 Export Engine
*   **FR-4.1**: The system shall compile the quiz structure into a downloadable JSON file.
*   **FR-4.2**: The system shall compile a clean Markdown document listing questions, options, explanations, and references.
*   **FR-4.3**: The system shall use the `fpdf2` library to generate a styled printable PDF complete with a clean header, body, page numbering, and a separate Answer Key section.

---

## 5. Non-Functional Requirements

### 5.1 Performance
*   **PDF Extraction**: Local extraction of text from standard PDFs (under 50 pages) should complete within 1.5 seconds.
*   **Generation Time**: Gemini AI generation should complete and return results within 10 seconds.
*   **Download Compilation**: File exports (JSON/MD/PDF) must compose and download in under 1 second.

### 5.2 Security
*   **Rate Limiting**: To prevent API misuse, upload and quiz endpoints must enforce rate limits via IP address limits (using `slowapi`).
*   **Environment Safety**: The backend must exclude API keys from client-side bundles, hosting configuration in a secured server-side `.env` file.
*   **No Persistent PII**: Document parsing and quizzes remain session-bound in server memory and are not written to persistent disks.

### 5.3 Reliability
*   The application must detect network timeouts or Gemini API failures, displaying user-friendly error banners in the UI instead of crashing.
