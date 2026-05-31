"""③ 검증 + 스킨 형식 단일 출처.

마인크래프트 64×64 스킨의 UV 레이아웃 좌표와 검증 함수를 제공한다.
- BASE_LAYER_RECTS / OVERLAY_LAYER_RECTS / PARTS: 형식 단일 출처(single source of truth)
- validate_skin(img): 형식 검사. 빈 리스트를 반환하면 통과.

기준 모델: 클래식(Steve, 팔 4px), 64×64 RGBA.
SDXL 등으로 생성된 스킨은 반드시 validate_skin()을 통과해야 한다.

※ 주의: 이 파일에서는 좌표 상수와 validate_skin'만' 재활용한다.
   (초기 접근의 정면도 생성 로직은 현재 SDXL 파이프라인에서 쓰지 않음)
"""

from PIL import Image

# 스킨 한 변의 크기
SKIN_SIZE = 64

# 베이스 레이어가 차지하는 영역 (반드시 불투명, alpha 255). (x, y, w, h)
# 64×64 클래식 레이아웃. 각 부위는 [top/bottom 행] + [옆/앞/뒤 행] 두 사각형으로 표현.
BASE_LAYER_RECTS = {
    "head": [(8, 0, 16, 8), (0, 8, 32, 8)],
    "body": [(20, 16, 16, 4), (16, 20, 24, 12)],
    "right_arm": [(44, 16, 8, 4), (40, 20, 16, 12)],   # 4px 팔
    "right_leg": [(4, 16, 8, 4), (0, 20, 16, 12)],
    "left_leg": [(20, 48, 8, 4), (16, 52, 16, 12)],
    "left_arm": [(36, 48, 8, 4), (32, 52, 16, 12)],
}

# 겉(두 번째) 레이어 영역 — 투명 허용. (x, y, w, h)
OVERLAY_LAYER_RECTS = {
    "hat": [(40, 0, 16, 8), (32, 8, 32, 8)],
    "jacket": [(20, 32, 16, 4), (16, 36, 24, 12)],
    "right_sleeve": [(44, 32, 8, 4), (40, 36, 16, 12)],
    "right_pant": [(4, 32, 8, 4), (0, 36, 16, 12)],
    "left_pant": [(4, 48, 8, 4), (0, 52, 16, 12)],
    "left_sleeve": [(52, 48, 8, 4), (48, 52, 16, 12)],
}

# 전체 부위 목록(참조용)
PARTS = list(BASE_LAYER_RECTS.keys())


def validate_skin(img: Image.Image) -> list[str]:
    """스킨 형식을 검사한다. 빈 리스트면 통과.

    검사 항목:
      1) 크기 64×64
      2) 모드 RGBA
      3) 베이스 레이어 영역이 모두 불투명(alpha 255)
    """
    errors = []

    # 1) 크기
    if img.size != (SKIN_SIZE, SKIN_SIZE):
        errors.append(f"크기가 {img.size}, 64×64 여야 함")

    # 2) 모드 (RGBA 아니면 alpha 검사 불가 → 여기서 종료)
    if img.mode != "RGBA":
        errors.append(f"모드가 {img.mode}, RGBA 여야 함")
        return errors

    # 3) 베이스 레이어 불투명 검사
    alpha = img.getchannel("A")
    for part, rects in BASE_LAYER_RECTS.items():
        for (x, y, w, h) in rects:
            region = alpha.crop((x, y, x + w, y + h))
            lo, _ = region.getextrema()  # 최소 alpha
            if lo < 255:
                errors.append(
                    f"베이스 레이어 '{part}' 영역 ({x},{y},{w},{h})에 "
                    f"투명/반투명 픽셀 있음 (min alpha={lo})"
                )

    return errors


def load_skin(path: str) -> Image.Image:
    """스킨 PNG를 RGBA로 연다."""
    return Image.open(path).convert("RGBA")


if __name__ == "__main__":
    # 자체 테스트: 유효한 스킨 / 깨진 스킨

    # (a) 베이스 전부 불투명 → 통과해야 함
    valid = Image.new("RGBA", (64, 64), (100, 150, 200, 255))
    print("유효 스킨 검사:", validate_skin(valid) or "통과(빈 리스트)")

    # (b) 전부 투명 → 베이스 레이어 불투명 위반
    transparent = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    print("투명 스킨 검사:", len(validate_skin(transparent)), "개 위반 감지")

    # (c) 잘못된 크기 → 위반
    wrong = Image.new("RGBA", (32, 32), (0, 0, 0, 255))
    print("32x32 검사:", validate_skin(wrong))
