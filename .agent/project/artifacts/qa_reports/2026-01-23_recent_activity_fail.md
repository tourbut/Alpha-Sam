# QA Result Report: v0.3.0 (Recent Activity Feature)

**Date:** 2026-01-23
**Tester:** QA Agent

## 1. 요약
- **테스트 대상**: 대시보드 "Recent Activity" UI 및 데이터 로딩 기능.
- **결과**: **FAIL**
- **원인**: 
  1. Frontend Import 에러 (`$lib/apis/dashboard.ts` -> `../auth` 경로 문제).
  2. Backend API (`GET /api/v1/dashboard/activities`) 인증 (`401 Unauthorized`) 문제.

## 2. 세부내용

### 2.1 Issue Reproduction (버그 재현)
- **절차**:
  1. `http://localhost:5173/` (대시보드) 접속.
- **관찰 결과**:
  - 화면이 렌더링되지 않고 500 에러 오버레이 발생.
  - Console Log: `Failed to resolve import "../auth" from "src/lib/apis/dashboard.ts".`
  - 수동 API Fetch 시도 시 `401 Unauthorized` 반환.

### 2.2 Analysis (원인 분석)
1. **Frontend**: `$lib/apis/dashboard.ts` 파일이 `src/lib/apis` 폴더에 위치하므로, `../auth`는 `src/lib/auth.ts`를 가리킵니다. 하지만 `auth.ts`는 `src/lib/stores/` 또는 `src/lib/`에 위치할 가능성이 높으며, 정확한 경로 확인이 필요합니다. (`$lib/auth` alias 사용 권장).
2. **Backend**: `dashboard.router` 엔드포인트에 `dependencies=[Depends(get_current_user)]` 또는 유사한 인증 종속성이 누락되었거나, 토큰 처리가 잘못되었을 수 있습니다.

## 3. 결론 및 조치사항
- **결론**: Frontend와 Backend 모두 수정이 필요함.
- **조치**: 
  - **Frontend**: Import 경로 수정 (`../auth` -> `$lib/stores/auth` 또는 `$lib/auth`).
  - **Backend**: API 인증 로직 점검 및 로그인 필수 처리 확인.
