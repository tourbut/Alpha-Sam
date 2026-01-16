# Handovers: To Frontend Developer

## 날짜
- 2026-01-15

## 현재 상황 (Context)
- 현재 프로젝트 테마는 `app.css`에서 **"Trusted Professional"** 스타일(Rich Cerulean Blue #2774AE, Montserrat 폰트)을 기반으로 구성되어 있습니다.
- 코디네이터가 `.kombai/resources/theme-preview-fintech.html` 파일을 참고 테마로 지정했습니다.
- 해당 테마 프리뷰 파일에는 3가지 테마 옵션이 있으며, **Option 1 (Trusted Professional)** 이 현재 우리 앱과 가장 일치합니다.
- 전반적인 UI 레이아웃과 컴포넌트 스타일을 테마 프리뷰에 맞게 리팩토링이 필요합니다.

## 해야 할 일 (Tasks)

### Phase 1: 레이아웃 구조 개선

1. **사이드바 네비게이션 도입 검토**
   - 현재: 상단 Navbar만 사용 중 (`AppNavbar.svelte`)
   - 테마 참고: 대시보드에서 **좌측 사이드바 + 우측 메인 콘텐츠** 레이아웃 사용
   - 작업: 대시보드 페이지(`/routes/+page.svelte`)에 2-컬럼 레이아웃 적용 고려
     - 선택 1: 기존 상단 Navbar 유지하면서 대시보드 내부에만 사이드바 패널 추가
     - 선택 2: 인증된 페이지 전체에 사이드바 레이아웃 적용 (대규모 변경)
   - **권장**: 선택 1로 시작 (대시보드 내부 사이드 패널)

2. **컨테이너 최대 너비 설정**
   - 테마 참고: `max-width: 1400px`
   - 현재 `container mx-auto` 사용 중
   - 작업: Tailwind 설정 또는 인라인으로 `max-w-[1400px]` 적용 확인

### Phase 2: 카드 컴포넌트 스타일 개선

3. **Stat Cards 스타일 강화**
   - 테마 참고 스타일:
     ```css
     background: var(--bg-secondary);
     border: 1px solid var(--border-color);
     border-radius: 8px;
     padding: 24px;
     box-shadow: var(--shadow-sm);
     transition: all 0.2s;
     /* hover 시 */
     box-shadow: var(--shadow-md);
     border-color: var(--primary-500);
     ```
   - 작업: 대시보드의 Stat Card들이 위 스타일과 일치하는지 확인 및 조정
   - 특히 **hover 효과** (shadow 증가, border 색상 변경) 적용

4. **카드 타이틀 스타일**
   - 테마 참고:
     ```css
     font-size: 14px;
     font-weight: 600;
     color: var(--text-secondary);
     text-transform: uppercase;
     margin-bottom: 8px;
     ```
   - 작업: `card-title` 스타일 클래스 추가 또는 기존 스타일 조정

5. **카드 값(Value) 스타일**
   - 테마 참고:
     ```css
     font-size: 32px;
     font-weight: 700;
     color: var(--primary-600);
     margin-bottom: 12px;
     ```
   - 작업: 주요 숫자값에 primary 색상과 bold 강조 적용

### Phase 3: 테이블 스타일 개선

6. **테이블 컨테이너 스타일**
   - 테마 참고:
     ```css
     background: var(--bg-secondary);
     border: 1px solid var(--border-color);
     border-radius: 8px;
     overflow: hidden;
     ```
   - 작업: Positions, Transactions 등 테이블 페이지의 테이블 컨테이너 스타일 통일

7. **테이블 헤더 스타일**
   - 테마 참고:
     ```css
     background: var(--bg-tertiary);
     padding: 16px;
     font-size: 12px;
     font-weight: 600;
     text-transform: uppercase;
     color: var(--text-secondary);
     ```
   - 작업: 테이블 `th` 요소에 위 스타일 적용

8. **테이블 행 hover 효과**
   - 테마 참고: `tr:hover { background: var(--bg-tertiary); }`
   - 작업: 테이블 행에 hover 배경색 효과 추가

### Phase 4: 뱃지 및 상태 표시 개선

9. **Performance 뱃지 스타일**
   - 테마 참고:
     ```css
     display: inline-block;
     padding: 4px 12px;
     border-radius: 20px;
     font-size: 12px;
     font-weight: 600;
     /* positive */
     background: rgba(46, 139, 87, 0.1);
     color: var(--accent-500);
     /* negative */
     background: rgba(255, 107, 107, 0.1);
     color: var(--accent-500);
     ```
   - 작업: PnL, 수익률 표시 뱃지에 위 스타일 적용

### Phase 5: 버튼 스타일 통일

10. **버튼 기본 스타일 확인**
    - 테마 참고:
      ```css
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s;
      ```
    - 작업: `app.css`의 `.btn-primary`, `.btn-secondary` 등이 위 스타일과 일치하는지 확인

### Phase 6: 네비게이션 아이템 스타일

11. **Nav Item 스타일 (사이드바/메뉴용)**
    - 테마 참고:
      ```css
      padding: 12px 16px;
      margin-bottom: 8px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      color: var(--text-secondary);
      transition: all 0.2s;
      /* hover */
      background: var(--bg-tertiary);
      color: var(--text-primary);
      /* active */
      background: var(--primary-600);
      color: white;
      ```
    - 작업: 네비게이션 메뉴 아이템에 위 스타일 적용

## 기대 산출물 (Expected Outputs)

1. **수정될 파일들**:
   - `frontend/src/app.css` - 필요시 추가 유틸리티 클래스
   - `frontend/src/routes/+page.svelte` - 대시보드 레이아웃 개선
   - `frontend/src/routes/positions/+page.svelte` - 테이블 스타일 개선
   - `frontend/src/routes/transactions/+page.svelte` - 테이블 스타일 개선
   - `frontend/src/lib/components/common/AppNavbar.svelte` - 필요시 스타일 조정

2. **완료 후 상태**:
   - 대시보드가 테마 프리뷰(`theme-preview-fintech.html`)의 Option 1 스타일과 유사하게 보여야 함
   - 카드, 테이블, 뱃지 등 주요 컴포넌트가 일관된 디자인 시스템을 따름
   - hover/active 상태에서 적절한 시각적 피드백 제공

## 참고 자료 (References)

- `.kombai/resources/theme-preview-fintech.html` - **핵심 참고 파일**
  - 브라우저에서 열어서 3가지 테마와 다크모드를 직접 확인 가능
- `.artifacts/projects/tech_stack.md` - 기술 스택 정보
- 현재 테마 설정: `frontend/src/app.css`

## 우선순위 노트

- 현재 구현된 "Trusted Professional" 색상 팔레트는 유지
- 레이아웃 구조보다는 **컴포넌트 스타일 일관성**에 먼저 집중
- 큰 변경(사이드바 레이아웃 전환 등)은 별도 피처 브랜치에서 진행 권장
