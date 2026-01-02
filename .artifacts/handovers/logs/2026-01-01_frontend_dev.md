# Handovers: To Frontend Developer (Archived Tasks)

## 날짜
- 2026-01-01

## 현재 상황 (Context)
- 개발 서버(Node, UV) 실행 중.
- Navbar, Session 기능 구현 완료 상태에서 전반적인 UI/UX 다듬기와 리팩토링 필요.

## 해야 할 일 (Tasks)
1. **[UI Polish & Consistency]**
   - "Add Asset" 버튼 및 Navbar의 사용자 닉네임 표시 디자인이 전체 테마와 어울리는지 점검 및 스타일 개선.
   - 모바일/데스크탑 반응형 동작 확인.

2. **[Refactoring]**
   - `src/lines` 나 컴포넌트 내의 하드코딩된 값, 불필요한 `console.log` 정리.
   - Auth Store (`src/lib/stores/auth.ts`) 로직 재검토 (세션 복구 로직 최적화).

3. **[End-to-End Verification]**
   - **브라우저에서 직접 점검**:
     1. 로그인 -> 대시보드 진입 -> 새로고침 (로그인 유지 확인).
     2. 로그아웃 -> 로그인 페이지 리다이렉트 확인.
     3. Asset 추가 기능 동작 확인.
   - 에러 발생 시 사용자에게 적절한 Toast 메시지나 알림이 뜨는지 확인.

## 기대 산출물 (Expected Outputs)
- 정돈된 프론트엔드 코드 (린트/포맷팅 준수).
- 부드럽게 동작하는 세션 유지 및 로그아웃 플로우.
- 시각적으로 완성도 높은 Navbar 및 Asset 추가 버튼.


## 날짜
- 2026-01-01

## 현재 상황 (Context)
- v1.1.0 Navbar 및 Session 기능 구현 완료.
- 현재 대기 중인 작업 없음.

## 해야 할 일 (Tasks)
- (없음)

## 기대 산출물 (Expected Outputs)
- (없음)
# Handovers: To Frontend Developer

## 날짜
- 2026-01-01

## 현재 상황 (Context)
- v1.0.0 검증 결과 Critical Bug가 발견되었습니다.
- 사용자가 UI 관련 버그 수정 및 블랙 테마 기능을 추가로 요청했습니다.

## 해야 할 일 (Tasks)
1. **[Bugfix: Logout]**
   - **Issue**: Navbar의 `Logout` 버튼 클릭 시, 로그아웃 API 호출 및 페이지 리다이렉트가 동작하지 않음.
   - **Action**: `+layout.svelte` 및 `auth.ts`의 로그아웃 핸들러를 점검하고 수정. 로그아웃 후 `/login`으로 강제 이동되도록 처리.

2. **[Bugfix: UI Visibility]**
   - **Issue**: 하얀 배경일 때 `Manage Assets` 버튼이 보이지 않음 (텍스트/배경 색상 문제로 추정).
   - **Action**: 버튼 스타일을 점검하고, 배경색에 관계없이 잘 보이도록 수정 (Contrast Ratio 준수).

3. **[Feature: Dark Mode]**
   - **Request**: Navbar에 **블랙 테마(Dark Mode)** 변경 토글 버튼 추가.
   - **Action**: 
     - TailwindCSS `dark` 모드 설정 확인.
     - Navbar 우측(Logout 버튼 근처)에 테마 토글(Sun/Moon 아이콘) 버튼 구현.
     - 로컬 스토리지에 테마 설정 저장 및 로드.

## 기대 산출물 (Expected Outputs)
- 정상 동작하는 로그아웃 기능.
- 가시성이 확보된 `Manage Assets` 버튼.
- 클릭 시 앱 전체 테마가 전환되는 Dark Mode 토글 버튼.
