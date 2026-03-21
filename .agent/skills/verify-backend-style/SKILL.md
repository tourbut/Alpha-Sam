---
name: verify-backend-style
description: 백엔드 코드 스타일 검증 (FastAPI + SQLModel). 백엔드 로직 수정 후 사용.
---

# 백엔드 코드 스타일 검증

## Purpose
백엔드 FastAPI 및 SQLModel의 코드베이스가 프로젝트에 지정된 스타일 규칙(`backend-code-style.md`)을 철저히 준수하는지 검증합니다.

백엔드 스키마, 데이터베이스 쿼리를 담당하는 CRUD 로직, 엔드포인트를 노출하는 라우터 각각에 대해 구체적인 코드 품질과 일관성을 평가합니다.

## When to Run
- 백엔드 기능을 구현하거나 수정한 후
- 백엔드 관련 PR(Pull Request) 생성 전

## Related Files
| File | Purpose |
|------|---------|
| `backend/app/src/schemas/*.py` | 데이터 정의 (Pydantic, SQLModel) |
| `backend/app/src/crud/*.py` | DB 비즈니스 로직 및 트랜잭션 관리 |
| `backend/app/src/routes/*.py` | API 라우트 정의 및 의존성 주입 |

## Workflow

코드 에이전트로서 당신은 아래의 단계에 따라 코드를 검증해야 합니다. 단순 `grep`을 사용할 수도 있으나, 문맥적인 이해가 필요한 항목(예: try-except 롤백 패턴)들은 `grep` 혹은 AST 파싱 툴 등을 이용하거나 파일을 직접 열람(view_file)하여 꼼꼼히 점검해야 합니다.

### Step 1: Schemas 검증 (`backend/app/src/schemas`)
- [ ] **SQLModel 상속**: 모든 데이터 스키마 모델 클래스가 BaseModel이 아닌 `SQLModel`을 반환/상속하고 있는지 확인합니다.
- [ ] **UUID 타입 사용**: 모델의 식별자(ID) 필드에 `uuid.UUID` 타입이 적용되었는지 확인합니다.
- [ ] **Optional 필드**: Optional 필드에는 `| None = None` 또는 `Optional[T] = None`을 올바르게 사용하는지 확인합니다.

```bash
# 단순 상속 누락 1차 확인 (결과가 없어야 패스)
grep -rn "^class " backend/app/src/schemas/ | grep -v "SQLModel" | grep -v "__init__.py" || echo "PASS"
```

### Step 2: CRUD 검증 (`backend/app/src/crud`)
- [ ] **비동기 함수**: 파일 내의 모든 함수는 동기(`def`)가 아닌 비동기(`async def`)로 구현되어야 합니다.
- [ ] **키워드 전용 인자 (`*`)**: 모든 CRUD 함수의 첫 번째 인자로는 키워드 전용 인자 구분자인 `*`가 들어가야 합니다.
  - 예: `async def create_item(*, session: AsyncSession, item_in: Schema):`
- [ ] **AsyncSession 주입**: 모든 CRUD는 인자로 `session: AsyncSession` 변수를 받아야 합니다.
- [ ] **트랜잭션 및 에러 핸들링**: DB에 쓰기, 수정, 삭제(add, commit, delete)하는 모든 로직은 반드시 `try...except Exception as e:` 블록 내부에서 실행되어야 합니다. 또한 에러 발생 시 `await session.rollback()` 과 `raise e` 가 실행되어 전체 트랜잭션을 롤백해야 합니다.

```bash
# 동기 함수 def 선언이 있는지 확인 (결과가 없어야 패스)
grep -rn "^def " backend/app/src/crud/ | grep -v "__init__.py" || echo "PASS"

# CRUD 함수 중 키워드 전용인자(*) 누락여부 텍스트 기반 검사
grep -rn "async def " backend/app/src/crud/ | grep -v "(\*" || echo "PASS"
```

### Step 3: Routes 검증 (`backend/app/src/routes`)
- [ ] **엔드포인트 비동기 세션**: API 엔드포인트에서 비동기 세션을 올바르게 의존성 주입(`SessionDep_async`)받는지 확인합니다.
- [ ] **엔드포인트 모델 정의**: 라우터 데코레이터 내부에 반환 형태(예: `@router.get("/...", response_model=...)`)가 명시되어 있는지 점검합니다.
- [ ] **키워드 전용 인자 (`*`)**: 라우터 함수의 첫 번째 인자로 키워드 전용 구분자 `*`가 포함되어 있는지 확인합니다.

