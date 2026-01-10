# Handovers: To DevOps

## 날짜
- 2026-01-11

## 현재 상황 (Context)
- v1.2.0 기능 개발 및 QA가 완료되었습니다 ("Ready for Deployment").
- 이제 배포 파이프라인(Release Branching & Migration)을 가동해야 합니다.

## 해야 할 일 (Tasks)
1. **Release Branching**:
    - `develop` 브랜치에서 `release/v1.2.0` 브랜치 생성.
    - 버전 정보 업데이트 (필요 시).
2. **Merge to Main**:
    - `release/v1.2.0` -> `main` 병합.
    - **Tag `v1.2.0` 생성 및 Push**.
3. **Deployment (Local/Simulated)**:
    - 로컬 환경 백업 수행 (만약 운영 데이터가 있다면).
    - `alembic upgrade head` 실행하여 DB 마이그레이션 적용.
    - 서버 재기동 및 헬스체크 확인.

## 기대 산출물 (Expected Outputs)
- Git Tag `v1.2.0` 존재.
- 마이그레이션이 적용된 DB 스키마 (`portfolios` 테이블 존재).
- 정상 동작하는 v1.2.0 애플리케이션.

## 참고 자료 (References)
- `.artifacts/projects/deployment_checklist_v1.2.0.md`
