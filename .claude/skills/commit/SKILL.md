---
name: commit
description: 변경 사항을 프로젝트 커밋 규칙에 맞게 git commit 한다. 사용자가 /commit 또는 "커밋해줘", "커밋하자"라고 할 때 사용.
---

# commit — 규칙에 맞는 git commit

현재 변경 사항을 아래 커밋 규칙에 맞춰 커밋한다.

## 할 일

1. `git status`와 `git diff`(스테이징 안 된 것 포함)로 무엇이 바뀌었는지 파악한다.
2. 변경을 논리적으로 묶는다. 성격이 다른 변경이 섞여 있으면 **여러 커밋으로 나눌지** 사용자에게 제안한다.
3. 아래 규칙대로 커밋 메시지를 만든다.
4. `git add` 후 `git commit` 한다. (사용자가 범위를 지정하지 않으면 무엇을 stage 할지 먼저 보여준다.)
5. 커밋 후 `git log --oneline -3`으로 결과를 확인해 보고한다.

## 커밋 메시지 규칙

형식:
```
<type>: <한국어로 간결한 요약 (50자 이내)>

<본문 — 필요할 때만. 왜 바꿨는지 설명. 한 줄 72자 권장>
```

type 종류:
| type | 의미 |
|---|---|
| `feat` | 새 기능 (예: 프롬프트 생성 함수 추가) |
| `fix` | 버그 수정 |
| `docs` | 문서만 변경 (CLAUDE.md, README, PLAN.md 등) |
| `refactor` | 동작 변화 없는 코드 정리 |
| `style` | 포맷·세미콜론 등 (로직 변화 없음) |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드·설정·의존성 등 잡일 |

예시:
- `feat: Gemini 텍스트 모드 프롬프트 생성 구현`
- `fix: validate_skin 알파 채널 검사 오류 수정`
- `docs: CLAUDE.md 웹 스택을 React+FastAPI로 갱신`

## 규칙 (중요)
- **API 키·시크릿이 diff에 들어갔는지 반드시 확인**한다. `GEMINI_API_KEY` 등 하드코딩된 비밀이 보이면 커밋을 멈추고 사용자에게 알린다.
- 한 커밋엔 한 가지 목적만 담는다.
- 사용자가 명시적으로 요청하지 않는 한 `git push` 는 하지 않는다.
- `--no-verify` 등 훅 우회 금지.
- 커밋 메시지 본문 끝에 아래 trailer를 붙인다:
  ```
  Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
  ```
