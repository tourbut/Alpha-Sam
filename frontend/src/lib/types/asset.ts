export interface Asset {
    id: string;
    symbol: string;
    name: string;
    category: string;
    owner_id?: string | null;
    latest_price?: number;
    latest_price_updated_at?: string;
    created_at?: string;
    updated_at?: string;
    quantity?: number;
    buy_price?: number;
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
}

export interface AssetCreate {
    symbol: string;
    name: string;
    category: string;
}

export interface SymbolSearchResult {
    symbol: string;
    longname?: string;
    shortname?: string;
    quoteType?: string;
    exchange?: string;
}

export interface AssetSummary {
    asset_id: string;
    symbol: string;
    name: string;
    quantity: number;
    avg_price: number;
    current_price: number | null;
    total_value: number;
    profit_loss: number;
    return_rate: number;
}
