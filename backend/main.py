"""④ 백엔드 — FastAPI 서버.

현재는 테스트용으로 ① 프롬프트 생성까지만 노출한다:
    POST /generate-prompt  (텍스트 idea / 이미지 / 둘 다) -> {"prompt": "..."}
② SDXL이 준비되면 여기에 스킨 생성 엔드포인트를 추가한다.
"""

import base64
import io
import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# backend/.env 에서 GEMINI_API_KEY 등을 자동 로드 (창마다 set 안 해도 됨)
load_dotenv()

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


async def _build_prompt(idea, image: UploadFile) -> str:
    """idea/업로드 이미지로 ① 프롬프트를 만든다. (두 엔드포인트 공용)"""
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
        return build_skin_prompt(key, idea=idea, image_path=image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프롬프트 생성 실패: {e}")
    finally:
        if image_path:
            os.unlink(image_path)  # 임시 파일 정리


@app.post("/generate-prompt")
async def generate_prompt(
    idea: str = Form(None),
    image: UploadFile = File(None),
):
    """입력 → Gemini 프롬프트만 반환 (가벼운 테스트용)."""
    prompt = await _build_prompt(idea, image)
    return {"prompt": prompt}


@app.post("/generate")
async def generate(
    idea: str = Form(None),
    image: UploadFile = File(None),
):
    """입력 → 프롬프트 → SDXL 스킨 PNG 생성 → 검증 → 반환.

    응답: {prompt, image(dataURL), valid, errors}
    """
    # torch/diffusers는 무거우니 여기서 지연 import
    from sdxl_skin import generate_skin
    from mc_skin_generator import validate_skin

    prompt = await _build_prompt(idea, image)

    try:
        skin = generate_skin(prompt)  # 64×64 RGBA
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"스킨 생성 실패: {e}")

    errors = validate_skin(skin)

    # PNG → base64 dataURL (프론트에서 표시·다운로드)
    buf = io.BytesIO()
    skin.save(buf, format="PNG")
    data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {"prompt": prompt, "image": data_url, "valid": not errors, "errors": errors}
