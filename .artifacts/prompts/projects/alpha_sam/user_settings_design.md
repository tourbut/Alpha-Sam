# User Settings Design (v0.3.0)

## 1. 개요
사용자가 자신의 프로필 정보(닉네임 등)를 수정하고, **비밀번호를 안전하게 변경**할 수 있는 기능을 제공합니다.
이를 위해 Backend의 `User` 모델을 확장하고, 관련 API 및 Frontend UI를 구현합니다.

## 2. Backend Design

### 2.1 Database & Model
**File:** `backend/app/models/user.py`

기존 `User` 모델에 사용자 식별을 위한 **닉네임(nickname)** 필드를 추가합니다.

```python
class User(SQLModel, table=True):
    # ... 기존 필드 ...
    nickname: Optional[str] = Field(default=None, max_length=50) # 추가
```

> **Note:** 마이그레이션(Alembic) 생성이 필요합니다.

### 2.2 API Schema (Pydantic)
**File:** `backend/app/schemas/user.py` (신규 혹은 기존 파일 수정)

데이터 검증을 위한 두 가지 Schema가 필요합니다.

1.  **UserUpdate**: 프로필 정보 수정용
    ```python
    class UserUpdate(SQLModel):
        nickname: Optional[str] = None
        email: Optional[EmailStr] = None # 이메일 변경 허용 시
    ```

2.  **UserPasswordUpdate**: 비밀번호 변경용
    ```python
    class UserPasswordUpdate(SQLModel):
        current_password: str
        new_password: str
    ```

### 2.3 API Endpoints
**File:** `backend/app/api/v1/endpoints/users.py`

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `PUT` | `/users/me` | 현재 로그인한 사용자의 프로필(닉네임) 수정 | Yes (JWT) |
| `POST` | `/users/password` | 현재 로그인한 사용자의 비밀번호 변경 | Yes (JWT) |

**Logic Detail:**
- **PUT /users/me**:
    - Request Body: `UserUpdate`
    - Logic: DB의 User 레코드를 업데이트.
- **POST /users/password**:
    - Request Body: `UserPasswordUpdate`
    - Logic:
        1. `current_password`가 현재 DB의 해시와 일치하는지 검증 (`verify_password`).
        2. 불일치 시 `400 Bad Request`.
        3. 일치 시 `new_password`를 해싱하여 저장.

## 3. Frontend Design

### 3.1 UI Structure
**Path:** `/settings` (신규 페이지)

페이지는 크게 두 상자(Card)로 구성합니다.

1.  **Profile Settings Card**
    - **Display**: 현재 이메일 (Read-only), 현재 닉네임.
    - **Input**: 닉네임 수정 필드.
    - **Action**: [저장] 버튼.
2.  **Security Settings Card**
    - **Input**: 현재 비밀번호, 새 비밀번호, 새 비밀번호 확인.
    - **Action**: [비밀번호 변경] 버튼.

### 3.2 State Management
- `auth` store(`src/lib/stores/auth.ts`)에 저장된 `user` 객체에 `nickname`이 포함되도록 로그인/세션 로직 업데이트 필요.
- 정보 수정 성공 시, 로컬 스토어의 사용자 정보도 동기화 업데이트.

## 4. Implementation Steps

1.  **Backend Model Update**: `User` 모델에 `nickname` 추가 및 Alembic Migration 수행.
2.  **Backend API Implementation**: `users.py` 라우터에 엔드포인트 구현.
3.  **Frontend API Client**: `api/v1/users/me` 호출 함수 추가.
4.  **Frontend UI**: `/settings` 페이지 및 폼 구현.
