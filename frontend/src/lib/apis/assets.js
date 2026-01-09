import { api_router } from "$lib/fastapi";

const router = "assets";

export const get_assets = api_router(router, 'get', ''); // /assets/
export const create_asset = api_router(router, 'post', ''); // /assets/