```bash
# SessionDep_async 주입 내역 검사
grep -rn "SessionDep_async" backend/app/src/routes/ || echo "PASS"

# response_model 누락 가능성이 있는 라우터 매핑 찾기 (수동 점검 필요)
grep -rn "@router\." backend/app/src/routes/ | grep -v "response_model" || echo "PASS"
```

### Step 4: Python 기반 자동화 통합 검증 실행 
터미널에서 텍스트 처리가 복잡한 규칙들(AST 이용)을 빠르게 잡아내려면 아래 스크립트를 작업 환경 내에 임시 파일(예: `/tmp/verify_backend.py`)로 저장하고 실행해 점검하세요.

```python
import ast
import os

def check_backend_style():
    schemas_dir = "backend/app/src/schemas"
    crud_dir = "backend/app/src/crud"
    routes_dir = "backend/app/src/routes"
    
    errors = []

    # 1. Schemas 체크
    if os.path.exists(schemas_dir):
        for root, _, files in os.walk(schemas_dir):
            for file in files:
                if not file.endswith(".py") or file == "__init__.py": continue
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read())
                for item in node.body:
                    if isinstance(item, ast.ClassDef):
                        bases = [b.id for b in item.bases if isinstance(b, ast.Name)]
                        if "SQLModel" not in bases and "BaseModel" in bases:
                            errors.append(f"[Schemas] {path} - {item.name}: SQLModel 상속 누락 (BaseModel 대신 SQLModel 상속 필요)")

    # 2. CRUD 체크
    if os.path.exists(crud_dir):
        for root, _, files in os.walk(crud_dir):
            for file in files:
                if not file.endswith(".py") or file == "__init__.py": continue
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read())
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef):
                        if not item.args.kwonlyargs:
                            errors.append(f"[CRUD] {path} - {item.name}: 키워드 전용 인자(*) 형태 누락")
                        has_session = any(arg.arg == "session" for arg in item.args.kwonlyargs) or any(arg.arg == "session" for arg in item.args.args)
                        if not has_session:
                            errors.append(f"[CRUD] {path} - {item.name}: session 전달 누락")
                    elif isinstance(item, ast.FunctionDef):
                        errors.append(f"[CRUD] {path} - {item.name}: 동기(def) 함수 선언. 비동기(async def)가 강제되어야 합니다.")

    # 3. Routes 체크
    if os.path.exists(routes_dir):
        for root, _, files in os.walk(routes_dir):
            for file in files:
                if not file.endswith(".py") or file == "__init__.py": continue
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read())
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef):
                        is_route = any(isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) and dec.func.value.id == "router" 
                                       for dec in item.decorator_list if hasattr(dec, 'func') and hasattr(dec.func, 'value') and hasattr(dec.func.value, 'id'))
                        if is_route:
                            if not item.args.kwonlyargs:
                                errors.append(f"[Routes] {path} - {item.name}: 라우터 엔드포인트 함수의 키워드 전용 인자(*) 누락")

    if errors:
        for err in errors:
            print(err)
        print("FAIL: 백엔드 스타일 규칙 위반 발견")
    else:
        print("PASS: 모든 백엔드 자동 검증 룰(SQLModel 상속 / async 유지 / 키워드인자(*) / 세션) 통과.")

if __name__ == "__main__":
    check_backend_style()
```

이외에도 **트랜잭션 롤백 처리(`await session.rollback()`) 여부** 등 자동화 스크립트로 감지하기 복잡한 부분은 `grep`이나 코드 열람을 통해 수동으로 반드시 점검하세요.

## Output Format
당신은 백엔드 작업 검수를 실행한 뒤, 사용자에게 명시적으로 룰 검사 결과를 피드백 해 주어야 합니다.  

| 검증 항목 | 대상 | 결과 |
|-----------|------|------|
| Schemas (SQLModel 상속, 필드 타입) | `backend/app/src/schemas/*.py` | PASS/FAIL/예외 사유 |
| CRUD (Async, `*`, Session 주입, Rollback) | `backend/app/src/crud/*.py` | PASS/FAIL/예외 사유 |
| Routes (Response Model, `*`, Session 주입) | `backend/app/src/routes/*.py` | PASS/FAIL/예외 사유 |

## Exceptions
1. **`__init__.py`**: 패키지 초기화 파일은 검사 대상에서 면제됩니다.
2. **비 데이터베이스 클래스**: 스키마 디렉토리 내에 있더라도 설정(Config), Pydantic 유틸리티 등 순수하게 DB와 연동되지 않는 보조 클래스는 `SQLModel` 상속 기준에서 제외될 수 있습니다.
