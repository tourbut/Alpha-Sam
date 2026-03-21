---
name: generate-tests
description: 원칙에 입각한 단위 테스트/통합 테스트 자동 스캐폴딩 생성기. 새 기능을 개발하고 테스트 환경이 필요할 때 사용.
---

# 테스트 자동 생성기 (Generate Tests)

## Purpose
`unit-testing.md` 및 `integration-testing.md`의 엄격한 가이드를 바탕으로, 사용자가 요청한 주요 기능(클래스/함수)에 대해 의존성이 완전히 분리되고 AAA(Arrange-Act-Assert) 구조가 완벽히 적용된 **테스트 코드의 초안을 스캐폴딩(자동 생성)**합니다.

단순히 템플릿만 채워 넣는 것이 아니라, 외부 의존성(DB, 파일 등)을 어떻게 Mocking/Stubbing 처리할지에 대한 최상의 구조를 제시합니다.

## When to Use
- 백엔드 CRUD, 비즈니스 로직(서비스 계층) 개발 완료 후.
- 특정 프론트엔드 유틸리티 및 계산 로직을 외부 모듈로 꺼낸 후 점검이 필요할 때.
- "이 코드의 단위 테스트나 통합 테스트를 작성해줘"라는 사용자 요청 발생 시.

## Instruction to Agent

사용자로부터 타깃 소스 코드(또는 파일)를 전달받았다면, 다음 절차를 거쳐 테스트 생성 업무를 인가하고 코드를 출력하십시오.

### 1) 구조적 분석 및 전략립
1. 대상 코드가 외부 데이터베이스 통신, 외부 API 요청, 혹은 Date 객체 등에 종속적인지 조사.
2. 단위 테스트(Unit Test)를 작성할지 통합 테스트(Integration Test)를 작성할지 결정 (일반적으로 DB 모킹은 유닛 테스트, Test Double/전체 호출은 통합 테스트).
3. 파이썬 환경의 경우 `pytest`의 `unittest.mock` (`patch`, `MagicMock`, `AsyncMock`)을 사용할 로드맵 수립.

### 2) 테스트 파일 생성 컨벤션
다음의 구조를 강제하여 테스트 코드를 생성하십시오:

1. **테스트 프레임워크**: Python의 경우 `pytest` + `pytest-asyncio` 문법 위주.
2. **함수 네이밍**: `test_should_<expected_behavior>_when_<condition>` 형태 권장 (예: `test_should_return_user_when_valid_id_provided`).
3. **AAA 주석 표기**: 반드시 각각의 블록을 분리하여 `# Arrange`, `# Act`, `# Assert` 주석을 달아 가독성을 확보할 것.
4. **Fixture**: 공통으로 사용되는 객체 설정 등은 `pytest.fixture`로 상단에 선언하여 재사용성을 높일 것.

### 3) 템플릿 예시 (Python. 백엔드)

이 형태가 출력의 베이스 템플릿이 되도록 강제합니다.

```python
import pytest
from unittest.mock import AsyncMock, patch
from app.src.schemas.user import UserCreate
from app.src.crud.user import create_user

# --- Fixtures ---
@pytest.fixture
def mock_session():
    # 비동기 커밋과 메서드들을 가지고 있는 세션 목(Mock) 객체
    session = AsyncMock()
    return session

@pytest.fixture
def valid_user_data():
    return UserCreate(email="test@example.com", username="tester")

# --- Tests ---
@pytest.mark.asyncio
async def test_should_create_user_and_return_db_obj_when_valid_data(mock_session, valid_user_data):
    # Arrange
    # 세션 동작 중 하나를 가짜(Stub)로 응답하게 만들기
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Act
    result = await create_user(session=mock_session, user_in=valid_user_data)

    # Assert
    assert result.email == valid_user_data.email
    assert result.username == valid_user_data.username
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_should_raise_exception_and_rollback_when_db_fails(mock_session, valid_user_data):
    # Arrange
    # 데이터베이스 에러 강제 유발
    mock_session.commit.side_effect = Exception("DB Connection Error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await create_user(session=mock_session, user_in=valid_user_data)
        
    assert "DB Connection Error" in str(exc_info.value)
    mock_session.rollback.assert_awaited_once()
```

## Output Format
1. 타겟에 맞춘 **전체 테스트 코드 (.py 나 .ts)** 스니펫 제공.
2. 해당 테스트를 실행(Run)하기 위한 터미널 명령어 (예: `pytest backend/tests/crud/test_user.py -v`) 제공.
3. 통합 테스트(DB 컨테이너 기반)가 필요한 상황이라면, 추가적으로 Database 적용 방법론(`conftest.py` 등) 조언.
