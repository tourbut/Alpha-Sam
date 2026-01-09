# Handovers: To Frontend Developer

## 날짜
- 2026-01-04

## 현재 상황 (Context)
- 백엔드 리팩토링이 완료되었으며, 프론트엔드 역시 유지보수성과 일관성을 위해 리팩토링이 필요합니다.
- 기존의 거대한 `api.ts`를 `frontend_code_style.md`에 정의된 모듈형 구조로 분리하고 표준화해야 합니다.

## 해야 할 일 (Tasks)

1.  **Frontend Code Style 가이드 숙지**
    - `.artifacts/projects/frontend_code_style.md`를 정독하십시오.
    - 핵심: `$lib/fastapi.js` 래퍼 구현, `apis/` 디렉토리 하위에 라우터별 파일 분리.

2.  **Core Wrapper 구현 (`frontend/src/lib/fastapi.js`)**
    - `frontend_code_style.md`의 **4. `api_router` 상세** 섹션을 참고하여 `api_router` 함수를 구현하십시오.
    - 기능: Base URL 설정, Auth 헤더 자동 주입, 에러 핸들링, JSON 파싱 등.

3.  **API 모듈화 (`frontend/src/lib/apis/`)**
    - `frontend/src/lib/apis/` 디렉토리를 생성하십시오.
    - 기존 `frontend/src/lib/api.ts`의 함수들을 백엔드 라우터 단위로 쪼개어 새 파일로 이관하십시오.
        - 예: `auth.js`, `users.js`, `assets.js`, `portfolio.js` 등.
    - 각 파일은 `api_router`를 사용하여 함수를 정의해야 합니다.

4.  **컴포넌트 연결 (`frontend/src/routes/**/*.svelte`)**
    - 기존 `api.ts`를 import해서 사용하던 컴포넌트들을 찾아, 새로 만든 `apis/*.js` 모듈을 사용하도록 수정하십시오.
    - `get_positions`, `create_asset` 등 함수 호출 시그니처가 변경될 수 있으니(콜백 방식 등) 가이드를 준수하여 수정하십시오.

5.  **검증 (Verification)**
    - 로그인, 자산 목록 조회, 포트폴리오 조회 등 핵심 기능이 정상 작동하는지 확인하십시오.
    - 브라우저 콘솔에 에러가 없는지 확인하십시오.

## 기대 산출물 (Expected Outputs)
- `frontend/src/lib/fastapi.js` 파일.
- `frontend/src/lib/apis/` 디렉토리 및 하위 API 모듈들.
- `frontend/src/routes/` 내 컴포넌트들이 새로운 API 모듈을 import하고 정상 동작함.
- `frontend/src/lib/api.ts` 제거 (또는 deprecated 처리).

## 참고 자료 (References)
- `.artifacts/projects/frontend_code_style.md` (Code Style Guide)
- `backend/app/src/routes/` (백엔드 라우터명 참조)
