---
name: verify-frontend-style
description: 프론트엔드 코드 스타일 검증 (Svelte 5 + FastAPI Client). 프론트엔드 구현 및 API 연동 후 사용.
---

# 프론트엔드 코드 스타일 및 API 규칙 검증

## Purpose
프론트엔드 애플리케이션(`.svelte`, `.ts`, `.js`)에서 코딩 규칙(`dev-frontend-svelte.md`) 및 백엔드와의 API 통신 양식을 포괄적으로 점검합니다. 

이 스킬은 Svelte 5(Runes), TypeScript 엄격성, CSS 제약 조건, API 래퍼 사용성 등 핵심 프론트엔드 룰이 준수되고 있는지 자동 및 수동 병합 검증을 통해 확인합니다.

## When to Run
- 새로운 화면이나 컴포넌트를 추가/수정한 후
- 프론트엔드 코드 리뷰 및 PR 생성 전

## Workflow

코드 에이전트로서 당신은 단순히 텍스트를 검색하는 것뿐만 아니라 AST 파싱 툴 등을 이용하거나 파일을 직접 열람(view_file)하여 아래의 규칙들을 꼼꼼히 점검해야 합니다.

### Step 1: 상태 관리 및 Svelte 5 Runes 점검
- [ ] **Runes Syntax**: 오래된 Svelte 스토어 컨벤션(예: `export let`, `$:`) 대신 `$state`, `$derived`, `$props`, `$effect`가 사용되었는지 확인합니다.
- [ ] **State Library**: 외부 전역 상태 관리 라이브러리(Redux 등)가 불필요하게 사용되지 않았는지 검사합니다.

### Step 2: 스타일 및 컴포넌트 구조 점검
- [ ] **No Inline CSS**: HTML 태그 내에 `style="..."` 형태의 인라인 CSS가 사용되었는지 점검합니다. Tailwind CSS 유틸리티 클래스나 스코프 `<style>` 블록을 사용해야 합니다.
- [ ] **TypeScript 강제**: 스크립트 블록이 `<script lang="ts">` 로 선언되었는지, 모델이나 Props에 대한 인터페이스가 존재하는지 조사합니다. (No `any` rule)

### Step 3: API 통신 규칙 점검
- [ ] **`api_router` 래퍼 사용**: 외부 호출과 공통 처리가 필요한 부분에 `$lib/fastapi` 모듈의 `api_router`가 올바르게 사용되는지 점검합니다.
- [ ] **직접적인 fetch 호출 금지**: 직접 `fetch()` 를 사용하여 공통 헤더/에러 핸들링을 우회하는 패턴이 커스텀 페치 모듈 외에 존재하는지 확인합니다.

### Step 4: Python 기반 통합 자동화 검증 환경 제공
터미널에서 아래의 Python 검증 스크립트를 임시 파일(예: `/tmp/verify_frontend.py`)로 만들어 실행하여, 반복되는 실수를 빠르게 찾아내세요.

```python
import os
import re

def check_frontend_style():
    frontend_dir = "frontend/src"
    errors = []

    if not os.path.exists(frontend_dir):
        print("프론트엔드 디렉토리를 찾을 수 없습니다.")
        return

    # 정규식 패턴 정의
    legacy_export_pattern = re.compile(r'^\s*export\s+let\s+')
    legacy_reactive_pattern = re.compile(r'^\s*\$:\s+')
    inline_style_pattern = re.compile(r'<[^>]+style\s*=\s*["\'][^"\']+["\'][^>]*>')
    fetch_pattern = re.compile(r'\bfetch\s*\(')

    for root, _, files in os.walk(frontend_dir):
        for file in files:
            path = os.path.join(root, file)
            is_svelte = file.endswith('.svelte')
            is_script = file.endswith('.ts') or file.endswith('.js')

            if not (is_svelte or is_script):
                continue
                
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                line_num = i + 1
                
                if is_svelte:
                    # Svelte Legacy Syntax 검사
                    if legacy_export_pattern.search(line):
                        errors.append(f"[Svelte Runes] {path}:{line_num} -> 'export let' (Legacy) 사용됨. $props()를 사용하세요.")
                    if legacy_reactive_pattern.search(line):
                        errors.append(f"[Svelte Runes] {path}:{line_num} -> '$:' (Legacy) 사용됨. $derived() 또는 $effect()를 사용하세요.")
                    
                    # 인라인 CSS 검사
                    if inline_style_pattern.search(line):
                        errors.append(f"[Style] {path}:{line_num} -> inline style 사용됨. Tailwind CSS를 사용하세요.")

                # 직접 fetch 호출 검사 (api_router 미사용 시도)
                # 단, fastapi.ts나 의도된 래퍼 파일 내부는 제외 처리 필요
                if fetch_pattern.search(line) and not path.endswith('fastapi.ts') and not path.endswith('+server.ts'):
                    errors.append(f"[API] {path}:{line_num} -> 직접적인 'fetch' 호출 사용. $lib/fastapi의 api_router를 사용하세요.")

    if errors:
        for err in errors:
            print(err)
        print("\\nFAIL: 프론트엔드 스타일 규칙 위반 발견")
    else:
        print("\\nPASS: 모든 프론트엔드 자동 검증 룰(Svelte Runes / No inline CSS / No direct fetch) 통과.")

if __name__ == "__main__":
    check_frontend_style()
```

