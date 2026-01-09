import { api_router } from "$lib/fastapi";

const router = "market";

export const search_symbol = api_router(router, 'get', 'search');
