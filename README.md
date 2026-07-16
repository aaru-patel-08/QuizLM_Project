# QuizLM — AI Quiz Generator from PDF

QuizLM is a full-stack web application that allows users to upload PDF documents (such as textbook chapters, lecture notes, or research papers) and automatically generate structured, interactive quizzes from their content. 

The application utilizes Google Gemini Flash Lite to extract key concepts, formulate high-quality questions, generate detailed explanations, and cite exact page references from the source document.

---

## 🚀 Core Features

- **PDF Text Parsing**: Highly accurate layout extraction powered by PyMuPDF (`fitz`).
- **One-Click Generation**: Select the number of questions (5, 10, or 20) and difficulty levels (Easy, Medium, Hard).
- **Multiple Question Formats**: Generates a healthy mix of Multiple Choice, True/False, and Short Answer questions.
- **Interactive Quiz Interface**: Step-by-step navigation (one question at a time) or a full scrollable list view.
- **Detailed Explanations & Citations**: Graded breakdown showing correct answers, user selections, reasoning, and page number references.
- **Multi-Format Export**: Export your generated quiz as structured JSON, clean Markdown, or a styled, printable PDF document (including a formatted Answer Key).
- **Responsive Premium UI**: Beautiful modern dark glassmorphism design with responsive support for mobile and desktop screens.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React (Vite) | High-performance SPA frontend |
| **Styling** | Vanilla CSS | Premium glassmorphism design system & micro-animations |
| **Backend** | Python (FastAPI) | Lightweight, async API execution |
| **PDF Parsing** | PyMuPDF (`fitz`) | High-quality text extraction |
| **LLM Orchestration** | Google GenAI SDK | Free-tier Gemini Flash Lite structured JSON generator |
| **PDF Export** | `fpdf2` | Dynamically compiled printable PDFs |

---

## 📁 Project Structure

```text
ai-quiz-generator/
├── backend/
│   ├── main.py                 # FastAPI application entrypoint
│   ├── requirements.txt        # Python backend dependencies
│   ├── .env.example            # Environment variables template
│   ├── models/
│   │   └── schemas.py          # Pydantic models: Quiz, Question, Results
│   ├── routers/
│   │   ├── upload.py           # PDF upload + text extraction
│   │   └── quiz.py             # Quiz generation, scoring, and exporting
│   └── services/
│       ├── pdf_parser.py       # PyMuPDF extraction & chunking
│       ├── quiz_generator.py   # Gemini API connector with structured JSON
│       ├── prompt_templates.py # Quiz prompts and instructions
│       └── export_service.py   # PDF, JSON, and MD export formatting
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx      # Sticky navbar header
│   │   │   ├── UploadPanel.jsx # Drag-and-drop file uploader
│   │   │   ├── ConfigPanel.jsx # Question count & difficulty settings
│   │   │   ├── QuizView.jsx    # Interactive quiz taking panel
│   │   │   └── ResultsView.jsx # Detailed review, score, and downloads
│   │   ├── App.jsx             # Stateful application router
│   │   ├── index.css           # Global design system & theme variables
│   │   ├── main.jsx            # React root component
│   │   └── api.js              # Fetch requests to FastAPI backend
│   ├── package.json            # Node.js dependencies
│   └── index.html              # HTML entrypoint with font preconnects
└── README.md                   # Project documentation
```

---

## ⚙️ Installation & Local Setup

### Prerequisites
- Python 3.10+ installed
- Node.js (v18+) installed
- A free **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

---

### 1. Backend Setup

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your `.env` configuration file:
   ```bash
   cp .env.example .env
   ```

5. Open `.env` and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

6. Start the FastAPI local server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The backend API will run on `http://localhost:8000`.

---

### 2. Frontend Setup

1. Open a new terminal and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Install the package dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend application will load at `http://localhost:5173/`.

---

## 🧪 How to Use

1. **Upload**: Drag and drop any study document PDF onto the upload zone.
2. **Configure**: Select the count of questions (5, 10, or 20) and select Easy, Medium, or Hard difficulty.
3. **Take Quiz**: Answer questions interactively (stepper or full-list view).
4. **Scoring & Review**: Click submit to instantly see your grade and page-by-page references.
5. **Export**: Click the download buttons to save the quiz as a printable PDF, Markdown, or JSON.
