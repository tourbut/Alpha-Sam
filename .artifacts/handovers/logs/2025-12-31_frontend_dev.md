# Handovers: To Frontend Developer

## 날짜
2025-12-31

## 현재 상황 (Context)
- v0.8.0 인증 시스템이 배포되었으나, `api.ts` 등 클라이언트 코드의 리팩토링이 필요합니다.
- 향후 기능 확장을 위해 인증 상태 관리와 에러 핸들링을 견고하게 만들어야 합니다.

## 해야 할 일 (Tasks)
1. **API 모듈 리팩토링 (`api.ts`)**:
   - API 요청 시 Authorization 헤더 주입 로직 중앙화.
   - 401 Unauthorized 응답 시 로그인 페이지로 리다이렉트하는 Interceptor 구현.
2. **로그인 플로우 재검증**:
   - 리팩토링 후 로그인, 로그아웃, 보호된 페이지 접근이 정상 작동하는지 확인.

## 기대 산출물 (Expected Outputs)
- 리팩토링된 `src/lib/api.ts` (또는 관련 유틸리티).

## 참고 자료 (References)
- [.artifacts/projects/milestone_report_v0.8.0.md](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.artifacts/projects/milestone_report_v0.8.0.md)
