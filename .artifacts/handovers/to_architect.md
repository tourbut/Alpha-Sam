# Handovers: To Architect

## 날짜
2025-12-27

## 브랜치 (Version Control)
- `feature/arch-v0.8.0-planning`

## 현재 상황 (Context)
- v0.7.0(Multi-tenancy & Notifications) 구현 및 검증이 완료되었습니다.
- 다음 마일스톤인 v0.8.0(Authentication)으로 넘어가기 위한 상세 설계가 필요합니다.

## 해야 할 일 (Tasks)
1. `.artifacts/v0.8.0_implementation_plan.md` 파일 생성 및 작성.
   - 목표: `X-User-Id` 헤더 제거 및 `FastAPI Users` 기반 JWT 인증 도입.
   - 주요 포인트: DB Schema 변경(User 테이블), 인증 흐름, 기존 데이터 마이그레이션 전략.
2. `.artifacts/projects/domain_rules.md` 업데이트.
   - 인증(Authentication) 및 권한(Authorization) 관련 도메인 규칙 추가.
3. 기존 v0.7.0 산출물 중 누락된 문서화가 있다면 보완.

## 기대 산출물 (Expected Outputs)
- `.artifacts/v0.8.0_implementation_plan.md` (Draft 이상)
- 업데이트된 `domain_rules.md`

## 참고 자료 (References)
- `.artifacts/projects/tech_stack.md` (FastAPI Users 관련 내용 확인)
- `src/models/user.py` (현재 유저 모델 확인)
