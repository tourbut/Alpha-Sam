<script lang="ts">
    import {
        Navbar,
        NavBrand,
        NavLi,
        NavUl,
        NavHamburger,
        Button,
        DarkMode,
    } from "flowbite-svelte";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";
    import { APP_NAME } from "$lib/constants";

    let hidden = $state(true); // 모바일 메뉴 기본 비활성화

    function toggle() {
        hidden = !hidden;
    }

    function handleLogout() {
        auth.logout();
        goto("/login");
    }
</script>

<Navbar
    fluid={true}
    class="fixed w-screen z-20 top-0 left-0 border-b border-neutral-200 dark:border-neutral-700 px-4 py-2.5 bg-white dark:bg-neutral-800"
>
    <NavBrand href="/">
        <span
            class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
        >
            {APP_NAME}
        </span>
    </NavBrand>

    <div class="flex items-center md:order-2 space-x-3">
        <DarkMode
            class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600 rounded-lg text-sm p-2.5"
            aria-label="Toggle dark mode"
        />

        {#if auth.isAuthenticated}
            {#if auth.user}
                <div
                    class="hidden lg:flex items-center gap-2 text-sm font-medium text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full border border-gray-200 dark:border-gray-600"
                >
                    <span>👤 {auth.user.nickname || auth.user.email}</span>
                </div>
            {/if}
            <Button
                size="xs"
                color="light"
                class="border-0 hidden md:block"
                onclick={handleLogout}
            >
                Logout
            </Button>
        {:else}
            <div class="flex items-center gap-2">
                <Button href="/login" size="xs">Login</Button>
                <Button href="/signup" size="xs" color="alternative"
                    >Sign up</Button
                >
            </div>
        {/if}
        <NavHamburger onclick={toggle} class="md:hidden" />
    </div>

    <NavUl
        {hidden}
        class="justify-between hidden w-full md:flex md:w-auto md:order-1"
    >
        {#if auth.isAuthenticated}
            <NavLi href="/">Dashboard</NavLi>
            <NavLi href="/portfolios">Portfolios</NavLi>
            <NavLi href="/social/leaderboard">Leaderboard</NavLi>
            <NavLi href="/settings">Settings</NavLi>
            <NavLi
                href="#"
                class="cursor-pointer md:hidden"
                onclick={handleLogout}
            >
                Logout
            </NavLi>
        {:else}
            <NavLi href="/login" class="md:hidden">Login</NavLi>
            <NavLi href="/signup" class="md:hidden">Sign up</NavLi>
        {/if}
    </NavUl>
</Navbar>
