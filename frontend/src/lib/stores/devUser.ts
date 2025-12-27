import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Development User Simulation Store
// Used to switch between users in development mode to test multi-tenancy.

export interface DevUser {
    id: number;
    name: string;
    role: 'admin' | 'user' | 'tester';
}

export const DEV_USERS: DevUser[] = [
    { id: 1, name: 'User 1 (Admin)', role: 'admin' },
    { id: 2, name: 'User 2 (Tester)', role: 'tester' },
    { id: 3, name: 'User 3 (New)', role: 'user' }
];

function createDevUserStore() {
    // Default to User 1 if not set
    const initialId = browser ? parseInt(localStorage.getItem('dev_user_id') || '1') : 1;
    const initialUser = DEV_USERS.find(u => u.id === initialId) || DEV_USERS[0];

    const { subscribe, set } = writable<DevUser>(initialUser);

    return {
        subscribe,
        switchUser: (userId: number) => {
            const user = DEV_USERS.find(u => u.id === userId);
            if (user) {
                if (browser) {
                    localStorage.setItem('dev_user_id', userId.toString());
                }
                set(user);
                // Force reload or just state update? 
                // Ideally state update, but for API headers to pick it up immediately in non-reactive functions, 
                // we might need to rely on localStorage in api.ts or subscribe there.
                // For simplicity, api.ts will read from localStorage.
            }
        }
    };
}

export const devUser = createDevUserStore();
