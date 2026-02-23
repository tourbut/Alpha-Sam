---
name: verify-backend-style
description: 백엔드 코드 스타일 검증 (FastAPI + SQLModel). 백엔드 로직 수정 후 사용.
---

# 백엔드 코드 스타일 검증

## Purpose
백엔드 FastAPI 및 SQLModel의 코드베이스가 지정된 스타일 규칙(`backend-code-style.md`)을 준수하는지 검증합니다.

1. **Schemas 검증**: Pydantic 모델이 `SQLModel` 상속을 올바르게 수행하는지 검사
2. **CRUD 검증**: 모든 CRUD 함수들이 비동기(`async def`)로 구현되었는지 검사
3. **Routes 검증**: API 라우트 엔드포인트에서 비동기 세션 의존성(`SessionDep_async`)을 사용하는지 검사

## When to Run
- 백엔드 기능을 구현하거나 수정한 후
- 백엔드 관련 PR(Pull Request) 생성 전

## Related Files
| File | Purpose |
|------|---------|
| `backend/app/src/schemas/*.py` | 데이터 정의 (Pydantic, SQLModel) |
| `backend/app/src/crud/*.py` | DB 비즈니스 로직 |
| `backend/app/src/routes/*.py` | API 라우트 정의 |

## Workflow

### Step 1: Schemas 검증 (SQLModel 상속)
**검사:** 스키마 클래스에 `SQLModel`이 제대로 상속되어 있는지 검사합니다.
```bash
# class 선언 중 SQLModel 상속이 없는지 확인 (결과가 없어야 패스)
grep -rn "^class " backend/app/src/schemas/ | grep -v "SQLModel" | grep -v "__init__.py" || echo "PASS"
```
**PASS 기준:** `grep` 결과 없음 (`PASS` 출력)
**FAIL 기준:** `SQLModel`을 상속하지 않은 클래스 목록 출력
**실패 시 수정 방법:** `class ClassName(BaseModel):`을 `class ClassName(SQLModel):` 로 변경하고 sqlmodel을 import 하세요.

### Step 2: CRUD 검증 (비동기 함수)
**검사:** CRUD 함수가 모두 `async def`로 구현되어 있는지 검사합니다.
```bash
# 동기 함수 def 선언이 있는지 확인 (결과가 없어야 패스)
grep -rn "^def " backend/app/src/crud/ | grep -v "__init__.py" || echo "PASS"
```
**PASS 기준:** `grep` 결과 없음 (`PASS` 출력)
**FAIL 기준:** 동기 함수 `def func_name:` 형태가 출력됨
**실패 시 수정 방법:** `def`를 `async def`로 변경하고 내부 로직에 `await`를 적절히 추가하세요.

### Step 3: Routes 검증 (비동기 세션 주입)
**검사:** 엔드포인트가 비동기 DB 세션을 올바르게 주입받는지 검사합니다.
```bash
# SessionDep_async 임포트 내역 검사
grep -rn "SessionDep_async" backend/app/src/routes/ || echo "PASS"
```
**PASS 기준:** 각 파일이 `SessionDep_async`를 올바르게 임포트하거나 의존성을 받고 있음
**FAIL 기준:** 올바르지 않은 세션 사용

## Output Format
| 검증 항목 | 대상 | 결과 |
|-----------|------|------|
| Schemas | `backend/app/src/schemas/*.py` | PASS/FAIL |
| CRUD Async | `backend/app/src/crud/*.py` | PASS/FAIL |
| Routes Session| `backend/app/src/routes/*.py` | PASS/FAIL |

## Exceptions
1. **__init__.py**: 패키지 초기화 파일은 검사에서 면제됩니다.
2. **비 데이터 모델 클래스**: 설정(Config) 등 SQL DB 관련 데이터 모델이 아닌 보조 클래스는 면제될 수 있습니다.
