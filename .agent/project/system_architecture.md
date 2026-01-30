# System Architecture: Global Asset Management

## Overview
Alpha-Sam 프로젝트에서 `USD/KRW` 환율, 주가 지수 등 **전역적으로 공유되는 자산(Global Assets)**을 효율적으로 관리하기 위한 아키텍처를 정의합니다.

기존 데이터 모델(`Asset`은 특정 `Portfolio`에 종속)을 유지하면서 시세 수집 및 조회를 일원화하기 위해 **System Portfolio** 패턴을 도입합니다.

## Core Concepts

### 1. System Portfolio
- **정의**: 시스템 관리자가 소유한 특수 포트폴리오입니다.
- **역할**: 전역 자산(Exchange Rates, Indices)의 실제 인스턴스(`Asset`)를 보유합니다.
- **가시성**: `PRIVATE` (일반 사용자에게 노출되지 않음, 내부 로직 및 Admin API를 통해서만 관리).
- **소유자**: 데이터베이스에 존재하는 첫 번째 Superuser를 Owner로 지정합니다.

### 2. Admin Asset vs. System Asset
| 모델 | 역할 | 동기화 |
|---|---|---|
| **AdminAsset** | 자산의 메타데이터(심볼, 이름, 타입, 활성여부) 관리. <br> 관리자가 UI를 통해 제어. | Source of Truth |
| **Asset** | 시세 수집(`PriceTasks`) 및 `PriceDay` 연결을 위한 실제 엔티티. <br> System Portfolio 내에 자동 생성됨. | Derived (동기화됨) |

### 3. Synchronization Flow
1. **관리자**가 Admin 페이지에서 `AdminAsset`을 생성/수정/삭제합니다.
2. `AdminAsset`의 타입이 **Global Type** (`EXCHANGE_RATE`, `FOREX`, `INDEX`)인 경우:
3. **Backend Service**가 `System Portfolio` 내에 동일한 심볼의 `Asset`을 생성하거나 업데이트합니다.
4. **Price Collector**는 System Portfolio의 Asset을 포함하여 시세를 수집합니다.
5. 수집된 시세는 `PriceDay` 테이블과 Redis(`price:{SYMBOL}`)에 저장되어 전역적으로 조회 가능해집니다.

## Data Model Updates

### AssetType Enum (Extension)
기존 Asset Category 외에 시스템 관리를 위한 타입을 확장합니다.
- `STOCK` (기존)
- `CRYPTO` (기존)
- `EXCHANGE_RATE` (신규): 환율 (예: `KRW=X`)
- `INDEX` (신규): 지수 (예: `^GSPC`)
- `FOREX` (신규): 외환

### Symbol Naming Convention (Yahoo Finance Standard)
- **환율**: `TargetCurrency=X` (예: `KRW=X` -> USD to KRW, `EURKRW=X` -> EUR to KRW)
- **지수**: `^Symbol` (예: `^GSPC` -> S&P 500)

## Implementation Guidelines

### Backend
- **Service**: `SystemPortfolioService`를 구현하여 싱글톤 패턴으로 시스템 포트폴리오 접근 및 동기화를 담당합니다.
- **Initialization**: 서버 시작 시(또는 Admin API 호출 시) System User/Portfolio가 없으면 생성하는 로직이 필요합니다.

### Frontend
- Admin UI에서 `EXCHANGE_RATE` 등 글로벌 타입 선택 시, 사용자에게 적절한 심볼 포맷(예: `KRW=X`)을 가이드해야 합니다.
