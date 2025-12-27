# Handovers: To Frontend Developer

## 날짜
2025-12-17

## 현재 상황 (Context)
Backend에서 **v0.7.0 (Multi-tenancy & Notifications)** 을 위한 DB 스키마 수정(owner_id 추가)과 이메일 인프라 구축을 완료했습니다.
이제 프론트엔드에서 사용자별 포트폴리오를 구분하여 보여주고, 알림 설정을 할 수 있는 UI를 계획해야 합니다.

## 해야 할 일 (Tasks)
1. **v0.7.0 UI 기획 (`v0.7.0_frontend_plan.md`)**:
   - 로그인/회원가입은 현재 범위 밖(v0.8.0 예정)일 수 있으나, 현재 "Default User" 또는 "Switch User" 시뮬레이션 방법이 필요한지 검토.
   - (중요) 현재 UI는 모든 자산을 다 보여주는데, 내 자산만 필터링해서 보여주는 로직이 필요한지 확인.
   - 이메일 알림 설정을 위한 UI (내 정보 페이지 등) 구상.

2. **계획 리뷰 요청**:
   - 작성된 기획안을 사용자에게 리뷰 요청하십시오.

## 참고 자료 (References)
- `.artifacts/docs/v0.7.0_specs.md`
- Backend implementation logs

---
## 작업 완료 로그 (2025-12-20)
- **v0.7.0 Frontend Plan 작성 완료**: `v0.7.0_frontend_plan.md` 생성.
- **Dev User Switcher 구현**: `src/lib/stores/devUser.ts`, `src/lib/components/DevUserSwitcher.svelte` 추가 및 `+layout.svelte` 연동.
- **Notification Settings UI 구현**: `src/routes/settings/+page.svelte`에 알림 설정 섹션 추가 (Mock API 연동).
- **Multi-tenancy Support**: `src/lib/api.ts`에 `X-User-Id` 헤더 추가 및 `Asset` 목록에서 Global/Private 배지 구분 (`src/routes/assets/+page.svelte`).
# Handovers: To Frontend Developer

## 날짜
2025-12-20

## 현재 상황 (Context)
- 백엔드에서 `/api/v1/users/me/settings` 및 `X-User-Id`를 이용한 멀티테넌시 로직 구현이 완료되었습니다.
- 프론트엔드에서는 Mock 데이터를 제거하고 실제 API와 연동하여 기능을 마무리해야 합니다.

## 해야 할 일 (Tasks)
1. **Mock API 제거 및 실서버 연동**
   - `src/lib/api.ts` 또는 각 컴포넌트에서 사용 중인 Mock 로직을 제거하세요.
   - 실제 백엔드 엔드포인트(`/api/v1/users/me/settings`)를 호출하여 알림 설정(Toggle)이 DB에 저장되고 로드되는지 확인하세요.
2. **단위/컴포넌트 테스트 완성**
   - `UserSwitcher`가 변경될 때 `localStorage` 저장 및 API 호출 시 `X-User-Id` 헤더가 정상적으로 포함되는지 Vitest로 검증하세요.
3. **Asset Badge UI 최종 점검**
   - `AssetRead` 스키마의 `owner_id` 존재 여부에 따라 "Global" / "Private" 배지가 정확히 랜더링되는지 확인하세요.

## 기대 산출물 (Expected Outputs)
- 백엔드와 완전히 연동된 `/settings` 페이지.
- `src/lib/components/UserSwitcher.test.ts` 및 관련 테스트 결과물.

## 참고 자료 (References)
- `v0.7.0_implementation_plan.md`
- `v0.7.0_frontend_plan.md`
- Backend API Docs (Swagger)
