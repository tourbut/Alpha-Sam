import { api_router } from "$lib/fastapi";
import type { Position, PositionCreate, PositionUpdate } from "$lib/types";

export const get_positions = api_router('positions', 'get', '');
export const get_position = api_router('positions', 'get', '{id}');
export const create_position = api_router('positions', 'post', '');
export const update_position = api_router('positions', 'put', '{id}');
export const delete_position = api_router('positions', 'delete', '{id}');
