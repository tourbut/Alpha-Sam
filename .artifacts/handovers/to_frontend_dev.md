# Handovers: To Frontend Developer

## 날짜
- 2026-01-13

## 현재 상황 (Context)
- 대시보드 디자인 리뷰(`.kombai/resources/design-review-dashboard-1736769000.md`) 결과, 접근성 및 UX 개선 사항이 다수 발견되었습니다.
- v1.2.2 릴리즈 이후, 다음 스프린트(v1.3.0 목표)로 대시보드 고도화를 진행합니다.

## 해야 할 일 (Tasks)

### Phase 1: Accessibility & Critical Fixes (최우선)
1. **페이지 타이틀 추가**: `src/routes/+page.svelte`에 `<svelte:head>`를 사용하여 타이틀 설정.
2. **키보드 포커스 식별 강화**: 모든 버튼 및 인터랙티브 요소에 `focus:ring` 스타일 추가.
3. **ARIA 레이블 추가**: "Share", "Refresh" 등 아이콘 버튼에 `aria-label` 속성 추가.
4. **색각 이상 보조**: 수익률(PnL) 표시 시 색상 외에 `+`/`-` 심볼 또는 화살표 아이콘을 명시적으로 추가.

### Phase 2: UX Enhancements (고순위)
5. **Time Range Selecor UI**: 퍼포먼스 차트 상단에 기간 선택 버튼(1D, 1W, 1M, 3M, 1Y, ALL) 추가 (UI 구현 우선).
6. **Stat Cards 개선**:
   - 단순 수치 표시를 넘어, 전일 대비 변동폭(Trend Indicator)이나 화살표 추가.
   - 중요도에 따른 시각적 계층 구조(크기, 색상 등) 차별화.
7. **Quick Actions 확장**:
   - 기존 'Manage Assets', 'Positions' 외에 'Add Transaction', 'Import CSV(Mock)' 등 5~7개로 버튼 확장 및 아이콘 적용.
8. **Recent Activity / Insights Panel (Mock)**:
   - 대시보드 하단 또는 측면에 '최근 활동 내역' 및 'AI 인사이트' 패널 영역(Placeholder) 추가.

## 기대 산출물 (Expected Outputs)
- `src/routes/+page.svelte` 등 대시보드 관련 파일이 수정됨.
- 스크린 리더 및 키보드 네비게이션이 개선됨.
- 대시보드가 리뷰 문서의 Wireframe 제안(Time selector, Activity feed 등)과 유사한 구조를 갖춤.

## 참고 자료 (References)
- [Design Review Report](.kombai/resources/design-review-dashboard-1736769000.md)
