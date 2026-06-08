# 배포 (Deploy)

프론트엔드는 Vercel 정적 배포, 백엔드(로컬 GPU)는 PC에서 실행 + cloudflared 터널로 임시 공개.

```
[브라우저] → Vercel(프론트) → cloudflared 터널 → 내 PC 백엔드(:8000, GPU)
```

## 1. 백엔드 — 로컬 실행 + 터널
1. 백엔드 실행: 루트에서 `dev.bat` (또는 `cd backend && uvicorn main:app --port 8000`).
2. [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) 설치 후, 루트에서 `tunnel.bat` 실행 (`cloudflared tunnel --url http://localhost:8000`).
3. 출력된 `https://xxxx.trycloudflare.com` 주소를 복사 → 공개 백엔드 URL.

## 2. 프론트엔드 — Vercel
1. Vercel에서 이 레포 Import → **Root Directory = `frontend`** 지정 (Framework는 Vite 자동 감지, [frontend/vercel.json](../frontend/vercel.json) 참고).
2. Environment Variables 에 `VITE_API_URL` = 1번에서 복사한 터널 주소.
3. Deploy → `https://your-app.vercel.app`.

## 3. CORS 허용
백엔드 `backend/.env` 에 배포 도메인을 추가하고 백엔드 재시작:
```
ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:5173
```

## 주의
- 백엔드는 **GPU PC가 켜져 있고 터널이 떠 있을 때만** 동작한다.
- cloudflared quick tunnel 주소는 임시라 재실행 시 바뀜 → 바뀌면 Vercel의 `VITE_API_URL`도 갱신.
- 모델/원본 코드가 GPL-3.0 → 공개 배포 시 소스공개 의무·모델 가중치 라이선스 확인.
