# QA Result Report: v0.2.0 (Asset Loading Issue)

**Date:** 2026-01-23
**Tester:** QA Agent

## 1. 요약
- **테스트 대상**: 포트폴리오 상세 페이지 자산(Positions) 로딩 기능.
- **결과**: **FAIL**
- **원인**: Backend API (`GET /api/v1/portfolios/{portfolio_id}/positions`) 구현 오류.

## 2. 세부내용

### 2.1 Issue Reproduction (버그 재현)
- **절차**:
  1. `http://localhost:5173/portfolios` 접속.
  2. 임의의 포트폴리오 클릭.
- **관찰 결과**:
  - 자산 목록이 표시되지 않음.
  - 붉은색 에러 배너 표시: `Error! [{"type":"missing","loc":["query","x"],"msg":"Field required","input":null}]`
  - Browser Console 및 Network 탭에서 `422 Unprocessable Entity` 에러 확인.

### 2.2 API Analysis (원인 분석)
- **Request**: `GET /api/v1/portfolios/{uuid}/positions`
- **Response**: `422 Unprocessable Entity` (`x` query parameter missing)
- **Code Review**: `backend/app/src/routes/portfolios.py` 파일의 `read_portfolio_positions` 함수에서 파라미터 정의 오류 발견.
  ```python
  # Current Code (Bug)
  @router.get("/{portfolio_id}/positions", ...)
  async def read_portfolio_positions(
      x: uuid.UUID,  # <--- Error: 'x' variable name used instead of 'portfolio_id'
      ...
  )
  ```
  - Path Parameter는 `{portfolio_id}`이나, 함수 인자는 `x`로 정의되어 있어 FastAPI가 `x`를 필수 Query Parameter로 인식함.

## 3. 결론 및 조치사항
- **결론**: Backend 코드 수정 필요.
- **조치**: 
  - Backend 개발자에게 수정 요청 (Handovers 업데이트).
  - 수정 후 재검증 필요.
