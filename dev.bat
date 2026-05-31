@echo off
REM Run backend (FastAPI) and frontend (Vite) in separate windows.
REM One-time setup:  setx GEMINI_API_KEY your_key   (then open a NEW window)

if "%GEMINI_API_KEY%"=="" (
  echo [WARN] GEMINI_API_KEY is not set.
  echo   Run once:  setx GEMINI_API_KEY your_key
  echo   Then close this window and run dev.bat again in a NEW window.
  pause
  exit /b
)

start "backend" cmd /k "cd /d %~dp0backend && uvicorn main:app --reload"
start "frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Started both servers in new windows.
echo   backend:  http://localhost:8000
echo   frontend: http://localhost:5173  (open this in your browser)
