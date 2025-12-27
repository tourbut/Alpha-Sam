import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';
import { goto } from '$app/navigation';
import { browser } from '$app/environment';

export const BASE_URL = '/api/v1';

export interface Asset {
    id: number;
    symbol: string;
    name: string;
    category: string;
    owner_id?: number | null;
    latest_price?: number;
    latest_price_updated_at?: string;
    created_at?: string;
    updated_at?: string;
    quantity?: number;
    buy_price?: number;
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
}

export interface AssetCreate {
    symbol: string;
    name: string;
    category: string;
}

export interface NotificationSettings {
    user_id: number;
    daily_report_enabled: boolean;
    price_alert_enabled: boolean;
}

export interface NotificationSettingsUpdate {
    daily_report_enabled?: boolean;
    price_alert_enabled?: boolean;
}

export interface UserCreate {
    email: string;
    password: string;
    full_name?: string;
}

export interface UserLogin {
    username: string;
    password: string;
}

export interface UserUpdate {
    nickname?: string;
    email?: string;
}

export interface UserPasswordUpdate {
    current_password: string;
    new_password: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

// Helper to get headers
function getAuthHeaders(): HeadersInit {
    // We can read directly from localStorage for requests to ensure latest token
    // or use the store value. LocalStorage is safer for sync if store isn't ready.
    const token = browser ? localStorage.getItem('access_token') : null;
    return {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
}

// Centralized Fetch Wrapper
async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    const headers = {
        ...getAuthHeaders(),
        ...(options.headers || {})
    };

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
        if (browser) {
            auth.logout();
            goto('/login');
        }
        throw new Error('Unauthorized');
    }

    return response;
}

export async function login(credentials: UserLogin): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
    });
    if (!response.ok) {
        throw new Error('Login failed');
    }
    return await response.json();
}

export async function signup(user: UserCreate): Promise<any> {
    const response = await fetch(`${BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    });
    if (!response.ok) {
        throw new Error('Signup failed');
    }
    return await response.json();
}

export async function updateProfile(data: UserUpdate): Promise<any> {
    const response = await fetchWithAuth(`${BASE_URL}/users/me`, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update profile');
    return await response.json();
}

export async function changePassword(data: UserPasswordUpdate): Promise<void> {
    const response = await fetchWithAuth(`${BASE_URL}/users/password`, {
        method: 'POST',
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to change password');
}

export async function getAssets(): Promise<Asset[]> {
    try {
        const response = await fetchWithAuth(`${BASE_URL}/assets/`);
        if (!response.ok) {
            console.warn('Failed to fetch assets, returning empty list. Status:', response.status);
            return [];
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching assets:', error);
        return [];
    }
}

export async function createAsset(asset: AssetCreate): Promise<Asset> {
    const response = await fetchWithAuth(`${BASE_URL}/assets/`, {
        method: 'POST',
        body: JSON.stringify(asset),
    });
    if (!response.ok) throw new Error('Failed to create asset');
    return await response.json();
}

export interface SymbolSearchResult {
    symbol: string;
    longname?: string;
    shortname?: string;
    quoteType?: string;
    exchange?: string;
}

export async function searchSymbol(query: string): Promise<SymbolSearchResult[]> {
    const response = await fetchWithAuth(`${BASE_URL}/market/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Failed to search symbol');
    return await response.json();
}

export async function refreshPrices(): Promise<void> {
    const response = await fetchWithAuth(`${BASE_URL}/prices/refresh/`, {
        method: 'POST'
    });
    if (!response.ok) throw new Error('Failed to refresh prices');
}

export interface Position {
    id: number;
    asset_id: number;
    quantity: number;
    buy_price: number;
    buy_date?: string;
    created_at?: string;
    updated_at?: string;
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
    current_price?: number;
    asset_symbol?: string;
    asset_name?: string;
    asset_category?: string;
}

export interface PositionCreate {
    asset_id: number;
    quantity: number;
    buy_price: number;
    buy_date?: string;
}

export interface PositionUpdate {
    quantity?: number;
    buy_price?: number;
    buy_date?: string;
}

export async function getPositions(): Promise<Position[]> {
    try {
        const response = await fetchWithAuth(`${BASE_URL}/positions/`);
        if (!response.ok) {
            console.warn('Failed to fetch positions, returning empty list. Status:', response.status);
            return [];
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching positions:', error);
        return [];
    }
}

export async function getPosition(id: number): Promise<Position> {
    const response = await fetchWithAuth(`${BASE_URL}/positions/${id}/`);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch position: ${errorText}`);
    }
    return await response.json();
}

export async function createPosition(position: PositionCreate): Promise<Position> {
    const response = await fetchWithAuth(`${BASE_URL}/positions/`, {
        method: 'POST',
        body: JSON.stringify(position),
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to create position: ${errorText}`);
    }
    return await response.json();
}

