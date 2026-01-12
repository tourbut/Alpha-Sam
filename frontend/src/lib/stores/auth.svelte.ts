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
        console.log("AuthStore.login: Starting login process...");
        if (browser) {
            localStorage.setItem('access_token', token);
            localStorage.setItem('user', JSON.stringify(user));
            console.log("AuthStore.login: Token and User saved to localStorage");
        }
        this.isAuthenticated = true;
        this.token = token;
        this.user = user;
        console.log("AuthStore.login: State updated - isAuthenticated:", this.isAuthenticated, "Token exists:", !!this.token);
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
        console.log("AuthStore.initialize: Checking browser environment...");
        if (browser) {
            const token = localStorage.getItem('access_token');
            const userStr = localStorage.getItem('user');
            console.log("AuthStore.initialize: localStorage check - Token exists:", !!token, "User exists:", !!userStr);
            if (token && userStr) {
                try {
                    const user: UserRead = JSON.parse(userStr);
                    if (user && user.email) {
                        this.isAuthenticated = true;
                        this.token = token;
                        this.user = user;
                        console.log("AuthStore.initialize: Success - User email:", user.email);
                    } else {
                        throw new Error("Invalid user data in storage");
                    }
                } catch (e) {
                    console.error("AuthStore.initialize: Failed to restore auth state:", e);
                    this.logout();
                }
            } else {
                console.log("AuthStore.initialize: No credentials found in storage.");
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
