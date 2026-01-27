export interface Transaction {
    id: string;
    asset_id: string;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
    total_amount: number;
    timestamp: string;
}

export interface CreateTransaction {
    asset_id: string;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
}

export interface AssetTransaction {
    id: string;
    type: "buy" | "sell";
    date: string;
    quantity: number;
    price: number;
    total: number;
    fee: number | null;
}

// Position: 읽기 전용 (Transaction 집계 결과)
export interface IPosition {
    id?: string; // Optional: DB ID 없음 (동적 계산)
    asset_id: string;
    quantity: number;
    avg_price: number; // buy_price → avg_price
    created_at?: string; // Optional
    updated_at?: string; // Optional
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
    current_price?: number;
    asset_symbol?: string;
    asset_name?: string;
    asset_category?: string;
}

export type Position = IPosition;
