import { api_router } from "$lib/fastapi"
import { type Portfolio, type PortfolioShared, type PortfolioWithAssets, PortfolioVisibility } from "$lib/types";

export type { Portfolio, PortfolioShared, PortfolioWithAssets };
export { PortfolioVisibility };

export interface PortfolioCreate {
    name: string
    description?: string
    currency?: string
}

export interface TransactionCreate {
    portfolio_id: string
    asset_id: string
    type: "BUY" | "SELL"
    quantity: number
    price: number
    executed_at?: string
}

export interface Transaction {
    id: string
    portfolio_id: string
    asset_id: string
    type: "BUY" | "SELL"
    quantity: number
    price: number
    executed_at: string
    created_at: string
}

const _fetchPortfolios = api_router('portfolios', 'get', '');
const _createPortfolio = api_router('portfolios', 'post', '');
const _fetchPortfolio = api_router('portfolios', 'get', '{id}');
const _fetchPortfolioPositions = api_router('portfolios', 'get', '{id}/positions');
const _createTransaction = api_router('transactions', 'post', '');
const _updateVisibility = api_router('portfolios', 'patch', '{id}/visibility');
const _fetchSharedPortfolio = api_router('portfolios', 'get', 'shared/{token}');
const _deletePortfolio = api_router('portfolios', 'delete', '{id}');
const _updatePortfolio = api_router('portfolios', 'put', '{id}');

export const fetchPortfolios = async (): Promise<Portfolio[]> => {
    return await _fetchPortfolios();
}

export const createPortfolio = async (data: PortfolioCreate): Promise<Portfolio> => {
    return await _createPortfolio(data);
}

export const fetchPortfolio = async (id: string): Promise<Portfolio> => {
    return await _fetchPortfolio({ id });
}

export const fetchPortfolioPositions = async (id: string): Promise<any[]> => {
    return await _fetchPortfolioPositions({ id });
}

export const createTransaction = async (data: TransactionCreate): Promise<Transaction> => {
    return await _createTransaction(data);
}

export const get_portfolio_history = api_router('portfolios', 'get', 'history');
export const create_portfolio_snapshot = api_router('portfolios', 'post', 'snapshot');
export const get_portfolio_summary = api_router('portfolios', 'get', 'summary');

export const updatePortfolioVisibility = async (id: string, visibility: PortfolioVisibility): Promise<Portfolio> => {
    return await _updateVisibility({ id, visibility });
}

export const fetchSharedPortfolio = async (token: string): Promise<PortfolioShared> => {
    return await _fetchSharedPortfolio({ token });
}

export const deletePortfolio = async (id: string): Promise<void> => {
    return await _deletePortfolio({ id });
}

export const updatePortfolio = async (id: string, data: PortfolioCreate): Promise<Portfolio> => {
    return await _updatePortfolio({ id, ...data });
}

// 포트폴리오 목록 + 자산 요약 정보 조회
const _fetchPortfoliosWithAssets = api_router('portfolios', 'get', 'with-assets');

// 백엔드 응답 타입 (snake_case)
interface PortfolioWithAssetsResponse {
    id: string;
    name: string;
    description?: string;
    created_at: string;
    total_value: number;
    assets: Array<{
        symbol: string;
        name: string;
        value: number;
        percentage: number;
    }>;
}


export const fetchPortfoliosWithAssets = async (): Promise<PortfolioWithAssets[]> => {
    const response: PortfolioWithAssetsResponse[] = await _fetchPortfoliosWithAssets();

    // snake_case → camelCase 변환
    return response.map((item) => ({
        id: item.id,
        name: item.name,
        description: item.description,
        created_at: item.created_at,
        totalValue: item.total_value,
        assets: item.assets
    }));
}

const _fetchPortfolioAsset = api_router('portfolios', 'get', '{id}/assets/{assetId}');
const _fetchPortfolioAssetTransactions = api_router('portfolios', 'get', '{id}/assets/{assetId}/transactions');

import type { AssetSummary, AssetTransaction } from "$lib/types";

export const fetchPortfolioAsset = async (id: string, assetId: string): Promise<AssetSummary> => {
    return await _fetchPortfolioAsset({ id, assetId });
}

export const fetchPortfolioAssetTransactions = async (id: string, assetId: string): Promise<AssetTransaction[]> => {
    return await _fetchPortfolioAssetTransactions({ id, assetId });
}


