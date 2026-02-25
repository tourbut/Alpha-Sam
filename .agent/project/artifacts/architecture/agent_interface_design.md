# Agent-Centric Interface Design (v2.2.0)

## 1. 개요 (Overview)
AI 에이전트가 Alpha-Sam 시스템을 조작할 때, 복잡한 DOM 트리를 파싱하며 발생하는 토큰 낭비와 환각(Hallucination) 현상을 방지하기 위한 전용 진입점 및 API 제어 규격입니다.
UI 중심의 기존 플로우와 달리, **최소한의 시맨틱 HTML 인증 + JSON 기반 REST API 통신(Headless Control)** 이라는 하이브리드 방식으로 동작합니다.

## 2. 보안 및 권한 정책
- **접근 권한**: 기존 사용자 계정 인증(JWT)과 동일한 권한 수준을 따르되, User-Agent 헤더(`AlphaSam-Agent`)를 통해 에이전트 요청임을 식별 권장.
- **Rate Limit**: 에이전트의 오작동 및 무한 루프 호출 방지를 위해, 일반 사용자보다 엄격한 Rate Limit을 적용할 수 있음 (예: 분당 60회).
- **소유권(Tenancy)**: 에이전트를 통해 생성된 모든 자원(포트폴리오, 자산, 거래 내역)은 연결된 유저의 `owner_id` 제약을 그대로 적용받습니다.

## 3. 인증 플로우 (`/agent/login`)
프론트엔드 라우트에 `/agent/login` 페이지를 신설합니다.
해당 페이지는 CSS 꾸밈 요소나 중첩된 `div` 태그 없이 순수 HTML 요소로만 구성되어야 합니다.

**Flow:**
1. 에이전트가 `/agent/login` 에 접속.
2. `<form>`을 통해 이메일과 비밀번호 입력 후 Submit.
3. 백엔드 인증 성공 시, 프론트엔드는 다음 데이터를 **화면 전환 없이 평문(Plain Text)**으로 즉시 렌더링.
   - `<div id="auth-token">eyJhb...</div>`
   - `<div id="api-docs">...JSON 명세...</div>`
4. 이후 에이전트는 렌더링 된 문서를 읽고 브라우징을 멈춘 뒤, 헤더에 `Authorization: Bearer <auth-token>`을 넣고 API 직접 호출 단계로 전환.

## 4. 필수 CRUD API 명세 (JSON Endpoint Specs)

에이전트는 제공된 명세를 바탕으로 다음의 기능들을 완벽히 수행할 수 있어야 합니다.

### 4.1 포트폴리오 관리
- **목록 조회**: `GET /api/v1/portfolios`
- **생성**: `POST /api/v1/portfolios`
  - Body: `{"name": "새 포트폴리오", "description": "설명", "currency": "USD"}`
- **상세 조회**: `GET /api/v1/portfolios/{portfolio_id}`
- **삭제**: `DELETE /api/v1/portfolios/{portfolio_id}`

### 4.2 자산(Asset) 관리
- **자산 목록 조회**: `GET /api/v1/portfolios/{portfolio_id}/assets`
- **커스텀 자산/글로벌 자산 추가**: `POST /api/v1/portfolios/{portfolio_id}/assets`
  - Body: `{"symbol": "AAPL", "name": "Apple Inc.", "category": "Stock"}` 

### 4.3 거래 내역(Transaction) 관리
- **현재 포지션 및 기초 정보 조회**: `GET /api/v1/portfolios/{portfolio_id}/positions`
- **거래 내역 등록 (매수/매도)**: `POST /api/v1/transactions`
  - Body: 
    ```json
    {
      "portfolio_id": "uuid",
      "asset_id": "uuid",
      "type": "BUY",
      "quantity": 1.5,
      "price": 150.0,
      "executed_at": "YYYY-MM-DDTHH:mm:ssZ"
    }
    ```

## 5. 시스템 검증 (Verification)
- REST API 접근 시 `owner_id` 격리가 정상 동작하는지 테스트 스위트에 에이전트 전용 시나리오 추가 필요.
- 프론트엔드의 `/agent/login`이 실제로 어떠한 스타일이나 불필요한 태그를 포함하지 않음을 HTML 파싱 테스트로 검증.
