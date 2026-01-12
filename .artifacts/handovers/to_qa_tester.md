# Handovers: To QA Tester

## 날짜
- 2026-01-11

## 현재 상황 (Context)

Position 모델을 DB에서 완전히 제거하고, Transaction을 집계하여 실시간으로 Position을 계산하는 방식으로 리팩토링이 진행되었습니다. 이는 데이터 일관성을 높이고 중복을 제거하기 위한 구조적 변경입니다.

주요 변경 사항:
- Position CRUD API 제거 (사용자가 Position을 직접 생성/수정/삭제 불가)
- Transaction 추가를 통한 간접적인 Position 관리
- Portfolio Summary 및 Positions 조회 API는 유지되나, Transaction 집계 결과를 반환

## 해야 할 일 (Tasks)

### 1. Backend API 테스트

#### 1.1 Transaction CRUD 기능 검증
1. **Transaction 생성 (BUY)**
   - Endpoint: `POST /api/portfolios/{portfolio_id}/transactions`
   - 시나리오:
     - 정상 BUY Transaction 추가
     - Asset이 존재하지 않는 경우 에러 확인
   - 기대 결과:
     - 201 Created 응답
     - Transaction 데이터 정확하게 저장됨

2. **Transaction 생성 (SELL)**
   - 시나리오:
     - 보유 수량 범위 내 SELL → 성공
     - 보유 수량 초과 SELL → 400 Bad Request 에러
     - Position이 없는 Asset SELL → 400 Bad Request 에러
   - 기대 결과:
     - 유효한 SELL만 성공
     - 에러 메시지가 명확하게 반환됨

#### 1.2 Position 계산 로직 검증
1. **Portfolio Summary 조회**
   - Endpoint: `GET /api/portfolios/summary`
   - 시나리오:
     - Transaction 없음 → 빈 positions 배열 반환
     - BUY만 있음 → 수량, 평단가 정확성 확인
     - BUY + SELL 혼합 → 수량 감소, 평단가 유지 확인
     - 여러 Asset의 Transaction → Asset별 독립 계산 확인
   - 기대 결과:
     - Position 데이터가 Transaction 집계 결과와 일치
     - 평가액, 손익, 수익률 계산 정확

2. **Portfolio Positions 조회**
   - Endpoint: `GET /api/portfolios/{portfolio_id}/positions`
   - 기대 결과:
     - Portfolio Summary와 동일한 Position 데이터 반환

#### 1.3 Position CRUD API 제거 확인
1. Position 생성/수정/삭제 API 호출 시 404 Not Found 반환 확인

### 2. Frontend UI/UX 테스트

#### 2.1 Dashboard 페이지
1. **Portfolio Summary 표시**
   - URL: `/`
   - 시나리오:
     - 로그인 후 Dashboard 로딩
     - Transaction 추가 후 Dashboard 새로고침
   - 기대 결과:
     - 총 평가액, 손익, 수익률 정확하게 표시
     - Position 목록이 최신 Transaction 반영

#### 2.2 Assets 페이지
1. **Transaction 추가 기능**
   - URL: `/assets`
   - 시나리오:
     - "Add Transaction" 버튼 클릭 → Modal 열림
     - Asset 선택, BUY/SELL 선택, 수량/가격 입력
     - Transaction 추가 성공 → Modal 닫힘, Position 자동 업데이트
   - 기대 결과:
     - Transaction Modal이 정상 작동
     - Transaction 추가 후 UI가 자동으로 최신 Position 반영
     - 에러 발생 시 (예: SELL 수량 초과) 명확한 에러 메시지 표시

2. **Position 직접 수정/삭제 기능 제거 확인**
   - 기대 결과:
     - "Edit Position", "Delete Position" 버튼이 없음

#### 2.3 Positions 페이지
1. **읽기 전용 Position 목록**
   - URL: `/positions`
   - 기대 결과:
     - Position 목록이 정확하게 표시됨
     - 수정/삭제 버튼이 없음 (읽기 전용)

