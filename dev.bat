@echo off
REM Run backend (FastAPI) and frontend (Vite) in separate windows.
REM API key is read from backend/.env (see backend/.env.example).

REM backend: auto-activate venv (torch lives there), then run uvicorn
start "backend" cmd /k "cd /d %~dp0backend && call ..\.venv\Scripts\activate.bat && uvicorn main:app"
start "frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo Started both servers in new windows.
echo   backend:  http://localhost:8000
echo   frontend: http://localhost:5173  (open this in your browser)
