import { api_router } from "$lib/fastapi";

const router = "prices";

export const refresh_prices = api_router(router, 'post', 'refresh');
