import { api_router } from "$lib/fastapi"
import type { LeaderboardEntry, FollowListResponse, UserProfile } from "$lib/types";

const _getLeaderboard = api_router('social', 'get', 'leaderboard');
const _followUser = api_router('social', 'post', 'follow/{target_id}');
const _unfollowUser = api_router('social', 'delete', 'follow/{target_id}');
const _getFollowers = api_router('social', 'get', 'users/{user_id}/followers');
const _getFollowing = api_router('social', 'get', 'users/{user_id}/following');

export const getLeaderboard = async (n: number = 10): Promise<LeaderboardEntry[]> => {
    return await _getLeaderboard({ n });
}

// UUID 형식으로 ID 타입 변경 (string)
export const followUser = async (target_id: string): Promise<any> => {
    return await _followUser({ target_id });
}

export const unfollowUser = async (target_id: string): Promise<any> => {
    return await _unfollowUser({ target_id });
}

export const getFollowers = async (id: string, skip: number = 0, limit: number = 20): Promise<FollowListResponse> => {
    return await _getFollowers({ user_id: id, skip, limit });
}

export const getFollowing = async (id: string, skip: number = 0, limit: number = 20): Promise<FollowListResponse> => {
    return await _getFollowing({ user_id: id, skip, limit });
}

