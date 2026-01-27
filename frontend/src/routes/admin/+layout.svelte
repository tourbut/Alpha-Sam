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
    <slot />
{/if}
