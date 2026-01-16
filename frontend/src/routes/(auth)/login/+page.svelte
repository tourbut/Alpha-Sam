<script lang="ts">
    import { login, get_me } from "$lib/apis/auth";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";

    let email = "";
    let password = "";
    let error = "";
    let isLoading = false;

    async function handleSubmit() {
        try {
            error = "";
            isLoading = true;
            const data = await login({ username: email, password });

            // Set token temporarily to fetch user info
            auth.token = data.access_token;

            // Fetch full user info using the token (get_me imported from same module)
            const user = await get_me();

            auth.login(data.access_token, user);
            goto("/");
        } catch (e) {
            console.error("Login failed:", e);
            error = "Login failed. Please check your credentials.";
        } finally {
            isLoading = false;
        }
    }
</script>

<div
    class="min-h-screen w-full flex items-center justify-center bg-neutral-50 dark:bg-neutral-900 px-4 py-8 md:py-0"
>
    <div>
        <!-- Card Container - Theme Preview 기반 스타일 -->
        <div
            class="bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-lg transition-all duration-200 overflow-hidden"
        >
            <!-- Card Content -->
            <div class="p-8 space-y-8">
                <!-- Header -->
                <div class="space-y-2">
                    <h1
                        class="text-3xl font-bold text-neutral-900 dark:text-neutral-100"
                    >
                        Sign in
                    </h1>
                    <p
                        class="text-sm font-medium text-neutral-600 dark:text-neutral-400"
                    >
                        Welcome back to your portfolio
                    </p>
                </div>

                <!-- Form -->
                <form
                    class="space-y-6"
                    method="POST"
                    on:submit|preventDefault={handleSubmit}
                >
                    <!-- Email Field -->
                    <div class="space-y-2">
                        <label
                            for="email"
                            class="block text-sm font-semibold text-neutral-900 dark:text-neutral-100"
                        >
                            Email address
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="you@example.com"
                            required
                            bind:value={email}
                            disabled={isLoading}
                            aria-label="Email address"
                            aria-describedby="email-error"
                            aria-invalid={error ? "true" : "false"}
                            class="w-full px-4 py-3 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 placeholder-neutral-600 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-neutral-900 focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        />
                        {#if error}
                            <div
                                id="email-error"
                                role="alert"
                                class="text-xs text-red-600 dark:text-red-400"
                            ></div>
                        {/if}
                    </div>

                    <!-- Password Field -->
                    <div class="space-y-2">
                        <label
                            for="password"
                            class="block text-sm font-semibold text-neutral-900 dark:text-neutral-100"
                        >
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            placeholder="••••••••"
                            required
                            bind:value={password}
                            disabled={isLoading}
                            aria-label="Password"
                            aria-describedby="password-error"
                            aria-invalid={error ? "true" : "false"}
                            class="w-full px-4 py-3 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100 placeholder-neutral-600 dark:placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-neutral-900 focus:border-transparent transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        />
                        {#if error}
                            <div
                                id="password-error"
                                role="alert"
                                class="text-xs text-red-600 dark:text-red-400"
                            ></div>
                        {/if}
                    </div>

                    <!-- Error Message -->
                    {#if error}
                        <div
                            role="alert"
                            class="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/50"
                        >
                            <p
                                class="text-sm font-medium text-red-800 dark:text-red-300"
                            >
                                ✕ {error}
                            </p>
                        </div>
                    {/if}

                    <!-- Submit Button - Theme Preview 기반 -->
                    <button
                        type="submit"
                        disabled={isLoading}
                        aria-busy={isLoading}
                        class="w-full px-4 py-3 bg-primary-600 hover:bg-primary-500 active:bg-primary-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 dark:focus:ring-offset-neutral-900 border border-primary-600 hover:border-primary-500 min-h-12"
                    >
                        {#if isLoading}
                            <span class="inline-flex items-center gap-2">
                                <span
                                    class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                                ></span>
                                Signing in...
                            </span>
                        {:else}
                            Sign in
                        {/if}
                    </button>
                </form>

                <!-- Divider - Theme Preview 기반 -->
                <div class="relative flex items-center">
                    <div
                        class="flex-grow border-t border-neutral-300 dark:border-neutral-600"
                    ></div>
                    <span
                        class="px-3 text-xs font-medium text-neutral-500 dark:text-neutral-400 bg-white dark:bg-neutral-800"
                    >
                        Don't have an account?
                    </span>
                    <div
                        class="flex-grow border-t border-neutral-300 dark:border-neutral-600"
                    ></div>
                </div>

                <!-- Sign Up Link - Theme Preview 기반 -->
                <a
                    href="/signup"
                    class="block w-full px-4 py-3 text-center border-2 border-primary-600 text-primary-600 dark:text-primary-400 font-semibold rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2 dark:focus:ring-offset-neutral-900 min-h-12 flex items-center justify-center"
                >
                    Create account
                </a>
            </div>
        </div>

        <!-- Footer - 엔터프라이즈 보안 메시지 -->
        <p
            class="text-center text-xs font-medium text-neutral-500 dark:text-neutral-400 mt-6"
        >
            Protected by enterprise-grade security
        </p>
    </div>
</div>
