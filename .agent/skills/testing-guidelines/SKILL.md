---
name: testing-guidelines
description: Alpha-Sam 프로젝트의 모든 테스트(Unit, Integration, E2E 등) 작성 및 실행 규칙. "테스트 작성", "테스트 실행", "단위 테스트", "통합 테스트", "pytest" 등의 키워드가 언급될 때, 코드를 작성하거나 실행하기 전 반드시 이 스킬을 참고하여 올바른 디렉토리와 환경에서 수행하세요.
---

# Testing Guidelines (Alpha-Sam)

이 문서는 Alpha-Sam 프로젝트 내 모든 테스트(Unit, Integration, E2E 등) 작성 및 실행에 대한 핵심 규칙을 안내합니다. 
테스트 환경은 애플리케이션 소스 코드와 분리되어 관리됩니다.

## 1. 전역 테스트 디렉토리 (`tester/`) 사용
- 모든 테스트 코드와 테스트 스크립트는 `backend/` 또는 `frontend/` 본 위치 내에 소스 코드와 혼재시켜서는 안 됩니다. 
- 테스트 코드는 반드시 프로젝트 최상단에 위치한 통합 **`tester/`** 디렉토리 하위에 구성해야 합니다.
  - **예시**: 백엔드 테스트는 `tester/backend/tests/` 구조로 관리합니다.

## 2. 테스트 수행 (Execution)
- 테스트 실행은 항상 `tester/` 하위 계층에서 수행되어야 합니다.
- **백엔드 테스트 실행 방법 (루트 기준)**:
  ```bash
  cd tester/backend
  uv run pytest
  ```
- **환경 변수 참조 및 의존성 주입**:
  - `tester/backend/pytest.ini` 설정의 `pythonpath = ../../backend` 설정을 통해서 `backend` 모듈의 내부 절대 경로(예: `from app.src...`)를 올바르게 인식하도록 구성되어 있습니다.

## 3. 새로운 모듈 개발 시 주의사항
- 기능을 새롭게 개발하는 개발자 (Backend, Frontend) 또는 QA-Tester가 테스트를 생성할 때, 반드시 `tester/` 디렉토리를 타겟으로 새 테스트 스크립트를 작성하세요.
- 각 에이전트는 테스트를 수행할 때 현재 디렉토리가 `tester/` 내부인지 확인한 뒤 스크립트를 실행해야 합니다.
