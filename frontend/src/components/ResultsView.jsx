import React, { useState } from "react";
import { Check, X, Download, RefreshCw, PlusCircle, Bookmark, Copy, FileJson, FileText } from "lucide-react";
import { exportQuiz } from "../api";

export default function ResultsView({ results, onRetake, onNewQuiz }) {
  const [copied, setCopied] = useState(false);

  const { score, total, percentage, grade, results: questionsBreakdown } = results;

  // Determine score color theme
  let themeClass = "danger";
  if (percentage >= 80) themeClass = "success";
  else if (percentage >= 50) themeClass = "warning";

  const handleExport = async (format) => {
    try {
      await exportQuiz(results.quiz_id, format);
      // Optional: show a transient toast
    } catch (err) {
      alert("Failed to download export file: " + err.message);
    }
  };

  return (
    <div className="glass-panel">
      {/* 1. Score Summary Circle */}
      <div className="score-section">
        <h1 style={{ marginBottom: "1.5rem" }}>Quiz Results</h1>
        <div className={`score-circle ${themeClass}`}>
          <div className="score-number">{score}</div>
          <div className="score-total">out of {total}</div>
          <div className="grade-badge">{grade}</div>
        </div>
        <div className="text-center mt-2">
          <h2>{percentage}% Correct</h2>
          <p className="text-sm text-muted mt-1">
            {grade === "A" || grade === "B" ? "Fantastic job! You've mastered this material." : "Review the explanations below and try again."}
          </p>
        </div>
      </div>

      {/* Export Options */}
      <div className="text-center mb-10">
        <h3 className="text-sm text-muted uppercase tracking-wider mb-3">Export Options</h3>
        <div className="export-actions">
          <button className="btn btn-secondary btn-sm" onClick={() => handleExport("json")}>
            <FileJson size={16} /> JSON
          </button>
          <button className="btn btn-secondary btn-sm" onClick={() => handleExport("markdown")}>
            <FileText size={16} /> Markdown
          </button>
          <button className="btn btn-secondary btn-sm" onClick={() => handleExport("pdf")}>
            <Download size={16} /> PDF Document
          </button>
        </div>
      </div>

      {/* 2. Questions Breakdown */}
      <div className="results-list">
        <h2 style={{ fontSize: "1.4rem", marginBottom: "1rem" }}>Detailed Review</h2>
        {questionsBreakdown.map((r, idx) => {
          const isCorrect = r.is_correct;
          const isShortAnswer = r.question_type === "short_answer";
          
          return (
            <div key={r.question_id} className={`result-card ${isCorrect ? "correct" : "incorrect"}`}>
              <div className="result-card-header">
                <div>
                  <span className="q-badge">Question {idx + 1}</span>
                  <div className="font-semibold text-lg mt-1" style={{ color: "var(--text-primary)" }}>
                    {r.question_text}
                  </div>
                </div>
                <div className={`result-badge ${isCorrect ? "correct" : "incorrect"}`}>
                  {isCorrect ? (
                    <>
                      <Check size={14} /> Correct
                    </>
                  ) : (
                    <>
                      <X size={14} /> {isShortAnswer ? "Review" : "Incorrect"}
                    </>
                  )}
                </div>
              </div>

              {/* Show Options list if multiple_choice */}
              {r.options && r.options.length > 0 && (
                <div className="options-list" style={{ pointerEvents: "none", opacity: 0.8 }}>
                  {r.options.map((opt, oIdx) => {
                    const letter = String.fromCharCode(65 + oIdx);
                    const isSelected = r.user_answer === opt;
                    const isAnswerCorrect = r.correct_answer === opt;
                    
                    let optClass = "";
                    if (isSelected) optClass = isCorrect ? "selected" : "selected"; // standard selection
                    if (isAnswerCorrect) optClass = "selected"; // highlight correct one
                    
                    return (
                      <div 
                        key={opt} 
                        className={`option-item ${optClass}`}
                        style={{ 
                          borderColor: isAnswerCorrect ? "var(--status-success)" : isSelected ? "var(--status-error)" : "var(--border-color)",
                          background: isAnswerCorrect ? "rgba(16,185,129,0.06)" : isSelected ? "rgba(239,68,68,0.06)" : "transparent"
                        }}
                      >
                        <div 
                          className="option-letter" 
                          style={{
                            background: isAnswerCorrect ? "var(--status-success)" : isSelected ? "var(--status-error)" : "var(--bg-tertiary)",
                            color: isAnswerCorrect || isSelected ? "white" : "var(--text-secondary)"
                          }}
                        >
                          {letter}
                        </div>
                        <div className="option-text">{opt}</div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Answer comparison */}
              <div className="answer-comparison">
                <div className="answer-comp-box">
                  <span className="answer-comp-title">Your Answer</span>
                  <span className={`answer-comp-val ${isCorrect ? "correct" : "incorrect"}`} style={{ color: isShortAnswer ? "var(--text-primary)" : undefined }}>
                    {r.user_answer || <span className="text-muted italic">No Answer</span>}
                  </span>
                </div>
                <div className="answer-comp-box">
                  <span className="answer-comp-title">Correct Answer</span>
                  <span className="answer-comp-val correct">
                    {r.correct_answer}
                  </span>
                </div>
              </div>

              {/* Explanation & Source reference */}
              <div className="explanation-box">
                <div className="text-sm text-secondary">
                  <strong>Explanation:</strong> {r.explanation}
                </div>
                <div className="source-ref-link">
                  <Bookmark size={12} /> Source: {r.source_reference}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer Navigation Actions */}
      <div className="nav-actions mt-10 border-t border-color pt-6">
        <button className="btn btn-secondary" onClick={onRetake}>
          <RefreshCw size={16} /> Retake Quiz
        </button>
        <button className="btn btn-primary" onClick={onNewQuiz}>
          <PlusCircle size={16} /> Start New Quiz
        </button>
      </div>
    </div>
  );
}
