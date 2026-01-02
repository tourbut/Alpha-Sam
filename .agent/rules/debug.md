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
  uv run python scripts/migrate_v090_legacy_data.py
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
  npm run dev
  ```
- **Run Type/Svelte Check**:
  ```bash
  cd frontend
  npm run check
  ```
