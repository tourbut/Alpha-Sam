- [2025-12-27 10:47:00] v0.7.0 알림 시스템 검증 및 강화를 완료함. 현재 대기 중인 추가 태스크 없음.
- [2025-12-28 17:50:00] FastAPI Users 도입 완료. User 모델은 int PK를 유지하며 `SQLAlchemyBaseUserTable`을 상속받도록 수정함. `X-User-Id` 헤더는 개발용으로 `deps.get_current_user`에 통합됨.
- [2025-12-29 23:35:00] QA 이슈(405 Error) 확인 결과, FastAPI Users 라우터 등록 및 설정 코드가 누락되어 있음을 발견. `users_config.py` 작성, `api.py` 라우터 등록, `User` 모델 `is_verified` 추가 후 QA 테스트(`qa_auth_api.py`) 통과함.
- [2025-12-31 15:15:00] v0.9.0 데이터 마이그레이션 스크립트 작성 완료(`scripts/migrate_v090_legacy_data.py`). `portfolio.py`의 `create_portfolio_snapshot`에서 N+1 쿼리 문제를 해결하기 위해 Bulk Fetching 로직을 적용함.
- [2025-12-31 16:50:00] v0.9.0 배포를 위해 `deps.py`(JWT 옵션), `portfolio.py`, `positions.py`, `migrations_script` 등 미커밋 변경사항을 `develop` 브랜치에 커밋 및 푸시함. Standby 상태 진입.
- [2026-01-01 17:30:00] v1.0.0 대비 Backend Refactoring 완료. `main.py`/`api.py` 라우터 정리, `AssetService` 분리(비즈니스 로직 캡슐화), `security.py` JWT 로직 중앙화, `deps.py` 환경 분리 적용. 테스트(`test_assets_autofill` 등) 수정 및 통과 확인.

- [2026-01-04 22:35:00] Hotfix: Frontend 연동 검증 중 `AssetService.get_assets_with_metrics`에서 `crud_asset.get_assets` 호출 시 `session` 인자가 Positional로 전달되어 TypeError 발생하는 문제 확인. Keyword Argument (`session=session`)로 수정하여 해결함. Style Guide 준수 확인.
