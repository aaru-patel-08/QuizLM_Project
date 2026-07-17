"""
AI Quiz Generator — FastAPI Backend
Main application entrypoint.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Load environment variables from .env file
load_dotenv()

# In-memory storage for documents and quizzes (session-only for MVP)
documents_store: dict = {}
quizzes_store: dict = {}

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: validate API key is present
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        print("⚠️  WARNING: GEMINI_API_KEY not set. Quiz generation will fail.")
        print("   Copy .env.example to .env and add your API key.")
    else:
        print("✅ Gemini API key loaded.")
    print("🚀 AI Quiz Generator backend started.")
    yield
    # Shutdown
    print("👋 Backend shutting down.")


app = FastAPI(
    title="AI Quiz Generator",
    description="Generate quizzes from PDF documents using AI",
    version="1.0.0",
    lifespan=lifespan,
)

# Rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return a clean JSON error."""
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": str(exc),
        },
    )


# Import and include routers
from routers.upload import router as upload_router
from routers.quiz import router as quiz_router

app.include_router(upload_router, tags=["Upload"])
app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    api_key = os.getenv("GEMINI_API_KEY")
    return {
        "status": "healthy",
        "api_key_configured": bool(api_key and api_key != "your_key_here"),
    }
