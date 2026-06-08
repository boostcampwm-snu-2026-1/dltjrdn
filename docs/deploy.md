# 배포 (Deploy)

스킨 생성이 로컬 GPU(SDXL)에 묶여 있어, 백엔드를 내 PC에서 실행하고 cloudflared 터널로 공개한다. **백엔드가 빌드된 프론트까지 함께 서빙**하므로, 터널 주소 하나로 전체 앱이 동작한다 (별도 프론트 호스팅·CORS 설정 불필요).

```
[브라우저] → cloudflared 터널(https) → 내 PC 백엔드(:8000) → 프론트(dist) + API + GPU
```

## 1. 프론트 빌드
```powershell
cd frontend
npm install
npm run build
```
→ `frontend/dist` 생성. 백엔드가 이 폴더를 `/`에 서빙한다. (프론트 코드를 바꾸면 다시 빌드)

## 2. 백엔드 실행
- `backend/.env` 에 `GEMINI_API_KEY` 필요.
- 루트에서 `dev.bat` (또는 `cd backend && uvicorn main:app --port 8000`).
- 브라우저에서 `http://localhost:8000` 접속 → 프론트가 뜨고 스킨 생성까지 되면 정상.

## 3. cloudflared 터널로 공개
[cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) 설치 후, 루트에서 `tunnel.bat` 실행 (= `cloudflared tunnel --url http://localhost:8000`).
출력된 `https://xxxx.trycloudflare.com` 가 **공개 주소**. 이 한 주소로 접속하면 프론트·생성 전부 동작한다.

## 주의
- 백엔드 PC가 켜져 있고 터널이 떠 있어야 동작한다.
- quick tunnel 주소는 재실행 시 바뀐다 (고정이 필요하면 Cloudflare 계정 + named tunnel).
- 프론트 코드를 수정하면 `npm run build` 를 다시 해야 최신이 서빙된다.
- 모델/원본 코드가 GPL-3.0 → 공개 배포 시 소스공개 의무·모델 가중치 라이선스 확인.
