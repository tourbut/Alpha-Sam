# Project: Alpha-Sam

> 마지막 업데이트: 2026-01-19

## 개요

**Alpha-Sam**은 개인 투자자를 위한 **통합 자산 관리 및 포트폴리오 트래킹 웹 대시보드**입니다.
암호화폐, 주식, 펀드 등 다양한 투자 자산을 한곳에서 관리하고, 실시간 시세와 연동하여 정확한 수익률(PnL)을 분석할 수 있습니다.

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| **현재 버전** | v1.2.0 (Multi-Portfolio) |
| **다음 버전** | v1.1.0 (Social Features) - 진행 중 |
| **배포 상태** | Production 운영 중 |

---

## 구현된 주요 기능

### 1. 인증 및 보안 (v0.8.0)
- JWT 기반 사용자 인증 (FastAPI Users)
- 안전한 회원가입/로그인 UI
- Argon2 해싱을 통한 패스워드 보안
- 멀티 테넌시(Multi-tenancy) 아키텍처로 사용자 데이터 격리

### 2. 대시보드 (v1.0.0, v1.3.0)
- **총 자산 현황**: 전체 포트폴리오 평가액 합계
- **자산 구성 차트**: Pie Chart를 통한 자산 비중 시각화
- **손익(PnL) 분석**: 전일 대비 등락률, 총 평가 손익
- **퀵 액션**: 자산 추가, 거래 기록 등 빠른 접근 UI
- **다크 모드 지원**: 테마 전환 기능
- **반응형 레이아웃**: 모바일/태블릿 지원

### 3. 멀티 포트폴리오 관리 (v1.2.0)
- **다중 포트폴리오 지원**: 사용자별 여러 포트폴리오 생성/관리
- **포트폴리오 선택기**: 현재 활성 포트폴리오 전환
- **포트폴리오 카드 UI**: 각 포트폴리오 요약 정보 표시

### 4. 자산 관리 (Assets)
- **전역 자산**: BTC, ETH, AAPL 등 시스템 등록 자산 검색/추가
- **커스텀 자산**: 사용자 정의 자산 직접 등록
- **실시간 시세 연동**: yfinance를 통한 시세 조회
- **자산별 상세 정보**: 보유 수량, 평균 매수가, 현재가, 수익률

### 5. 거래(Transaction) 기반 포지션 (v1.2.0)
- **매수/매도 거래 기록**: 정확한 포지션 계산
- **거래 이력 조회**: 자산별 거래 히스토리
- **자동 평균단가 계산**: 거래 기반 평균 매수가 산출

### 6. 알림 서비스 (v0.7.0)
- **시세 알림**: 목표 가격 도달 시 이메일 알림
- **Celery/Redis 기반 비동기 처리**

### 7. 소셜 기능 (v1.1.0 - 개발 중)
- **포트폴리오 공유**: Private/Public/Link-only 공개 설정
- **리더보드**: 수익률 기반 사용자 랭킹
- **소셜 그래프**: 팔로우/팔로잉 기능

---

## 프론트엔드 라우트 구조

| 경로 | 기능 |
|------|------|
| `/` | 대시보드 (메인 화면) |
| `/(auth)/login` | 로그인 페이지 |
| `/(auth)/register` | 회원가입 페이지 |
| `/portfolios` | 포트폴리오 목록 |
| `/portfolios/[id]` | 포트폴리오 상세 |
| `/assets` | 자산 관리 |
| `/transactions` | 거래 내역 |
| `/positions` | 포지션 현황 |
| `/leaderboard` | 리더보드 |
| `/settings` | 사용자 설정 |

---

## 기술 스택 요약

| 영역 | 기술 |
|------|------|
| **Frontend** | SvelteKit 2 + Svelte 5 (Runes) + Flowbite-Svelte + Tailwind v4 |
| **Backend** | FastAPI + SQLAlchemy + SQLModel |
| **Database** | PostgreSQL (asyncpg) |
| **Cache/Queue** | Redis + Celery |
| **인증** | JWT + FastAPI Users + Argon2 |
| **시세 데이터** | yfinance |
| **차트** | Chart.js |
| **배포** | Docker + Docker Compose + Nginx |

---

## 참고 문서

- [기술 스택 상세](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.agent/project/info/tech_stack.md)
- [도메인 규칙](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.agent/project/info/domain_rules.md)
- [기능 매뉴얼](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.agent/project/info/docs/functional_manual.md)
- [마일스톤 현황](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.agent/project/artifacts/milestone/milestones.md)
- [v1.1.0 설계 문서](file:///Users/shin/MyDir/MyGit/Alpha-Sam/.agent/project/artifacts/architecture/v1.1.0_design_draft.md)