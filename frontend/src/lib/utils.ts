import type { Position, PortfolioSummary } from './types';

export function calculatePortfolioSummary(positions: Position[]): PortfolioSummary {
    let totalValuation = 0;
    let totalInvested = 0;

    positions.forEach(position => {
        if (position.valuation !== undefined && position.valuation !== null) {
            totalValuation += position.valuation;
        }
        totalInvested += position.buy_price * position.quantity;
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
