# Tech Stack – Alpha-Sam

## Backend

- **Language:** Python 3.13 (latest)
- **Framework:** FastAPI
- **ORM / DB Layer:**
  - SQLAlchemy (Async)
  - SQLModel (타입 안정성과 선언적 모델 정의를 위해 사용)
- **Server Runtime:**
  - uv (패키지/환경 관리)
  - uvicorn (ASGI 서버)

## Frontend

- **Framework:** Svelte, SvelteKit
- **Language:** TypeScript
- **UI / 스타일링:**
  - Tailwind CSS
  - Flowbite (Tailwind 기반 UI 컴포넌트 라이브러리)
- **Serving:**
  - nginx를 사용하여 정적 파일/리버스 프록시 구성

## Database

- **PostgreSQL**
  - 메인 트랜잭션 데이터 저장소로 사용
  - 자산, 포지션, 사용자 계정 등 핵심 도메인 데이터 저장

## Cache

- **Redis**
  - 외부 시세 API 응답 캐싱
  - 자주 조회되는 포트폴리오 요약 정보 캐싱
  - (선택) 세션/레이트 리밋 관리 등에 활용 가능

## Asynchronous / Background Tasks

- **Celery**
  - 주기적 시세 업데이트
  - 무거운 연산(포트폴리오 재계산 등)을 백그라운드 태스크로 처리
  - Redis 또는 다른 브로커를 사용하여 작업 큐 관리

## Infrastructure

- **Docker Compose**
  - Backend, Frontend, PostgreSQL, Redis, (필요 시) Celery Worker/Beat, nginx를 컨테이너로 구성
  - 개발 환경에서 `docker compose up` 한 번으로 전체 스택을 기동할 수 있도록 설계

## Version Control & Collaboration

- **GitHub**
  - 소스 코드 버전 관리에 사용
  - 브랜치 전략 예:
    - `main`: 배포 가능한 안정 버전
    - `develop`: 통합 개발 브랜치
    - `feature/*`: 개별 기능 개발용 브랜치
  - 이슈 관리:
    - 버그/기능 요청/QA 결과를 GitHub Issues로 관리
    - 필요 시 Labels (bug, feature, qa, infra 등)로 분류
