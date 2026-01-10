import { api_router } from "$lib/fastapi";
import type { Asset, AssetCreate } from "$lib/types";

export const get_assets = api_router('assets', 'get', '');
export const get_asset = api_router('assets', 'get', '{id}');
export const create_asset = api_router('assets', 'post', '');
export const update_asset = api_router('assets', 'put', '{id}');
export const delete_asset = api_router('assets', 'delete', '{id}');
