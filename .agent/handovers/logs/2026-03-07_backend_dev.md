# Handovers: To Backend Developer

## 날짜
- 2026-03-07

## 브랜치
- `feature/backend-parser-engine`

## 현재 상황
- 아키텍트의 설계에 따라, 기존 단일 토스증권 파서에서 벗어나 **공통 거래내역 포맷과 파서 엔진 시스템**을 구현해야 합니다.
- 파일 업로드는 1) 공통 양식 파일(변환 없음) 또는 2) 특정 증권사 PDF 파일(엔진이 공통 양식으로 변환) 두 가지 형태로 진행됩니다.

## 해야 할 일
1. Architect가 설계한 표준 인터페이스(`BaseParser` 등)를 기반으로 파서 엔진 디렉토리(`app/src/services/parsers/`)를 구성.
2. 기존 `TossParserService`를 엔진의 플러그인 형태(`toss_parser.py`)로 리팩토링.
3. 업로드 API(`POST /api/v1/portfolios/upload`) 통합 및 리팩토링:
   - `provider` 또는 `format` 파라미터를 받아 (예: "common", "toss", "kiwoom" 등) 적절한 파서 전략을 런타임에 결정하여 변환 처리.
   - 공통 양식 포맷인 경우 변환 없이 바로 파싱 및 포트폴리오 적재 처리 로직 구현.
4. 통합 과정에서 변경된 로직에 맞춰 서비스 및 API 단위 테스트 업데이트.

## 기대 산출물
- 플러그인 확장이 용이한 파서 엔진 폴더 구조 및 코드.
- 확장 가능한 통합 업로드 엔드포인트 API (`routes/portfolios.py` 내).
- 관련 테스트 코드 정상 통과.

## 참고 자료
- `to_architect.md`에서 도출된 설계 산출물.
