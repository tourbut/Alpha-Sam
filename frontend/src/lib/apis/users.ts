import { api_router } from "$lib/fastapi";
import type { UserRead, UserUpdate, UserPasswordUpdate } from "$lib/types";

export const get_me = api_router('users', 'get', 'me');
export const update_me = api_router('users', 'put', 'me');
export const update_password = api_router('users', 'post', 'password');
