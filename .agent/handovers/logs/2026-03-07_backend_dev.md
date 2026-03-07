# Handovers: To Backend Developer

## 날짜
- 2026-03-07

## 브랜치
- `feature/backend-pdf-upload`

## 현재 상황
- 샌드박스에서 파이썬 스크립트(`sandbox/import_toss_portfolio.py`)를 통해 토스증권 거래내역서 PDF(`sandbox/토스증권_거래내역서.pdf`)를 성공적으로 파싱하고 DB에 포트폴리오를 생성하여 45건의 거래 내역을 저장하는 테스트를 완료했습니다.
- 이제 이 로직을 프로덕션 백엔드 코드에 통합하여 클라이언트에서 PDF를 업로드하면 자동으로 거래내역이 반영되는 기능을 개발해야 합니다.

## 해야 할 일
1. `pdfplumber` 등 필요한 의존성을 백엔드 패키지 매니저(`pyproject.toml` 또는 `uv.lock`)에 추가하세요.
2. `POST /api/v1/portfolios/upload/toss` 형태의 새로운 FastAPI 엔드포인트를 구현하여 PDF 파일 업로드를 받으세요.
3. `sandbox/import_toss_portfolio.py`의 파싱 로직(`parse_pdf`, `guess_ticker` 등)을 적절한 서비스(Service) 계층 또는 유틸리티 모듈로 이관 및 리팩토링하세요.
4. 파싱된 데이터를 사용하여 `Portfolio`, `Asset`, `Transaction` 정보를 DB에 삽입하는 비즈니스 로직을 구성하세요. 
5. 해당 기능에 대한 단위 테스트를 작성하세요.

## 기대 산출물
- PDF 업로드를 처리하고 파싱을 통해 DB에 포트폴리오/거래내역을 적재하는 API 엔드포인트 코드가 생성되어야 합니다.
- 관련 테스트 코드가 작성되고 모두 통과해야 합니다.

## 참고 자료
- `sandbox/import_toss_portfolio.py`
- `sandbox/토스증권_거래내역서.pdf`
