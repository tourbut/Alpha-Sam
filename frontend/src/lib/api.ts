export const BASE_URL = '/api/v1';
export const STORAGE_KEY_ACCESS_TOKEN = 'access_token';
export const STORAGE_KEY_USER_ID = 'dev_user_id';

/**
 * Centralized API Endpoints
 */
export const API_ENDPOINTS = {
    LOGIN: '/auth/jwt/login',
    SIGNUP: '/auth/signup',
    USERS_ME: '/users/me',
    USERS_PASSWORD: '/users/password',
    ASSETS: '/assets/',
    MARKET_SEARCH: '/market/search',
    PRICES_REFRESH: '/prices/refresh/',
    POSITIONS: '/positions/',
    TRANSACTIONS: '/transactions/',
    PORTFOLIO_HISTORY: '/portfolio/history',
    PORTFOLIO_SNAPSHOT: '/portfolio/snapshot',
    PORTFOLIO_SUMMARY: '/portfolio/summary',
    NOTIFICATIONS: '/users/me/settings',
};

// --- Generic Request Helper ---

/**
 * Generic helper for making authenticated API requests.
 * Automatically adds the `Authorization` header if a token exists.
 *
 * @template T The expected response type.
 * @param {string} path The API endpoint path (relative to BASE_URL).
 * @param {RequestInit} [config={}] Optional fetch configuration.
 * @returns {Promise<T>} The parsed JSON response.
 * @throws {Error} If the response status is not OK.
 */
async function request<T>(path: string, config: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem(STORAGE_KEY_ACCESS_TOKEN);
    const devUserId = localStorage.getItem(STORAGE_KEY_USER_ID) || '1';

    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        'X-User-Id': devUserId,
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...config.headers,
    };

    const response = await fetch(`${BASE_URL}${path}`, {
        ...config,
        headers,
    });

    if (!response.ok) {
        // Handle 401 Unauthorized
        if (response.status === 401) {
            localStorage.removeItem(STORAGE_KEY_ACCESS_TOKEN);
            localStorage.removeItem(STORAGE_KEY_USER_ID);

            // Redirect to login page only if we are in a browser environment
            if (typeof window !== 'undefined') {
                window.location.href = '/login';
            }
            throw new Error('Unauthorized');
        }

        // Try to get error message from body
        let errorMessage = `Request failed with status ${response.status}`;
        try {
            const errorBody = await response.text();
            if (errorBody) {
                // Try to parse JSON error if possible
                try {
                    const jsonError = JSON.parse(errorBody);
                    if (jsonError.detail) {
                        errorMessage = Array.isArray(jsonError.detail)
                            ? JSON.stringify(jsonError.detail)
                            : jsonError.detail;
                    } else {
                        errorMessage = errorBody;
                    }
                } catch {
                    errorMessage = errorBody;
                }
            }
        } catch (e) {
            // ignore text reading error (e.g. empty body)
        }
        throw new Error(errorMessage);
    }

    // Handle 204 No Content
    if (response.status === 204) {
        return {} as T;
    }

    return await response.json();
}

// --- Types ---

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

