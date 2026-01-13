<script lang="ts">
    import { Card, Button } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import {
        get_portfolio_summary as getPortfolioSummary,
        get_portfolio_history as getPortfolioHistory,
    } from "$lib/apis/portfolio";
    import { refresh_prices as refreshPrices } from "$lib/apis/prices";
    import type {
        Asset,
        Position,
        ApiPortfolioSummary,
        PortfolioHistory,
    } from "$lib/types";
    import PortfolioDistributionChart from "$lib/components/PortfolioDistributionChart.svelte";
    import PortfolioHistoryChart from "$lib/components/PortfolioHistoryChart.svelte";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";

    let assets: Asset[] = [];
    let positions: Position[] = [];
    let portfolioSummary: ApiPortfolioSummary = {
        total_value: 0,
        total_cost: 0,
        total_pl: 0,
        total_pl_stats: { percent: 0, direction: "flat" },
    };
    let history: PortfolioHistory[] = [];
    let error: string | null = null;
    let loading = true;
    let refreshing = false;

    async function handleRefresh() {
        refreshing = true;
        try {
            await refreshPrices();
            await loadData();
        } catch (e) {
            console.error("Failed to refresh prices:", e);
            alert("Failed to refresh prices");
        } finally {
            refreshing = false;
        }
    }

    async function loadData() {
        loading = true;
        error = null;
        try {
            const [assetsData, summaryResponse, historyData] =
                await Promise.all([
                    getAssets(),
                    getPortfolioSummary(),
                    getPortfolioHistory({ skip: 0, limit: 30 }),
                ]);
            assets = assetsData;
            positions = summaryResponse.positions;
            portfolioSummary = summaryResponse.summary;
            history = historyData;
        } catch (e) {
            console.error("Error loading data:", e);
            error = "Failed to load portfolio data. Please try again later.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        auth.initialize();
        if (!auth.isAuthenticated) {
            goto("/login");
            return;
        }
        loadData();
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
            Portfolio Dashboard
        </h1>
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

    {#if loading}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <Button onclick={loadData}>Retry</Button>
        </div>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Total Assets
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
                    {formatCurrency(portfolioSummary.total_value)}
                </div>
            </Card>
            <Card class="p-6">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Portfolio Return
                </div>
                <div
                    class="text-3xl font-bold {getColorClass(
                        portfolioSummary.total_pl_stats.percent,
                    )}"
                >
                    {formatPercent(portfolioSummary.total_pl_stats.percent)}
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
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Performance (Value)
                </h2>
                <PortfolioHistoryChart {history} />
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
                            {formatCurrency(portfolioSummary.total_cost)}
                        </span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600 dark:text-gray-400"
                            >Total Profit/Loss:</span
                        >
                        <span
                            class="font-medium {getColorClass(
                                portfolioSummary.total_pl,
                            )}"
                        >
                            {formatCurrency(portfolioSummary.total_pl)}
                        </span>
                    </div>
                </div>
            </Card>
        </div>
    {/if}
</div>
