import React, { useState, useRef } from "react";
import { UploadCloud, FileText, CheckCircle, AlertTriangle, RefreshCw } from "lucide-react";
import { uploadPDF } from "../api";

export default function UploadPanel({ onUploadSuccess }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [fileInfo, setFileInfo] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const processFile = async (file) => {
    if (!file) return;

    // Validate type
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endswith(".pdf")) {
      setError("Please upload a PDF file only.");
      return;
    }

    // Validate size (max 50MB)
    const MAX_SIZE = 50 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      setError("File size exceeds 50MB limit.");
      return;
    }

    setError(null);
    setUploading(true);
    setFileInfo({ name: file.name, size: (file.size / (1024 * 1024)).toFixed(2) + " MB" });

    try {
      const data = await uploadPDF(file);
      setUploading(false);
      onUploadSuccess(data);
    } catch (err) {
      setError(err.message || "Failed to process PDF file.");
      setUploading(false);
      setFileInfo(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="glass-panel upload-container">
      <div className="text-center mb-8">
        <h1>Generate Quizzes instantly</h1>
        <p className="max-w-md mx-auto">
          Upload any lecture notes, textbook chapters, or research papers in PDF format. QuizLM will read the content and construct a custom quiz for you.
        </p>
      </div>

      {error && (
        <div className="error-banner">
          <AlertTriangle size={20} />
          <span>{error}</span>
        </div>
      )}

      {!uploading && !fileInfo && (
        <div 
          className={`dropzone ${dragActive ? "active" : ""}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={onButtonClick}
        >
          <input 
            ref={fileInputRef}
            type="file" 
            className="hidden" 
            style={{ display: "none" }}
            accept=".pdf"
            onChange={handleChange}
          />
          <div className="upload-icon-wrapper">
            <UploadCloud size={32} />
          </div>
          <div>
            <h3 className="mb-1">Drag and drop your PDF here</h3>
            <p className="text-sm text-muted">or click to browse from device</p>
          </div>
          <div className="text-xs text-muted mt-2 border-t border-color pt-3 w-full max-w-xs">
            Supports PDFs up to 50MB
          </div>
        </div>
      )}

      {uploading && (
        <div className="loading-overlay w-full">
          <div className="spinner"></div>
          <div>
            <h3>Reading PDF Content...</h3>
            <p className="text-sm text-muted mt-1">Analyzing pages and extracting text ({fileInfo?.name})</p>
          </div>
        </div>
      )}

      {fileInfo && !uploading && !error && (
        <div className="file-info-bar">
          <CheckCircle size={20} color="#10b981" />
          <div className="text-left flex-1">
            <div className="font-semibold text-sm truncate max-w-xs">{fileInfo.name}</div>
            <div className="text-xs text-muted">{fileInfo.size}</div>
          </div>
          <button className="btn btn-secondary btn-sm py-1.5 px-3" onClick={() => setFileInfo(null)}>
            <RefreshCw size={14} className="mr-1" /> Change
          </button>
        </div>
      )}
    </div>
  );
}
