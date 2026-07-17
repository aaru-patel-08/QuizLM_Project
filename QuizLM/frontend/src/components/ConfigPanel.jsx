import React, { useState } from "react";
import { Settings, BarChart2, BookOpen, AlertTriangle } from "lucide-react";
import { generateQuiz } from "../api";

export default function ConfigPanel({ documentInfo, onQuizGenerated, onBack }) {
  const [numQuestions, setNumQuestions] = useState(10);
  const [difficulty, setDifficulty] = useState("medium");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const quiz = await generateQuiz(documentInfo.document_id, numQuestions, difficulty);
      setLoading(false);
      onQuizGenerated(quiz);
    } catch (err) {
      setError(err.message || "Failed to generate quiz. Please verify API key.");
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel">
      {loading ? (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <div>
            <h2>Generating Quiz via LLM...</h2>
            <p className="text-sm text-muted mt-2">
              Structuring questions, explanations, and citing references.
            </p>
            <div className="text-xs text-secondary bg-secondary px-3 py-1.5 rounded-full mt-4 inline-block">
              Usually takes 10 to 20 seconds.
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <h1>Configure Quiz Settings</h1>
            <p>Customize your generated quiz parameters based on the extracted contents.</p>
            
            {documentInfo && (
              <div className="bg-secondary rounded-lg p-3.5 border border-color mt-4 text-sm flex gap-4 text-secondary justify-center">
                <span>📄 <strong>File:</strong> {documentInfo.filename}</span>
                <span>•</span>
                <span>📖 <strong>Pages:</strong> {documentInfo.page_count}</span>
                <span>•</span>
                <span>📊 <strong>Chunks:</strong> {documentInfo.chunk_count}</span>
              </div>
            )}
          </div>

          {error && (
            <div className="error-banner">
              <AlertTriangle size={20} />
              <span>{error}</span>
            </div>
          )}

          <div className="config-grid">
            {/* Question Count Select */}
            <div className="config-card">
              <div className="config-label text-accent-primary">
                <BookOpen size={18} />
                <span>Question Count</span>
              </div>
              <p className="text-xs text-muted">Select total questions to extract from the PDF.</p>
              <div className="toggle-group">
                {[5, 10, 20].map((count) => (
                  <button
                    key={count}
                    type="button"
                    className={`toggle-btn ${numQuestions === count ? "active" : ""}`}
                    onClick={() => setNumQuestions(count)}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty Select */}
            <div className="config-card">
              <div className="config-label text-accent-secondary">
                <Settings size={18} />
                <span>Difficulty Level</span>
              </div>
              <p className="text-xs text-muted">Adjust complexity of options and depth of logic.</p>
              <div className="toggle-group">
                {["easy", "medium", "hard"].map((level) => (
                  <button
                    key={level}
                    type="button"
                    className={`toggle-btn ${difficulty === level ? "active" : ""}`}
                    style={{ textTransform: "capitalize" }}
                    onClick={() => setDifficulty(level)}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="nav-actions mt-8">
            <button className="btn btn-secondary" onClick={onBack}>
              Back to Upload
            </button>
            <button className="btn btn-primary" onClick={handleGenerate}>
              Generate Quiz
            </button>
          </div>
        </>
      )}
    </div>
  );
}