## Output Format
검증 완료 후 리포트를 출력해 줍니다. 

| 검증 항목 | 대상 | 결과 |
|-----------|------|------|
| Svelte 5 (Runes) 문법 적용 여부 | `.svelte` | PASS/FAIL |
| 인라인 CSS 미사용 검증 | `.svelte` | PASS/FAIL |
| Type-safe 구현 (lang="ts") | `.svelte`, `.ts` | PASS/FAIL/WARN |
| API 래퍼 적용 (api_router) | `.svelte`, `.js`, `.ts` | PASS/FAIL |

## Exceptions
1. **외부 모듈 및 스캐폴딩 내역**: `node_modules`, `build`, `.svelte-kit` 폴더 등은 검사 대상이 아닙니다.
2. 컴포넌트 간 통신에 쓰이지 않는 SvelteKit 기본 기능(예: Page Server Load의 순수 Fetch)은 허용됩니다.

## Core Frontend Development Style Guidelines (현재 개발 스타일 요약)
프론트엔드 작업 시 다음의 아키텍처 및 스타일을 일관되게 적용시킵니다.

### 1. Svelte 5 (Runes) 문법 및 상태 관리
- **Runes 적극 도입**: 기존 Svelte 4(`export let`, `$:`) 패턴은 레거시이므로 신규 구현에 사용을 금지하며, `$state`, `$derived`, `$props`, `$effect`를 표준으로 사용합니다.
- **클래스 기반 전역 상태**: 컴포넌트 외부의 전역 상태는 Redux나 `writable` 스토어 대신, `auth.svelte.ts`처럼 Svelte 5 Runes를 활용한 클래스 기반`.svelte.ts` 파일로 관리됩니다.

### 2. API 통신 및 래퍼(Wrapper) 사용
- **커스텀 `api_router` 강제**: 백엔드 API와의 통신은 반드시 `$lib/fastapi.ts`에 정의된 `api_router` 래퍼를 거쳐야 합니다. (`Authorization` 토큰 주입 및 공통 에러 핸들링 포함)
- **Fetch 직접 호출 금지**: 컴포넌트나 일반 모듈에서 네이티브 `fetch()`를 직접 호출하는 것은 금지됩니다. (예외: `+server.ts` 등 서버 측 로직)

### 3. TypeScript 및 타입 안정성 (Type-safety)
- **엄격한 타입 적용**: 모든 Svelte 컴포넌트 스크립트 블록은 `<script lang="ts">`로 선언합니다.
- **인터페이스 분리**: 도메인 모델이나 API 응답 형식은 구체적인 `interface`(`type`)로 `$lib/types` 등에 정의하여 사용하며 `any` 타입의 남발을 방지합니다.

### 4. 스타일링 (CSS) 및 UI 컴포넌트
- **Tailwind CSS Utility-first**: 별도의 Scoped `<style>` 블록이나 태그 내 인라인 CSS(`style="..."`)의 사용을 지양하고, Tailwind CSS 유틸리티 클래스로 일관된 스타일링을 적용합니다.
- **아이콘 및 모듈화**: 아이콘은 `flowbite-svelte-icons`를 주로 사용하며, 재사용 가능한 뷰티/도메인 컴포넌트는 `$lib/components/` 위치에 모듈화합니다.

### 5. 라우팅 및 레이아웃 구조
- **SvelteKit 전역 상태 기반 레이아웃**: `+layout.svelte` 및 `$app/state` 라우팅 정보, 글로벌 `auth` 스토어에 따라 Global Navbar, Sidebar, Footer의 노출 여부를 동적으로 제어합니다. (예: `/agent/*` 경로 전용 레이아웃 분리 처리 등)
