"""② SDXL 스킨 생성 — Monadical 파인튜닝 모델 래퍼.

generate_skin(prompt) -> PIL.Image (64×64 RGBA)

로컬 GPU(RTX 4060 Ti, 8GB) 대응:
- fp16 로 로드
- enable_model_cpu_offload: 활성 모듈만 GPU에 올려 VRAM 절약
- attention slicing / VAE tiling: 추가 메모리 절약

모델: monadical-labs/minecraft-skin-generator-sdxl (GPL-3.0 / 모델 카드 라이선스 확인)
첫 실행 시 모델(~7GB)을 자동 다운로드한다.
"""

import torch
from diffusers import DiffusionPipeline
from PIL import Image

MODEL_ID = "monadical-labs/minecraft-skin-generator-sdxl"

_pipeline = None  # 파이프라인은 한 번만 로드(지연 로딩)


def _get_pipeline():
    """SDXL 파이프라인을 로드(최초 1회). 8GB VRAM 최적화 적용."""
    global _pipeline
    if _pipeline is None:
        _pipeline = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
        )
        # 8GB VRAM 대응 — 메모리 절약 옵션
        _pipeline.enable_model_cpu_offload()
        _pipeline.enable_attention_slicing()
        _pipeline.enable_vae_tiling()
    return _pipeline


def generate_skin(
    prompt: str,
    num_inference_steps: int = 25,
    guidance_scale: float = 7.5,
    seed: int | None = None,
) -> Image.Image:
    """프롬프트로 64×64 RGBA 스킨을 생성한다.

    Args:
        prompt: SDXL용 영어 프롬프트 (① prompt_skill 출력).
        num_inference_steps: 디노이즈 스텝 수(↑품질·↑시간).
        guidance_scale: 프롬프트 충실도.
        seed: 재현용 시드(없으면 랜덤).
    """
    pipe = _get_pipeline()

    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=generator,
    )
    image = result.images[0]

    # SDXL은 큰 해상도로 출력 → 64×64 스킨으로 축소(픽셀 보존 위해 NEAREST)
    skin = image.resize((64, 64), Image.NEAREST).convert("RGBA")
    return skin


if __name__ == "__main__":
    # 단독 테스트: 프롬프트 1개 생성 → validate_skin 통과 확인
    from mc_skin_generator import validate_skin

    test_prompt = "a wizard in a deep purple robe with silver stars and a tall pointed hat"
    print("스킨 생성 중... (첫 실행은 모델 다운로드로 오래 걸림)")
    skin = generate_skin(test_prompt, seed=42)

    out_path = "test_skin.png"
    skin.save(out_path)
    print(f"저장됨: {out_path}  크기={skin.size} 모드={skin.mode}")

    errors = validate_skin(skin)
    print("검증 결과:", errors or "통과(빈 리스트)")
