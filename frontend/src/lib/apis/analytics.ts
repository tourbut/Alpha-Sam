import { api_router } from "$lib/fastapi";

export const get_portfolio_allocation = api_router('analytics', 'get', 'portfolio/{portfolio_id}/allocation');
export const get_portfolio_history = api_router('analytics', 'get', 'portfolio/{portfolio_id}/history');

export const get_portfolios_allocation = api_router('analytics', 'get', 'portfolios/allocation');
export const get_portfolios_history = api_router('analytics', 'get', 'portfolios/history');
