import { api_router } from "$lib/fastapi";
import type { ActivityItem } from "$lib/types";

export const get_recent_activities = api_router('dashboard', 'get', 'activities');

