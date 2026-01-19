---
name: Debug
description: 디버깅을 위한 서버 구동 스크립트입니다. "테스트", "QA", "디버깅", "서버 구동", "로그 확인" 등의 키워드가 언급되면 이 스킬을 고려. 개발 중 테스트가 필요할시 사용합니다. 
---

# System Verification & Debugging Commands

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