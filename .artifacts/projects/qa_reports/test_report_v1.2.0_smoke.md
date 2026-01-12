# Test Report - v1.2.0 & v1.2.1 Smoke Test
**Date**: 2026-01-11
**Tester**: QA Engineer
**Version**: v1.2.0 -> v1.2.1 (Hotfix)
**Status**: 🟠 PARTIALLY RESOLVED / FAILED (New Issues Found)

## Summary
v1.2.0에서 발생했던 Frontend 접속 불가 문제(500 Error, Missing Module)는 v1.2.1 Hotfix를 통해 해결된 것으로 보였으나, 실제 검증 결과 Backend 소스 코드 내부의 Import 누락으로 인해 서버 가동이 실패하는 새로운 Critical Issue가 발견되었습니다.

## v1.2.0 Issues Status
- **Resolved**: `Missing Module '$lib/stores/auth'` 에러 해결됨. (Frontend 접속 가능해짐)

## v1.2.1 Critical Issues (Unresolved)
### 1. Backend ImportError (Refactor Side Effect)
- **Error**: `ImportError: cannot import name 'PortfolioCreate' from 'app.src.schemas.portfolio'`
- **Impact**: Backend 서버 가동 실패. (/api/v1/... 모든 요청에 대해 500 에러 발생)
- **Current Action**: QA Engineer가 임시로 `app/src/schemas/portfolio.py`에 누락된 스키마를 추가하여 백엔드를 기동함. 영구적인 코드 반영 필요.

### 2. Login Logic/Integration Issue
- **Error**: Endpoint `/api/v1/auth/login` 호출 시 422 Unprocessable Entity (또는 400 Incorrect credentials).
- **Impact**: 대시보드 및 서비스 진입 불가.
- **Cause**: Backend는 Form-data(`username`/`password`)를 기대하지만 Frontend가 JSON 형식을 보내거나 필드명이 불일치할 가능성 있음.

### 3. Frontend Routing (404)
- **Issue**: `/dashboard`, `/portfolios` 경로로 직접 이동 시 404 메세지 출력.
- **Impact**: 인증 우회 테스트 시에도 기능 페이지 접근 불가.

## Recommendations
- **Backend Refactoring**: `schemas.portfolio`에 누락된 클래스를 공식적으로 추가.
- **Authentication Alignment**: `$lib/fastapi.ts`와 `$lib/apis/auth.ts`가 Backend의 OAuth2 규격(Form-data)을 정확히 따르는지 재검토.
- **Frontend Route Audit**: 현재 `/dashboard` 및 주요 메뉴의 파일 경로 및 라우팅 설정 확인.
