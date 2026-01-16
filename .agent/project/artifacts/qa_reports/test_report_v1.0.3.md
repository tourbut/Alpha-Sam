# QA Test Report: v1.0.3 Release

## 개요
- **Target Version**: v1.0.3
- **Date**: 2026-01-07
- **Tester**: QA Agent
- **Description**: 로그인 401 에러 수정, CORS 설정, Remember ID 기능, 자산 생성 핫픽스에 대한 집중 검증.
- **Result**: ❌ **FAIL (Critical Regression)**

## 테스트 환경
- **Backend**: FastAPI (Local:8000) - **Healthy**
- **Frontend**: SvelteKit (Local:5173) - **Healthy**

## 테스트 상세 결과

### 1. 인증 및 세션 (Authentication & Session)
- [x] **TC-1.1**: 로그인 성공 후 대시보드 진입 시 401 에러 발생 여부 확인.
  - **Result**: ❌ **FAIL**
  - **Root Cause Analysis**:
    - 로그인 시도 시 백엔드 엔드포인트 `/auth/jwt/login` (또는 프론트엔드가 호출하는 경로)에서 문제 발생 가능성 높음.
    - **Curl Test**: `POST http://127.0.0.1:8000/auth/jwt/login` 실행 시 **404 Not Found** 반환.
    - **Hypothesis**: 백엔드 라우트 구조 변경(예: `/api/v1/auth/login`으로 변경됨)이 프론트엔드 또는 마이그레이션 스크립트에 반영되지 않았을 가능성 있음.
  - **Symptom**: 프론트엔드에서는 에러 메시지 없이 대시보드로 리다이렉트 시도 후, `/api/v1/assets/` 호출 시 **401 Unauthorized**가 발생하여 다시 로그인 페이지로 튕김.

- [ ] **TC-1.2, TC-1.3**: (로그인 실패로 인해 진입 불가 - **BLOCKED**)

### 2. Remember ID 기능 (Feature)
- [x] **TC-2.1**: 로그인 화면에서 'ID 기억하기' 체크 후 로그인 -> 로그아웃 -> 로그인 화면 재진입 시 이메일 자동 입력 확인.
  - **Result**: ✅ **PARTIAL PASS**
  - **Observation**: 'ID 기억하기' 체크 시 `localStorage.savedEmail`에 값이 정상 저장되며, 페이지 리로드 시 이메일 입력란이 자동 채워짐을 확인. (기능 동작함)

### 3. 자산 관리 (Asset Management - Hotfix)
- [ ] **TC-3.1 ~ 3.3**: (대시보드 진입 불가로 인해 **BLOCKED**)

## 결론 및 제언
- **Critical Issue Found**: 백엔드 API 경로 불일치(404 Not Found)로 인해 로그인이 불가능합니다.
- **Action Required**:
  1. 백엔드의 실제 로그인 라우트 경로 확인 (`/api/v1/auth/login` vs `/auth/jwt/login`).
  2. 프론트엔드 `api.js` 또는 `auth.js`의 로그인 타겟 URL 수정.
  3. 수정 후 재배포 및 QA 재검증 필요.