export interface UserRead {
    id: number | string; // Supporting both for now
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
    nickname?: string;
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

export interface SymbolSearchResult {
    symbol: string;
    longname?: string;
    shortname?: string;
    quoteType?: string;
    exchange?: string;
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

export interface PortfolioSummary {
    totalValuation: number;
    totalProfitLoss: number;
    totalReturnRate: number;
    totalInvested: number;
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

// --- API Functions ---

/**
 * Logs in a user and returns an access token.
 * Note: Uses URLSearchParams for body as per OAuth2 spec (or default FastAPI behavior).
 */
export async function login(credentials: UserLogin): Promise<Token> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${BASE_URL}${API_ENDPOINTS.LOGIN}`, {
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

/**
 * Registers a new user.
 */
export function signup(user: UserCreate): Promise<UserRead> {
    return request<UserRead>(API_ENDPOINTS.SIGNUP, {
        method: 'POST',
        body: JSON.stringify(user),
    });
}

/**
 * Updates the current user's profile information.
 */
export function updateProfile(data: UserUpdate): Promise<UserRead> {
    return request<UserRead>(API_ENDPOINTS.USERS_ME, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
}

/**
 * Changes the current user's password.
 */
export function changePassword(data: UserPasswordUpdate): Promise<void> {
    return request<void>(API_ENDPOINTS.USERS_PASSWORD, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * Fetches the list of assets. Returns empty list on failure.
 */
export function getAssets(): Promise<Asset[]> {
    return request<Asset[]>(API_ENDPOINTS.ASSETS).catch(error => {
        console.warn('Failed to fetch assets, returning empty list.', error);
        return [];
    });
}

/**
 * Creates a new asset.
 */
export function createAsset(asset: AssetCreate): Promise<Asset> {
    return request<Asset>(API_ENDPOINTS.ASSETS, {
        method: 'POST',
        body: JSON.stringify(asset),
    });
}

/**
 * Searches for a stock/crypto symbol.
 */
export function searchSymbol(query: string): Promise<SymbolSearchResult[]> {
    return request<SymbolSearchResult[]>(`${API_ENDPOINTS.MARKET_SEARCH}?q=${encodeURIComponent(query)}`);
}

/**
 * Triggers a price refresh for all assets.
 */
export function refreshPrices(): Promise<void> {
    return request<void>(API_ENDPOINTS.PRICES_REFRESH, { method: 'POST' });
}

/**
 * Fetches all positions. Returns empty list on failure.
 */
export function getPositions(): Promise<Position[]> {
    return request<Position[]>(API_ENDPOINTS.POSITIONS).catch(error => {
        console.warn('Failed to fetch positions, returning empty list.', error);
        return [];
    });
}

/**
 * Fetches a single position by ID.
 */
export function getPosition(id: number): Promise<Position> {
    return request<Position>(`${API_ENDPOINTS.POSITIONS}${id}/`);
}

/**
 * Creates a new position.
 */
export function createPosition(position: PositionCreate): Promise<Position> {
    return request<Position>(API_ENDPOINTS.POSITIONS, {
        method: 'POST',
        body: JSON.stringify(position),
    });
}

/**
 * Updates a position.
 */
export function updatePosition(id: number, position: PositionUpdate): Promise<Position> {
    return request<Position>(`${API_ENDPOINTS.POSITIONS}${id}/`, {
        method: 'PUT',
        body: JSON.stringify(position),
    });
}

/**
 * Deletes a position.
 */
export function deletePosition(id: number): Promise<void> {
    return request<void>(`${API_ENDPOINTS.POSITIONS}${id}/`, { method: 'DELETE' });
}

/**
 * Fetches transaction history with pagination.
 */
export function getTransactions(skip = 0, limit = 100): Promise<Transaction[]> {
    return request<Transaction[]>(`${API_ENDPOINTS.TRANSACTIONS}?skip=${skip}&limit=${limit}`);
}

/**
 * Records a new transaction (BUY/SELL).
 */
export function createTransaction(data: CreateTransaction): Promise<Transaction> {
    return request<Transaction>(API_ENDPOINTS.TRANSACTIONS, {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * Fetches portfolio value history.
 */
export function getPortfolioHistory(skip = 0, limit = 30): Promise<PortfolioHistory[]> {
    return request<PortfolioHistory[]>(`${API_ENDPOINTS.PORTFOLIO_HISTORY}?skip=${skip}&limit=${limit}`);
}

/**
 * Creates a snapshot of the current portfolio state.
 */
export function createPortfolioSnapshot(): Promise<void> {
    return request<void>(API_ENDPOINTS.PORTFOLIO_SNAPSHOT, { method: 'POST' });
}

/**
 * Fetches the portfolio summary (total value, profit/loss, etc).
 */
export function getPortfolioSummary(): Promise<PortfolioResponse> {
    return request<PortfolioResponse>(API_ENDPOINTS.PORTFOLIO_SUMMARY);
}

/**
 * Fetches notification settings for the user.
 */
export function getNotificationSettings(): Promise<NotificationSettings> {
    return request<NotificationSettings>(API_ENDPOINTS.NOTIFICATIONS);
}

/**
 * Updates notification settings.
 */
export function updateNotificationSettings(settings: NotificationSettingsUpdate): Promise<NotificationSettings> {
    return request<NotificationSettings>(API_ENDPOINTS.NOTIFICATIONS, {
        method: 'POST',
        body: JSON.stringify(settings),
    });
}

/**
 * Client-side calculation of portfolio summary (fallback/utility).
 */
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

