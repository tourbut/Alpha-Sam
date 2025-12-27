# Alpha-Sam 배포 가이드

이 문서는 Alpha-Sam 애플리케이션을 Docker Compose를 사용하여 배포하는 방법을 설명합니다.

## 사전 요구사항

- Docker (20.10 이상)
- Docker Compose (v2.0 이상)
- 최소 4GB RAM
- 최소 10GB 디스크 공간

## 빠른 시작

### 1. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 환경 변수를 설정하세요.

```bash
# .env.example 파일을 참고하여 .env 파일 생성
cp .env.example .env
```

`.env` 파일에서 다음 변수들을 설정하세요:

```env
# PostgreSQL 설정
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=alpha_sam
POSTGRES_PORT=5432

# Redis 설정
REDIS_URL=redis://localhost:6379/0
REDIS_PORT=6379

# Backend 설정
DATABASE_URL=postgresql+asyncpg://postgres:your-secure-password@db:5432/alpha_sam
BACKEND_PORT=8000

# Celery 설정
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# nginx 설정
NGINX_PORT=80
```

**⚠️ 중요**: 프로덕션 환경에서는 반드시 강력한 비밀번호를 사용하세요.

### 2. Docker Compose로 전체 스택 실행

```bash
# 모든 서비스 빌드 및 실행
docker compose up -d

# 로그 확인
docker compose logs -f

# 특정 서비스 로그만 확인
docker compose logs -f backend
docker compose logs -f celery_worker
docker compose logs -f celery_beat
```

### 3. 데이터베이스 마이그레이션 실행

Alembic을 사용하여 데이터베이스 스키마를 초기화하거나 업데이트합니다.

```bash
# Backend 컨테이너에서 마이그레이션 실행
docker compose exec backend alembic upgrade head

# 또는 로컬에서 실행 (DATABASE_URL 환경 변수 필요)
cd backend
alembic upgrade head
```

### 4. 서비스 확인

모든 서비스가 정상적으로 실행되었는지 확인하세요:

```bash
# 컨테이너 상태 확인
docker compose ps

# Health check 확인
curl http://localhost/health
curl http://localhost:8000/health
```

예상되는 출력:
- `http://localhost` (nginx를 통한 접근)
- `http://localhost:8000` (Backend 직접 접근)
- 모든 컨테이너가 `Up` 상태여야 합니다.

## 프로덕션 배포 (Production Deployment)

개발 환경(`docker-compose.yml`)과 달리, 프로덕션 환경에서는 최적화된 이미지를 사용하고 소스 코드 변경을 실시간으로 감지하지 않습니다.

### 1. 프로덕션 이미지 빌드

```bash
# Backend (v1.0.0)
docker build -f backend/Dockerfile.prod -t alpha-sam-backend:v1.0.0 ./backend

# Frontend (v1.0.0)
docker build -f frontend/Dockerfile.prod -t alpha-sam-frontend:v1.0.0 ./frontend
```

### 2. 프로덕션 서비스 실행

`docker-compose.prod.yml` 파일을 사용하여 서비스를 실행합니다.

```bash
docker compose -f docker-compose.prod.yml up -d
```

## 서비스 구성

### 실행되는 서비스

1. **PostgreSQL** (`db`)
   - 포트: 5432
   - 데이터 영구 저장: `postgres_data` 볼륨

2. **Redis** (`redis`)
   - 포트: 6379
   - 캐시 및 Celery 브로커로 사용
   - 데이터 영구 저장: `redis_data` 볼륨

3. **Backend** (`backend`)
   - FastAPI 애플리케이션
   - 포트: 8000
   - Health check: `http://localhost:8000/health`

4. **Frontend** (`frontend`)
   - SvelteKit 애플리케이션
   - nginx를 통해서만 접근 가능 (직접 포트 노출 없음)

5. **Celery Worker** (`celery_worker`)
   - 백그라운드 작업 처리
   - 시세 업데이트 등 비동기 작업 실행

6. **Celery Beat** (`celery_beat`)
   - 주기적 작업 스케줄링
   - 5분마다 모든 자산의 시세를 자동 업데이트

7. **nginx** (`nginx`)
   - 리버스 프록시
   - 포트: 80
   - `/api/*` → Backend
   - `/*` → Frontend

## 일반적인 작업

