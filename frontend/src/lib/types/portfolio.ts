import type { Position } from "./transaction";
import type { UserProfile } from "./user";

export interface PortfolioSummary {
    totalValuation: number;
    totalProfitLoss: number;
    totalReturnRate: number;
    totalInvested: number;
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
    updated_at?: string;
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
    updated_at?: string;
    totalValue: number;
    assets: PortfolioAsset[];
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
