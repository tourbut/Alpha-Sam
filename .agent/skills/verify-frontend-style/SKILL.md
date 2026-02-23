---
name: verify-frontend-style
description: 프론트엔드 API 호출 양식 검증 (Svelte + FastAPI Client). 프론트엔드 API 연동 후 사용.
---

# 프론트엔드 코드 스타일 검증

## Purpose
프론트엔드 애플리케이션(`.svelte`, `.js`)에서 백엔드와의 통신을 위해 지정된 API 호출 규칙(`frontend-code-style.md`)을 준수하는지 검증합니다.

1. **라이브러리 사용 검증**: `$lib/fastapi` 모듈의 `api_router` 래퍼를 올바르게 수입하고 사용하는지 확인합니다.
2. **라우터 템플릿 검증**: API 정의 시 `api_router(router, method, endpoint)` 형식을 지키는지 검사합니다.

## When to Run
- 새로운 프론트엔드 API 연동 코드를 추가한 후
- 백엔드 라우터 구조가 변경되어 프론트 측 API 설정을 일괄 개편할 때

## Related Files
| File | Purpose |
|------|---------|
| `frontend/src/lib/apis/*.js` | API 통신 함수들을 모아둔 클라이언트 파일 |

## Workflow

### Step 1: 라이브러리 사용 확인
**검사:** API 함수들이 `$lib/fastapi`의 `api_router`를 import 해서 사용하고 있는지 검증합니다.
```bash
grep -rn "api_router" frontend/src/lib/apis/ || echo "PASS"
```
**PASS 기준:** `import { api_router }` 가 올바르게 탐지됨
**FAIL 기준:** 임포트 내역 없음
**실패 시 수정 방법:** 커스텀 페치(fetch) 대신 `import { api_router } from "$lib/fastapi";` 를 사용하도록 수정하세요.

### Step 2: 잘못된 fetch API 직접 접근 금지
**검사:** 프론트엔드 apis 내에서 직접 `fetch()` 를 사용하여 공통 헤더/에러 핸들링을 우회하는지 검사합니다.
```bash
grep -rn "fetch(" frontend/src/lib/apis/ || echo "PASS"
```
**PASS 기준:** `grep` 결과 없음 (`PASS` 출력)
**FAIL 기준:** `fetch()` 직접 호출 내역 출력
**실패 시 수정 방법:** `fetch` 로직을 제거하고 `$lib/fastapi` 의 `api_router`로 변경하여 모든 호출이 `frontend/src/lib/fastapi.js` 를 통하도록 하세요.

## Output Format
| 검증 항목 | 결과 |
|-----------|------|
| api_router 사용 여부 | PASS/FAIL |
| fetch 직접 사용 금지 | PASS/FAIL |

## Exceptions
1. **fastapi.js 래퍼 자체**: `frontend/src/lib/fastapi.js` 내부에서는 `fetch` 사용이 허용(면제)됩니다.
2. 외부 서비스(예: 클라우드 스토리지 직접 업로드)로의 `fetch` 요청이 있을 경우, 불가피하면 면제 처리할 수 있습니다.
