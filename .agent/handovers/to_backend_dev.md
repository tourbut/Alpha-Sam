# Handovers: To Backend Dev

## 날짜
- 2026-02-21

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- 아키텍처 대규모 개편(UUID 전환 등) 이후, 기능 안정성 확보를 위해 백엔드 코드의 전반적인 점검과 API 테스트가 필요한 상황입니다.

## 해야 할 일 (Tasks)
1. 전체 API 엔드포인트 파이썬 코드 컨벤션 및 로직 리뷰 수행 (불필요한 레거시 코드 정리, 타입 힌트 및 예외 처리 강화).
2. 멀티 포트폴리오 및 자산, PnL 계산 등 핵심 도메인 로직에 대한 단위 테스트(`pytest`) 구동 및 실패 내역 원인파악 후 수정.
3. Architect의 점검 리포트가 발행될 경우, 해당 권고안을 반영하여 구조 리팩토링 진행.

## 기대 산출물 (Expected Outputs)
- 백엔드 테스트 스위트(`pytest`) 에러 없이 전체 통과.
- 잠재적 에러 상황 방지를 위한 방어 로직 추가 및 리팩토링 커밋.

## 참고 자료 (References)
- `.agent/project/info/domain_rules.md`
- `.agent/handovers/to_architect.md` (진행 및 완료 상황 참조)
