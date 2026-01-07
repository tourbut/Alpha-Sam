<script lang="ts">
    import { onMount } from "svelte";
    import { Card, Button, Label, Input, Checkbox } from "flowbite-svelte";
    import { login } from "$lib/apis/auth";
    import { get_me } from "$lib/apis/users";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import type { UserRead } from "$lib/types";

    let email = "";
    let password = "";
    let error = "";
    let rememberMe = false;

    onMount(() => {
        const savedEmail = localStorage.getItem("savedEmail");
        if (savedEmail) {
            email = savedEmail;
            rememberMe = true;
        }
    });

    async function handleSubmit() {
        console.log("Login attempt starting...", { email, rememberMe });
        try {
            error = "";
            console.log("Calling login API...");
            // api_router('auth', 'login', 'jwt/login') returns { access_token, token_type }
            const data = await login({ username: email, password });
            console.log("Login API success:", data);

            if (rememberMe) {
                console.log("Saving email to localStorage");
                localStorage.setItem("savedEmail", email);
            } else {
                console.log("Removing email from localStorage");
                localStorage.removeItem("savedEmail");
            }

            // 1. Initial Login with minimal data to set token in store/localStorage
            // This allows api_router (which reads store) to include the token in headers
            const tempUser: UserRead = {
                id: 0,
                email: email,
                is_active: true,
                is_superuser: false,
                is_verified: false,
            };
            auth.login(data.access_token, data.user);

            try {
                console.log("Navigating to dashboard...");

                await goto("/");
                console.log($auth.isAuthenticated);
                console.log("Navigation called.");
            } catch (userError) {
                console.error("Failed to fetch user details:", userError);
                // CRITICAL: Rollback if profile fetch fails to avoid partial login state
                auth.logout();
                error =
                    "Login succeeded but failed to load profile. Please try again.";
            }
        } catch (e) {
            console.error("Login Error:", e);
            error = "Login failed. Please check your credentials.";
        }
    }
</script>

<div
    class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
>
    <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
    >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
            <h1
                class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
            >
                Sign in to your account
            </h1>
            <form
                class="space-y-4 md:space-y-6"
                method="POST"
                on:submit|preventDefault={handleSubmit}
            >
                <div>
                    <Label for="email" class="mb-2">Your email</Label>
                    <Input
                        type="email"
                        name="email"
                        id="email"
                        placeholder="name@company.com"
                        required
                        bind:value={email}
                    />
                </div>
                <div>
                    <Label for="password" class="mb-2">Password</Label>
                    <Input
                        type="password"
                        name="password"
                        id="password"
                        placeholder="••••••••"
                        required
                        bind:value={password}
                    />
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-start">
                        <Checkbox bind:checked={rememberMe}
                            >Remember ID</Checkbox
                        >
                    </div>
                </div>

                {#if error}
                    <div class="text-red-500 text-sm">{error}</div>
                {/if}

                <Button type="submit" class="w-full">Sign in</Button>
                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    Don’t have an account yet? <a
                        href="/signup"
                        class="font-medium text-primary-600 hover:underline dark:text-primary-500"
                        >Sign up</a
                    >
                </p>
            </form>
        </div>
    </div>
</div>
