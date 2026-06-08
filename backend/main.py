import base64
import io
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

try:
    from prompt_skill import build_skin_prompt
except ImportError:
    from backend.prompt_skill import build_skin_prompt

app = FastAPI(title="마크 스킨생성기 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _build_prompt(idea, image: UploadFile) -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY 미설정")

    idea = idea or None
    if not idea and image is None:
        raise HTTPException(status_code=400, detail="아이디어 또는 이미지를 입력하세요.")

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
            os.unlink(image_path)


@app.post("/generate-prompt")
async def generate_prompt(
    idea: str = Form(None),
    image: UploadFile = File(None),
):
    prompt = await _build_prompt(idea, image)
    return {"prompt": prompt}


@app.post("/generate")
async def generate(
    idea: str = Form(None),
    image: UploadFile = File(None),
    direct: bool = Form(False),
):
    from sdxl_skin import generate_skin
    from mc_skin_generator import validate_skin

    if direct:
        if not idea or not idea.strip():
            raise HTTPException(status_code=400, detail="직접 모드는 영어 프롬프트 입력이 필요합니다.")
        prompt = idea.strip()
    else:
        prompt = await _build_prompt(idea, image)

    try:
        skin = generate_skin(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"스킨 생성 실패: {e}")

    errors = validate_skin(skin)

    buf = io.BytesIO()
    skin.save(buf, format="PNG")
    data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    return {"prompt": prompt, "image": data_url, "valid": not errors, "errors": errors}


_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="frontend")
