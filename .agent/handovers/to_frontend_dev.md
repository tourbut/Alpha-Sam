# Handovers: To Frontend Dev

## 날짜
- 2026-03-23

## 브랜치 (Version Control)
- `refactor/frontend-style-compliance`

## 현재 상황 (Context)
- 프론트엔드의 Svelte 5 (Runes) 문법 및 API 통신 래퍼(`api_router`) 사용 등 핵심 개발 스타일의 기준이 `verify-frontend-style/SKILL.md`와 `frontend_style_analysis.md` 파일에 성공적으로 확립되었습니다.
- 하지만 기존 코드 중 불필요한 레거시 문법(`export let`, 직접적인 네이티브 `fetch()` 호출)이 일부 남아있어, 이를 모두 식별하고 일관된 스타일 기준에 맞게 교체하는 정밀 리팩토링 및 코드 정리(Cleanup)가 필요한 상황입니다.

## 해야 할 일 (Tasks)
1. `frontend_style_analysis.md` 문서 및 `.agent/skills/verify-frontend-style/SKILL.md` 가이드라인을 꼼꼼히 구문 숙지하기.
2. `python /tmp/verify_frontend.py` 스크립트를 사용하여 현재 검출되는 프론트엔드 스타일 위반 사항(Svelte Runes 미서용, 직접 fetch 등) 스캔 및 파악.
3. `AssetModal.svelte` 등에서 검출된 레거시 Svelte 4 구문(`export let` 등)을 최신 Svelte 5 Runes(`$props()`, `$state()` 등) 표준으로 전면 리팩토링.
4. `routes/agent/login/+page.svelte` 및 `lib/apis/portfolio.ts`(`uploadPortfolio` 등) 코드 내에 존재하는 모든 네이티브 `fetch()` 호출부 제거 후, `$lib/fastapi.ts` 구조의 `api_router` 래퍼로 교체 (이미 FormData 처리가 지원됨).
5. `frontend/src` 내에 남아있는 불필요한 레거시 파일, 데드 코드(사용되지 않는 컴포넌트나 함수), 더 이상 참조되지 않는 상태 변수 및 주석 등을 대대적으로 식별하여 완전하게 제거하기.
6. 전체 스타일 리팩토링 및 불필요한 코드 정리 후, 빌드 오류(`npm run check`, `npm run build`)가 없는지 확인하고, 다시 한번 `python /tmp/verify_frontend.py` 검증 스크립트를 실행해 위반 0건('PASS')이 출력되는지 체크할 것.

## 기대 산출물 (Expected Outputs)
- 스크립트 실행 시 콘솔에서 규칙 위반 0건("PASS") 확인 가능해야 함.
- 프론트엔드 내부의 모든 외부 통신 지점이 직접 `fetch()` 없이 오직 `$lib/fastapi.ts`의 `api_router`로 통일됨.
- `frontend/src` 내 모종의 데드 코드/무의미한 컴포넌트가 말끔히 정리되고 최신 Svelte 5 표준에 맞춰짐.

## 참고 자료 (References)
- `.agent/skills/verify-frontend-style/SKILL.md`
- `/Users/shin/.gemini/antigravity/brain/f6a7a953-97aa-4223-b957-3d2177ef8ce7/frontend_style_analysis.md`
- `python /tmp/verify_frontend.py` (자동 검증 툴 확인용)
