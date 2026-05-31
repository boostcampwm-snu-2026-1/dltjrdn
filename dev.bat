@echo off
REM 백엔드(FastAPI)와 프론트(Vite)를 각각 새 창에서 동시에 실행한다.
REM 사용 전 1회: setx GEMINI_API_KEY 키   (영구 등록 → 새 창들이 자동으로 키를 가짐)

REM 키가 등록돼 있는지 확인
if "%GEMINI_API_KEY%"=="" (
  echo [경고] GEMINI_API_KEY 가 없습니다.
  echo  먼저 한 번만 실행하세요:  setx GEMINI_API_KEY 여기에_키
  echo  그 다음 이 창을 닫고 dev.bat 를 다시 실행하세요.
  pause
  exit /b
)

REM 백엔드: backend 폴더에서 uvicorn
start "backend" cmd /k "cd /d %~dp0backend && uvicorn main:app --reload"

REM 프론트: frontend 폴더에서 vite dev
start "frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo 두 서버를 새 창에서 실행했습니다.
echo  - 백엔드:  http://localhost:8000
echo  - 프론트:  http://localhost:5173  (이걸 브라우저로 여세요)
