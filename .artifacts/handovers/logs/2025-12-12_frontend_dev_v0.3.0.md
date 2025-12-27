# Handovers: To Frontend Developer

## 날짜
2025-12-12

## 현재 상황 (Context)
- Backend에서 v0.3.0 기능(User Settings API, Real-time Price Logic) 구현이 완료되었습니다.
- 이제 Frontend에서 해당 기능을 사용자가 이용할 수 있도록 UI를 구성해야 합니다.

## 해야 할 일 (Tasks)

### 1. User Settings 페이지 구현
- **경로**: `/settings` (Navbar에 링크 추가)
- **디자인 가이드**:
  - **Profile Settings**: 현재 닉네임 표시 및 수정(Input + Save Button). `PUT /api/v1/users/me` 호출.
  - **Security Settings**: 비밀번호 변경(Current PW, New PW, Confirm PW). `POST /api/v1/users/password` 호출.
- **참고**: `.artifacts/prompts/projects/alpha_sam/user_settings_design.md`

### 2. Real-time Price 연동 확인
- Backend가 이제 랜덤 값이 아닌 실제 마켓 데이터를 반환합니다 (`yfinance`).
- **Dashboard/Assets 페이지**:
  - 자산의 현재가(Latest Price)와 평가액(Valuation)이 실제 데이터 기반으로 잘 나오는지 확인.
  - (선택사항) "Latest Update" 시간 표시 형식 개선.

### 3. API Client 업데이트
- `src/lib/api.ts`에 사용자 정보 수정 및 비밀번호 변경 관련 함수 추가.
  - `updateUserProfile(payload: { nickname?: str, email?: str })`
  - `changePassword(payload: { current_password: str, new_password: str })`

## 기대 산출물 (Expected Outputs)
- 동작하는 `/settings` 페이지.
- 실제 데이터가 연동된 대시보드.


## Execution Result
- Verified User Settings Page () implementation.
- Verified API and Store logic.
- Added Tooltip for 'Latest Update' time in Assets table.
- Handed over to QA.
