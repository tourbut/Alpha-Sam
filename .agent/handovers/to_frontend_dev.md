# Handovers: To Frontend Developer

## 날짜
- 2026-01-22

## 브랜치 (Version Control)
- `feature/frontend-app-name-constant`

## 현재 상황 (Context)
- `src/lib/constants.ts`에 `APP_NAME = "Alphafolio"` 상수가 추가되었습니다.
- 현재 프로젝트 곳곳에 "Alpha-Sam"이라는 하드코딩된 문자열이 남아있어 이를 일괄 수정해야 합니다.

## 해야 할 일 (Tasks)
1. `src/lib/constants.ts`에서 `APP_NAME`을 import 하여 다음 파일들의 하드코딩된 앱 이름("Alpha-Sam")을 상수로 교체합니다.
   - `src/lib/components/common/AppNavbar.svelte` (로고/브랜드명)
   - `src/lib/components/Footer.svelte` (Copyright 등)
   - `src/routes/+page.svelte` (랜딩 페이지 텍스트 및 `<title>`)
   - `src/routes/portfolios/+page.svelte` (`<title>`)
   - `src/routes/transactions/+page.svelte` (`<title>`)
   - `src/routes/positions/+page.svelte` (`<title>`)
   - `src/routes/(auth)/signup/+page.svelte` (`<title>` 등)
   - `src/lib/components/chat/ChatWidget.svelte` (챗봇 타이틀 등)
2. 기타 소스 코드 내 "Alpha-Sam" 검색 결과가 있다면 모두 `APP_NAME` 상수로 대체합니다.
3. 변경 후 `npm run dev`로 화면에 "Alphafolio"가 정상적으로 출력되는지 확인합니다.

## 기대 산출물 (Expected Outputs)
- 모든 UI 및 페이지 타이틀에서 "Alpha-Sam" 대신 "Alphafolio"가 표시되어야 함.
- 하드코딩된 앱 이름이 제거되고 `APP_NAME` 상수를 사용해야 함.

## 참고 자료 (References)
- `src/lib/constants.ts`
- `grep "Alpha-Sam" src/` 결과 활용
