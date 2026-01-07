import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { UserRead } from '$lib/types';

function createAuthStore() {
    const { subscribe, set, update } = writable<{ isAuthenticated: boolean; token: string | null; user: UserRead | null }>({
        isAuthenticated: false,
        token: null,
        user: null,
    });

    return {
        subscribe,
        login: (token: string, user: UserRead) => {
            if (browser) {
                localStorage.setItem('access_token', token);
                // Store minimal user info or full object, ensuring it matches UserRead structure
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
                    try {
                        const user: UserRead = JSON.parse(userStr);
                        // Basic validation if needed
                        if (user && user.email) {
                            set({ isAuthenticated: true, token, user });
                        } else {
                            throw new Error("Invalid user data");
                        }
                    } catch (e) {
                        console.error("Failed to restore auth state:", e);
                        localStorage.removeItem('access_token');
                        localStorage.removeItem('user');
                        set({ isAuthenticated: false, token: null, user: null });
                    }
                }
            }
        },
        updateUser: (updates: Partial<UserRead>) => {
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
