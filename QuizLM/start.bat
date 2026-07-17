@echo off
echo ==============================================
echo  Starting QuizLM - AI Quiz Generator Setup...
echo ==============================================

:: 1. Setup Python Virtual Environment
echo.
echo [1/4] Checking Python virtual environment...
if not exist "backend\venv" (
    echo Creating backend\venv virtual environment...
    python -m venv backend\venv
)

echo Activating virtual environment...
call backend\venv\Scripts\activate.bat

echo Installing/Updating Python dependencies...
pip install --upgrade pip
pip install -r backend\requirements.txt

:: 2. Setup Frontend dependencies
echo.
echo [2/4] Verifying frontend dependencies...
if not exist "frontend\node_modules" (
    echo Running npm install in frontend...
    cd frontend
    npm install
    cd ..
)

:: 3. Start Backend Server
echo.
echo [3/4] Launching FastAPI backend on http://localhost:8000...
start "QuizLM Backend" cmd /k "cd backend && ..\backend\venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Give backend a moment to spin up
timeout /t 3 /nobreak > nul

:: 4. Start Frontend Server
echo.
echo [4/4] Launching Vite frontend on http://localhost:5173...
start "QuizLM Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==============================================
echo  QuizLM is running!
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:5173
echo  API Docs: http://localhost:8000/docs
echo ==============================================
echo.
echo Close this window or press Ctrl+C to stop.
pause
