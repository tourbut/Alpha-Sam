---
name: analyze-code-smells
description: 코드 스멜(Long Method, Large Class, Too many parameters 등) 감지 보고서 자동 생성기. 리팩토링 검토 시 사용.
---

# 코드 스멜 분석기 (Refactoring Analyzer)

## Purpose
`refactoring.md`의 원칙을 기반으로, 전체 코드베이스나 특정 파일에서 **리팩토링 대상이 되는 코드 스멜(Code Smells)**을 찾아내어 시각적인 보고서를 제공합니다.

이 스킬은 지나치게 긴 함수, 많은 컴포넌트 크기, 많은 수의 파라미터를 가진 함수 등을 식별해 변경 권고안을 던져줍니다.

## When to Run
- 리팩토링(Refactoring) 작업 시작 전
- 코드 품질 검토를 원할 때
- 앱의 복잡도가 증가해 유지보수가 어려울 때

## Workflow

당신은 백엔드(Python)와 프론트엔드(TypeScript/Svelte) 환경에서 정적 분석 스크립트를 구동하여 문제의 소지를 파악해야 합니다.

### Python 기반 탐지 스크립트 (백엔드 및 TypeScript 분석 혼용)
코드 분석을 위해 아래의 Python 스크립트를 임시 경로(`/tmp/analyze_smells.py`)에 저장하고 실행하세요.

```python
import ast
import os

def analyze_python_smells(target_dir):
    long_method_threshold = 20
    too_many_params_threshold = 4
    
    results = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith('.py'): continue
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    node = ast.parse(f.read())
            except Exception as e:
                continue

            for item in ast.walk(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Long Method Check
                    length = getattr(item, 'end_lineno', 0) - getattr(item, 'lineno', 0)
                    if length > long_method_threshold:
                        results.append(f"[Long Method] {path} -> {item.name}() is {length} lines long (Threshold: {long_method_threshold}).")
                    
                    # Too Many Parameters Check
                    # self, cls 등은 제외하거나 단순하게 args 수를 확인
                    total_args = len(item.args.args) + len(item.args.kwonlyargs)
                    if total_args > too_many_params_threshold:
                        results.append(f"[Long Parameter List] {path} -> {item.name}() has {total_args} parameters (Threshold: {too_many_params_threshold}).")
    return results

def analyze_svelte_files(target_dir):
    long_component_threshold = 300
    results = []

    for root, _, files in os.walk(target_dir):
        for file in files:
            if not file.endswith('.svelte'): continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Svelte Component Size Check
            if len(lines) > long_component_threshold:
                results.append(f"[Large Class/Component] {path} is {len(lines)} lines long (Threshold: {long_component_threshold}). Consider splitting into smaller components.")
    
    return results

if __name__ == "__main__":
    print("=== Analyzing Backend (Python) ===")
    py_results = analyze_python_smells("backend/app/src")
    if py_results:
        for r in py_results: print(r)
    else:
        print("No severe Code Smells detected in Python codebase.")

    print("\\n=== Analyzing Frontend (Svelte) ===")
    svelte_results = analyze_svelte_files("frontend/src")
    if svelte_results:
        for r in svelte_results: print(r)
    else:
        print("No severe Code Smells detected in Svelte codebase.")
```

### 후속 작업: 시사점 제공 가이드
도출된 결과를 단순히 나열하는 데 그치지 마세요. 결과를 기반으로 어떻게 리팩토링해야 할지 가이드를 제시해야 합니다.
1. **Long Method**: 특정 책임을 별개의 헬퍼 함수나 모듈 레벨로 분리하라고 조언.
2. **Large Class/Component**: Svelte 컴포넌트의 경우 상태나 UI(예: Button, Modal)를 하위 컴포넌트로 쪼개라고 조언.
3. **Long Parameter List**: 데이터 클래스(Parameter Object, DTO)를 생성해 파라미터를 묶어서 전달하라고 조언.

## Output Format
Markdown 문서 양식을 활용해 깔끔한 구조의 **"Code Smells Analysis Report"**를 최종 출력하세요.

### Report Example:
```markdown
# Code Smells Analysis Report

## ⚠ Backend (FastAPI) Issues
- **[Long Parameter List]** `backend/app/src/crud/user.py` -> `create_user_with_profile()` (7 param)
  - *Recommendation*: Introduce `UserCreateRequest` object to encapsulate parameters.

## ⚠ Frontend (Svelte) Issues
- **[Large Component]** `frontend/src/routes/portfolios/[id]/+page.svelte` (352 lines)
  - *Recommendation*: Extract table structures into common layout components.
```
