import { api_router } from "$lib/fastapi"
import { type Portfolio, type PortfolioShared, PortfolioVisibility } from "$lib/types";

export type { Portfolio, PortfolioShared };
export { PortfolioVisibility };

export interface PortfolioCreate {
    name: string
    description?: string
    currency?: string
}

export interface TransactionCreate {
    asset_id: number
    type: "BUY" | "SELL"
    quantity: number
    price: number
    executed_at?: string
}

export interface Transaction {
    id: number
    portfolio_id: number
    asset_id: number
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
const _createTransaction = api_router('portfolios', 'post', '{id}/transactions');
const _updateVisibility = api_router('portfolios', 'patch', '{id}/visibility');
const _fetchSharedPortfolio = api_router('portfolios', 'get', 'shared/{token}');

export const fetchPortfolios = async (): Promise<Portfolio[]> => {
    return await _fetchPortfolios();
}

export const createPortfolio = async (data: PortfolioCreate): Promise<Portfolio> => {
    return await _createPortfolio(data);
}

export const fetchPortfolio = async (id: number): Promise<Portfolio> => {
    return await _fetchPortfolio({ id });
}

export const fetchPortfolioPositions = async (id: number): Promise<any[]> => {
    return await _fetchPortfolioPositions({ id });
}

export const createTransaction = async (portfolioId: number, data: TransactionCreate): Promise<Transaction> => {
    return await _createTransaction({ id: portfolioId, ...data });
}

export const get_portfolio_history = api_router('portfolios', 'get', 'history');
export const create_portfolio_snapshot = api_router('portfolios', 'post', 'snapshot');
export const get_portfolio_summary = api_router('portfolios', 'get', 'summary');

export const updatePortfolioVisibility = async (id: number, visibility: PortfolioVisibility): Promise<Portfolio> => {
    return await _updateVisibility({ id, visibility });
}

export const fetchSharedPortfolio = async (token: string): Promise<PortfolioShared> => {
    return await _fetchSharedPortfolio({ token });
}
