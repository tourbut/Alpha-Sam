import { api_router } from "$lib/fastapi"
import type { LeaderboardEntry, FollowListResponse, UserProfile } from "$lib/types";

const _getLeaderboard = api_router('social', 'get', 'leaderboard');
const _followUser = api_router('social', 'post', 'follow/{target_id}');
const _unfollowUser = api_router('social', 'delete', 'follow/{target_id}');
const _getFollowers = api_router('social', 'get', 'users/{id}/followers');
const _getFollowing = api_router('social', 'get', 'users/{id}/following');

export const getLeaderboard = async (n: number = 10): Promise<LeaderboardEntry[]> => {
    return await _getLeaderboard({ n });
}

export const followUser = async (target_id: number): Promise<any> => {
    return await _followUser({ target_id });
}

export const unfollowUser = async (target_id: number): Promise<any> => {
    return await _unfollowUser({ target_id });
}

export const getFollowers = async (id: number, skip: number = 0, limit: number = 20): Promise<FollowListResponse> => {
    return await _getFollowers({ id, skip, limit });
}

export const getFollowing = async (id: number, skip: number = 0, limit: number = 20): Promise<FollowListResponse> => {
    return await _getFollowing({ id, skip, limit });
}
