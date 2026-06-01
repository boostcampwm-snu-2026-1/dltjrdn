import os
import sys

from prompt_skill import build_skin_prompt
from sdxl_skin import generate_skin
from mc_skin_generator import validate_skin


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[오류] GEMINI_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    idea = " ".join(sys.argv[1:]).strip()
    if not idea:
        idea = input("아이디어를 입력하세요: ").strip()
    if not idea:
        print("[오류] 아이디어가 비었습니다.")
        sys.exit(1)

    print(f"\n[①] 아이디어: {idea}")
    prompt = build_skin_prompt(key, idea=idea)
    print(f"[①] 생성된 프롬프트: {prompt}")

    print("\n[②] 스킨 생성 중... (잠시 걸림)")
    skin = generate_skin(prompt)

    out_path = f"skin_{idea.replace(' ', '_')[:20]}.png"
    skin.save(out_path)
    print(f"[②] 저장됨: {out_path}  ({skin.size}, {skin.mode})")

    errors = validate_skin(skin)
    print("\n[③] 검증 결과:", errors or "통과(빈 리스트)")
    if errors:
        print("  → 형식 위반이 있습니다. 위 목록 확인.")
    else:
        print("  → 파이프라인 전체 통과! 스킨 뷰어에 올려보세요.")


if __name__ == "__main__":
    main()
