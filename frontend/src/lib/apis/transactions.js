import { api_router } from "$lib/fastapi";

const router = "transactions";

export const get_transactions = api_router(router, 'get', '');
export const create_transaction = api_router(router, 'post', '');
