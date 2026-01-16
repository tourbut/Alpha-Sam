# Redis Schema & Data Flow Architecture

## Overview
To improve response times and reliability, the `PriceService` decouples data collection from data serving.
- **Collector**: Runs in the background (Cron/Celery), fetches data from external providers (Yahoo Finance), and updates Redis.
- **Service**: Reads directly from Redis. Fast, reliable, no external blocking.

## Redis Schema

### 1. Market Price
Stores the latest market price for a given symbol.

- **Key Format**: `price:{SYMBOL}`
  - Example: `price:BTC-USD`, `price:AAPL`, `price:ETH-USD`
  - Note: Symbols are always Uppercase. Crypto symbols typically follow `{COIN}-USD` format in Yahoo Finance.
- **Value Details**:
  - Type: `String` (Float representation)
  - Example: `"95000.50"`, `"180.25"`
  - Constraint: Must be parseable as `float`.
- **TTL (Time To Live)**: `180 seconds` (3 minutes)
  - Data is considered "stale" if not updated within 3 minutes.
  - Collector should run more frequently than TTL (e.g., every 1-2 minutes).

### 2. Price Alerts (Existing)
Rate limiting for price alerts.

- **Key Format**: `alert:{user_id}:{symbol}:{date}`
- **Value**: Counter or Timestamp
- **TTL**: 24 hours (Expires at end of day or sliding window)

## Data Flow

```mermaid
graph TD
    A[Cron/Celery Worker] -- 1. Fetch --> B(Yahoo Finance API)
    B -- 2. Return Price --> A
    A -- 3. SET namespaced Key (TTL 3m) --> C[(Redis Cache)]
    
    D[Client/Frontend] -- 4. GET /api/prices/{symbol} --> E[Backend API]
    E -- 5. GET price:{symbol} --> C
    C -- 6. Return Value --> E
    E -- 7. Return JSON --> D
    
    subgraph Fallback Logic
    E -.-> |Cache Miss| F{Handle Miss}
    F --> |Dev| Return Mock Data
    F --> |Prod| Return Error / Last Known DB Value
    end
```

## Maintenance
- **Key Eviction**: Automatic via TTL.
- **Monitoring**: Check `dbsize` or specific keys in Redis.
