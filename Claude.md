# CLAUDE.md

마인크래프트 스킨 생성기 — 졸업작품. Claude Code가 자동으로 읽는 컨텍스트.

## 한 줄 요약
캐릭터 **이미지** 또는 **텍스트 아이디어** → 게임에 업로드 가능한 **64×64 마인크래프트 스킨 PNG** 생성.

## 파이프라인
`입력 → ① 프롬프트(Gemini) → ② 스킨(SDXL, 로컬 GPU) → ③ 검증 → ④ 웹 UI`

| 단계 | 파일 | 상태 |
|---|---|---|
| ① 프롬프트 생성 | `backend/prompt_skill.py` | ✅ |
| ② SDXL 스킨 생성 | `backend/sdxl_skin.py` | ✅ (품질 튜닝 중) |
| ③ 검증 | `backend/mc_skin_generator.py` | ✅ |
| ④ 웹 UI | `frontend/` + `backend/main.py` | ✅ |

## 📄 상세 문서 (먼저 참고)
- [docs/architecture.md](docs/architecture.md) — 구조·데이터 흐름·실행 환경
- [docs/design.md](docs/design.md) — 설계 결정과 근거 (역할 분리, 프롬프트 규칙, 후처리 등)
- [docs/checklist.md](docs/checklist.md) — 진행 상황 / 남은 일
- [docs/git.md](docs/git.md) — 커밋 규칙
- [README.md](README.md) — 설치·실행

## 마인크래프트 스킨 형식 (불변 규칙 — 절대 어기지 말 것)
- 출력은 **64×64 RGBA PNG**.
- UV 좌표는 `mc_skin_generator.py`의 `BASE_LAYER_RECTS`/`OVERLAY_LAYER_RECTS`가 **단일 출처**.
- 베이스 레이어 면은 **완전 불투명**(alpha 255), 겉(두 번째) 레이어는 투명 허용.
- 기준 모델은 클래식(Steve, 팔 4px).
- 모든 생성 결과는 `validate_skin()`이 빈 리스트(=통과)를 반환해야 한다.

## 작업 지침 (Claude Code용)
- 코드 주석은 한국어 OK, 식별자(변수·함수명)는 영어.
- API 키·시크릿은 **`backend/.env`에만** (gitignore). 코드/커밋에 하드코딩 금지.
- 새 코드가 스킨을 만들면 항상 `validate_skin` 검증 경로를 포함.
- 백엔드는 **Python 3.12 venv**(torch)에서 실행. 코드 바꾸면 백엔드 재시작 필요(uvicorn 자동reload 아님).
- 커밋은 [docs/git.md](docs/git.md) 규칙대로. 외부 모델·라이브러리 추가 시 라이선스 확인(특히 GPL 전파).
