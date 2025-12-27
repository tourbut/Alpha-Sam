# Handovers: To Backend Developer

## 날짜
2025-12-12

## 🚨 긴급 변경 사항 (Priority Change)
기존에 할당된 v0.3.0 기능 개발(User Settings, Price API)을 **일시 중단**하고, **코드 구조 리팩토링**을 최우선으로 진행합니다.

## 현재 상황 (Context)
- 프로젝트의 장기적인 유지보수성을 위해 백엔드 폴더 구조를 "Layered Architecture"에 가깝게 재구성합니다.
- `app/` 바로 아래에 산재된 모듈들을 `app/src/` 내부로 구조화합니다.

## 해야 할 일 (Tasks)

### 1. Backend 구조 리팩토링 (Refactoring)
다음 목표 구조(`Target`)에 맞춰 파일 및 폴더를 이동하고, 관련된 **Import 경로를 모두 수정**하세요.

**목표 구조 (Target Structure)**
```text
backend/app/
├── main.py            # 진입점 (Entry Point)
└── src/               # 핵심 비즈니스 로직 (New Directory)
    ├── api.py         # API Router 통합 관리
    ├── routes/        # API Endpoints (기존 app/api)
    ├── crud/          # DB CRUD 작업 (New, 로직 분리 필요)
    ├── schemas/       # Pydantic Models (기존 app/schemas)
    ├── models/        # ORM Models (기존 app/models)
    ├── engine/        # Business Logic & Background Tasks (기존 app/services + tasks)
    ├── deps.py        # Dependency Injection (New)
    ├── utils/         # Utility Functions
    └── core/          # Config, Security, Logging (기존 app/core)
```

**세부 마이그레이션 가이드:**
1.  **디렉토리 생성**: `backend/app/src` 생성.
2.  **이동 (Move)**:
    -   `app/core/` -> `app/src/core/`
    -   `app/models/` -> `app/src/models/`
    -   `app/schemas/` -> `app/src/schemas/`
    -   `app/api/` -> `app/src/routes/` (폴더명 변경)
    -   `app/services/` -> `app/src/engine/` (혹은 `engine` 내 하위 모듈로 통합)
    -   `app/tasks/` -> `app/src/engine/tasks/` (추천)
3.  **파일 생성/작성 (Create)**:
    -   `app/src/api.py`: `src/routes`의 라우터들을 `include_router`로 묶는 메인 라우터 파일 생성.
    -   `app/src/deps.py`: 인증(`get_current_user`)이나 DB 세션(`get_db`) 등의 의존성을 이곳으로 추출/이동.
    -   `app/src/crud/`: 라우터나 서비스에 섞여 있는 DB 쿼리(Select/Add/Commit) 로직을 분리하여 이곳으로 이동(점진적 수행 가능).
4.  **수정 (Update)**:
    -   `main.py`: `app.src.api`를 참조하도록 수정.
    -   모든 파일의 Import 문 수정 (예: `from app.core` -> `from app.src.core`).

### 2. 서버 정상 동작 확인
- 리팩토링 후 `uvicorn` 서버가 에러 없이 시작되는지 확인.
- 기존 API(로그인, 대시보드 등)가 정상 동작하는지 Smoke Test 진행.

---
## (보류됨) v0.3.0 기능 개발
*리팩토링 완료 후 진행 예정*
1. User Settings API 구현 (`user_settings_design.md`)
2. Real-time Price Service 개선 (`price_api_analysis.md`)

## 기대 산출물 (Expected Outputs)
- 재구조화된 `backend/app/src` 기반의 코드 베이스.
- 정상 구동되는 서버.


## Execution Result (2025-12-12)
- Refactored backend structure to 'app/src'.
- Verified server startup.

---
# Handovers: To Backend Developer (Completed)

## 날짜
2025-12-12

## 현재 상황 (Context)
- **v0.4.0 Development Cycle 시작**.
- v0.3.0 QA 완료/통과됨 (Price API 문자열 반환 주의).
- 기획 문서: `.artifacts/planning/v0.4.0_design.md`

## 해야 할 일 (Tasks)
1. **Portfolio Analytics API 구현**:
   - `GET /api/v1/portfolio/summary` 엔드포인트 생성.
   - 각 Position에 대해 최신 가격(Price DB or external)을 조회하여 평가금액 및 P/L 계산.
   - 응답 포맷은 기획 문서 참조.
   
2. **Production Deployment Setup**:
   - `docker-compose.prod.yml` 작성 (Restart policy, Env var 분리).
   - `Dockerfile` 최적화 (Multi-stage build 확인).

## 기대 산출물 (Expected Outputs)
- 작동하는 `/portfolio/summary` API (Swagger 확인).
- 로컬에서 실행 가능한 프로덕션 Docker 구성 (`docker-compose -f docker-compose.prod.yml up` 테스트).

## Execution Result
- Implemented `GET /api/v1/portfolio/summary` in `backend/app/src/routes/portfolio.py`.
- Created Pydantic models in `backend/app/src/schemas/portfolio.py`.
- Registered new router in `backend/app/src/api.py`.
- Created `docker-compose.prod.yml`.
- Optimized `backend/Dockerfile` (multi-stage).
- Optimized `frontend/Dockerfile` (multi-stage, adapter-node) and installed adapter-node.

---

# Handovers: To Backend Developer (v0.4.0 Deployment Setup)

## 날짜
2025-12-12

## 현재 상황 (Context)
- v0.3.0 tasks completed.
- v0.4.0 deployment setup requested.

## 해야 할 일 (Tasks)
1. **Implement Portfolio Analytics API**:
   - `GET /api/v1/portfolio/summary` (Completed previously).
2. **Production Deployment Setup**:
   - Create `docker-compose.prod.yml`.
   - Setup Nginx production config.
   - Separate `.env.example`.

## 기대 산출물 (Expected Outputs)
- Working `docker-compose.prod.yml`.
- `nginx.prod.conf`.

## Execution Result
- Confirmed `Portfolio Analytics API` is implemented and logic is verified using `PortfolioService`.
- Created `nginx/nginx.prod.conf` pointing to frontend:3000 (adapter-node).
- Updated `docker-compose.prod.yml` to use `nginx.prod.conf`.
- Populated `.env.example` with necessary production environment variables.
- Verified `frontend/Dockerfile` uses multi-stage build and `adapter-node`.

---

# Handovers: To Backend Developer (v0.4.0 Deployment Setup)

## 날짜
2025-12-12

## 현재 상황 (Context)
- v0.3.0 tasks completed.
- v0.4.0 deployment setup requested.

## 해야 할 일 (Tasks)
1. **Implement Portfolio Analytics API**:
   - `GET /api/v1/portfolio/summary` (Completed previously).
2. **Production Deployment Setup**:
   - Create `docker-compose.prod.yml`.
   - Setup Nginx production config.
   - Separate `.env.example`.

## 기대 산출물 (Expected Outputs)
- Working `docker-compose.prod.yml`.
- `nginx.prod.conf`.

## Execution Result
- Confirmed `Portfolio Analytics API` is implemented and logic is verified using `PortfolioService`.
- Created `nginx/nginx.prod.conf` pointing to frontend:3000 (adapter-node).
- Updated `docker-compose.prod.yml` to use `nginx.prod.conf`.
- Populated `.env.example` with necessary production environment variables.
- Verified `frontend/Dockerfile` uses multi-stage build and `adapter-node`.
