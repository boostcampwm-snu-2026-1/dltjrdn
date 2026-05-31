"""① 프롬프트 생성 — Gemini로 입력(텍스트 아이디어 / 이미지)을 SDXL용 영어 프롬프트로 변환.

핵심 기여 단계: '좋은 프롬프트'를 만드는 곳. 출력 규칙은 CLAUDE.md ① 규칙을 따른다.
- 영어 한 줄, 캐릭터 묘사(장면 X)
- 포함: 역할/아키타입, 의상, 색상, 헤드기어, 특징 액세서리 1~3개
- 금지: 포즈/앵글/배경/조명, 단어 Minecraft/skin/pixel art, 화질 표현

사용:
    from prompt_skill import build_skin_prompt
    build_skin_prompt(key, idea="좀비 해적")
    build_skin_prompt(key, image_path="char.png")
"""

import mimetypes
import re

from google import genai
from google.genai import types

# Gemini 모델 — 텍스트/비전 모두 지원
MODEL = "gemini-2.5-flash"

# 출력 규칙을 강제하는 시스템 지침 (모델이 영어로 출력하도록 영어로 작성)
SYSTEM_INSTRUCTION = """You write ONE short English prompt describing a single CHARACTER for an image generator.

STRICT RULES:
- Output ONE line only. No quotes, no list, no explanation.
- Describe the CHARACTER, not a scene.
- Include: role/archetype, clothing, explicit COLORS, headgear, 1-3 signature accessories.
- 8-20 words. Prefer concrete colors over vague adjectives.
- ALWAYS describe concrete visual features — the creature/character TYPE (e.g. dinosaur,
  penguin, knight), colors, clothing, headgear, distinctive body parts — detailed enough
  to DRAW the character WITHOUT knowing its name.
- Do NOT output the character's NAME. Translate any recognized character into the visual
  features above. If you are unsure of the exact species, describe shape and colors only
  (e.g. "a small round green creature") rather than guessing a wrong animal.
- FORBIDDEN: poses, camera angles, background, lighting, image-quality words
  (e.g. "high quality", "4k", "detailed"), and the words "Minecraft", "skin", "pixel art".

Good examples:
- a grizzled pirate captain in a dark red coat with a black tricorn hat and gold earrings
- a young wizard in a deep purple robe with silver star patterns and a tall pointed hat
- a rotting zombie sailor in a torn blue uniform with a tattered captain's hat and a hook hand
"""


def _sanitize(text: str) -> str:
    """모델 출력을 한 줄로 정리하고 금지어를 제거한다."""
    # 줄바꿈/연속 공백을 하나로, 따옴표 제거
    line = " ".join(text.split())
    line = line.strip().strip('"').strip("'").strip()
    # 끝의 마침표 제거 (CLAUDE.md 스타일: 마침표 없는 한 줄)
    line = line.rstrip(".")
    # 금지 단어 제거 (대소문자 무시)
    for word in ("minecraft", "pixel art", "pixelated", "skin"):
        line = re.sub(rf"\b{re.escape(word)}\b", "", line, flags=re.IGNORECASE)
    # 제거로 생긴 중복 공백 정리
    line = " ".join(line.split())
    return line


def build_skin_prompt(key: str, idea: str = None, image_path: str = None) -> str:
    """입력을 SDXL용 영어 프롬프트 한 줄로 변환한다.

    Args:
        key: Gemini API 키 (환경변수에서 읽어 전달).
        idea: 텍스트 아이디어 (예: "좀비 해적"). 텍스트 모드.
        image_path: 캐릭터 이미지 경로. 이미지 모드.

    셋 중 하나의 모드로 동작한다:
        - 텍스트만 (idea): 아이디어를 상상해 묘사
        - 이미지만 (image_path): 이미지를 보고 묘사
        - 둘 다: 이미지를 기본으로, idea를 추가 지시로 반영
    idea / image_path 중 최소 하나는 전달해야 한다.
    """
    if not idea and not image_path:
        raise ValueError("idea 또는 image_path 중 최소 하나는 전달하세요.")

    client = genai.Client(api_key=key)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.7,
        # 구글 검색 grounding: 모델이 모르는 캐릭터(예: 마이너 애니 캐릭터)를
        # 실시간 검색해 정체(종·외형)를 파악하도록 보강한다.
        tools=[types.Tool(google_search=types.GoogleSearch())],
    )

    contents = []

    # 이미지가 있으면 먼저 넣는다 (Gemini는 이미지+텍스트를 한 맥락으로 처리)
    if image_path:
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/png"  # 판별 실패 시 기본값
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

    # 모드별 지시문
    if image_path and idea:
        instruction = (
            "Base the character on the image, then apply this extra direction: "
            f"{idea}. Output one prompt following the rules."
        )
    elif image_path:
        instruction = "Describe this character as one prompt following the rules."
    else:  # idea만
        instruction = f"Turn this idea into one character prompt: {idea}"
    contents.append(instruction)

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=config,
    )
    return _sanitize(response.text)


if __name__ == "__main__":
    # 단독 테스트: GEMINI_API_KEY 환경변수 필요
    import os

    api_key = os.environ["GEMINI_API_KEY"]
    for idea in ["좀비 해적", "보라색 정장을 입은 마법사", "사이버펑크 닌자"]:
        print(f"[{idea}] -> {build_skin_prompt(api_key, idea=idea)}")