### 서비스 재시작

```bash
# 모든 서비스 재시작
docker compose restart

# 특정 서비스만 재시작
docker compose restart backend
docker compose restart celery_worker
```

### 서비스 중지

```bash
# 모든 서비스 중지 (컨테이너 유지)
docker compose stop

# 모든 서비스 중지 및 컨테이너 제거
docker compose down

# 볼륨까지 삭제 (⚠️ 데이터 삭제됨)
docker compose down -v
```

### 로그 확인

```bash
# 모든 서비스 로그
docker compose logs -f

# 특정 서비스 로그
docker compose logs -f backend
docker compose logs -f celery_worker
docker compose logs -f celery_beat
docker compose logs -f nginx

# 최근 100줄만 확인
docker compose logs --tail=100 backend
```

### 데이터베이스 접근

```bash
# PostgreSQL에 접속
docker compose exec db psql -U postgres -d alpha_sam

# Redis CLI 접속
docker compose exec redis redis-cli
```

### Celery 태스크 모니터링

```bash
# Celery Worker 상태 확인
docker compose exec celery_worker celery -A app.celery_app inspect active

# Celery Beat 스케줄 확인
docker compose exec celery_beat celery -A app.celery_app inspect scheduled
```

## 문제 해결

### 컨테이너가 시작되지 않는 경우

1. **포트 충돌 확인**
   ```bash
   # 사용 중인 포트 확인
   lsof -i :80
   lsof -i :8000
   lsof -i :5432
   ```

2. **로그 확인**
   ```bash
   docker compose logs [service_name]
   ```

3. **컨테이너 재빌드**
   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

### 데이터베이스 연결 오류

1. **PostgreSQL이 준비되었는지 확인**
   ```bash
   docker compose exec db pg_isready -U postgres
   ```

2. **환경 변수 확인**
   ```bash
   docker compose exec backend env | grep DATABASE_URL
   ```

3. **네트워크 확인**
   ```bash
   docker compose exec backend ping db
   ```

### Celery Worker/Beat가 작동하지 않는 경우

1. **Redis 연결 확인**
   ```bash
   docker compose exec redis redis-cli ping
   ```

2. **Celery 설정 확인**
   ```bash
   docker compose exec celery_worker celery -A app.celery_app inspect stats
   ```

3. **태스크 로그 확인**
   ```bash
   docker compose logs celery_worker
   docker compose logs celery_beat
   ```

### nginx가 작동하지 않는 경우

1. **nginx 설정 파일 확인**
   ```bash
   docker compose exec nginx nginx -t
   ```

2. **nginx 로그 확인**
   ```bash
   docker compose logs nginx
   ```

3. **Backend/Frontend 연결 확인**
   ```bash
   docker compose exec nginx wget -O- http://backend:8000/health
   docker compose exec nginx wget -O- http://frontend:5173
   ```

## 프로덕션 배포 고려사항

### 보안

1. **강력한 비밀번호 사용**
   - `.env` 파일의 모든 비밀번호를 강력한 값으로 변경
   - `.env` 파일은 절대 Git에 커밋하지 않음

2. **HTTPS 설정**
   - nginx에 SSL/TLS 인증서 설정
   - Let's Encrypt 또는 상용 인증서 사용

3. **방화벽 설정**
   - 필요한 포트만 열기
   - SSH 접근 제한

### 성능 최적화

1. **리소스 제한 설정**
   ```yaml
   # docker-compose.yml에 추가
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

2. **로깅 설정**
   - 프로덕션에서는 로그 레벨을 `INFO` 또는 `WARNING`으로 설정
   - 로그 로테이션 설정

3. **데이터베이스 최적화**
   - PostgreSQL 연결 풀 크기 조정
   - 인덱스 최적화

### 모니터링

1. **Health Check 모니터링**
   - 정기적으로 `/health` 엔드포인트 확인
   - Prometheus, Grafana 등 모니터링 도구 통합

2. **로그 집계**
   - ELK Stack, Loki 등 로그 집계 시스템 사용

3. **백업**
   - PostgreSQL 데이터 정기 백업
   - 볼륨 스냅샷 생성

## 추가 리소스

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Celery 공식 문서](https://docs.celeryq.dev/)
- [nginx 공식 문서](https://nginx.org/en/docs/)

