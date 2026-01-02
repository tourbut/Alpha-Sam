# Handovers: To Frontend Developer

## 날짜
2025-12-30

## 현재 상황 (Context)
- v0.8.0 배포 완료. v0.9.0은 Backend/DB 위주의 작업입니다.
- Frontend는 현행 유지 및 기술 부채 해결(Refactoring)에 집중합니다.

## 해야 할 일 (Tasks)
1. **Refactoring**:
   - v0.8.0 급하게 수정된 Auth 관련 코드(`api.ts` 등)의 클린 코드 리팩토링.
   - 하드코딩된 문자열 상수화, 타입 정의 보완.
2. **Standby**:
   - 백엔드 성능 최적화 후 API 응답 포맷 변경 가능성에 대비.

## 기대 산출물 (Expected Outputs)
- 리팩토링 PR (선택 사항).

## 완료 내역 (Completed)
- [x] Refactoring: `src/lib/api.ts` 리팩토링 완료.
    - API endpoint 상수화 (`API_ENDPOINTS`).
    - JSDoc 추가 및 타입 정의 보완.
    - 기존 테스트 통과 확인.
