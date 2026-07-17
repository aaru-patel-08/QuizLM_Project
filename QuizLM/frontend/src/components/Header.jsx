import React from "react";
import { BookOpen } from "lucide-react";

export default function Header() {
  return (
    <header className="app-header">
      <a href="/" className="logo-group">
        <div className="logo-icon">
          <BookOpen size={22} color="white" />
        </div>
        <span className="logo-text">QuizLM</span>
      </a>
      <div className="badge-v">
        AI Quiz Generator
      </div>
    </header>
  );
}
