from PIL import Image

SKIN_SIZE = 64

BASE_LAYER_RECTS = {
    "head": [(8, 0, 16, 8), (0, 8, 32, 8)],
    "body": [(20, 16, 16, 4), (16, 20, 24, 12)],
    "right_arm": [(44, 16, 8, 4), (40, 20, 16, 12)],
    "right_leg": [(4, 16, 8, 4), (0, 20, 16, 12)],
    "left_leg": [(20, 48, 8, 4), (16, 52, 16, 12)],
    "left_arm": [(36, 48, 8, 4), (32, 52, 16, 12)],
}

OVERLAY_LAYER_RECTS = {
    "hat": [(40, 0, 16, 8), (32, 8, 32, 8)],
    "jacket": [(20, 32, 16, 4), (16, 36, 24, 12)],
    "right_sleeve": [(44, 32, 8, 4), (40, 36, 16, 12)],
    "right_pant": [(4, 32, 8, 4), (0, 36, 16, 12)],
    "left_pant": [(4, 48, 8, 4), (0, 52, 16, 12)],
    "left_sleeve": [(52, 48, 8, 4), (48, 52, 16, 12)],
}

PARTS = list(BASE_LAYER_RECTS.keys())


def validate_skin(img: Image.Image) -> list[str]:
    errors = []

    if img.size != (SKIN_SIZE, SKIN_SIZE):
        errors.append(f"크기가 {img.size}, 64×64 여야 함")

    if img.mode != "RGBA":
        errors.append(f"모드가 {img.mode}, RGBA 여야 함")
        return errors

    alpha = img.getchannel("A")
    for part, rects in BASE_LAYER_RECTS.items():
        for (x, y, w, h) in rects:
            region = alpha.crop((x, y, x + w, y + h))
            lo, _ = region.getextrema()
            if lo < 255:
                errors.append(
                    f"베이스 레이어 '{part}' 영역 ({x},{y},{w},{h})에 "
                    f"투명/반투명 픽셀 있음 (min alpha={lo})"
                )

    return errors


def load_skin(path: str) -> Image.Image:
    return Image.open(path).convert("RGBA")


if __name__ == "__main__":

    valid = Image.new("RGBA", (64, 64), (100, 150, 200, 255))
    print("유효 스킨 검사:", validate_skin(valid) or "통과(빈 리스트)")

    transparent = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    print("투명 스킨 검사:", len(validate_skin(transparent)), "개 위반 감지")

    wrong = Image.new("RGBA", (32, 32), (0, 0, 0, 255))
    print("32x32 검사:", validate_skin(wrong))
