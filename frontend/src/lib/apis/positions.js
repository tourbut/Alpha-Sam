import { api_router } from "$lib/fastapi";

const router = "positions";

export const get_positions = api_router(router, 'get', '');
export const create_position = api_router(router, 'post', '');
export const get_position = api_router(router, 'get', '{id}');
export const update_position = api_router(router, 'put', '{id}');
export const delete_position = api_router(router, 'delete', '{id}');
