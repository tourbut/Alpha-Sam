import { api_router } from "$lib/fastapi";

export const get_admin_assets = api_router('admin', 'get', 'assets');
export const create_admin_asset = api_router('admin', 'post', 'assets');
export const delete_admin_asset = api_router('admin', 'delete', 'assets/{id}');
export const toggle_admin_asset = api_router('admin', 'post', 'assets/{id}/toggle');
