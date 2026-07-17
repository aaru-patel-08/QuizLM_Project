import React, { useState } from "react";
import Header from "./components/Header";
import UploadPanel from "./components/UploadPanel";
import ConfigPanel from "./components/ConfigPanel";
import QuizView from "./components/QuizView";
import ResultsView from "./components/ResultsView";

export default function App() {
  const [step, setStep] = useState("upload"); // 'upload' | 'config' | 'quiz' | 'results'
  const [documentInfo, setDocumentInfo] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [results, setResults] = useState(null);

  const handleUploadSuccess = (data) => {
    setDocumentInfo(data);
    setStep("config");
  };

  const handleQuizGenerated = (generatedQuiz) => {
    setQuiz(generatedQuiz);
    setStep("quiz");
  };

  const handleQuizSubmitted = (quizResults) => {
    setResults(quizResults);
    setStep("results");
  };

  const handleRetake = () => {
    // Reset results and go back to quiz view
    setResults(null);
    setStep("quiz");
  };

  const handleNewQuiz = () => {
    // Clear all states and reset to upload
    setDocumentInfo(null);
    setQuiz(null);
    setResults(null);
    setStep("upload");
  };

  return (
    <>
      <Header />
      <main className="app-container">
        {step === "upload" && (
          <UploadPanel onUploadSuccess={handleUploadSuccess} />
        )}

        {step === "config" && (
          <ConfigPanel 
            documentInfo={documentInfo} 
            onQuizGenerated={handleQuizGenerated} 
            onBack={() => setStep("upload")} 
          />
        )}

        {step === "quiz" && (
          <QuizView 
            quiz={quiz} 
            onQuizSubmitted={handleQuizSubmitted} 
            onBack={() => setStep("config")} 
          />
        )}

        {step === "results" && (
          <ResultsView 
            results={results} 
            onRetake={handleRetake} 
            onNewQuiz={handleNewQuiz} 
          />
        )}
      </main>
    </>
  );
}
