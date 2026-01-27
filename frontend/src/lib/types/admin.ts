export interface AdminAsset {
    id: string;
    symbol: string;
    name: string;
    type: string;
    currency: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface AdminAssetCreate {
    symbol: string;
    name: string;
    type: string;
    currency?: string;
    is_active?: boolean;
}
