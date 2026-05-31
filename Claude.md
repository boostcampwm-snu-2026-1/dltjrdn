# CLAUDE.md

마인크래프트 스킨 생성기 — 졸업작품. 이 파일은 프로젝트 컨텍스트를 담아 Claude Code가 자동으로 읽는다.

## 한 줄 요약
캐릭터 **이미지** 또는 **텍스트 아이디어**를 입력하면, 게임에 바로 업로드 가능한 **64×64 마인크래프트 스킨 PNG**를 생성한다.

## 동작 방식 (파이프라인)
`입력 → ① 프롬프트 생성(Gemini) → ② 스킨 생성(SDXL) → ③ 검증 → ④ UI`

| 단계 | 역할 | 구현 파일 | 상태 |
|---|---|---|---|
| ① 프롬프트 생성 | 입력(이미지/아이디어)을 SDXL용 영어 프롬프트로 변환 | `prompt_skill.py` | ✅ 완료 |
| ② 스킨 생성 | 프롬프트 → 64×64 스킨 (GPU 필요) | `sdxl_skin.py` | ⏳ 예정 |
| ③ 검증 | 64×64·RGBA·투명레이어 형식 확인 | `mc_skin_generator.py` (`validate_skin`) | ✅ 재활용 |
| ④ UI | 업로드/입력/결과 표시·다운로드 (웹) | `frontend/` (React) + `backend/` (FastAPI) | ⏳ 예정 |

## 핵심 설계 원칙
- **역할 분리**: 이미지 이해·프롬프트 설계 = Gemini / 스킨 픽셀 생성 = SDXL 파인튜닝 모델.
- **유효성 이중 보장**: SDXL(진짜 스킨으로 학습됨) + ③ 검증. 출력 스킨은 반드시 `validate_skin` 통과.
- **졸업작품 기여 포인트**: ① 프롬프트 엔지니어링 + 결과 품질 평가 + 파이프라인 설계. (단순 API 연결로 보이지 않도록 이 부분을 강조한다.)

## 기술 스택
**백엔드 / 모델 (Python 3.10+)**
- `google-genai` — Gemini (① 단계, 텍스트·비전 → 텍스트)
- `diffusers` + `torch` — SDXL 모델 추론 (② 단계)
- `Pillow` — 이미지 처리·검증
- `fastapi` + `uvicorn` — 웹 API 서버 (④ 백엔드). 엔드포인트: `POST /generate` (텍스트/이미지 입력 → 스킨 PNG)
- GPU 필요(②). 로컬 VRAM 부담되면 **Google Colab** 권장.

**프론트엔드 (웹 UI, ④)**
- `React` (Vite 또는 Next.js) — 텍스트 입력창 + 이미지 업로드 + 결과 스킨 표시·다운로드
- 백엔드와 분리(SPA). FastAPI에 `fetch`로 요청 → 결과 PNG 표시.
- 배포 시 CORS 설정 / 프론트는 정적 호스팅(예: Vercel), 백엔드는 GPU 서버 또는 Colab 터널.

> 입력은 **웹 화면**에서 받는다: 텍스트 아이디어 입력 + 이미지 파일 업로드 → 서버로 전송.

## 모델
- HuggingFace: `monadical-labs/minecraft-skin-generator-sdxl` (투명 레이어 지원 버전)
- 원본 레포: https://github.com/Monadical-SAS/minecraft_skin_generator (GPL-3.0)
- ② 구현 시 raw `diffusers`로 재발명하지 말 것. 위 레포를 클론해 추론 스크립트(`bin/minecraft-skins-sdxl.py`)를 재사용/래핑한다 — 스킨 특화 후처리가 들어있다.
- ⚠️ **라이선스**: 레포 코드 GPL-3.0 → 배포 시 소스 공개 의무. 모델 가중치 라이선스는 모델 카드에서 별도 확인.
- 프롬프트는 짧고 시각 특징 중심의 영어가 가장 잘 먹는다 (예: `"a man in a purple suit wearing a tophat"`).

