import { api_router } from "$lib/fastapi";
import type { UserLogin, UserCreate, Token, UserRead } from "$lib/types";

export const login = api_router('auth', 'login', 'login');
export const signup = api_router('auth', 'post', 'signup');
export const get_me = api_router('auth', 'get', 'me');
