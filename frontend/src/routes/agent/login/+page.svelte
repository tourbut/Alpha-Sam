<script lang="ts">
    import { API_URL } from "$lib/constants";
    import { api_router } from "$lib/fastapi";
    import { auth } from "$lib/stores/auth.svelte";

    let result = $state("");
    let error = $state("");
    let accessToken = $state("");

    // API Tester State
    let reqMethod = $state("GET");
    let reqUrl = $state("/portfolios");
    let reqBody = $state("");
    let apiResult = $state("");
    let apiError = $state("");

    async function handleSubmit(event: Event) {
        event.preventDefault();
        const form = event.target as HTMLFormElement;
        const formData = new FormData(form);

        const urlEncodedData = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            urlEncodedData.append(key, value.toString());
        }

        try {
            const _agentLogin = api_router('agent', 'login', '');
            const data = await _agentLogin(Object.fromEntries(formData));

            accessToken = data.access_token;
            auth.token = accessToken; // Set global token so api_router can pick it up

            // Only show the api_docs to keep it clean, drop token text from screen
            result = JSON.stringify(data.api_docs, null, 2);
            error = "";
        } catch (err: any) {
            error = err.message;
            result = "";
        }
    }

    async function handleApiTest(event: Event) {
        event.preventDefault();
        apiResult = "Loading...";
        apiError = "";

        try {
            // Remove leading slash for api_router and construct router logic
            const cleanUrl = reqUrl.startsWith("/") ? reqUrl.substring(1) : reqUrl;
            // Split if URL contains path parameters or just use trailing as router and '' as endpoint
            const test_api = api_router(cleanUrl, reqMethod.toLowerCase(), '');

            let params = {};
            if (reqMethod !== "GET" && reqMethod !== "DELETE" && reqBody.trim() !== "") {
                try {
                    params = JSON.parse(reqBody);
                } catch (e) {
                    apiError = "Invalid JSON format in body";
                    apiResult = "";
                    return;
                }
            } else if (reqMethod === "GET" && reqBody.trim() !== "") {
                // If it's a GET, parse body as query params, which api_router converts automatically
                try {
                    params = JSON.parse(reqBody);
                } catch (e) {
                    // Ignore or warn
                }
            }

            const data = await test_api(params);
            
            if (data === null) { // api_router returns null for 204 No Content
                apiResult = "Success (204 No Content)";
                return;
            }
            apiResult = JSON.stringify(data, null, 2);
        } catch (err: any) {
            apiError = err.message;
            apiResult = "";
        }
    }
</script>

<svelte:head>
    <title>Agent Login & API Interface</title>
</svelte:head>

<main class="max-w-4xl mx-auto p-6 mt-10">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-6">
        Agent Authentication & REST Interface
    </h1>

    {#if accessToken}
        <section
            class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md mb-8"
        >
            <h2
                class="text-xl font-semibold text-gray-900 dark:text-white mb-2"
            >
                1. Authentication Success
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-4">
                Token has been securely stored in memory. Below are the
                available API operations:
            </p>
            <pre
                id="agent-response"
                class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-300 p-4 rounded-lg max-h-64 overflow-y-auto whitespace-pre-wrap break-words text-sm font-mono border border-gray-200 dark:border-gray-700">{result}</pre>
        </section>

        <section class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <h2
                class="text-xl font-semibold text-gray-900 dark:text-white mb-2"
            >
                2. Agent API Tester
            </h2>
            <p class="text-gray-600 dark:text-gray-400 mb-4">
                Execute authorized API calls directly from this interface.
            </p>

            <form
                id="api-tester-form"
                onsubmit={handleApiTest}
                class="flex flex-col gap-4 mb-6"
            >
                <div class="flex flex-col sm:flex-row gap-4">
                    <select
                        id="req-method"
                        bind:value={reqMethod}
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white sm:w-32"
                    >
                        <option value="GET">GET</option>
                        <option value="POST">POST</option>
                        <option value="PUT">PUT</option>
                        <option value="DELETE">DELETE</option>
                        <option value="PATCH">PATCH</option>
                    </select>
                    <input
                        type="text"
                        id="req-url"
                        bind:value={reqUrl}
                        placeholder="/portfolios"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 flex-1 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        required
                    />
                    <button
                        type="submit"
                        id="submit-api-test"
                        class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-primary-600 dark:hover:bg-primary-700"
                        >Send Request</button
                    >
                </div>

                {#if reqMethod !== "GET" && reqMethod !== "DELETE"}
                    <textarea
                        id="req-body"
                        bind:value={reqBody}
                        placeholder="&#123;&quot;name&quot;: &quot;My Portfolio&quot;, &quot;currency&quot;: &quot;USD&quot;&#125;"
                        rows="6"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 p-2.5 font-mono dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    ></textarea>
                {/if}
            </form>

            {#if apiError}
                <div class="mt-4">
                    <h3
                        class="text-lg font-medium text-red-600 dark:text-red-400 mb-2"
                    >
                        API Error
                    </h3>
                    <pre
                        id="api-tester-error"
                        class="bg-red-50 dark:bg-red-900/30 text-red-800 dark:text-red-400 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap break-words text-sm font-mono border border-red-200 dark:border-red-800">{apiError}</pre>
                </div>
            {/if}

            {#if apiResult}
                <div class="mt-4">
                    <h3
                        class="text-lg font-medium text-gray-900 dark:text-white mb-2"
                    >
                        API Result
                    </h3>
                    <pre
                        id="api-tester-result"
                        class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-300 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap break-words text-sm font-mono border border-gray-200 dark:border-gray-700">{apiResult}</pre>
                </div>
            {/if}
        </section>
    {:else}
        <div
            class="max-w-[400px] w-full mx-auto bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md mt-10"
        >
            <h2
                class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center"
            >
                Agent Login
            </h2>
            <form
                id="agent-login-form"
                onsubmit={handleSubmit}
                class="flex flex-col gap-6"
            >
                <div class="w-full">
                    <label
                        for="username"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                    >
                        Username/Email
                    </label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                        required
                    />
                </div>
                <div class="w-full">
                    <label
                        for="password"
                        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                    >
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                        required
                    />
                </div>
                <button
                    type="submit"
                    id="submit-login"
                    class="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 w-full dark:bg-primary-600 dark:hover:bg-primary-700 mt-2"
                >
                    Access Interface
                </button>
            </form>

            {#if error}
                <p
                    id="error-message"
                    class="mt-4 text-sm text-red-600 dark:text-red-400 text-center font-medium"
                >
                    {error}
                </p>
            {/if}
        </div>
    {/if}
</main>
