import { browser } from '$app/environment';
import type { UserRead } from '$lib/types';

class AuthStore {
    isAuthenticated = $state(false);
    token = $state<string | null>(null);
    user = $state<UserRead | null>(null);

    constructor() {
        this.initialize();
    }

    login(token: string, user: UserRead) {
        if (browser) {
            localStorage.setItem('access_token', token);
            localStorage.setItem('user', JSON.stringify(user));
        }
        this.isAuthenticated = true;
        this.token = token;
        this.user = user;
    }

    logout() {
        if (browser) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
        }
        this.isAuthenticated = false;
        this.token = null;
        this.user = null;
    }

    initialize() {
        if (browser) {
            const token = localStorage.getItem('access_token');
            const userStr = localStorage.getItem('user');
            if (token && userStr) {
                try {
                    const user: UserRead = JSON.parse(userStr);
                    if (user && user.email) {
                        this.isAuthenticated = true;
                        this.token = token;
                        this.user = user;
                    } else {
                        throw new Error("Invalid user data");
                    }
                } catch (e) {
                    console.error("Failed to restore auth state:", e);
                    this.logout();
                }
            }
        }
    }

    updateUser(updates: Partial<UserRead>) {
        if (this.user) {
            const newUser = { ...this.user, ...updates };
            if (browser) {
                localStorage.setItem('user', JSON.stringify(newUser));
            }
            this.user = newUser;
        }
    }
}

export const auth = new AuthStore();
