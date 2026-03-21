# Handovers: To Frontend Dev

## 날짜
- 2026-03-12

## 브랜치 (Version Control)
- `develop`

## 현재 상황 (Context)
- 포트폴리오의 자산 목록(`AssetTable.svelte`)과 개별 자산의 거래 내역(`routes/portfolios/[id]/assets/[assetId]/+page.svelte`)에서 각각 Flowbite Svelte의 Table 컴포넌트를 사용하여 데이터를 표시하고 있습니다.
- 정렬 로직, 테이블 헤더 구성, 테이블 바디 렌더링 등의 비슷한 스크립트(로직)가 중복으로 발생하고 있습니다.
- 사용자 요청에 따라 테이블을 구성하는 핵심 스크립트와 마크업을 별도의 완전한 공용 컴포넌트(예: `DataTable.svelte`)로 만들고, 자산 목록과 거래 내역 화면 모두에서 이 공용 컴포넌트를 사용하여 테이블을 구성해야 합니다.

## 해야 할 일 (Tasks)
1. 제네릭한 데이터 테이블 컴포넌트(`frontend/src/lib/components/common/DataTable.svelte`)를 생성.
   - 데이터 배열과 컬럼 정의(헤더명, 정렬키, 데이터 추출 방식 등) 배열을 prop으로 받도록 설계.
   - 내부에 포함된 기본 정렬(sorting) 로직과 오름차순/내림차순 아이콘 표시 로직을 이 컴포넌트 안에 캡슐화.
   - Svelte 5의 `{#snippet}` 기능을 활용하여 각 컬럼의 특정 렌더링 방식(커스텀 셀)을 주입받을 수 있도록 구성.
2. 기존에 분리했던 `frontend/src/lib/components/portfolio/AssetTable.svelte`를 수정하여, 내부에서 직접 `Table`을 그리지 않고 새로 만든 `DataTable.svelte` 컴포넌트를 활용하도록 리팩토링.
3. `frontend/src/routes/portfolios/[id]/assets/[assetId]/+page.svelte` 내부의 트랜잭션(거래내역) 테이블 역시 직접 렌더링하는 대신 `DataTable.svelte`를 활용하도록 교체 (현금 자산/일반 자산 카테고리에 따른 컬럼 분기 처리 포함).
4. Svelte check (`npm run check`) 및 컴파일 에러 발생 여부 확인 후 단위 테스트 처리.

## 기대 산출물 (Expected Outputs)
- 재사용성이 극대화된 통합 컴포넌트 파일이 생성됨 (`src/lib/components/common/DataTable.svelte`).
- `AssetTable.svelte`와 `[assetId]/+page.svelte` 양쪽 모두에서 기존 복잡한 정렬 로직과 `TableHead`, `TableBody` 보일러플레이트가 제거되고 `DataTable` 컴포넌트 하나로 통일됨.

## 참고 자료 (References)
- `frontend/src/lib/components/portfolio/AssetTable.svelte`
- `frontend/src/routes/portfolios/[id]/assets/[assetId]/+page.svelte`
