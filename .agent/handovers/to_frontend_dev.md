# Handovers: To Frontend Developer

## 날짜
- 2026-01-30

## 브랜치
- feature/portfolio-currency-select

## 현재 상황
- 포트폴리오 생성 모달(`CreatePortfolioModal.svelte`)에서 통화(Currency)가 "USD"로 고정된 비활성화된 텍스트 입력필드로 되어 있습니다.
- 사용자가 다양한 통화를 선택할 수 있어야 합니다.

## 해야 할 일
1. `frontend/src/lib/components/portfolio/CreatePortfolioModal.svelte` 파일 수정.
2. `flowbite-svelte`에서 `Select` 컴포넌트 임포트.
3. 주요 통화 목록 정의 (`USD`, `KRW`, `EUR`, `JPY`, `CNY`, `GBP`).
4. 기존 `Input` 컴포넌트를 `Select` 컴포넌트로 교체하고 `currency` 변수와 바인딩.
5. `USD`와 `KRW`는 필수적으로 포함.

## 기대 산출물
- 포트폴리오 생성 시 사용자가 콤보 박스를 통해 통화를 선택할 수 있음.
