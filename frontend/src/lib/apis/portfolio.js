import { api_router } from "$lib/fastapi";

const router = "portfolio";

export const get_portfolio_history = api_router(router, 'get', 'history');
export const create_portfolio_snapshot = api_router(router, 'post', 'snapshot');
export const get_portfolio_summary = api_router(router, 'get', 'summary');
