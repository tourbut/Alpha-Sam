# Issue Tracker (v1.1.0 Prep)

## [CRITICAL] Dashboard Infinite Loading

### Description
로그인 후 대시보드(`/`) 진입 시, 데이터가 존재함에도 불구하고 화면이 **"Loading..."** 상태에서 멈추고 렌더링되지 않음.
백엔드 API는 정상적으로 데이터를 반환하고 있으나, 프론트엔드가 이를 처리하지 못하거나 렌더링 중단됨.

### Severity
- **Critical** (서비스 사용 불가)

### Reproduction Steps
1. 로그인 (`/login`).
2. 대시보드 진입.
3. 자산이 있거나 없는 상태 모두에서 "Loading..." 텍스트만 표시되고 차트/리스트가 뜨지 않음.

### Technical Details
- **Backend API**:
  - `GET /api/v1/assets/` -> 200 OK (Data returns correctly)
  - `GET /api/v1/portfolio/summary/` -> 200 OK
- **Frontend Symptom**:
  - `Loading...` indicator persists.
  - Manual DOM inspection shows content is NOT hidden, but simply not rendered (or `if` block condition not met).

### Assigned To
- **Frontend Developer**

---

## [Enhancement] Login Redirect UX
- 회원가입 직후 자동 로그인이 되지 않고 로그인 페이지로 리다이렉트되는 UX 개선 필요 (Optional).
