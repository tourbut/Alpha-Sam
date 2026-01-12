import { API_URL } from '$lib/constants';
import { auth } from '$lib/stores/auth.svelte';

import { browser } from '$app/environment';

/**
 * Creates an API function bound to a router and endpoint.
 * @param {string} router - The router prefix (e.g., 'assets', 'users').
 * @param {string} method - HTTP method ('get', 'post', 'put', 'delete') or 'login'.
 * @param {string} endpoint - The endpoint path (e.g., '', 'search', '{id}').
 */
export const api_router = (router: string, method: string, endpoint: string) => {
    return async (params: Record<string, any> = {}, success_callback?: (data: any) => void, failure_callback?: (err: any) => void) => {
        const fetchMethod = method.toUpperCase();
        let url = `${API_URL}/${router}`;

        // Clone params to avoid mutation
        const requestParams = { ...params };

        // 1. Handle Path Parameters (e.g., {id})
        // If endpoint contains {key}, replace with param value and delete from requestParams
        // Note: We handle the trailing slash logic carefully.

        let processedEndpoint = endpoint;
        const pathParamMatches = processedEndpoint.match(/{([^}]+)}/g);

        if (pathParamMatches) {
            pathParamMatches.forEach(match => {
                const paramName = match.slice(1, -1); // remove { and }
                if (requestParams[paramName] !== undefined) {
                    processedEndpoint = processedEndpoint.replace(match, requestParams[paramName]);
                    delete requestParams[paramName];
                } else {
                    console.warn(`Missing path parameter: ${paramName}`);
                }
            });
        }

        // Append endpoint to URL
        if (processedEndpoint) {
            url += `/${processedEndpoint}`;
        }

        // REMOVED: Automatic trailing slash. FastAPI routes might not expect it, 
        // and redirects can lose Authorization headers in some client configurations.
        /*
        if (!url.endsWith('/')) {
            url += '/';
        }
        */

        // 2. Prepare Fetch Options
        let options: RequestInit = {
            method: method === 'login' ? 'POST' : fetchMethod,
            headers: {} as Record<string, string>,
        };

        // Dev User ID (from localStorage)
        // FIXED: Removed to prevent Data Leak (User 1 default).
        // if (browser) {
        //     const devUserId = localStorage.getItem('dev_user_id') || '1';
        //     options.headers['X-User-Id'] = devUserId;
        // }

        // Auth Header (from store)
        console.log(`Checking Auth Token for ${url}:`, auth.token ? "PRESENT" : "MISSING");
        if (auth.token) {
            (options.headers as Record<string, string>)['Authorization'] = `Bearer ${auth.token}`;
        }

        // 3. Handle Body / Query Params
        if (method === 'login') {
            (options.headers as Record<string, string>)['Content-Type'] = 'application/x-www-form-urlencoded';
            const formData = new URLSearchParams();

            // Map email to username for OAuth2 compliance if needed
            const loginParams = { ...requestParams };
            if (loginParams.email && !loginParams.username) {
                loginParams.username = loginParams.email;
                delete loginParams.email;
            }

            Object.entries(loginParams).forEach(([k, v]) => {
                if (v !== undefined && v !== null) formData.append(k, String(v));
            });
            options.body = formData;
            console.log(`Login Request Data:`, formData.toString());
        } else if (fetchMethod === 'GET') {
            const searchParams = new URLSearchParams();
            Object.entries(requestParams).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    searchParams.append(key, String(value));
                }
            });
            const queryString = searchParams.toString();
            // If query string exists, remove trailing slash from URL if preferred, or keep it.
            // FastAPI is usually fine with `/assets/?q=...`
            if (queryString) {
                // Remove trailing slash if it precedes '?' is sometimes cleaner, but keeping it is safer for FastAPI default router
                url += `?${queryString}`;
            }
        } else {
            // POST, PUT, DELETE (JSON)
            (options.headers as Record<string, string>)['Content-Type'] = 'application/json';
            options.body = JSON.stringify(requestParams);
        }

        // 4. Execute Request
        try {
            console.log(`API Request: ${method} ${url}`, { headers: options.headers });
            const response = await fetch(url, options);

            if (!response.ok) {
                // Handle 401
                console.log(response.status);
                if (response.status === 401) {
                    if (browser) {
                        auth.logout();
                        window.location.href = '/login';
                    }
                    throw new Error('Unauthorized');
                }

                // Parse Error
                const errorText = await response.text();
                let errorDetail = errorText;
                try {
                    const jsonError = JSON.parse(errorText);
                    if (jsonError.detail) {
                        errorDetail = typeof jsonError.detail === 'object'
                            ? JSON.stringify(jsonError.detail)
                            : jsonError.detail;
                    }
                } catch (e) {
                    // unexpected error format
                }
                throw new Error(errorDetail);
            }

            // Handle 204 No Content
            let data = null;
            if (response.status !== 204) {
                data = await response.json();
            }

            // Success Callback
            if (success_callback) success_callback(data);
            return data;

        } catch (error) {
            // Failure Callback
            if (failure_callback) failure_callback(error);
            throw error;
        }
    };
};
