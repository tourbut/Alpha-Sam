<script lang="ts">
    import { Card, Button, Label, Input, Checkbox } from "flowbite-svelte";
    import { signup, login, get_me } from "$lib/apis/auth";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";

    let email = "";
    let password = "";
    let confirmPassword = "";
    let fullName = "";
    let error = "";

    async function handleSubmit() {
        if (password !== confirmPassword) {
            error = "Passwords do not match";
            return;
        }

        try {
            error = "";
            await signup({ email, password, full_name: fullName });

            // Auto login after signup
            const data = await login({ username: email, password });
            auth.token = data.access_token;
            const user = await get_me();
            auth.login(data.access_token, user);
            goto("/");
        } catch (e: any) {
            error = "Signup failed. " + (e.message || "");
        }
    }
</script>

<div
    class="min-h-screen w-full flex flex-col items-center justify-center px-4 py-8 bg-neutral-50 dark:bg-neutral-900"
>
    <div
        class="w-full max-w-md bg-white dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-lg transition-all duration-200 overflow-hidden"
    >
        <div class="p-8 space-y-8">
            <div class="space-y-2">
                <h1
                    class="text-3xl font-bold text-neutral-900 dark:text-neutral-100"
                >
                    Create account
                </h1>
                <p
                    class="text-sm font-medium text-neutral-600 dark:text-neutral-400"
                >
                    Join Alpha-Sam to start managing your portfolio
                </p>
            </div>
            <form
                class="space-y-4 md:space-y-6"
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
                    <Label for="fullName" class="mb-2">Full Name</Label>
                    <Input
                        type="text"
                        name="fullName"
                        id="fullName"
                        placeholder="John Doe"
                        bind:value={fullName}
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
                <div>
                    <Label for="confirmPassword" class="mb-2"
                        >Confirm password</Label
                    >
                    <Input
                        type="password"
                        name="confirmPassword"
                        id="confirmPassword"
                        placeholder="••••••••"
                        required
                        bind:value={confirmPassword}
                    />
                </div>

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

                <button
                    type="submit"
                    class="w-full px-4 py-3 bg-primary-600 hover:bg-primary-500 active:bg-primary-700 text-white font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 dark:focus:ring-offset-neutral-900 border border-primary-600 hover:border-primary-500 min-h-12"
                >
                    Create account
                </button>

                <div class="relative flex items-center">
                    <div
                        class="flex-grow border-t border-neutral-300 dark:border-neutral-600"
                    ></div>
                    <span
                        class="px-3 text-xs font-medium text-neutral-500 dark:text-neutral-400 bg-white dark:bg-neutral-800"
                    >
                        Already have an account?
                    </span>
                    <div
                        class="flex-grow border-t border-neutral-300 dark:border-neutral-600"
                    ></div>
                </div>

                <a
                    href="/login"
                    class="block w-full px-4 py-3 text-center border-2 border-primary-600 text-primary-600 dark:text-primary-400 font-semibold rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:ring-offset-2 dark:focus:ring-offset-neutral-900 min-h-12 flex items-center justify-center"
                >
                    Sign in instead
                </a>
            </form>
        </div>
    </div>
</div>
