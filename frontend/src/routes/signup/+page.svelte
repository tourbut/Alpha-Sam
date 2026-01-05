<script lang="ts">
    import { Card, Button, Label, Input, Checkbox } from "flowbite-svelte";
    import { signup, login } from "$lib/apis/auth";
    import { auth } from "$lib/stores/auth";
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
            auth.login(data.access_token, { email });
            goto("/");
        } catch (e: any) {
            error = "Signup failed. " + (e.message || "");
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
                Create an account
            </h1>
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
                    <div class="text-red-500 text-sm">{error}</div>
                {/if}

                <Button type="submit" class="w-full">Create an account</Button>
                <p class="text-sm font-light text-gray-500 dark:text-gray-400">
                    Already have an account? <a
                        href="/login"
                        class="font-medium text-primary-600 hover:underline dark:text-primary-500"
                        >Login here</a
                    >
                </p>
            </form>
        </div>
    </div>
</div>
