
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import * as api from './api';
import { BASE_URL } from './api';

// Mock localStorage
const localStorageMock = (function () {
    let store: { [key: string]: string } = {};
    return {
        getItem: function (key: string) {
            return store[key] || null;
        },
        setItem: function (key: string, value: string) {
            store[key] = value.toString();
        },
        clear: function () {
            store = {};
        },
        removeItem: function (key: string) {
            delete store[key];
        },
    };
})();

Object.defineProperty(global, 'localStorage', {
    value: localStorageMock,
});

// Mock fetch
const fetchMock = vi.fn();
global.fetch = fetchMock;

describe('api.ts', () => {
    beforeEach(() => {
        localStorage.clear();
        fetchMock.mockClear();
    });

    it('getAssets should fetch assets with correct headers', async () => {
        const mockAssets = [{ id: 1, symbol: 'AAPL', name: 'Apple' }];
        fetchMock.mockResolvedValueOnce({
            ok: true,
            json: async () => mockAssets,
        });

        localStorage.setItem('access_token', 'fake-token');

        const assets = await api.getAssets();

        expect(fetchMock).toHaveBeenCalledWith(`${BASE_URL}/assets/`, expect.objectContaining({
            headers: expect.objectContaining({
                'Authorization': 'Bearer fake-token',
                'Content-Type': 'application/json',
            }),
        }));
        expect(assets).toEqual(mockAssets);
    });

    it('login should post credentials and return token', async () => {
        const mockToken = { access_token: 'new-token', token_type: 'bearer' };
        fetchMock.mockResolvedValueOnce({
            ok: true,
            json: async () => mockToken,
        });

        const credentials = { username: 'test@example.com', password: 'password' };
        const token = await api.login(credentials);

        expect(fetchMock).toHaveBeenCalledWith(`${BASE_URL}/auth/jwt/login`, expect.objectContaining({
            method: 'POST',
            body: expect.any(URLSearchParams),
        }));
        expect(token).toEqual(mockToken);
    });

    it('signup should post user data', async () => {
        const mockUser = { id: 1, email: 'test@test.com', is_active: true };
        fetchMock.mockResolvedValueOnce({
            ok: true,
            json: async () => mockUser
        });

        await api.signup({ email: 'test@test.com', password: 'pw' });

        expect(fetchMock).toHaveBeenCalledWith(`${BASE_URL}/auth/signup`, expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ email: 'test@test.com', password: 'pw' })
        }));
    });

    it('should handle errors gracefully', async () => {
        fetchMock.mockResolvedValueOnce({
            ok: false,
            status: 400,
            text: async () => JSON.stringify({ detail: 'Bad Request' }),
        });

        await expect(api.createAsset({ symbol: 'X', name: 'X', category: 'X' })).rejects.toThrow('Bad Request');
    });
});
