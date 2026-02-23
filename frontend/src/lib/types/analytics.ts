export interface AssetAllocationResponse {
    ticker: string;
    percentage: number;
    total_value: number;
}

export interface PortfolioHistoryResponse {
    date: string;
    total_value: number;
    uninvested_cash: number;
}
