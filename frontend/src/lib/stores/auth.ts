import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface User {
    email: string;
    nickname?: string;
    // Add other user properties if needed
}

function createAuthStore() {
    const { subscribe, set, update } = writable<{ isAuthenticated: boolean; token: string | null; user: User | null }>({
        isAuthenticated: false,
        token: null,
        user: null,
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
