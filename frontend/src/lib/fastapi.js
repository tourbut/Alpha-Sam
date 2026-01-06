import { API_URL } from '$lib/constants';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';
import { browser } from '$app/environment';

/**
 * Creates an API function bound to a router and endpoint.
 * @param {string} router - The router prefix (e.g., 'assets', 'users').
 * @param {string} method - HTTP method ('get', 'post', 'put', 'delete') or 'login'.
 * @param {string} endpoint - The endpoint path (e.g., '', 'search', '{id}').
 */
export const api_router = (router, method, endpoint) => {
    return async (params = {}, success_callback, failure_callback) => {
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
        // If processedEndpoint is empty string, we might just append '/' if backend expects it
        if (processedEndpoint) {
            url += `/${processedEndpoint}`;
        }

        // Ensure trailing slash for REST consistency if not query param
        // (FastAPI strictly redirects without it usually, but let's see)
        // Actually, if endpoint was empty, we currently look like `/api/v1/router`
        // Should likely be `/api/v1/router/`
        if (!url.endsWith('/')) {
            url += '/';
        }

        // 2. Prepare Fetch Options
        let options = {
            method: method === 'login' ? 'POST' : fetchMethod,
            headers: {},
        };

        // Dev User ID (from localStorage)
        // FIXED: Removed to prevent Data Leak (User 1 default).
        // if (browser) {
        //     const devUserId = localStorage.getItem('dev_user_id') || '1';
        //     options.headers['X-User-Id'] = devUserId;
        // }

        // Auth Header (from store)
        const $auth = get(auth);
        if ($auth.token) {
            options.headers['Authorization'] = `Bearer ${$auth.token}`;
        }

        // 3. Handle Body / Query Params
        if (method === 'login') {
            options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
            const formData = new URLSearchParams();
            Object.entries(requestParams).forEach(([k, v]) => {
                if (v !== undefined && v !== null) formData.append(k, String(v));
            });
            options.body = formData;
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
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(requestParams);
        }

        // 4. Execute Request
        try {
            console.log(`API Request: ${method} ${url}`, { headers: options.headers });
            const response = await fetch(url, options);

            if (!response.ok) {
                // Handle 401
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
