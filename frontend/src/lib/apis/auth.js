import { api_router } from "$lib/fastapi";

const router = "auth";

export const login = api_router(router, 'login', 'login');
export const signup = api_router(router, 'post', 'signup');
