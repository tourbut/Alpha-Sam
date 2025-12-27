# Handovers: To QA Tester

## 날짜
2025-12-08

## 현재 상황 (Context)
- 백엔드 마이그레이션 적용 완료.
- 프론트엔드 API 연동 설정(Vite Proxy) 확인 완료.
- 이제 실제 브라우저에서 통합 테스트를 수행할 준비가 되었습니다.

## 해야 할 일 (Tasks)
1. **웹페이지 접속 테스트**:
   - `http://localhost:5173/assets` 접속.
2. **기능 검증**:
   - 자산 목록이 (빈 상태라도) 정상적으로 로딩되는지 확인.
   - "Add Asset" 버튼을 눌러 새 자산(예: BTC)을 추가해보고, 리스트에 반영되는지 확인.
3. **버그 리포팅**:
   - 에러 발생 시 브라우저 콘솔 로그와 네트워크 탭을 캡처하여 보고.

## 기대 산출물 (Expected Outputs)
- 테스트 결과 리포트 (성공/실패).

## 참고 자료 (References)
- `handovers/logs/2025-12-08_backend_dev_01.md`
- `handovers/logs/2025-12-08_frontend_dev_01.md`
