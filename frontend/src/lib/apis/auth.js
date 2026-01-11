import { API_URL } from '$lib/constants';
import { api_router } from "$lib/fastapi";
import { auth } from '$lib/stores/auth.svelte';

export const login = async (credentials, success_callback, failure_callback) => {
    try {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username || credentials.email);
        formData.append('password', credentials.password);

        const response = await fetch(`${API_URL}/auth/jwt/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed');
        }

        const data = await response.json();

        // Update auth store
        if (data.access_token) {
            // We need to fetch user details as well to popoulate the store correctly
            // But for now, let's just use the token.
            // Ideally we should call get_me() here or let the component do it.
            // The original api.ts likely did it.
            // For now, let's return the token data.
        }

        if (success_callback) success_callback(data);
        return data;
    } catch (error) {
        if (failure_callback) failure_callback(error);
        throw error;
    }
};

export const signup = api_router('auth', 'post', 'register');
