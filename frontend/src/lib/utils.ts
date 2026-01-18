import type { Position, PortfolioSummary } from './types';

export function calculatePortfolioSummary(positions: Position[]): PortfolioSummary {
    let totalValuation = 0;
    let totalInvested = 0;

    positions.forEach(position => {
        if (position.valuation !== undefined && position.valuation !== null) {
            totalValuation += position.valuation;
        }
        totalInvested += position.avg_price * position.quantity;
    });

    const totalProfitLoss = totalValuation - totalInvested;
    const totalReturnRate = totalInvested > 0
        ? ((totalValuation - totalInvested) / totalInvested) * 100
        : 0;

    return {
        totalValuation,
        totalProfitLoss,
        totalReturnRate,
        totalInvested,
    };
}

export const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
};

export const formatPercent = (value: number) => {
    if (isNaN(value)) return '0.00%';
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
};

export const getColorClass = (value: number) => {
    if (isNaN(value) || value === 0) return 'text-gray-500';
    return value > 0 ? 'text-red-500' : 'text-blue-500';
};
