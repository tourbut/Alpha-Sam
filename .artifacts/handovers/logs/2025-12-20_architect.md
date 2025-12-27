# Handovers: To Architect

## 날짜
2025-12-20

## 현재 상황 (Context)
- v0.7.0 개발 진행 중 (Multi-tenancy, Email Notifications).
- DB Schema에 `owner_id` 및 `users` 테이블 마이그레이션이 존재함.
- 프론트엔드에서 `UserSwitcher` 시뮬레이션 및 `/settings` 페이지 계획이 수립됨.

## 해야 할 일 (Tasks)
1. `NotificationSettings` 데이터 모델 설계 검토
   - 사용자별 알림 설정(리포트 수신 여부, 가격 알림 여부 등)을 저장할 테이블 구조 정의.
   - `users` 테이블과 1:1 관계 확인.
2. 이메일 발송 관련 비즈니스 규칙 정의
   - 'Daily Report' 발송 시각 및 내용 포맷 정의.
   - 'Price Alert' 트리거 조건 및 빈도 제한 정책 수립.
3. API 명세 확정
   - `/api/v1/users/me/settings` 의 Request/Response 포맷 정의.

## 기대 산출물 (Expected Outputs)
- `NotificationSettings` 스키마 디자인 문서 (또는 PR 코멘트).
- 이메일 알림 로직 정책 문서 (`v0.7.0_implementation_plan.md` 업데이트).

## 참고 자료 (References)
- `v0.7.0_frontend_plan.md`
- `backend/alembic/versions` (기존 마이그레이션 참고)
# Handovers: To Architect

## 날짜
2025-12-20

## 현재 상황 (Context)
- v0.7.0의 아키텍처 및 인터페이스 설계가 성공적으로 구현에 반영되었습니다.

## 해야 할 일 (Tasks)
1. **v0.7.0 설계 회고**
   - 현재의 멀티테넌시 방식(`X-User-Id` 헤더)이 v0.8.0의 정식 인증 시스템(OAuth2/JWT)으로 전환될 때의 호환성을 검토하세요.
2. **v0.8.0 (Auth System) 리서치**
   - FastAPI-Users 또는 직접 구현 방식 중 우리 프로젝트에 적합한 인증 라이브러리를 조사하고 가이드를 준비하세요.

## 기대 산출물 (Expected Outputs)
- (선택 사항) v0.8.0 설계 초안 또는 리서치 메모.

## 참고 자료 (References)
- `v0.7.0_implementation_plan.md`
- `tech_stack.md`

