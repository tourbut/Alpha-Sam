---
trigger: model_decision
description: backend_dev 호출시 사용
---

# Backend Code Style Guide (FastAPI + SQLModel)

이 문서는 `backend/app/src` 내의 `crud`, `schemas`, `routes` 디렉토리에 적용되는 코드 스타일 및 규칙을 정의합니다. 다른 코딩 에이전트가 이 프로젝트의 스타일을 준수하여 코드를 작성할 때 참고해야 합니다.

## 1. 기술 스택 및 공통 사항

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **ORM**: SQLModel (Async Support)
- **Database**: PostgreSQL (AsyncPG)
- **Type Hinting**: 모든 함수와 메서드에 명시적인 타입 힌트(`typing.List`, `uuid.UUID`, `User | None` 등)를 사용합니다.
- **Imports**: 절대 경로 import를 선호합니다 (e.g., `from app.src.schemas import ...`).

---

## 2. Schemas (`backend/app/src/schemas`)

Pydantic 모델(SQLModel 상속)을 정의하는 계층입니다.

### 규칙

1. **상속**: 모든 스키마 클래스는 `SQLModel`을 상속받습니다.
2. **Naming**:
    - 파일명: `snake_case` (도메인별 분리, 예: `users.py`, `chat.py`)
    - 클래스명: `PascalCase`
    - 목적에 따른 접두사/접미사 사용 권장 (예: `CreateUser`, `GetUser`, `UpdateUser`).
3. **Fields**:
    - `uuid.UUID` 타입을 ID로 사용합니다.
    - 날짜/시간 필드에는 `datetime = datetime.now()`와 같이 기본값을 설정하는 패턴이 자주 사용됩니다.
    - `Optional` 필드에는 `| None = None` 또는 `Optional[T] = None`을 사용합니다.
4. **구조 예시**:

```python
from typing import List, Optional
import uuid
from sqlmodel import SQLModel
from datetime import datetime

# 데이터 생성용 요청 스키마
class CreateItem(SQLModel):
    title: str
    description: str | None = None
    category_id: uuid.UUID

# 응답용 스키마
class GetItem(SQLModel):
    id: uuid.UUID
    title: str
    create_date: datetime = datetime.now()

# 업데이트용 스키마
class UpdateItem(SQLModel):
    id: uuid.UUID
    title: str | None = None
    delete_yn: bool | None = None
```

---

## 3. CRUD (`backend/app/src/crud`)

비즈니스 로직 및 데이터베이스 상호작용을 담당하는 계층입니다. **모든 함수는 비동기(`async`)**로 작성되어야 합니다.

### 규칙

1. **함수 시그니처**:
    - `async def` 필수.
    - 첫 번째 인자로 키워드 전용 인자 구분자 `*`를 사용합니다.
    - `session: AsyncSession`을 반드시 인자로 받습니다.
    - 예: `async def create_something(*, session: AsyncSession, item_in: SchemaClass) -> ReturnType:`
2. **트랜잭션 및 에러 핸들링 패턴 (중요)**:
    - **모든** 쓰기/수정/삭제 작업은 `try...except` 블록으로 감싸야 합니다.
    - 예외 발생 시 `current exception`을 출력(`print(e)`)하고, `await session.rollback()`을 수행한 후, 에러를 다시 발생(`raise e`)시킵니다.
    - 이는 트랜잭션 무결성을 보장하기 위함입니다.
3. **데이터 조회**:
    - `await session.exec(select(...))` 패턴을 사용합니다.
    - 결과는 `.all()` 또는 `.first()`로 반환합니다.
    - 조건절에는 `where(Model.field == value)` 형태를 사용하며, 필요 시 `and_`, `or_`를 사용합니다.
4. **데이터 생성/수정**:
    - `model_validate`를 사용하여 스키마를 DB 모델로 변환합니다.
    - `session.add(obj)` -> `await session.commit()` -> `await session.refresh(obj)` 순서를 따릅니다.

### 코드 예시

```python
from typing import List
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.item import Item
from app.src.schemas import item as item_schema

# 조회 (Read)
async def get_item_by_id(*, session: AsyncSession, item_id: uuid.UUID) -> Item | None:
    try:
        statement = select(Item).where(Item.id == item_id, Item.delete_yn == False)
        result = await session.exec(statement)
        return result.first()
    except Exception as e:
        print(e)
        await session.rollback()
        raise e

# 생성 (Create)
async def create_item(*, session: AsyncSession, item_in: item_schema.CreateItem) -> Item:
    try:
        db_obj = Item.model_validate(item_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as e:
        print(e)
        await session.rollback() # 롤백 필수
        raise e
```

---

## 4. Routes (`backend/app/src/routes`)

API 엔드포인트를 정의하는 계층입니다.

### 규칙

1. **Router 설정**: `router = APIRouter()` 사용.
2. **Dependency Injection**:
    - `app.src.deps`에서 `SessionDep_async` (비동기 세션)와 `CurrentUser` (현재 로그인 유저)를 가져와 사용합니다.
    - 예: `session: SessionDep_async`, `current_user: CurrentUser`
3. **Endpoint 정의**:
    - `response_model`을 명시하여 응답 스키마를 정의합니다.
    - 함수 인자는 키워드 전용(`*`)으로 시작하는 것을 권장합니다.
4. **CRUD 호출**:
    - 비즈니스 로직은 가능한 `crud` 모듈로 위임하고, 라우터에서는 파라미터 전달 및 응답 반환에 집중합니다.
5. **Redis 사용**:
    - Redis가 필요한 경우 `request.app.state.redis` 또는 의존성을 통해 접근합니다.

### 코드 예시

```python
from typing import Any, List
import uuid
from fastapi import APIRouter, HTTPException, Request
from app.src.deps import SessionDep_async, CurrentUser
from app.src.crud import item as item_crud
from app.src.schemas import item as item_schema

router = APIRouter()

@router.post("/create_item", response_model=item_schema.GetItem)
async def create_item(
    *,
    session: SessionDep_async,
    current_user: CurrentUser,
    item_in: item_schema.CreateItem
) -> Any:
    # Service/CRUD 호출
    item = await item_crud.create_item(session=session, item_in=item_in)
    return item

@router.get("/get_items", response_model=List[item_schema.GetItem])
async def get_items(
    *,
    session: SessionDep_async,
    current_user: CurrentUser
) -> Any:
    items = await item_crud.get_items(session=session, user_id=current_user.id)
    return items
```

