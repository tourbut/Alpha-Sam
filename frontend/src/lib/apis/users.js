import { api_router } from "$lib/fastapi";

const router = "users";

export const get_me = api_router(router, 'get', 'me');
export const update_me = api_router(router, 'put', 'me'); // profile update calls this
export const change_password = api_router(router, 'post', 'password');

// Notification settings seem to be under users/me/settings in api.ts
export const get_notification_settings = api_router(router, 'get', 'me/settings');
export const update_notification_settings = api_router(router, 'post', 'me/settings');
