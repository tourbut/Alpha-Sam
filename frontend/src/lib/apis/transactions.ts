import { api_router } from "$lib/fastapi";
import type { Transaction, CreateTransaction } from "$lib/types";

export const get_transactions = api_router('transactions', 'get', '');
export const create_transaction = api_router('transactions', 'post', '');
export const get_transaction = api_router('transactions', 'get', '{id}');
export const delete_transaction = api_router('transactions', 'delete', '{id}');
