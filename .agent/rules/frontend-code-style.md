---
trigger: model_decision
description: frontend-dev 호출시 사용
---

# Frontend Code Style Guide (Svelte + FastAPI Client)

이 문서는 `frontend/src/lib/apis` 디렉토리 내의 API 모듈 작성 규칙을 정의합니다. 백엔드 FastAPI와 통신하기 위한 표준화된 패턴을 따릅니다.

## 1. 기본 원칙

- **라이브러리**: `frontend/src/lib/fastapi.js`의 `api_router`를 사용하여 API 함수를 생성합니다.
- **경로**: 모든 API 정의 파일은 `frontend/src/lib/apis` 내에 위치시킵니다.
- **네이밍**: 파일명은 백엔드의 `router` 이름과 일치시키는 것이 관례입니다 (예: `backend/app/src/routes/users.py` -> `frontend/src/lib/apis/user.js`).

---

## 2. API 모듈 작성 규칙 (`frontend/src/lib/apis/*.js`)

### 구조

1.  **Import**: `$lib/fastapi`에서 `api_router`를 import합니다.
2.  **Router 정의**: `const router` 변수에 백엔드 라우터의 prefix를 지정합니다.
3.  **Export**: 각 엔드포인트에 대응하는 함수를 `api_router`를 통해 생성하고 `export` 합니다.

### 문법

```javascript
import { api_router } from "$lib/fastapi";

const router = "backend_router_prefix"; // 예: "users", "chat"

// export const function_name = api_router(router, method, endpoint);
export const function_name = api_router(router, 'method', 'endpoint_name');
```

- **method**: `'get'`, `'post'`, `'put'`, `'delete'`, `'stream'`, `'login'`, `'upload'`, `'download'` 중 하나를 사용합니다.
- **endpoint**: 백엔드 라우터 데코레이터의 경로와 일치시킵니다 (슬래시 제외).

### 예시 (`frontend/src/lib/apis/example.js`)

```javascript
import { api_router } from "$lib/fastapi";

const router = "example";

// GET Request: /api/v1/example/get_items
export const get_items = api_router(router, 'get', 'get_items');

// POST Request (JSON): /api/v1/example/create_item
export const create_item = api_router(router, 'post', 'create_item');

// Stream Request: /api/v1/example/stream_data
export const stream_data = api_router(router, 'stream', 'stream_data');
```

---

## 3. 컴포넌트에서의 사용 (`.svelte`)

생성된 API 함수는 다음과 같은 시그니처를 가집니다.

### 일반 요청 (`get`, `post`, `put`, `delete`)

```javascript
import { get_items } from "$lib/apis/example";

// params: 쿼리 파라미터(GET) 또는 Body(POST/PUT)
// success_callback: 성공 시 실행 (response data 전달됨)
// failure_callback: 실패 시 실행 (error data 전달됨)

const params = { category_id: "..." };

get_items(params, 
    (data) => {
        console.log("Success:", data);
        items = data;
    },
    (error) => {
        console.error("Error:", error);
    }
);
```

### 스트림 요청 (`stream`)

```javascript
import { stream_data } from "$lib/apis/example";

// params: Body
// success_callback: 스트림 종료 후 실행? (구현에 따라 다름, 보통 onFinish 용도)
// failure_callback: 에러 시 실행
// streamCallback: 데이터 청크가 들어올 때마다 실행

stream_data(
    { prompt: "hello" },
    () => console.log("Stream finished"),
    (err) => console.error(err),
    (chunk) => {
        // NDJSON 라인 단위로 파싱된 객체가 전달됨
        console.log("Chunk:", chunk);
        response_text += chunk.content;
    }
);
```

---

## 4. `api_router` 상세 (참고용)

`frontend/src/lib/fastapi.js`의 `api_router` 래퍼는 다음을 자동으로 처리합니다.

- **Base URL**: `$lib/constants`의 `API_URL` 사용.
- **URL 구성**: `/{router}/{endpoint}/` 형식을 따름.
- **Auth**: `$lib/stores`의 `user_token`이 있으면 `Authorization: Bearer ...` 헤더 자동 추가.
- **Content-Type**: 기본 `application/json` (파일 업로드/로그인 예외 처리).
- **Error Handling**: 401 Unauthorized 시 로그인 페이지 리다이렉트 등 공통 처리 포함.
