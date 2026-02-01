# Handovers: To Frontend Developer

## 날짜
- 2026-02-01

## 브랜치
- feature/frontend-update-ui

## 현재 상황
- 백엔드에서 자산 및 거래 내역 수정을 위한 API(`PUT`)를 개발 중입니다.
- 프론트엔드에서도 이를 지원하기 위한 UI 및 API 연동 작업이 필요합니다.

## 해야 할 일
1. **API Client 업데이트**
   - 백엔드 배포 후, 자산 수정(`updateAsset`) 및 거래 수정(`updateTransaction`) API 호출 함수 추가.

2. **UI 구현**
   - **자산 수정**:
     - 자산 목록 또는 상세 페이지에 '수정' 버튼 추가.
     - `EditAssetModal` (또는 기존 모달 재사용) 구현: 이름, 카테고리 등 수정 가능.
   - **거래 수정**:
     - 거래 내역 목록(`TransactionTable` 등)에 '수정' 버튼 추가.
     - `EditTransactionModal` 구현: 수량, 가격, 날짜, 타입 수정 가능.

3. **상태 관리**
   - 수정 완료 후 스토어(`portfolioStore` 등)에 변경 사항 반영 (리로드 또는 로컬 업데이트).

## 기대 산출물
- 사용자가 자산 및 거래 내역을 UI에서 수정할 수 있어야 함.
