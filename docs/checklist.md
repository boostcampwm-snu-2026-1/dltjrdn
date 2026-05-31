# 진행 체크리스트 (Checklist)

> 주차별 상세 계획은 [../PLAN.md](../PLAN.md). 여기는 기능 단위 현재 상태.

## ① 프롬프트 생성 (Gemini)
- [x] `build_skin_prompt` — 텍스트 모드
- [x] 이미지 모드 (Gemini 비전)
- [x] 이미지+텍스트 혼합 모드
- [x] 출력 규칙(영어 한 줄·외형·색·고유명사 금지) 강제 + few-shot
- [x] 금지어 필터 / 마침표 제거
- [ ] 무료 한도 대응 (결제 등록 or 모델 조정)

## ② SDXL 스킨 생성 (로컬 GPU)
- [x] 로컬 환경 (Python 3.12 venv + torch cu121 + diffusers)
- [x] `generate_skin(prompt) -> 64×64 RGBA` (8GB 최적화)
- [x] 후처리 정정 (768 크롭 → 64×32 → 64×64 변환)
- [x] 추론 스텝 50
- [ ] 몸통 마젠타(투명 마커) 배경 후처리 보강

## ③ 검증
- [x] `validate_skin` (크기/RGBA/베이스 불투명)
- [x] UV 좌표 단일 출처 (`BASE/OVERLAY_LAYER_RECTS`)

## ④ 웹 UI
- [x] React + Vite 프론트 (입력폼·드래그앤드롭·사진 제거)
- [x] FastAPI 백엔드 (`/generate-prompt`, `/generate`)
- [x] 스킨 생성 → 결과 표시 → 다운로드
- [x] 3D 미리보기 (`skinview3d`)
- [x] 직접 프롬프트 토글 (임시 Gemini 우회)
- [x] `dev.bat` 동시 실행 + venv 자동화 + `.env` 키 관리

## 마무리 / 졸업작품 강화
- [ ] 스킨 품질 튜닝 (마젠타 해결, 의상 반영도)
- [ ] `eval/` 품질 평가 스크립트 (프롬프트 유무/few-shot 비교)
- [x] 문서화 (architecture / design / git / README)
- [ ] 발표용 예시 스킨 모음 + 데모 영상
- [ ] 라이선스 표기 (Monadical 모델 GPL-3.0 확인)
