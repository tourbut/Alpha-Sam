<script lang="ts">
    import { Card, Button } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import { refresh_prices as refreshPrices } from "$lib/apis/prices";
    import type { Asset, Position, PortfolioHistory } from "$lib/types";
    import PortfolioDistributionChart from "$lib/components/PortfolioDistributionChart.svelte";
    // import PortfolioHistoryChart from "$lib/components/PortfolioHistoryChart.svelte"; // History not ready for v1.2.0
    import { auth } from "$lib/stores/auth.svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";
    import { calculatePortfolioSummary } from "$lib/utils";
    import ShareModal from "$lib/components/ShareModal.svelte";
    import { goto } from "$app/navigation";

    let assets: Asset[] = $state([]);
    // Positions from store
    let positions = $derived(portfolioStore.positions);
    let loading = $derived(portfolioStore.loading);

    // Computed Summary
    let portfolioSummary = $derived(calculatePortfolioSummary(positions));

    // History mocked for now
    let history: PortfolioHistory[] = $state([]);

    let error: string | null = $state(null);
    let refreshing = $state(false);
    let showShareModal = $state(false);

    async function handleRefresh() {
        refreshing = true;
        try {
            await refreshPrices();
            if (portfolioStore.selectedPortfolioId) {
                await portfolioStore.loadPositions(
                    portfolioStore.selectedPortfolioId,
                );
            }
        } catch (e) {
            console.error("Failed to refresh prices:", e);
            alert("Failed to refresh prices");
        } finally {
            refreshing = false;
        }
    }

    onMount(async () => {
        if (!auth.isAuthenticated) {
            auth.initialize();
            if (!auth.isAuthenticated) {
                goto("/login");
                return;
            }
        }

        // Load assets for the count display
        try {
            assets = await getAssets();
        } catch (e) {
            console.error("Failed to load assets", e);
        }

        // Ensure positions are loaded if not already
        if (portfolioStore.selectedPortfolioId) {
            portfolioStore.loadPositions(portfolioStore.selectedPortfolioId);
        }
    });

    function formatCurrency(value: number | undefined): string {
        if (value === undefined || value === null) return "$0.00";
        return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function formatPercent(value: number | undefined): string {
        if (value === undefined || value === null) return "0.00%";
        return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
    }

    function getColorClass(value: number | undefined): string {
        if (value === undefined || value === null)
            return "text-gray-900 dark:text-white";
        if (value < 0) return "text-red-600 dark:text-red-400";
        if (value > 0) return "text-green-600 dark:text-green-400";
        return "text-gray-900 dark:text-white";
    }
</script>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {#if portfolioStore.selectedPortfolio}
                {portfolioStore.selectedPortfolio.name} Dashboard
            {:else}
                Portfolio Dashboard
            {/if}
        </h1>
        <div class="flex gap-2">
            <Button
                color="alternative"
                size="sm"
                onclick={() => (showShareModal = true)}
            >
                Share Portfolio
            </Button>
            <Button
                color="light"
                size="sm"
                onclick={handleRefresh}
                disabled={refreshing}
            >
                {#if refreshing}
                    Refreshing...
                {:else}
                    Refresh Prices
                {/if}
            </Button>
        </div>
    </div>

    <ShareModal bind:open={showShareModal} />

    {#if loading && positions.length === 0}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400 mb-4">{error}</p>
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Market Assets
                </div>
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                    {assets.length}
                </div>
            </Card>
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Active Positions
                </div>
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                    {positions.length}
                </div>
            </Card>
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Total Valuation
                </div>
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                    {formatCurrency(portfolioSummary.totalValuation)}
                </div>
            </Card>
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Portfolio Return
                </div>
                <div
                    class="text-3xl font-bold {getColorClass(
                        portfolioSummary.totalReturnRate,
                    )}"
                >
                    {formatPercent(portfolioSummary.totalReturnRate)}
                </div>
            </Card>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Allocation
                </h2>
                <PortfolioDistributionChart {positions} />
            </Card>
            <!-- History Chart Disabled -->
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Performance (Coming Soon)
                </h2>
                <div
                    class="flex items-center justify-center h-64 bg-gray-50 dark:bg-gray-800 rounded"
                >
                    <p class="text-gray-500">
                        History chart update needed for v1.2.0
                    </p>
                </div>
                <!-- <PortfolioHistoryChart {history} /> -->
            </Card>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Quick Actions
                </h2>
                <div class="flex flex-col gap-2">
                    <Button href="/assets" class="w-full text-white"
                        >Manage Assets</Button
                    >
                    <Button href="/positions" color="alternative" class="w-full"
                        >Manage Positions</Button
                    >
                    <Button
                        href="/social/leaderboard"
                        color="green"
                        class="w-full">View Leaderboard</Button
                    >
                </div>
            </Card>
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Portfolio Summary
                </h2>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-600 dark:text-gray-400"
                            >Total Invested:</span
                        >
                        <span class="font-medium text-gray-900 dark:text-white">
                            {formatCurrency(portfolioSummary.totalInvested)}
                        </span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600 dark:text-gray-400"
                            >Total Profit/Loss:</span
                        >
                        <span
                            class="font-medium {getColorClass(
                                portfolioSummary.totalProfitLoss,
                            )}"
                        >
                            {formatCurrency(portfolioSummary.totalProfitLoss)}
                        </span>
                    </div>
                </div>
            </Card>
        </div>
    {/if}
</div>
