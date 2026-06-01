import torch
from diffusers import DiffusionPipeline
from PIL import Image

from mc_skin_generator import OVERLAY_LAYER_RECTS

MODEL_ID = "monadical-labs/minecraft-skin-generator-sdxl"

GEN_SIZE = 768

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
        )
        _pipeline.enable_model_cpu_offload()
        _pipeline.enable_attention_slicing()
        _pipeline.enable_vae_tiling()
    return _pipeline


def generate_skin(
    prompt: str,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    seed: int | None = None,
) -> Image.Image:
    pipe = _get_pipeline()

    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt,
        height=GEN_SIZE,
        width=GEN_SIZE,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )
    return _to_skin(result.images[0])


def _to_skin(image: Image.Image) -> Image.Image:
    top = image.crop((0, 0, GEN_SIZE, GEN_SIZE // 2))
    legacy = top.resize((64, 32), Image.NEAREST).convert("RGBA")

    skin = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    skin.paste(legacy, (0, 0))
    skin.paste(legacy.crop((40, 16, 56, 32)), (32, 48))
    skin.paste(legacy.crop((0, 16, 16, 32)), (16, 48))

    for rects in OVERLAY_LAYER_RECTS.values():
        for (x, y, w, h) in rects:
            skin.paste((0, 0, 0, 0), (x, y, x + w, y + h))

    return skin


if __name__ == "__main__":
    from mc_skin_generator import validate_skin

    test_prompt = "a wizard in a deep purple robe with silver stars and a tall pointed hat"
    print("스킨 생성 중... (첫 실행은 모델 다운로드로 오래 걸림)")
    skin = generate_skin(test_prompt, seed=42)

    out_path = "test_skin.png"
    skin.save(out_path)
    print(f"저장됨: {out_path}  크기={skin.size} 모드={skin.mode}")

    errors = validate_skin(skin)
    print("검증 결과:", errors or "통과(빈 리스트)")
