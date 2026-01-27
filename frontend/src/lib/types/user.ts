export interface UserRead {
    id: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
    nickname?: string;
}

export interface UserUpdate {
    nickname?: string;
    email?: string;
}

export interface UserProfile {
    id: string;
    nickname?: string;
    email: string;
}

export interface FollowListResponse {
    total: number;
    users: UserProfile[];
}

export interface NotificationSettings {
    user_id: string;
    daily_report_enabled: boolean;
    price_alert_enabled: boolean;
}

export interface NotificationSettingsUpdate {
    daily_report_enabled?: boolean;
    price_alert_enabled?: boolean;
}
