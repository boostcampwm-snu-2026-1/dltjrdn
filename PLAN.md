# 작업 계획 — 마인크래프트 스킨 생성기

> 설계 한 줄: **텍스트/이미지 → Gemini로 디퓨전(SDXL)용 프롬프트 생성 → SDXL이 64×64 스킨 PNG 생성 → 검증 → UI**
> 핵심 기여 = "좋은 프롬프트를 만드는 ① 단계" (단순 API 연결로 안 보이게)

---

## 1주차 — ① 프롬프트 생성 (Gemini)  〔내 핵심 기여〕

목표: 입력(텍스트 아이디어 / 이미지)을 받아 **SDXL용 영어 프롬프트 한 줄**을 출력하는 `prompt_skill.py` 완성.

- [x] 개발 환경 세팅 (Python 3.10+, `pip install google-genai pillow`)
- [x] `GEMINI_API_KEY` 환경변수 등록 (키 하드코딩 금지 확인)
- [x] Gemini API 호출 최소 예제 동작 확인 (텍스트 → 텍스트)
- [x] `build_skin_prompt(key, idea="...")` — **텍스트 모드** 구현
- [x] `build_skin_prompt(key, image_path="...")` — **이미지 모드** 구현 (Gemini 비전) ※ 코드 완료, 실사진 테스트 미완
- [x] 출력 규칙 강제: 영어 한 줄 / 캐릭터 묘사 / 색·의상·헤드기어·액세서리 포함
- [x] 금지어 필터: `Minecraft`, `skin`, `pixel art`, 포즈·배경·조명·화질 표현 제거
- [x] few-shot 예시 2~3개 넣어 출력 품질·형식 안정화
- [~] 입력 5개로 수동 테스트 — 텍스트 3개 확인 완료 / 이미지 입력 테스트 남음

**1주차 끝 = 콘솔에서 아이디어/이미지 넣으면 그럴듯한 영어 프롬프트가 나온다.**

---

## 2주차 — ② SDXL 스킨 생성 + ③ 검증

목표: 1주차 프롬프트를 **실제 64×64 스킨 PNG**로 바꾸고, 형식이 맞는지 자동 검증.

- [ ] SDXL = "프롬프트 → 이미지" 디퓨전 모델임을 이해 (새로 학습 X, 갖다 씀)
- [ ] Monadical 레포 클론: `github.com/Monadical-SAS/minecraft_skin_generator`
- [ ] 모델 `monadical-labs/minecraft-skin-generator-sdxl` 카드/라이선스 확인 (GPL-3.0 전파 주의)
- [ ] **Google Colab 노트북**에서 GPU 추론 환경 구성 (`diffusers` + `torch`)
- [ ] 레포의 `bin/minecraft-skins-sdxl.py`를 래핑 → `generate_skin(prompt) -> PIL.Image`
- [ ] 프롬프트 1개로 스킨 1장 생성 성공 (눈으로 확인)
- [ ] ③ `mc_skin_generator.py`의 `validate_skin` 작성/이식 (64×64·RGBA·투명레이어 체크)
- [ ] `PARTS` / `UV` 좌표 상수 정의 (스킨 형식 단일 출처)
- [ ] 생성 결과가 `validate_skin()` 통과(빈 리스트) 하는지 확인
- [ ] ① → ② → ③ 연결: "아이디어 → 프롬프트 → 스킨 → 검증" 한 번에 돌려보기

**2주차 끝 = 텍스트 한 줄 넣으면 검증 통과한 스킨 PNG가 나온다 (콘솔/노트북 기준).**

---

## 3주차 — ④ 웹 UI (React + FastAPI) + 통합 + 마무리

목표: React 프론트 + FastAPI 백엔드로 웹앱을 묶고, 졸업작품 발표용으로 정리.

- [ ] `backend/main.py` — FastAPI 서버 + `POST /generate` 엔드포인트 (텍스트/이미지 → 스킨 PNG)
- [ ] CORS 설정 (프론트 도메인 허용)
- [ ] `frontend/` — React 프로젝트 생성 (Vite) + 입력폼(텍스트 입력 + 이미지 업로드)
- [ ] 프론트 → 백엔드 `fetch('/generate')` 연결, 결과 PNG 표시
- [ ] 결과 스킨 **다운로드 버튼** + 64×64 미리보기
- [ ] 전체 파이프라인 동작 (웹 입력 → 프롬프트 → 스킨 → 다운로드)
- [ ] 예외 처리: 잘못된 입력 / 검증 실패 / API 오류 메시지 표시
- [ ] (선택) `eval/` 품질 평가 스크립트 — 프롬프트 유무/few-shot 유무 비교
- [ ] `README.md` 작성: 설치·실행법·파이프라인 그림
- [ ] 발표 자료용 결과 예시 스킨 3~5개 캡처
- [ ] 코드 정리 + 라이선스 표기 (GPL 의무 확인)

**3주차 끝 = 발표 가능한 데모 + 정리된 코드/문서.**

---

## 진행 현황 요약
- [ ] 1주차 — ① 프롬프트 생성
- [ ] 2주차 — ② SDXL + ③ 검증
- [ ] 3주차 — ④ UI + 마무리

※ 현재 실제 파일 상태: `README.md`(제목만), `Claude.md`, `PLAN.md`만 존재. 코드 파일은 아직 없음 (= 1주차부터 시작).
