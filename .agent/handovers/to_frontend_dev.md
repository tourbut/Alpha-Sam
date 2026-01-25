# Handovers: To Frontend Developer

## 날짜
- 2026-01-25

## 브랜치 (Version Control)
- `feature/admin-menu-link`

## 현재 상황 (Context)
- 관리자 페이지(`/admin/assets`)는 구현되었으나, UI상에서 진입할 수 있는 메뉴가 없습니다.
- 사용자는 관리자 계정일 때 메뉴에 "System Admin" 등의 링크가 보이길 원합니다.

## 해야 할 일 (Tasks)
1. **AppNavbar.svelte (`frontend/src/lib/components/common/AppNavbar.svelte`) 수정**:
   - `auth.user.is_superuser`가 true일 때만 보이는 `NavLi` 항목 추가.
   - Link: `/admin/assets` (Label: "System Admin")
2. **+layout.svelte (`frontend/src/routes/+layout.svelte`) 수정**:
   - `navItems` 배열에 관리자 전용 아이템 추가 로직 구현 (또는 템플릿에서 조건부 렌더링).
   - Sidebar에도 "System Admin" 메뉴가 superuser에게만 보이도록 처리.

## 기대 산출물 (Expected Outputs)
- 관리자로 로그인 시 상단 네비게이션과 사이드바에 "System Admin" 메뉴가 노출됨.
- 일반 사용자는 해당 메뉴가 보이지 않음.
