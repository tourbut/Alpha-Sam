import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface User {
    email: string;
    nickname?: string;
    // Add other user properties if needed
}

function createAuthStore() {
    let initialIsAuthenticated = false;
    let initialToken: string | null = null;
    let initialUser: User | null = null;

    if (browser) {
        const token = localStorage.getItem('access_token');
        const userStr = localStorage.getItem('user');
        if (token) { // User might be null if just token exists? Assume we need both or just token implies auth?
            // Let's assume if token exists, we are tentatively auth, but user might be missing.
            // If user is missing, we might want to fetch it.
            // For now, adhere to previous logic: token && userStr
            if (userStr) {
                initialIsAuthenticated = true;
                initialToken = token;
                initialUser = JSON.parse(userStr);
            }
        }
    }

    const { subscribe, set, update } = writable<{ isAuthenticated: boolean; token: string | null; user: User | null }>({
        isAuthenticated: initialIsAuthenticated,
        token: initialToken,
        user: initialUser,
    });

    return {
        subscribe,
        login: (token: string, user: User) => {
            if (browser) {
                localStorage.setItem('access_token', token);
                localStorage.setItem('user', JSON.stringify(user));
            }
            set({ isAuthenticated: true, token, user });
        },
        logout: () => {
            if (browser) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
            }
            set({ isAuthenticated: false, token: null, user: null });
        },
        initialize: () => {
            // Redundant if we init on creation, but good for re-verification or if called manually
            if (browser) {
                const token = localStorage.getItem('access_token');
                const userStr = localStorage.getItem('user');
                if (token && userStr) {
                    set({ isAuthenticated: true, token, user: JSON.parse(userStr) });
                }
            }
        },
        updateUser: (updates: Partial<User>) => {
            update(state => {
                if (state.user) {
                    const newUser = { ...state.user, ...updates };
                    if (browser) {
                        localStorage.setItem('user', JSON.stringify(newUser));
                    }
                    return { ...state, user: newUser };
                }
                return state;
            });
        }
    };
}

export const auth = createAuthStore();
