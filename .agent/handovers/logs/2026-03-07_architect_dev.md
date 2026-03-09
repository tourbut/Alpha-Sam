# Handovers: To Architect

## 날짜
- 2026-03-07

## 브랜치
- `feature/arch-parser-engine`

## 현재 상황
- 현재 토스증권 PDF 전용 업로드 API가 구현되어 있으나, 여러 증권사로 확장할 예정입니다.
- 공통 거래내역 양식(Common Format)을 정의하고, 각 증권사 PDF 업로드 시 이를 해당 양식으로 변환하는 **파서 엔진(Parser Engine)** 아키텍처 도입이 필요합니다. 
- 변환 스크립트는 향후 새 증권사가 추가될 때마다 엔진에 손쉽게 플러그인(Plug-in) 형태로 꽂아 넣을 수 있도록 하여 점진적으로 발전하는 구조를 목표로 합니다.

## 해야 할 일
1. **공통 거래내역 양식 설계**: 증권사에 구애받지 않고 사용할 표준 거래내역 데이터 스키마 (DTO 및 CSV/Excel 템플릿용 구조) 정의.
2. **파서 엔진 아키텍처 설계**: 
   - 팩토리/전략 패턴 등을 활용하여 증권사별 파서 스크립트를 독립된 모듈로 쉽게 추가/관리할 수 있는 구조 설계.
   - `BaseParser` 인터페이스 정의 및 템플릿.
3. 구현될 아키텍처에 맞추어 기존 코드를 어떻게 재편할지 백엔드 작업 지침 구체화.

## 기대 산출물
- `app/src/schemas/transaction_common.py` 등 표준 거래내역 스키마 정의서.
- `app/src/services/parsers/base.py` 등 엔진 코어 아키텍처 설계.
- 전체 리팩토링 가이드.

## 참고 자료
- 기존 `TossParserService` (app/src/services/toss_parser_service.py)
