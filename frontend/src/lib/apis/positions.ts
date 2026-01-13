/**
 * Position API Client
 * 
 * 참고: Position은 더 이상 직접 생성/수정/삭제할 수 없습니다.
 * Transaction을 추가하여 간접적으로 Position을 변경합니다.
 * Position 조회는 Portfolio Summary API를 사용하는 것을 권장합니다.
 */

import { api_router } from "$lib/fastapi";

// 읽기 전용 API (사용 권장하지 않음, Portfolio Summary 사용 권장)
export const get_positions = api_router('positions', 'get', '');
export const get_position = api_router('positions', 'get', '{id}');

// CRUD 함수 제거됨 (Transaction으로 대체)
// export const create_position = ...
// export const update_position = ...
// export const delete_position = ...
