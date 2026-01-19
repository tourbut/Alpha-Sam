<script lang="ts">
    import {
        Button,
        Dropdown,
        DropdownItem,
        DropdownHeader,
        DropdownDivider,
    } from "flowbite-svelte";
    import {
        ChevronDownOutline,
        WalletSolid,
        PlusOutline,
    } from "flowbite-svelte-icons";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";
    import CreatePortfolioModal from "./CreatePortfolioModal.svelte";
    import { onMount } from "svelte";
    import { auth } from "$lib/stores/auth.svelte";

    let openCreateModal = $state(false);

    onMount(() => {
        if (auth.isAuthenticated) {
            portfolioStore.loadPortfolios();
        }
    });

    function handleSelect(id: number) {
        portfolioStore.selectPortfolio(id);
    }
</script>

<div class="relative w-full">
    {#if portfolioStore.selectedPortfolio}
        <Button color="light" class="w-full flex items-center justify-between gap-2">
            <div class="flex items-center gap-2">
                <WalletSolid class="w-4 h-4 text-gray-500" />
                <span class="font-medium text-gray-900 dark:text-white">
                    {portfolioStore.selectedPortfolio.name}
                </span>
            </div>
            <ChevronDownOutline class="w-3 h-3 text-gray-500" />
        </Button>
        <Dropdown>
            <DropdownHeader>
                <span class="block text-sm text-gray-900 dark:text-white"
                    >Switch Portfolio</span
                >
            </DropdownHeader>
            {#each portfolioStore.portfolios as p}
                <DropdownItem
                    on:click={() => handleSelect(p.id)}
                    class={portfolioStore.selectedPortfolioId === p.id
                        ? "bg-gray-100 dark:bg-gray-600"
                        : ""}
                >
                    <div class="flex justify-between items-center">
                        <span>{p.name}</span>
                        {#if p.id === portfolioStore.selectedPortfolioId}
                            <span class="text-xs text-primary-600 font-bold"
                                >Current</span
                            >
                        {/if}
                    </div>
                </DropdownItem>
            {/each}
            <DropdownDivider />
            <DropdownItem on:click={() => (openCreateModal = true)}>
                <div class="flex items-center gap-2 text-primary-600">
                    <PlusOutline class="w-3 h-3" />
                    Create New
                </div>
            </DropdownItem>
        </Dropdown>
    {:else}
        <Button color="light" class="w-full flex items-center justify-center gap-2">
            Loading...
        </Button>
    {/if}
</div>

<CreatePortfolioModal bind:open={openCreateModal} />