export async function updatePosition(id: number, position: PositionUpdate): Promise<Position> {
    const response = await fetchWithAuth(`${BASE_URL}/positions/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(position),
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to update position: ${errorText}`);
    }
    return await response.json();
}

export async function deletePosition(id: number): Promise<void> {
    const response = await fetchWithAuth(`${BASE_URL}/positions/${id}/`, {
        method: 'DELETE'
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to delete position: ${errorText}`);
    }
}

export interface PortfolioSummary {
    totalValuation: number;
    totalProfitLoss: number;
    totalReturnRate: number;
    totalInvested: number;
}

export function calculatePortfolioSummary(positions: Position[]): PortfolioSummary {
    let totalValuation = 0;
    let totalInvested = 0;

    positions.forEach(position => {
        if (position.valuation !== undefined && position.valuation !== null) {
            totalValuation += position.valuation;
        }
        totalInvested += position.buy_price * position.quantity;
    });

    const totalProfitLoss = totalValuation - totalInvested;
    const totalReturnRate = totalInvested > 0
        ? ((totalValuation - totalInvested) / totalInvested) * 100
        : 0;

    return {
        totalValuation,
        totalProfitLoss,
        totalReturnRate,
        totalInvested,
    };
}
export interface Transaction {
    id: number;
    asset_id: number;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
    total_amount: number;
    timestamp: string;
}

export interface CreateTransaction {
    asset_id: number;
    type: "BUY" | "SELL";
    quantity: number;
    price: number;
}

export interface PortfolioHistory {
    id: number;
    total_value: number;
    total_cost: number;
    total_pl: number;
    timestamp: string;
}

export async function getTransactions(skip = 0, limit = 100): Promise<Transaction[]> {
    const response = await fetchWithAuth(`${BASE_URL}/transactions/?skip=${skip}&limit=${limit}`);
    if (!response.ok) throw new Error("Failed to fetch transactions");
    return response.json();
}

export async function createTransaction(data: CreateTransaction): Promise<Transaction> {
    const response = await fetchWithAuth(`${BASE_URL}/transactions/`, {
        method: "POST",
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create transaction");
    return response.json();
}

export async function getPortfolioHistory(skip = 0, limit = 30): Promise<PortfolioHistory[]> {
    const response = await fetchWithAuth(`${BASE_URL}/portfolio/history?skip=${skip}&limit=${limit}`);
    if (!response.ok) throw new Error("Failed to fetch portfolio history");
    return response.json();
}

export async function createPortfolioSnapshot(): Promise<void> {
    const response = await fetchWithAuth(`${BASE_URL}/portfolio/snapshot`, {
        method: "POST"
    });
    if (!response.ok) throw new Error("Failed to create snapshot");
}

export interface PortfolioStats {
    percent: number;
    direction: 'up' | 'down' | 'flat';
}

export interface ApiPortfolioSummary {
    total_value: number;
    total_cost: number;
    total_pl: number;
    total_pl_stats: PortfolioStats;
}

export interface PortfolioResponse {
    summary: ApiPortfolioSummary;
    positions: Position[];
}

export async function getPortfolioSummary(): Promise<PortfolioResponse> {
    const response = await fetchWithAuth(`${BASE_URL}/portfolio/summary`);
    if (!response.ok) throw new Error('Failed to fetch portfolio summary');
    return await response.json();
}

export async function getNotificationSettings(): Promise<NotificationSettings> {
    const response = await fetchWithAuth(`${BASE_URL}/users/me/settings`);
    if (!response.ok) throw new Error('Failed to fetch notification settings');
    return await response.json();
}

export async function updateNotificationSettings(settings: NotificationSettingsUpdate): Promise<NotificationSettings> {
    const response = await fetchWithAuth(`${BASE_URL}/users/me/settings`, {
        method: 'POST',
        body: JSON.stringify(settings),
    });
    if (!response.ok) throw new Error('Failed to update notification settings');
    return await response.json();
}
