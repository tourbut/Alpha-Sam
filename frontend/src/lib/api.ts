export const BASE_URL = '/api/v1';

export interface Asset {
    id: number;
    symbol: string;
    name: string;
    category: string;
    owner_id?: number | null; // Added for Multi-tenancy
    latest_price?: number;
    latest_price_updated_at?: string;
    created_at?: string;
    updated_at?: string;
    // Position 정보가 있을 경우 계산되는 필드들
    quantity?: number;
    buy_price?: number;
    valuation?: number; // current_price * quantity
    profit_loss?: number; // (current_price - buy_price) * quantity
    return_rate?: number; // ((current_price - buy_price) / buy_price) * 100
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

// Auth types
export interface UserCreate {
    email: string;
    password: string;
    full_name?: string;
}

export interface UserLogin {
    username: string; // OAuth2PasswordRequestForm uses username
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

export async function login(credentials: UserLogin): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${BASE_URL}/auth/jwt/login`, {
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

function getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    const devUserId = localStorage.getItem('dev_user_id') || '1'; // Default to 1
    return {
        'Content-Type': 'application/json',
        'X-User-Id': devUserId,
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
}

export async function updateProfile(data: UserUpdate): Promise<any> {
    const response = await fetch(`${BASE_URL}/users/me`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to update profile');
    }
    return await response.json();
}

export async function changePassword(data: UserPasswordUpdate): Promise<void> {
    const response = await fetch(`${BASE_URL}/users/password`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error('Failed to change password');
    }
}

export async function getAssets(): Promise<Asset[]> {
    try {
        const response = await fetch(`${BASE_URL}/assets/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) {
            console.warn('Failed to fetch assets, returning empty list. Status:', response.status);
            return [];
        }
        const data = await response.json();
        console.log('Fetched assets:', data);
        return data;
    } catch (error) {
        console.error('Error fetching assets:', error);
        return [];
    }
}

export async function createAsset(asset: AssetCreate): Promise<Asset> {
    const response = await fetch(`${BASE_URL}/assets/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(asset),
    });
    if (!response.ok) {
        throw new Error('Failed to create asset');
    }
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
    const response = await fetch(`${BASE_URL}/market/search?q=${encodeURIComponent(query)}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        throw new Error('Failed to search symbol');
    }
    return await response.json();
}

export async function refreshPrices(): Promise<void> {
    const response = await fetch(`${BASE_URL}/prices/refresh/`, {
        method: 'POST',
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        throw new Error('Failed to refresh prices');
    }
}

// Position 관련 타입 및 함수
export interface Position {
    id: number;
    asset_id: number;
    quantity: number;
    buy_price: number;
    buy_date?: string;
    created_at?: string;
    updated_at?: string;
    // 계산된 필드
    valuation?: number;
    profit_loss?: number;
    return_rate?: number;
    current_price?: number;
    // Asset 정보 (PositionWithAsset에서)
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
        const response = await fetch(`${BASE_URL}/positions/`, {
            headers: getAuthHeaders()
        });
        if (!response.ok) {
            console.warn('Failed to fetch positions, returning empty list. Status:', response.status);
            return [];
        }
        const data = await response.json();
        console.log('Fetched positions:', data);
        return data;
    } catch (error) {
        console.error('Error fetching positions:', error);
        return [];
    }
}

export async function getPosition(id: number): Promise<Position> {
    const response = await fetch(`${BASE_URL}/positions/${id}/`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to fetch position: ${errorText}`);
    }
    return await response.json();
}

export async function createPosition(position: PositionCreate): Promise<Position> {
    const response = await fetch(`${BASE_URL}/positions/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(position),
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to create position: ${errorText}`);
    }
    return await response.json();
}

export async function updatePosition(id: number, position: PositionUpdate): Promise<Position> {
    const response = await fetch(`${BASE_URL}/positions/${id}/`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(position),
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to update position: ${errorText}`);
    }
    return await response.json();
}

export async function deletePosition(id: number): Promise<void> {
    const response = await fetch(`${BASE_URL}/positions/${id}/`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to delete position: ${errorText}`);
    }
}

// 포트폴리오 요약 정보 (프론트엔드에서 계산)
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
    const response = await fetch(`${BASE_URL}/transactions/?skip=${skip}&limit=${limit}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch transactions");
    return response.json();
}

export async function createTransaction(data: CreateTransaction): Promise<Transaction> {
    const response = await fetch(`${BASE_URL}/transactions/`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create transaction");
    return response.json();
}

export async function getPortfolioHistory(skip = 0, limit = 30): Promise<PortfolioHistory[]> {
    const response = await fetch(`${BASE_URL}/portfolio/history?skip=${skip}&limit=${limit}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to fetch portfolio history");
    return response.json();
}

export async function createPortfolioSnapshot(): Promise<void> {
    const response = await fetch(`${BASE_URL}/portfolio/snapshot`, {
        method: "POST",
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error("Failed to create snapshot");
}


// Backend Portfolio API Types
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
    const response = await fetch(`${BASE_URL}/portfolio/summary`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        throw new Error('Failed to fetch portfolio summary');
    }
    return await response.json();
}

export async function getNotificationSettings(): Promise<NotificationSettings> {
    const response = await fetch(`${BASE_URL}/users/me/settings`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) {
        throw new Error('Failed to fetch notification settings');
    }
    return await response.json();
}

export async function updateNotificationSettings(settings: NotificationSettingsUpdate): Promise<NotificationSettings> {
    const response = await fetch(`${BASE_URL}/users/me/settings`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(settings),
    });
    if (!response.ok) {
        throw new Error('Failed to update notification settings');
    }
    return await response.json();
}
