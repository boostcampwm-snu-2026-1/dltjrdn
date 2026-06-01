import mimetypes
import re
import time

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """You write ONE short English prompt describing a single CHARACTER for an image generator.

STRICT RULES:
- Output ONE line only. No quotes, no list, no explanation.
- Describe the CHARACTER, not a scene.
- Include: role/archetype, clothing, explicit COLORS, headgear, 1-3 signature accessories.
- 8-20 words. Prefer concrete colors over vague adjectives.
- ALWAYS describe concrete visual features — the creature/character TYPE (e.g. dinosaur,
  penguin, knight), colors, clothing, headgear, distinctive body parts — detailed enough
  to DRAW the character WITHOUT knowing its name.
- Only if the subject is GLOBALLY iconic (a world-famous person or character almost
  everyone would recognize, e.g. Spider-Man, Lionel Messi, Mario), you MAY start with
  its name, then STILL add the visual features above (signature outfit, colors).
  For anyone/anything less than globally famous, omit the name and describe appearance only.
- If unsure of a creature's exact species, describe shape and colors only
  (e.g. "a small round green creature") rather than guessing a wrong animal.
- FORBIDDEN: poses, camera angles, background, lighting, image-quality words
  (e.g. "high quality", "4k", "detailed"), and the words "Minecraft", "skin", "pixel art".

Good examples:
- a grizzled pirate captain in a dark red coat with a black tricorn hat and gold earrings
- a young wizard in a deep purple robe with silver star patterns and a tall pointed hat
- a rotting zombie sailor in a torn blue uniform with a tattered captain's hat and a hook hand
"""


def _sanitize(text: str) -> str:
    line = " ".join(text.split())
    line = line.strip().strip('"').strip("'").strip()
    line = line.rstrip(".")
    for word in ("minecraft", "pixel art", "pixelated", "skin"):
        line = re.sub(rf"\b{re.escape(word)}\b", "", line, flags=re.IGNORECASE)
    line = " ".join(line.split())
    return line


def build_skin_prompt(key: str, idea: str = None, image_path: str = None) -> str:
    if not idea and not image_path:
        raise ValueError("idea 또는 image_path 중 최소 하나는 전달하세요.")

    client = genai.Client(api_key=key)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.7,
    )

    contents = []

    if image_path:
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = "image/png"
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

    if image_path and idea:
        instruction = (
            "Base the character on the image, then apply this extra direction: "
            f"{idea}. Output one prompt following the rules."
        )
    elif image_path:
        instruction = "Describe this character as one prompt following the rules."
    else:
        instruction = f"Turn this idea into one character prompt: {idea}"
    contents.append(instruction)

    last_err = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=config,
            )
            return _sanitize(response.text)
        except Exception as e:
            last_err = e
            msg = str(e).lower()
            transient = "503" in msg or "unavailable" in msg or "overloaded" in msg
            if transient and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise last_err


if __name__ == "__main__":
    import os

    api_key = os.environ["GEMINI_API_KEY"]
    for idea in ["좀비 해적", "보라색 정장을 입은 마법사", "사이버펑크 닌자"]:
        print(f"[{idea}] -> {build_skin_prompt(api_key, idea=idea)}")
