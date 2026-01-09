# Handovers: To Frontend Developer

## 날짜
- 2026-01-03

## 현재 상황 (Context)
- v1.0.0 QA 검증 결과, **UX Issue**가 보고되었습니다.
- "Add Asset" 모달에서 이미 존재하는 심볼을 입력했을 때, 사용자가 겪는 경험이 매끄럽지 않습니다. (단순 에러 메시지 노출)

## 해야 할 일 (Tasks)
1. **중복 자산 처리 UX 개선**
   - `frontend/src/routes/assets/+page.svelte` (또는 관련 컴포넌트)
   - 자산 생성 시 "이미 존재하는 자산" 오류(400 Bad Request 등)가 발생하면, 사용자에게 "이미 존재하는 자산입니다. 포지션을 추가하시겠습니까?" 와 같은 안내를 제공하거나, 해당 자산의 'Add Position' 모달을 바로 띄워주는 흐름으로 개선하십시오.

2. **백엔드 수정 사항 대기 및 확인**
   - 백엔드 개발자가 `/api/v1/positions/` 엔드포인트를 복구할 예정입니다.
   - 복구 후 프론트엔드의 자산 추가/포지션 추가 기능이 정상 동작하는지 최종 확인하십시오.

## 기대 산출물 (Expected Outputs)
- 개선된 "Add Asset" 에러 핸들링 UI.

## 참고 자료 (References)
- `.artifacts/projects/qa_reports/unit_consistency_check_v1.0.0.md` (UX Issue 항목)
