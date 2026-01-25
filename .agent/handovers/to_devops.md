# Handovers: To DevOps

## 날짜
- 2026-01-25

## 브랜치 (Version Control)
- `feature/admin-stock-batch-job`

## 현재 상황 (Context)
- 백엔드 팀이 1분 주기의 시세 수집 배치 작업을 구현합니다.
- 현재 `docker-compose.yml`에 `celery_beat` 서비스가 존재하지만, 실제 배치 작업 수행 시 리소스 사용량이나 로그 확인이 필요할 수 있습니다.

## 해야 할 일 (Tasks)
1. `celery_beat` 컨테이너 로그 모니터링 준비.
2. 배치 작업 추가 후, `celery_worker`의 부하(Concurrency 이슈)가 없는지 간단히 확인.
3. (Optional) Production 환경(`docker-compose.prod.yml`)에도 `celery_beat` 설정이 동일하게 유효한지 크로스 체크.

## 기대 산출물 (Expected Outputs)
- `docker-compose up` 시 Celery Beat가 정상적으로 스케줄을 픽업하고 Worker에게 전달하는 로그 확인.

## 참고 자료 (References)
- `docker-compose.yml`
