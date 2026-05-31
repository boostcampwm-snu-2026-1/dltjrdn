# 아키텍처 (Architecture)

마인크래프트 스킨 생성기의 시스템 구조와 데이터 흐름.

## 한눈에 보기

```
┌──────────────┐      HTTP (multipart/form-data)      ┌─────────────────────────┐
│  Frontend     │  ─────────────────────────────────▶ │  Backend (FastAPI)       │
│  React + Vite │                                      │  :8000                   │
│  :5173        │  ◀───────────────────────────────── │                          │
└──────────────┘      JSON {prompt, image(base64)}     │  ┌────────────────────┐  │
                                                        │  │ ① prompt_skill     │──┼──▶ Gemini API
                                                        │  │   build_skin_prompt│  │   (google-genai)
                                                        │  └────────────────────┘  │
                                                        │  ┌────────────────────┐  │
                                                        │  │ ② sdxl_skin        │──┼──▶ 로컬 GPU
                                                        │  │   generate_skin    │  │   (SDXL, diffusers)
                                                        │  └────────────────────┘  │
                                                        │  ┌────────────────────┐  │
                                                        │  │ ③ mc_skin_generator│  │
                                                        │  │   validate_skin    │  │
                                                        │  └────────────────────┘  │
                                                        └─────────────────────────┘
```

## 파이프라인 (4단계)

`입력 → ① 프롬프트 생성(Gemini) → ② 스킨 생성(SDXL) → ③ 검증 → ④ UI`

| 단계 | 역할 | 파일 | 외부 의존 |
|---|---|---|---|
| ① 프롬프트 생성 | 텍스트/이미지 → SDXL용 영어 프롬프트 | `backend/prompt_skill.py` | Gemini API |
| ② 스킨 생성 | 프롬프트 → 64×64 스킨 | `backend/sdxl_skin.py` | 로컬 GPU + diffusers |
| ③ 검증 | 64×64·RGBA·베이스 불투명 확인 | `backend/mc_skin_generator.py` | Pillow |
| ④ UI | 입력·결과 표시·다운로드 | `frontend/` + `backend/main.py` | React / FastAPI |

## 구성 요소

### Frontend (`frontend/`)
- React + Vite (개발 서버 `:5173`).
- 입력: 텍스트 아이디어 / 이미지 업로드(드래그앤드롭) / 직접 프롬프트 토글.
- 결과: 3D 스킨 미리보기(`skinview3d`) + 전개도 + 다운로드.
- 핵심 파일: `src/App.jsx`, `src/SkinViewer3D.jsx`, `src/index.css`.

### Backend (`backend/`)
- FastAPI + uvicorn (`:8000`). Python 3.12 가상환경(`.venv`)에서 실행 (torch 때문).
- 엔드포인트:
  - `POST /generate-prompt` — ①만 (프롬프트 텍스트 반환, 가벼운 테스트).
  - `POST /generate` — ①→②→③ 전체 (스킨 PNG를 base64 dataURL로 반환).
- 키는 `backend/.env`에서 로드 (python-dotenv).

## 요청 흐름 — `POST /generate`

```
1. Frontend: FormData { idea?, image?, direct } 전송
2. Backend:
   - direct=true  → idea 텍스트를 프롬프트로 직행 (Gemini 생략)
   - direct=false → build_skin_prompt(idea/image)  [Gemini 호출]
3. generate_skin(prompt)            [로컬 SDXL, 64×64 RGBA]
4. validate_skin(skin)              [형식 검사]
5. PNG → base64 dataURL
6. Frontend: 3D 미리보기 + 다운로드
```

## 실행 환경
- Frontend: Node 18+, `npm run dev`.
- Backend: Python 3.12 venv + torch(cu121) + diffusers. `uvicorn main:app`.
- GPU: NVIDIA RTX 4060 Ti (8GB). fp16 + CPU offload로 8GB에 맞춤.
- 두 서버 동시 실행: 루트의 `dev.bat` (backend는 venv 자동 활성화).

## 관련 문서
- 설계 결정과 근거: [design.md](design.md)
- 진행 체크리스트: [checklist.md](checklist.md)
- 프로젝트 컨텍스트: [../CLAUDE.md](../CLAUDE.md)
