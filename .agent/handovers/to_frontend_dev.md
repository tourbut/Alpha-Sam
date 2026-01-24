# Handovers: To Frontend Developer

## 날짜
- 2026-01-25

## 브랜치 (Version Control)
- `fix/portfolio-detail-ui`

## 현재 상황 (Context)
- 사용자가 포트폴리오 상세 페이지(`http://localhost:5173/portfolios/[uuid]`)에서 UI 오류를 보고했습니다.
- **증상**:
  1. 자산 목록 테이블의 컬럼 정렬이 맞지 않음.
  2. 자산명(Asset Name)이 보이지 않음.

## 해야 할 일 (Tasks)
1. **포트폴리오 상세 페이지 UI 점검**:
   - 대상 파일: `frontend/src/routes/portfolios/[id]/+page.svelte` (및 관련 컴포넌트)
   - 테이블 헤더(Header)와 본문(Body)의 컬럼 개수 및 `width` 설정이 일치하는지 확인.
   - Flowbite-Svelte 테이블 컴포넌트 사용 시 `class`나 태그 구조가 올바른지 확인.

2. **자산명 표시 오류 수정**:
   - API로부터 받아온 데이터(`portfolio.assets` 또는 관련 데이터)에 `name` 필드가 존재하는지 확인.
   - Svelte 템플릿에서 해당 필드를 올바르게 바인딩하고 있는지 확인 (`{asset.name}` 등).
   - 만약 데이터가 `undefined`라면 백엔드 응답 문제일 수 있으나, 일단 프론트엔드 코드의 키 매핑을 먼저 점검.

## 기대 산출물 (Expected Outputs)
- 포트폴리오 상세 페이지의 자산 목록 테이블이 깨지지 않고 정렬됨.
- 각 자산의 이름이 정상적으로 표시됨.

## 참고 자료 (References)
- `frontend/src/routes/portfolios/[id]/+page.svelte`
