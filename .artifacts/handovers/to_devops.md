# Handovers: To DevOps

## 날짜
- 2026-01-05

## 현재 상황 (Context)
- v1.0.0에서 발견된 Critical Bug(Backend 500 Error, Data Leak)가 수정되었습니다.
- QA 검증이 완료되었으며, 해당 수정 사항을 포함한 `v1.0.1` 릴리즈가 필요합니다.

## 해야 할 일 (Tasks)
1.  **Release v1.0.1 (Git Tag & Merge)**
    - 현재 작업 내용을 확인하고 커밋하십시오 (Message: `fix: resolve asset creation error and data leak`).
    - Git Tag `v1.0.1`을 생성하십시오.
    - `main` 및 `develop` 브랜치에 병합(Merge)하고 원격 저장소에 Push 하십시오.

2.  **Deployment Verification**
    - 로컬 도커 환경(또는 배포 환경)에서 clean build 후 서버가 정상 기동되는지 최종 확인하십시오.

## 기대 산출물 (Expected Outputs)
- Git Tag `v1.0.1`
- Clean `git status` (on `develop` branch)

## 참고 자료 (References)
- `.artifacts/projects/version_control_guidelines.md`
