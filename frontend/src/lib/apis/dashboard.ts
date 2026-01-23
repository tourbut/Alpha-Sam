import { fetchWithAuth } from "../auth";
import type { ActivityItem } from "../types";

export const get_recent_activities = async (): Promise<ActivityItem[]> => {
    const response = await fetchWithAuth("/api/v1/dashboard/activities");
    if (response.ok) {
        return await response.json();
    }
    throw new Error("Failed to fetch recent activities");
};
