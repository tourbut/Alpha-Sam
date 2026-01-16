# Handovers: To Architect

## 날짜
2025-12-16

## 현재 상황 (Context)
v0.6.0 Hotfix 및 검증이 완료되었으며, 이제 **v0.7.0(사용자 포트폴리오 격리 및 이메일 알림)** 개발을 시작하는 단계입니다.
현재 시스템은 단일 사용자 상황을 가정하고 있거나 명시적인 소유권 개념이 약하므로, 이를 다중 사용자 지원 구조로 확장해야 합니다.

## 해야 할 일 (Tasks)
1. **DB 스키마 설계 (Multi-tenancy):**
   - `Asset`, `Portfolio`, `Transaction`, `Holding` 등 주요 모델에 `owner_id`(사용자 식별자)를 추가하는 방안을 설계하십시오.
   - 기존 데이터(`owner_id`가 없는 데이터)를 어떻게 처리할지(Default User 할당 등)에 대한 마이그레이션 전략을 수립하십시오.

2. **이메일 알림 시스템 아키텍처 설계:**
   - 알림 발송 시점(예: 목표가 도달, 일일 리포트 등) 정의.
   - 비동기 처리 방식(Celery 등) 및 이메일 전송 서비스(SMTP, SendGrid 등) 연동 구조 설계.

3. **설계 문서 작성:**
   - 위 내용을 정리하여 `.artifacts/docs/v0.7.0_specs.md` (또는 적절한 설계 문서)를 작성하십시오.

## 기대 산출물 (Expected Outputs)
- `.artifacts/docs/v0.7.0_specs.md`: 스키마 변경안 및 알림 시스템 아키텍처가 포함된 설계 문서.

## 참고 자료 (References)
- `.artifacts/prompts/projects/alpha_sam/domain_rules.md`
- `backend/app/src/models/` (현재 모델 구조)
