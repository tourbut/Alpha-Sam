# QA Test Report: Position Logic & Short-Selling Constraints

**Date**: 2026-02-22
**Tester**: QA Agent
**Branch**: `release`

## 1. Overview
The purpose of this test was to verify the frontend and backend integration regarding the new `Position` calculation logic. Specifically, testing that the portfolio real-time updates function correctly and that short-selling (selling more than the owned quantity) is properly blocked.

## 2. Test Environment
- Local dev server for frontend and backend API.
- Test User: `qa_tester_3@test.com`

## 3. Test Execution Results

| Test Case | Description | Result | Comments |
| :--- | :--- | :--- | :--- |
| **TC-1** | 매수 (BUY) 트랜잭션 반영 | **PASS** | `BUY` 트랜잭션을 추가했을 때, 해당 에셋의 보유 수량(`Quantity`)이 즉각적으로 증가하고 총 평가 가치(`Total Value`)가 갱신되는 것을 확인했습니다. |
| **TC-2** | 매도 (SELL) 트랜잭션 반영 | **PASS** | 잔고 한도 내의 `SELL` 트랜잭션을 승인 시, 보유 수량이 정상적으로 즉각 차감됨을 UI상에서 확인했습니다. |
| **TC-3** | 공매도 초과 차단 방지 정책 확인 | **PASS** | 보유 수량보다 큰 값을 `SELL` 하려 시도 시, 백엔드에서 에러를 던지고 UI의 트랜잭션 모달 최상단에 붉은색 `Alert` ("Insufficient quantity to sell")가 렌더링되며 등록이 차단됨을 확인했습니다. |
| **TC-4** | 삭제(Delete) 롤백 검증 | **PASS** | **[Bug Fixed]** 최초 UI에서 `Delete` 휴지통 버튼 누락 및 오작동(Edit 모달 진입) 현상이 발견되었으나, 핫픽스로 수정 후 테스트를 완료했습니다. 삭제 후 정상적으로 기존 수량으로 롤백됨을 확인했습니다. |

## 4. Other Identified Bugs
- **Infinite Loading Spinner Issue (Fixed)**: 
  포트폴리오에 등록된 자산이 없어 `total_value` 필드 등이 `null`로 내려올 때, Svelte 스토어 내에서 `.toLocaleString()` 메서드 호출 시 `TypeError`가 발생해 화면이 멈추는(무한 스피너) 이슈가 있었습니다. 프론트엔드 모델에서 `null`을 `0`으로 처리하도록 수정(Data parser)하여 버그를 완벽히 해결했습니다.
- **Transaction Table Delete Icon (Fixed)**:
  `Action` 컬럼에 삭제 아이콘이 누락되어 있어 수동으로 추가하고 백엔드 API와 바인딩을 마쳤습니다.

## 5. Conclusion
`Position` 실시간 계산 및 초과 매도 제약 기능에 대한 E2E 시나리오 테스트 결과 전원 합격(Pass) 판정을 내립니다. 발견된 UI 렌더링 사이드 이펙트(Spinner hang)와 삭제 버튼 누락 버그 역시 성공적으로 픽스되었습니다. 기능 안전성을 공식적으로 검증하였습니다.
