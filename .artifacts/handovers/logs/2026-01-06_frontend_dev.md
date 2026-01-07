# Frontend Developer Log - 2026-01-06

## Completed Tasks
- **[Feature] Remember ID**:
    - `login/+page.svelte`에 `localStorage` 연동 로직 구현 및 체크박스 추가.
    - 로그인 성공 시 `savedEmail` 키로 이메일 저장, 로드 시 자동 완성 기능 확인.
- **[Bugfix] Authentication & CORS**:
    - Backend `main.py`의 CORS 허용 origin에 포트 `5173` 추가.
    - `fastapi.js`의 강제 trailing slash 제거하여 리다이렉트 이슈 해결.
    - `auth.js`를 `api_router` 기반으로 리팩토링 및 로그인 후 유저 정보 fetch 로직 추가.

## Verification
- 브라우저 서브에이전트 검증 결과, 이메일 자동 완성 및 API 호출(CORS) 정상 확인.
- 대시보드 진입 시의 간헐적 401 이슈는 별도 분석 필요.