### 3. 데이터 일관성 테스트

#### 3.1 Multi-Transaction 시나리오
1. **복잡한 Transaction 시퀀스**
   - 시나리오:
     - Asset A에 대해: BUY 10개 @$100 → BUY 5개 @$120 → SELL 7개 @$110
   - 검증:
     - 최종 수량: 8개
     - 평단가: (10*100 + 5*120) / 15 = $106.67
     - SELL 후 평단가 유지 확인
   - 기대 결과:
     - Position 계산이 정확함

#### 3.2 Edge Cases
1. **수량 0인 Position**
   - 시나리오: BUY 10개 → SELL 10개
   - 기대 결과: Position 목록에 나타나지 않거나 수량 0으로 표시

2. **동시 Transaction 추가** (동시성 테스트, 선택 사항)
   - 시나리오: 같은 Asset에 대해 두 개의 Transaction 거의 동시에 추가
   - 기대 결과: 모든 Transaction이 반영되고, Position 계산 정확

### 4. 성능 테스트

1. **많은 Transaction이 있는 Portfolio**
   - 시나리오: 100개 이상의 Transaction이 있는 Portfolio Summary 조회
   - 측정: API 응답 시간
   - 기대 결과: 2초 이내 응답 (목표치, 조정 가능)

2. **여러 Asset의 많은 Transaction**
   - 시나리오: 10개 Asset에 각각 20개씩 Transaction
   - 기대 결과: 성능 저하 없이 정상 작동

### 5. Regression 테스트

1. **기존 기능 영향 확인**
   - 로그인/로그아웃
   - Asset 생성/조회
   - Portfolio 생성/조회
   - Price 데이터 조회
   - 기대 결과: 모든 기존 기능 정상 작동

### 6. Database Migration 검증

1. **Migration 실행 확인**
   ```bash
   cd backend
   alembic upgrade head
   ```
   - 기대 결과: 에러 없이 완료, `positions` 테이블 삭제됨

2. **Downgrade 테스트** (선택 사항)
   ```bash
   alembic downgrade -1
   ```
   - 기대 결과: `positions` 테이블 재생성 (데이터 없음)

3. **Production Migration 시뮬레이션**
   - 기존 데이터가 있는 DB에서 Migration 실행
   - 기대 결과: Position 데이터 삭제되지만, Transaction 데이터는 유지되며 Position 재계산 가능

## 기대 산출물 (Expected Outputs)

1. **QA Report 작성**
   - 파일: `.artifacts/projects/qa_reports/position_refactoring_qa_report.md`
   - 포함 내용:
     - 테스트 시나리오별 결과 (Pass/Fail)
     - 발견된 버그 목록 및 재현 방법
     - 성능 측정 결과
     - 권장 사항

2. **버그 리포트** (버그 발견 시)
   - GitHub Issue 생성
   - 라벨: `bug`, `position-refactoring`
   - 상세한 재현 방법 및 스크린샷 첨부

3. **검증 완료 확인**
   - 모든 주요 시나리오 Pass
   - Critical 버그 없음
   - 성능 목표치 달성

## 참고 자료 (References)

- [구현 계획서](file:///Users/shin/.gemini/antigravity/brain/0d719204-f57d-41e6-aeb4-d97c45e699c6/implementation_plan.md)
- [작업 체크리스트](file:///Users/shin/.gemini/antigravity/brain/0d719204-f57d-41e6-aeb4-d97c45e699c6/task.md)
- [프로젝트 컨텍스트](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.artifacts/projects/context.md)
- [Domain Rules](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.artifacts/projects/domain_rules.md)
- [Debug Commands](file:///Users/shin/.gemini/antigravity/brain/0d719204-f57d-41e6-aeb4-d97c45e699c6/.agent/rules/debug.md)
