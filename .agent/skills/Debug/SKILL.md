---
name: Debug
description: 디버깅을 위한 서버 구동 스크립트입니다. "디버깅", "서버 구동", "로그 확인" 등의 키워드가 언급되면 이 스킬을 고려. 개발 중 테스트가 필요할시 사용합니다. 
---

# System Verification & Debugging Commands

## Purpose

이 스킬은 프로젝트의 백엔드 및 프론트엔드 환경을 로컬에서 실행하고, 테스트 데이터를 시뮬레이션하며, 오류 발생 시 디버깅을 돕기 위한 명령어 모음입니다.

## When to Run

- "디버깅"이나 "서버 구동"이 요청될 때
- "로그 확인"이 필요할 때
- 로컬 개발 환경에서 빠른 테스트 환경이 필요할 때
## Backend (FastAPI)
- **Run Development Server**:
  ```bash
  cd backend
  uv run uvicorn app.main:app --reload
  ```
- **Run v0.9.0 Data Migration**:
  ```bash
  cd backend
  uv run uvicorn app.main:app --reload| tee .agent/project/logs/backend.log
  ```
- **Generate QA Dirty Data (Legacy Simulation)**:
  ```bash
  cd backend
  uv run python scripts/qa_generate_dirty_data_v090.py
  ```
- **Verify Portfolio Snapshot Optimization**:
  ```bash
  cd backend
  uv run python verify_snapshot.py
  ```

## Frontend (SvelteKit)
- **Run Development Server**:
  ```bash
  cd frontend
  npm run dev 2>&1| tee .agent/project/logs/frontend.log
  ```
- **Run Type/Svelte Check**:
  ```bash
  cd frontend
  npm run check
  ```

## Test User
- ID: tester@example.com
- PW: password123

## Related Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI 서버 엔트리포인트 |
| `frontend/package.json` | 프론트엔드 실행 및 Svelte Check를 위한 스크립트 |
| `scripts/qa_generate_dirty_data_v090.py` | 더티 데이터 생성 시뮬레이션 |