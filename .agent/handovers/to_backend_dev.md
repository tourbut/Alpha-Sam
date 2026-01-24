# Handovers: To Backend Developer

## 날짜
- 2026-01-24

## 브랜치 (Version Control)
- `refactor/backend-structure-optimization` (develop 브랜치에서 분기)

## 현재 상황 (Context)
- 사용자 요청에 따라 백엔드 코드의 모듈화 및 리팩토링을 진행해야 합니다.
- 현재 `engine`과 `services` 디렉토리 간 역할 중복이 있으며, 로직이 과도하게 세분화되거나 비표준적인 파일명(`crud_*.py`)을 사용하고 있습니다.
- 백엔드 코드 스타일 가이드(`backend-code-style.md`)를 준수해야 합니다.

## 해야 할 일 (Tasks)

### 1. 서비스 및 엔진 계층 통합 (Service Layer Refactoring)
- **목표**: `engine` 디렉토리를 제거하고 비즈니스 로직을 `services`로 통합.
- 1.1 `backend/app/src/engine/portfolio_service.py`의 계산 로직 함수들(`calculate_*`)을 `backend/app/src/services/portfolio_calculator.py` (신규 파일)로 이동합니다.
- 1.2 `backend/app/src/engine/portfolio_service.py`의 `PortfolioService` 클래스에 있는 DB 관련 메서드(`create_portfolio`, `get_user_portfolios` 등)를 확인합니다. 이들은 **CRUD Layer**로 이동해야 합니다 (아래 2번 참조).
- 1.3 `backend/app/src/engine` 디렉토리를 삭제합니다. (관련 import 경로 모두 수정 필요: `from app.src.engine...` -> `from app.src.services...`)
- 1.4 `backend/app/src/services/portfolio_service.py`가 새 위치의 계산 모듈(`portfolio_calculator.py`)을 참조하도록 수정합니다.

### 2. CRUD 모듈 표준화 (CRUD Layer Refactoring)
- **목표**: 스타일 가이드에 맞춰 `crud` 디렉토리 구조 개선.
- 2.1 `backend/app/src/crud/crud_*.py` 파일들을 `backend/app/src/crud/*.py`로 변경합니다.
  - `crud_user.py` -> `users.py`
  - `crud_asset.py` -> `assets.py`
  - `crud_position.py` -> `positions.py`
  - `crud_transaction.py` -> `transactions.py`
  - `crud_portfolio_history.py` -> `portfolio_histories.py`
  - `crud_notification.py` -> `notifications.py`
- 2.2 `portfolios.py`를 `crud` 디렉토리에 새로 생성합니다.
  - 기존 `engine/portfolio_service.py`에 있던 `create_portfolio`, `get_user_portfolios` 등의 DB 접근 로직을 여기로 옮깁니다. (`async`, `*`, `session` 인자 규칙 준수)
- 2.3 변경된 CRUD 모듈명을 반영하여 프로젝트 전체의 import 구문을 수정합니다. (예: `from app.src.crud import crud_user` -> `from app.src.crud import users as user_crud`)

### 3. 라우터 로직 다이어트 (Refactor Routes)
- 3.1 `backend/app/src/routes/portfolios.py`를 검토하여, 비즈니스 로직이 라우터에 직접 구현된 부분이 있다면 `Service` 계층(`services/portfolio_service.py` 등)으로 이동시킵니다.
- 3.2 라우터는 오직 Request/Response 처리와 Service/CRUD 호출만 담당해야 합니다.

### 4. 코드 스타일 점검
- 4.1 모든 신규/수정 파일이 `.agent/rules/backend-code-style.md`를 준수하는지 확인합니다(Type Hinting, Async Session, Pydantic Schema 사용 등).

## 기대 산출물 (Expected Outputs)
- `engine` 디렉토리가 삭제되고 로직이 `services`로 통합됨.
- `crud` 디렉토리 내 파일명이 `crud_` 접두어 없이 깔끔하게 정리됨.
- `routes/portfolios.py`가 가벼워지고 비즈니스 로직이 분리됨.
- 서버(`uvicorn`)가 정상 구동되고 기존 기능(포트폴리오 조회, 계산 등)이 문제없이 작동함.

## 참고 자료 (References)
- `.agent/rules/backend-code-style.md`: 백엔드 코드 스타일 가이드 (필독)
