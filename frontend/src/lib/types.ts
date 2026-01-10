export interface Asset {
    id: number;
    symbol: string;
    name: string;
    category: string;
    owner_id?: number | null;
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

export interface NotificationSettings {
    user_id: number;
    daily_report_enabled: boolean;
    price_alert_enabled: boolean;
}

export interface NotificationSettingsUpdate {
    daily_report_enabled?: boolean;
    price_alert_enabled?: boolean;
}

export interface UserCreate {
    email: string;
    password: string;
    full_name?: string;
}

export interface UserRead {
    id: number | string; // Supporting both for now
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
    nickname?: string;
}

export interface UserLogin {
    username: string;
    password: string;
}

export interface UserUpdate {
    nickname?: string;
    email?: string;
}

export interface UserPasswordUpdate {
    current_password: string;
    new_password: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export interface SymbolSearchResult {
    symbol: string;
    longname?: string;
    shortname?: string;
    quoteType?: string;
    exchange?: string;
}

export interface Position {
    id: number;
    asset_id: number;
    quantity: number;
    buy_price: number;
    buy_date?: string;
    created_at?: string;
    updated_at?: string;
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
    current_price?: number;
    asset_symbol?: string;
    asset_name?: string;
    asset_category?: string;
}

export interface PositionCreate {
    asset_id: number;
    quantity: number;
    buy_price: number;
    buy_date?: string;
}

export interface PositionUpdate {
    quantity?: number;
    buy_price?: number;
    buy_date?: string;
}

export interface PortfolioSummary {
    totalValuation: number;
    totalProfitLoss: number;
    totalReturnRate: number;
    totalInvested: number;
}

export interface Transaction {
    id: number;
    asset_id: number;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
    total_amount: number;
    timestamp: string;
}

export interface CreateTransaction {
    asset_id: number;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
}

export interface PortfolioHistory {
    id: number;
    total_value: number;
    total_cost: number;
    total_pl: number;
    timestamp: string;
}

export interface PortfolioStats {
    percent: number;
    direction: 'up' | 'down' | 'flat';
}

export interface ApiPortfolioSummary {
    total_value: number;
    total_cost: number;
    total_pl: number;
    total_pl_stats: PortfolioStats;
}

export interface PortfolioResponse {
    summary: ApiPortfolioSummary;
    positions: Position[];
}
