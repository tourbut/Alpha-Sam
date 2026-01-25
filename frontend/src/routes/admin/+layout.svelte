<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '$lib/stores/auth';
    import { Spinner } from 'flowbite-svelte';
    import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';

    let loading = true;

    onMount(() => {
        // user store가 초기화될 때까지 기다림 (보통 auth store는 localStorage에서 로드됨)
        const unsubscribe = user.subscribe(u => {
            if (u === undefined) return; // Loading state

            if (!u || !u.is_superuser) {
                alert("관리자 권한이 필요합니다.");
                goto('/');
            } else {
                loading = false;
            }
        });

        return unsubscribe;
    });
</script>

{#if loading}
    <div class="flex h-screen items-center justify-center">
        <Spinner size="12" />
    </div>
{:else}
    <div class="antialiased bg-gray-50 dark:bg-gray-900 min-h-screen">
        <Navbar class="px-4 py-2.5 dark:bg-gray-800 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-700">
            <NavBrand href="/admin/assets">
                <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Alpha-Sam Admin</span>
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
