# Handovers: To Frontend Developer

## 날짜
- 2026-03-07

## 브랜치
- `feature/frontend-generic-upload`

## 현재 상황
- 백엔드에 여러 증권사 거래내역 및 공통 양식을 유연하게 지원하는 파일 파서 엔진이 도입되었습니다.
- 기존의 단일 목적 모달(`TossUploadModal.svelte`)을 여러 유형을 지원하는 범용 모달로 업데이트해야 합니다.

## 해야 할 일
1. 기존 `TossUploadModal.svelte`를 `TransactionUploadModal.svelte` 와 같이 범용적인 이름으로 변경 (파일 이동 및 import 경로 전부 수정).
2. 모달 내에 폼 요소를 추가하여 **파일 유형 / 증권사 선택기** (예: "알파샘 공통 양식", "토스증권 PDF", 기타 증권사 추가 가능형) 구현.
3. 사용자가 "알파샘 공통 양식"을 선택했을 때 다운로드 가능한 빈 CSV/Excel 양식 파일 다운로드 안내 링크/버튼 추가.
4. 사용자가 선택한 증권사(Provider) 정보를 API 호출 시 함께 실어보내도록 `uploadTossPortfolio` 함수를 범용화(`uploadPortfolioTransactions`)하고 API 옵션을 수정.

## 기대 산출물
- 유형 선택이 가능한 범용 거래내역 업로드 컴포넌트 (`TransactionUploadModal.svelte`).
- 변경된 백엔드 API 스펙(Provider 타입 동적 전송)에 맞춰 수정된 API 클라이언트 로직.

## 참고 자료
- 백엔드 업로드 API 변경 내역 스펙.
