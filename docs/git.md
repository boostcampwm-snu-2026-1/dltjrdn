# Git 규칙 (Conventions)

## 커밋 메시지 형식
```
<type>: <한국어로 간결한 요약 (50자 이내)>

<본문 — 필요할 때만. 왜 바꿨는지. 한 줄 72자 권장>

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

### type 종류
| type | 의미 |
|---|---|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `docs` | 문서만 변경 (CLAUDE.md, README, docs/ 등) |
| `refactor` | 동작 변화 없는 코드 정리 |
| `style` | 포맷·세미콜론 등 (로직 변화 없음) |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드·설정·의존성 등 잡일 |

### 예시
- `feat: 웹 스킨 생성 - /generate 엔드포인트 추가`
- `fix: SDXL 스킨 후처리 정정 (768 크롭->64x64)`
- `docs: 아키텍처/설계 문서 추가`

## 원칙
- **한 커밋엔 한 가지 목적**. 성격이 다른 변경은 나눠서 커밋.
- 커밋 전 **시크릿 점검**: `AIza...` 같은 API 키가 diff에 있으면 멈추고 확인.
  - 키는 `backend/.env`(gitignore)에만. 코드·커밋에 하드코딩 금지.
- 사용자가 명시하지 않으면 `git push` 안 함.
- `--no-verify` 등 훅 우회 금지.

## 무시(gitignore) 대상
- `__pycache__/`, `*.pyc`, `.venv/`
- `.env` (키), `*.local`
- `backend/*.png` (생성 테스트 산출물)
- `node_modules/`, `dist/`

## 브랜치 / 원격
- 기본 브랜치: `main`
- 원격: `origin` (GitHub)
- `/commit` 스킬로 규칙대로 커밋 가능 ([../.claude/skills/commit/SKILL.md](../.claude/skills/commit/SKILL.md))
