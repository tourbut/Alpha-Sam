# Alpha-Sam 기술 스택

> 마지막 업데이트: 2026-01-13

## 📋 기술 스택 요약

| 항목 | 기술 |
|------|------|
| **Project Type** | Svelte |
| **Framework** | SvelteKit 2 |
| **Build Tool** | Vite 7 |
| **Component Library** | Flowbite-Svelte |
| **Tailwind Version** | v4 |
| **TS/JS** | TypeScript |
| **Router** | SvelteKit Router |
| **State Management** | Svelte Store (Runes) |
| **Testing Framework (Frontend)** | Vitest |
| **Testing Framework (Backend)** | pytest |
| **ORM/Client Library** | SQLAlchemy + SQLModel |
| **HTTP Server Framework** | FastAPI |
| **Charting Library** | Chart.js |
| **Server Runtime** | Node.js v22 |
| **Package Manager (Frontend)** | npm |
| **Package Manager (Backend)** | uv |
| **Deployment Platform** | Docker + Docker Compose |
| **Language (Backend)** | Python 3.13 |
| **Language (Frontend)** | TypeScript 5 |
| **Database** | PostgreSQL (asyncpg) | UUID v4 ID 정책 적용 |
| **ID Policy** | UUID v4 | 모든 주요 엔티티 적용 |
| **Cache/Queue** | Redis + Celery |

---

## 🎨 Frontend

| 항목 | 버전/기술 | 비고 |
|------|-----------|------|
| Svelte | ^5.43.8 | Svelte 5 Runes 문법 사용 |
| SvelteKit | ^2.48.5 | SSR/SSG 지원 |
| Vite | ^7.2.2 | HMR 지원 빌드 도구 |
| Tailwind CSS | ^4.1.17 | v4 최신 버전 |
| Flowbite | ^4.0.1 | UI 컴포넌트 기본 |
| Flowbite-Svelte | ^1.30.0 | Svelte용 컴포넌트 |
| Flowbite-Svelte-Icons | ^3.1.0 | 아이콘 라이브러리 |
| Chart.js | ^4.5.1 | 데이터 시각화 |
| TypeScript | ^5.9.3 | 타입 안전성 |
| Vitest | ^4.0.16 | 단위 테스트 |
| Testing Library (Svelte) | ^5.0.0 | 컴포넌트 테스트 |

---

## ⚙️ Backend

| 항목 | 버전/기술 | 비고 |
|------|-----------|------|
| Python | >=3.13 | 최신 Python 런타임 |
| FastAPI | >=0.109.0 | 비동기 API 프레임워크 |
| Uvicorn | >=0.27.0 | ASGI 서버 |
| SQLAlchemy | >=2.0.25 | ORM |
| SQLModel | >=0.0.14 | Pydantic + SQLAlchemy 통합 |
| Alembic | >=1.13.1 | DB 마이그레이션 |
| asyncpg | >=0.29.0 | PostgreSQL 비동기 드라이버 |
| Pydantic Settings | >=2.1.0 | 환경 설정 관리 |
| Redis | >=5.0.0 | 캐시 및 세션 스토어 |
| Celery | >=5.3.0 | 비동기 작업 큐 |
| PyJWT | >=2.10.1 | JWT 인증 |
| Passlib + Argon2 | - | 패스워드 해싱 |
| yfinance | >=0.2.66 | 주식 시세 데이터 |
| FastAPI-Users | >=13.0.0 | 사용자 인증 관리 |
| pytest | >=9.0.2 | 단위/통합 테스트 |
| pytest-asyncio | >=1.3.0 | 비동기 테스트 지원 |

---

## 🐳 DevOps / Infrastructure

| 항목 | 기술 | 비고 |
|------|------|------|
| 컨테이너 | Docker | 개발/프로덕션 환경 통일 |
| 오케스트레이션 | Docker Compose | 멀티 컨테이너 관리 |
| 웹 서버 / 리버스 프록시 | Nginx | 정적 파일 서빙, 프록시 |
| 데이터베이스 | PostgreSQL | 메인 RDBMS |
| 캐시 | Redis | 세션, 캐시, Celery 브로커 |

---

## 📁 프로젝트 구조

```
Alpha-Sam/
├── backend/          # FastAPI 백엔드
│   ├── app/          # 애플리케이션 코드
│   │   ├── src/
│   │   │   ├── api/      # API Router 등록
│   │   │   ├── core/     # 설정, DB, 캐시
│   │   │   ├── crud/     # [Layer 4] Data Access (CRUD)
│   │   │   ├── engine/   # [Layer 3] Business Logic (Pure Calculation)
│   │   │   ├── services/ # [Layer 2] Orchestration Service
│   │   │   ├── routes/   # [Layer 1] Controllers (HTTP Handlers)
│   │   │   ├── models/   # SQLModel/SQLAlchemy 모델
│   │   │   └── schemas/  # Pydantic Schemas
│   ├── alembic/      # DB 마이그레이션
│   └── pyproject.toml
├── frontend/         # SvelteKit 프론트엔드
│   ├── src/
│   │   ├── lib/      # 컴포넌트, 유틸리티
│   │   └── routes/   # SvelteKit 라우트
│   └── package.json
├── nginx/            # Nginx 설정
├── docker-compose.yml        # 개발 환경
├── docker-compose.prod.yml   # 프로덕션 환경
└── .artifacts/       # 프로젝트 문서 및 아티팩트
```

---

## 🔧 개발 환경 요구사항

- **Node.js**: v22.x
- **Python**: 3.13+
- **Docker**: 최신 버전
- **Docker Compose**: v2+
- **패키지 매니저**: npm (Frontend), uv (Backend)
