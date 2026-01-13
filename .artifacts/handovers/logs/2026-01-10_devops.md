# Handovers: To DevOps

## 날짜
- 2026-01-10

## 현재 상황 (Context)
- 백엔드에서 Redis 사용량이 증가할 예정입니다 (Price Caching).
- 현재 `docker-compose.yml`에 Redis가 포함되어 있습니다.

## 해야 할 일 (Tasks)
1. **Redis 서비스 상태 확인**:
    - 로컬 개발 환경에서 Redis 컨테이너가 정상 동작하는지 점검.
    - 필요 시 `redis-cli`로 접근 가능한지 확인.
2. **(추후 예정) Collector 스케줄링**:
    - 향후 `price_collector.py`를 Celery Beat나 CronJob으로 등록할 준비 (지금은 실행 테스트만).

## 기대 산출물 (Expected Outputs)
- `docker-compose ps`에서 redis 서비스 `healthy` 상태 확인.

## 참고 자료 (References)
- `docker-compose.yml`
