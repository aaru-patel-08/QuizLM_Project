# 🖥️ QuizLM — React Frontend UI Documentation

This directory contains the Single-Page Application (SPA) frontend codebase for **QuizLM**. It is built on **React 19** and **Vite 8**, leveraging **Vanilla CSS** to deliver a bespoke, premium dark glassmorphism design system.

---

## ✨ Design Aesthetic & Styling System

The application uses custom **Vanilla CSS custom properties** (CSS variables) to enforce a high-fidelity interface:
*   **Colors**: Sleek dark color schemes, vibrant purple/indigo accent tones, and clean warning/success variables.
*   **Aesthetic**: Semi-transparent backing panels with backdrop-blur effects (glassmorphism), clean border gradients, and subtle drop shadows.
*   **Typography**: Clean sans-serif layout loading Outfit and Inter type families from Google Fonts.
*   **Micro-animations**: Smooth hover transitions, scale-ups, and pulsing skeleton structures for load indicators.
*   **Responsive**: Adaptive grid layouts supporting screens from mobile scale to high-resolution desktops.

---

## 📁 Directory Structure

```text
frontend/
├── index.html                  # Main entry page linking font preconnects and React mounting scripts
├── package.json                # Project node scripts and modules list
├── public/                     # Static files and browser tab icons
├── src/
│   ├── components/             # Reusable UI component modules
│   │   ├── Header.jsx          # Top-sticky navbar with health monitors
│   │   ├── UploadPanel.jsx     # File upload dropzone and detail logs
│   │   ├── ConfigPanel.jsx     # Difficulty level options and question count settings
│   │   ├── QuizView.jsx        # Step stepper or list taker view options
│   │   └── ResultsView.jsx     # Scoring review screens, citations, and export buttons
│   ├── App.jsx                 # Stateful application view router
│   ├── api.js                  # Client fetch calls for FastAPI interactions
│   ├── index.css               # Design system rules, animations, and typography variables
│   └── main.jsx                # Application root entry mount point
└── vite.config.js              # Vite server port routing details
```

---

## ⚙️ Setup & Local Execution

### Prerequisites
Make sure you have **Node.js** (v18+) installed.

### 1. Install Dependencies
Navigate into this directory and run:
```bash
npm install
```

### 2. Launch Development Server
```bash
npm run dev
```
*   **Dev URL**: `http://localhost:5173/`
*   Features Hot Module Replacement (HMR) for instant CSS and JS hot reloading.

### 3. Verification & Build
To lint the project files using Oxlint:
```bash
npm run lint
```
To build optimized static bundles ready for production distribution:
```bash
npm run build
```
To run local previews of the compiled production bundle:
```bash
npm run preview
```

---

## 📡 API Client Interface (`api.js`)

The client encapsulates network fetches to communicate with the local FastAPI port (`http://localhost:8000`):
1.  `uploadPDF(file)`: Sends PDF bytes inside a `multipart/form-data` package. Returns document dimensions.
2.  `generateQuiz(documentId, numQuestions, difficulty)`: Post request requesting question synthesis. Returns full Quiz schema.
3.  `submitQuiz(quizId, answers)`: Transmits question selections. Returns grades, explanations, and citation mapping.
4.  `exportQuiz(quizId, format)`: Calls down raw JSON/Markdown attachments, or triggers download triggers for binary vector PDF blobs.
