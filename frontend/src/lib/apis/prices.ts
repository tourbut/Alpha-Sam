import { api_router } from "$lib/fastapi";

export const refresh_prices = api_router('prices', 'post', 'refresh');
export const get_price = api_router('prices', 'get', '{symbol}');
