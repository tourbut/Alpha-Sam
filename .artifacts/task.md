# Tasks - v0.5.0 Release & v0.6.0 Planning

- [x] **Release v0.5.0**
    - [x] Update `handovers/to_devops.md` with deployment instructions
    - [x] Verify release readiness (Tagging, etc. - mostly on DevOps side)

- [x] **Plan v0.6.0 (External Data & Analytics)**
    - [x] Analyze Requirements (Market Data API)
    - [x] Create `v0.6.0_implementation_plan.md`
    - [x] Distribute Backend Tasks (`to_backend_dev.md`)
    - [x] Distribute Frontend Tasks (`to_frontend_dev.md`)
    - [x] Archive `handovers/to_architect.md`

- [x] **Resume v0.6.0 Hotfix & QA**
    - [x] Resolve 500 Errors (Timeout/Deadlock)
    - [x] Verify Market Data API
    - [x] Verify Frontend Dashboard Loading

- [/] **Plan v0.7.0 (Multi-tenancy & Notifications)**
    - [x] **Architect**: Design v0.7.0 Specs
        - [x] DB Schema (Multi-tenancy)
        - [x] Email Notification Architecture
        - [x] Write `.artifacts/docs/v0.7.0_specs.md`
    - [x] **Backend**: Plan Implementation
    - [ ] **Frontend**: Plan UI Changes

- [ ] **Implement v0.7.0**
    - [x] **Backend**: DB Schema Migration (trans/pos owner_id)
    - [x] **Backend**: Email Service & Celery Setup
    - [x] **Backend**: Implement Notification Logic
    - [ ] **Frontend**: User Portfolio View
