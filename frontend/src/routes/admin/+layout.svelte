<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { auth } from "$lib/stores/auth.svelte";
    import { Spinner } from "flowbite-svelte";
    import {
        Navbar,
        NavBrand,
        NavLi,
        NavUl,
        NavHamburger,
    } from "flowbite-svelte";

    let loading = true;

    onMount(() => {
        // auth.connstructor에서 initialize()가 호출되므로 상태는 로드되어 있음
        if (!auth.isAuthenticated || !auth.user || !auth.user.is_superuser) {
            alert("관리자 권한이 필요합니다.");
            goto("/");
        } else {
            loading = false;
        }
    });
</script>

{#if loading}
    <div class="flex h-screen items-center justify-center">
        <Spinner size="12" />
    </div>
{:else}
    <div class="antialiased bg-gray-50 dark:bg-gray-900 min-h-screen">
        <Navbar
            class="px-4 py-2.5 dark:bg-gray-800 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-700"
        >
            <NavBrand href="/admin/assets">
                <span
                    class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
                    >Alpha-Sam Admin</span
                >
            </NavBrand>
            <NavHamburger />
            <NavUl>
                <NavLi href="/admin/assets" active={true}>Assets</NavLi>
                <NavLi href="/">Back to Site</NavLi>
            </NavUl>
        </Navbar>

        <div class="p-4 pt-20">
            <slot />
        </div>
    </div>
{/if}