## 파일 구조 (목표)
```
backend/
  prompt_skill.py      # ① 프롬프트 생성 (예정)
  sdxl_skin.py         # ② SDXL 래퍼: generate_skin(prompt) -> PIL.Image (예정)
  mc_skin_generator.py # UV 좌표 상수 + validate_skin (③). ※ 아래 주의 참고
  main.py              # ④ FastAPI 서버: POST /generate (예정)
  requirements.txt
frontend/              # ④ React 웹 UI (예정)
  src/                 #   입력폼(텍스트/이미지) + 결과 표시·다운로드
  package.json
eval/                  # 품질 평가 스크립트 (예정 — 졸업작품 기여 강화)
README.md
```

## ① 프롬프트 생성 규칙 (`prompt_skill.py` 출력 형식)
- 영어 **한 줄**, **캐릭터** 묘사 (장면 X).
- 포함: 역할/아키타입, 의상, **색상**, 헤드기어, 특징 액세서리 1~3개.
- 금지: 포즈, 카메라 앵글, 배경, 조명, 단어 `Minecraft`/`skin`/`pixel art`, 화질 표현.
- 길이 약 8~20단어. 모호한 형용사보다 구체적 색.
- 두 입력 모드: `build_skin_prompt(key, image_path=...)` / `build_skin_prompt(key, idea=...)`.

## 마인크래프트 스킨 형식 (불변 규칙 — 절대 어기지 말 것)
- 출력은 **64×64 RGBA PNG**.
- UV 레이아웃 좌표는 고정. `mc_skin_generator.py`의 `PARTS` / `UV` 상수를 **단일 출처(single source of truth)**로 사용.
- 베이스 레이어 면은 **완전 불투명**(alpha 255), 두 번째(겉) 레이어는 투명 유지.
- 기준 모델은 클래식(Steve, 팔 4px). 슬림(Alex, 3px)은 팔 좌표만 변형.
- 모든 생성 결과는 `validate_skin()`이 빈 리스트(=통과)를 반환해야 한다.

## ⚠️ `mc_skin_generator.py` 주의
- 이 파일엔 **초기 접근**("Gemini가 정면 그림 생성 → 코드로 잘라 UV에 매핑")도 들어있다 (`build_skin`, `slice_frontview`, `generate_frontview` 등).
- **현재 SDXL 파이프라인에서는 그 생성 로직을 쓰지 않는다.** `PARTS`/`UV` 좌표 상수와 `validate_skin`만 재활용한다.
- 혼동 방지: ② 스킨 생성의 주체는 SDXL이다.

## 명령어
```bash
# 백엔드 설치
pip install google-genai diffusers torch pillow fastapi "uvicorn[standard]" python-multipart

# 환경변수 (API 키 하드코딩 금지)
export GEMINI_API_KEY="..."

# ① 단독 테스트
python -c "import os; from prompt_skill import build_skin_prompt; print(build_skin_prompt(os.environ['GEMINI_API_KEY'], idea='좀비 해적'))"

# ④ 백엔드 서버 실행 (작성 후)
uvicorn backend.main:app --reload

# ④ 프론트엔드 (작성 후)
cd frontend && npm install && npm run dev
```

## 작업 지침 (Claude Code용)
- 코드 주석은 한국어 OK, 식별자(변수·함수명)는 영어.
- API 키·시크릿은 **환경변수로만**. 절대 코드/커밋에 하드코딩하지 말 것.
- 무거운 모델 추론은 로컬보다 **Colab 노트북** 형태로 작성하면 환경 리스크가 적다.
- 새 코드가 스킨을 만들면 항상 `validate_skin`으로 검증하는 경로를 포함한다.
- 외부 모델·라이브러리 추가 시 라이선스 확인(특히 GPL 전파).

## 현재 상태
- [x] 파이프라인 구조 설계
- [x] ① `prompt_skill.py` (이미지/텍스트 두 모드 + few-shot)
- [x] ③ `validate_skin` (`mc_skin_generator.py`)
- [ ] ② `sdxl_skin.py` — Monadical 레포 래핑, Colab용
- [ ] ④ `app.py` — Gradio UI
- [ ] 품질 평가 스크립트 (졸업작품 기여 강화)