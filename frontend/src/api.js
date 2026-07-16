/**
 * API client helper functions to communicate with the FastAPI backend.
 */

const API_BASE_URL = "http://localhost:8000";

/**
 * Upload a PDF file to the backend.
 * @param {File} file 
 * @returns {Promise<Object>} DocumentInfo { document_id, filename, page_count, chunk_count, total_characters }
 */
export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to upload PDF. Ensure it has readable text.");
  }

  return response.json();
}

/**
 * Generate a quiz from a document.
 * @param {string} documentId 
 * @param {number} numQuestions 
 * @param {string} difficulty 
 * @returns {Promise<Object>} Quiz { id, title, source_filename, questions, difficulty }
 */
export async function generateQuiz(documentId, numQuestions, difficulty) {
  const response = await fetch(`${API_BASE_URL}/quiz/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_id: documentId,
      num_questions: parseInt(numQuestions),
      difficulty: difficulty,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to generate quiz. Check API key configurations.");
  }

  return response.json();
}

/**
 * Submit answers and get scoring.
 * @param {string} quizId 
 * @param {Object} answers { question_id: answer_text }
 * @returns {Promise<Object>} QuizResult { quiz_id, score, total, percentage, grade, results }
 */
export async function submitQuiz(quizId, answers) {
  const response = await fetch(`${API_BASE_URL}/quiz/${quizId}/submit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ answers }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to grade answers.");
  }

  return response.json();
}

/**
 * Download a quiz export file (JSON, Markdown, PDF).
 * @param {string} quizId 
 * @param {string} format 'json' | 'markdown' | 'pdf'
 */
export async function exportQuiz(quizId, format) {
  const url = `${API_BASE_URL}/quiz/${quizId}/export?format=${format}`;
  
  if (format === "pdf") {
    // For PDF, download it as a binary blob
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to download PDF export");
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = `quiz_${quizId}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(blobUrl);
  } else {
    // For JSON and Markdown, we can trigger direct window download
    window.open(url, "_blank");
  }
}
