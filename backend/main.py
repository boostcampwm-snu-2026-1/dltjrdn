"""④ 백엔드 — FastAPI 서버.

현재는 테스트용으로 ① 프롬프트 생성까지만 노출한다:
    POST /generate-prompt  (텍스트 idea / 이미지 / 둘 다) -> {"prompt": "..."}
② SDXL이 준비되면 여기에 스킨 생성 엔드포인트를 추가한다.
"""

import os
import tempfile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# 실행 위치(루트 / backend)에 상관없이 import 되도록 처리
try:
    from prompt_skill import build_skin_prompt
except ImportError:  # uvicorn backend.main:app 로 실행한 경우
    from backend.prompt_skill import build_skin_prompt

app = FastAPI(title="마크 스킨생성기 API")

# 프론트(Vite dev 서버)에서 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-prompt")
async def generate_prompt(
    idea: str = Form(None),
    image: UploadFile = File(None),
):
    """입력을 받아 Gemini가 만든 SDXL용 프롬프트를 돌려준다 (테스트용)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY 미설정")

    idea = idea or None  # 빈 문자열은 None 취급
    if not idea and image is None:
        raise HTTPException(status_code=400, detail="아이디어 또는 이미지를 입력하세요.")

    # 업로드 이미지는 임시 파일로 저장해 경로를 넘긴다
    image_path = None
    if image is not None:
        suffix = os.path.splitext(image.filename)[1] or ".png"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(await image.read())
        tmp.close()
        image_path = tmp.name

    try:
        prompt = build_skin_prompt(key, idea=idea, image_path=image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프롬프트 생성 실패: {e}")
    finally:
        if image_path:
            os.unlink(image_path)  # 임시 파일 정리

    return {"prompt": prompt}
