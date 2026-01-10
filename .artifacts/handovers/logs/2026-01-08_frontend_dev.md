# Handovers: To Frontend Developer

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- 사용자로부터 **프론트엔드 코드의 컴포넌트화/리팩토링** 요청이 있었습니다.
- 특히 `src/routes/+layout.svelte`에 `Navbar` 구현이 직접 포함되어 있어, 유지보수성과 가독성을 위해 분리가 필요합니다.

## 해야 할 일 (Tasks)

### 1. Navbar 컴포넌트 분리 (우선순위 높음)
1. `src/lib/components/common/` 디렉토리를 생성합니다 (없을 경우).
2. `src/routes/+layout.svelte` 파일 내의 `Navbar` 관련 마크업과 스크립트를 추출하여 `src/lib/components/common/AppNavbar.svelte` 파일을 생성합니다.
   - `flowbite-svelte`의 `Navbar`, `NavBrand` 등 모든 import를 이동합니다.
   - `$lib/stores/auth` 관련 로직(로그인/로그아웃 상태 감지)을 새 컴포넌트에서도 잘 동작하도록 이동합니다.
   - 모바일 메뉴 토글 로직(`hidden` 상태)도 함께 이동합니다.
3. `src/routes/+layout.svelte`에서는 추출한 `<AppNavbar />` 컴포넌트를 import하여 사용하도록 코드를 간소화합니다.

### 2. (Optional) Dashboard 리팩토링 검토
- `src/routes/+page.svelte` 내의 "Quick Actions" 카드나 "Portfolio Summary" 카드 등이 너무 길다면, `src/lib/components/dashboard/` 와 같은 폴더를 만들고 분리하는 것을 고려해보세요. (이번 턴에서는 Navbar 분리가 최우선입니다.)

## 기대 산출물 (Expected Outputs)
- `src/lib/components/common/AppNavbar.svelte` 파일 생성.
- `src/routes/+layout.svelte` 파일이 대폭 줄어들고 가독성이 향상됨.
- 리팩토링 후에도 기존 네비게이션, 로그인/로그아웃, 모바일 메뉴가 **동일하게 동작**해야 함.
# Handovers: To Frontend Developer

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- 사용자 요청에 따라 **레이아웃 하단에 부유형(Floating) 챗 위젯(Mock)**을 추가하고, 더 이상 사용하지 않는 **`DevUserSwitcher` 관련 로직을 제거**해야 합니다.

## 해야 할 일 (Tasks)

### 1. DevUserSwitcher 제거
1. `src/routes/+layout.svelte`에서 `DevUserSwitcher` import 및 컴포넌트 호출(`<DevUserSwitcher />`)을 제거합니다.
2. `src/lib/components/DevUserSwitcher.svelte` 및 `src/lib/components/DevUserSwitcher.test.ts` 파일을 삭제합니다.

### 2. ChatWidget 컴포넌트 구현 (Mock)
1. `src/lib/components/chat/ChatWidget.svelte` 파일을 생성합니다.
2. **디인 및 기능 요구사항**:
   - 화면 우측 하단에 고정된(Fixed) 둥근 버튼 형태.
   - 버튼 클릭 시 채팅창(Pop-over 타입)이 열리고 닫히는 토글 기능.
   - **인증 상태 연동**: `auth.isAuthenticated`가 `true`인 경우에만 위젯을 표시합니다.
   - 채팅창 내부에는 간단한 Mock 메시지("안녕하세요! Alpha-Sam 도우미입니다 무엇을 도와드릴까요?")를 표시합니다.
   - 입력창(Input)은 마크업만 구성하고 실제 전송 로직은 Mock으로 처리(입력 시 '전송됨' 얼럿 등)합니다.

### 3. 레이아웃 적용
1. `src/routes/+layout.svelte`에 `<ChatWidget />`을 import하여 추가합니다.

## 기대 산출물 (Expected Outputs)
- `DevUserSwitcher` 제거로 인한 레이아웃 간소화.
- 로그이 시 우측 하단에 세련된 챗 위젯 아이콘 노출.
- 클리 시 채팅창이 부드럽게 나타나며 Mock 메시지가 보임.

# Handovers: To Frontend Developer

## 날짜
- 2026-01-08

## 현재 상황 (Context)
- `ChatWidget`이 Mock 형태로 구현되어 있으나, 메시지 전송 시 실제 대화 목록에 추가되지 않고 Alert만 뜨는 상황입니다.
- 사용자 요청에 따라, **전송한 메시지가 채팅창 리스트에 실제로 추가되고 보여지도록** 개선해야 합니다.

## 해야 할 일 (Tasks)
1. **상태 관리 개선**:
   - `ChatWidget.svelte` 내부에서 메시지 목록을 관리할 `$state` 배열(`messages`)을 추가합니다.
   - 각 메시지는 `{ id: number, text: string, sender: 'user' | 'bot', timestamp: Date }` 형태를 권장합니다.
2. **메시지 전송 로직 구현**:
   - 사용자가 메시지를 입력하고 전송하면:
     1. 사용자 메시지를 `messages` 배열에 추가합니다.
     2. 입력창을 비웁니다.
     3. (Mock Logic) 약 1초 뒤에 "안녕하세요! 저는 Mock 봇입니다." 같은 자동 응답 메시지를 `messages` 배열에 추가합니다.
3. **UI 렌더링 수정**:
   - 하드코딩된 채팅 내역을 제거하고, `{#each messages as msg}` 블록을 사용하여 동적으로 렌더링합니다.
   - 사용자 메시지는 오른쪽 정렬, 봇 메시지는 왼쪽 정렬로 구분합니다.

## 기대 산출물 (Expected Outputs)
- 채팅창에서 대화가 이어지는 듯한 UX가 구현된 `ChatWidget.svelte`.
