import { api_router } from "$lib/fastapi";
import type { SymbolSearchResult } from "$lib/types";

export const search_symbols = api_router('market', 'get', 'search');
