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

export interface NotificationSettings {
    user_id: string;
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
    id: string;
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

// Position Create/Update는 더 이상 사용하지 않음 (Transaction으로 대체)
// export interface PositionCreate {
// 	asset_id: string;
// 	quantity: number;
// 	buy_price: number;
// 	buy_date?: string;
// }
//
// export interface PositionUpdate {
// 	quantity?: number;
// 	buy_price?: number;
// 	buy_date?: string;
// }

export interface PortfolioSummary {
    totalValuation: number;
    totalProfitLoss: number;
    totalReturnRate: number;
    totalInvested: number;
}

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

export interface PortfolioHistory {
    id: string;
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

export enum PortfolioVisibility {
    PRIVATE = "PRIVATE",
    PUBLIC = "PUBLIC",
    LINK_ONLY = "LINK_ONLY"
}

export interface Portfolio {
    id: string;
    owner_id: string;
    name: string;
    description?: string;
    currency: string;
    created_at: string;
    visibility: PortfolioVisibility;
    share_token?: string;
    is_primary_for_leaderboard: boolean;
}

export interface PortfolioShared {
    id: string;
    name: string;
    owner_nickname: string;
    description?: string;
    total_value?: number;
    return_rate?: number;
    positions: Position[];
    visibility: PortfolioVisibility;
}

export interface LeaderboardEntry {
    user_id: string;
    nickname: string;
    return_rate: number;
    total_value: number;
    rank: number;
}

export interface UserProfile {
    id: string;
    nickname?: string;
    email: string;
}

export interface FollowListResponse {
    total: number;
    users: UserProfile[];
}

// 포트폴리오 카드용 확장 타입 (자산 정보 포함)
export interface PortfolioAsset {
    symbol: string;
    name: string;
    value: number;
    percentage: number;
}

export interface PortfolioWithAssets {
    id: string;
    name: string;
    description?: string;
    created_at?: string;
    totalValue: number;
    assets: PortfolioAsset[];
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

export interface AssetTransaction {
    id: string;
    type: "buy" | "sell";
    date: string;
    quantity: number;
    price: number;
    total: number;
    fee: number | null;
}

export enum ActivityType {
    PORTFOLIO_CREATED = "portfolio_create",
    ASSET_ADDED = "asset_add",
    TRANSACTION_EXECUTED = "transaction"
}

export interface ActivityItem {
    id: string;
    type: ActivityType;
    title: string;
    description: string;
    timestamp: string;
    entity_id: string;
    portfolio_id?: string;
}
