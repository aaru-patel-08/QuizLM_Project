import React, { useState } from "react";
import { ChevronLeft, ChevronRight, Eye, List, AlertTriangle } from "lucide-react";
import { submitQuiz } from "../api";

export default function QuizView({ quiz, onQuizSubmitted, onBack }) {
  const [viewMode, setViewMode] = useState("single"); // 'single' (one at a time) or 'list' (all at once)
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const questions = quiz.questions || [];
  const currentQuestion = questions[currentIdx];

  const handleSelectOption = (qId, optionVal) => {
    setAnswers((prev) => ({
      ...prev,
      [qId]: optionVal,
    }));
  };

  const handleTextChange = (qId, textVal) => {
    setAnswers((prev) => ({
      ...prev,
      [qId]: textVal,
    }));
  };

  const isQuestionAnswered = (qId) => {
    return answers[qId] !== undefined && answers[qId].trim() !== "";
  };

  const handleNext = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    }
  };

  const handlePrev = () => {
    if (currentIdx > 0) {
      setCurrentIdx(currentIdx - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const results = await submitQuiz(quiz.id, answers);
      setSubmitting(false);
      onQuizSubmitted(results);
    } catch (err) {
      setError(err.message || "Failed to submit answers.");
      setSubmitting(false);
    }
  };

  const renderQuestionInput = (q) => {
    if (q.type === "multiple_choice") {
      return (
        <div className="options-list">
          {(q.options || []).map((opt, oIdx) => {
            const letter = chrOption(oIdx);
            const isSelected = answers[q.id] === opt;
            return (
              <button
                key={opt}
                type="button"
                className={`option-item ${isSelected ? "selected" : ""}`}
                onClick={() => handleSelectOption(q.id, opt)}
              >
                <div className="option-letter">{letter}</div>
                <div className="option-text">{opt}</div>
              </button>
            );
          })}
        </div>
      );
    }

    if (q.type === "true_false") {
      return (
        <div className="tf-container">
          {["True", "False"].map((val) => {
            const isSelected = answers[q.id] === val;
            return (
              <button
                key={val}
                type="button"
                className={`tf-btn ${isSelected ? "selected" : ""}`}
                onClick={() => handleSelectOption(q.id, val)}
              >
                <span>{val}</span>
              </button>
            );
          })}
        </div>
      );
    }

    if (q.type === "short_answer") {
      return (
        <div>
          <textarea
            className="short-answer-input"
            placeholder="Type your answer here..."
            value={answers[q.id] || ""}
            onChange={(e) => handleTextChange(q.id, e.target.value)}
          />
          <div className="text-right text-xs text-muted mt-[-1rem] mb-[2rem]">
            Minimum suggested length: 5 characters.
          </div>
        </div>
      );
    }

    return null;
  };

  const chrOption = (idx) => {
    return String.fromCharCode(65 + idx); // A, B, C, D
  };

  if (submitting) {
    return (
      <div className="glass-panel text-center">
        <div className="loading-overlay">
          <div className="spinner"></div>
          <h2>Grading Quiz Submissions...</h2>
          <p className="text-sm text-muted">Calculating score and generating explanations.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-panel">
      {/* Quiz Header */}
      <div className="quiz-header">
        <div>
          <h2 style={{ fontSize: "1.4rem" }}>{quiz.title}</h2>
          <p className="text-xs text-muted" style={{ textTransform: "capitalize" }}>
            Difficulty: {quiz.difficulty} | Questions: {questions.length}
          </p>
        </div>

        {/* View Mode Toggle */}
        <div className="view-mode-selector">
          <button
            type="button"
            className={`view-mode-btn ${viewMode === "single" ? "active" : ""}`}
            onClick={() => setViewMode("single")}
            title="One question at a time"
          >
            <Eye size={14} style={{ display: "inline", marginRight: "4px" }} /> Step
          </button>
          <button
            type="button"
            className={`view-mode-btn ${viewMode === "list" ? "active" : ""}`}
            onClick={() => setViewMode("list")}
            title="Show all questions"
          >
            <List size={14} style={{ display: "inline", marginRight: "4px" }} /> List
          </button>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <AlertTriangle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Mode 1: One Question at a Time */}
      {viewMode === "single" && currentQuestion && (
        <div className="question-card">
          {/* Progress Bar */}
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${((currentIdx + 1) / questions.length) * 100}%` }}
            ></div>
          </div>

          <span className="q-badge">Question {currentIdx + 1} of {questions.length}</span>
          <div className="question-text">{currentQuestion.question}</div>

          {renderQuestionInput(currentQuestion)}

          <div className="nav-actions mt-8">
            <button
              className="btn btn-secondary"
              onClick={handlePrev}
              disabled={currentIdx === 0}
            >
              <ChevronLeft size={16} /> Previous
            </button>

            {currentIdx < questions.length - 1 ? (
              <button className="btn btn-primary" onClick={handleNext}>
                Next <ChevronRight size={16} />
              </button>
            ) : (
              <button 
                className="btn btn-primary" 
                style={{ background: "linear-gradient(135deg, #10b981 0%, #059669 100%)", boxShadow: "0 4px 15px rgba(16,185,129,0.3)" }}
                onClick={handleSubmit}
              >
                Submit Quiz
              </button>
            )}
          </div>
        </div>
      )}

      {/* Mode 2: Full List View */}
      {viewMode === "list" && (
        <div className="questions-list">
          {questions.map((q, idx) => (
            <div
              key={q.id}
              className="question-card mb-8 pb-8"
              style={{ borderBottom: idx < questions.length - 1 ? "1px solid var(--border-color)" : "none" }}
            >
              <span className="q-badge">Question {idx + 1}</span>
              <div className="question-text" style={{ marginBottom: "1.5rem" }}>{q.question}</div>
              
              {renderQuestionInput(q)}
            </div>
          ))}

          <div className="nav-actions mt-8 border-t border-color pt-6">
            <button className="btn btn-secondary" onClick={onBack}>
              Cancel
            </button>
            <button 
              className="btn btn-primary"
              style={{ background: "linear-gradient(135deg, #10b981 0%, #059669 100%)", boxShadow: "0 4px 15px rgba(16,185,129,0.3)" }}
              onClick={handleSubmit}
            >
              Submit answers ({Object.keys(answers).filter(isQuestionAnswered).length}/{questions.length})
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
