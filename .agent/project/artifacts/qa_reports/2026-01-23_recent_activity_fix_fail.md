# QA Result Report: v0.4.0 (Recent Activity Fix Verification)

**Date:** 2026-01-23
**Tester:** QA Agent

## 1. 요약
- **테스트 대상**: 대시보드 "Recent Activity" 섹션 로딩 및 API 인증.
- **결과**: **FAIL**
- **원인**: 
  1. **인증 토큰 불일치 (401)**: 앱이 `access_token` 대신 `auth_token` (mock-token)을 헤더에 사용 중.
  2. **UI 무한 로딩**: 데이터 로드 실패 또는 예외 처리 미비로 인해 "Loading..." 상태에서 벗어나지 못함.

## 2. 세부내용

### 2.1 Issue Reproduction (버그 재현)
- **절차**:
  1. 대시보드 접속.
  2. 무한 로딩 발생.
  3. 콘솔 확인 시 `/api/v1/dashboard/activities` 요청이 `401 Unauthorized` 반환.
  4. 요청 헤더에 `Authorization: Bearer mock-token`이 포함되어 있음 (실제 JWT 아님).

### 2.2 Analysis (원인 분석)
1. **Token Storage Key**: 프로젝트의 Auth 관련 코드가 `localStorage` 키로 `access_token`을 사용하는지, `auth_token`을 사용하는지 혼재되어 있을 가능성이 높음. `auth.ts` 스토어나 `fastapi.ts` 유틸리티가 서로 다른 키를 참조하는지 확인 필요.
2. **Infinite Loading**: `loadData` 함수 내에서 API 중 하나라도 실패하면 `finally { loading = false }`가 실행되어야 하나, 어떤 이유로 상태 업데이트가 차단되거나 비동기 처리가 꼬여 있을 수 있음.

## 3. 조치사항
- **Frontend**: 
  - 인증 토큰 저장 키 통일 (`access_token` vs `auth_token`).
  - `loadData` 함수의 에러 핸들링 및 `loading` 상태 해제 로직 점검.
