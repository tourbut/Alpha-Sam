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
    import ShareModal from "$lib/components/ShareModal.svelte";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";
    import {
        ShareNodesOutline,
        RefreshOutline,
        ChartPieOutline,
        DollarOutline,
        ArrowUpOutline,
        ArrowDownOutline,
        PlusOutline,
        FileExportOutline,
        ClipboardListOutline,
        BriefcaseOutline,
    } from "flowbite-svelte-icons";

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
    let shareModal = false;

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

<svelte:head>
    <title>Portfolio Dashboard - Alpha-Sam</title>
</svelte:head>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Portfolio Dashboard
        </h1>
        <div class="flex gap-2">
            <Button
                color="alternative"
                size="sm"
                onclick={() => (shareModal = true)}
                aria-label="Share portfolio"
                class="focus:ring-2 focus:ring-primary-500 focus:outline-none"
            >
                <ShareNodesOutline class="w-4 h-4 mr-2" />
                Share
            </Button>
            <Button
                color="light"
                size="sm"
                onclick={handleRefresh}
                disabled={refreshing}
                aria-label="Refresh prices and data"
                class="focus:ring-2 focus:ring-primary-500 focus:outline-none"
            >
                <RefreshOutline
                    class="w-4 h-4 mr-2 {refreshing ? 'animate-spin' : ''}"
                />
                {#if refreshing}
                    Refreshing...
                {:else}
                    Refresh Prices
                {/if}
            </Button>
        </div>
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
        <!-- Stat Cards Section -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <!-- Total Assets Card -->
            <Card class="p-6 hover:shadow-lg transition-shadow duration-200">
                <div
                    class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-2"
                >
                    <BriefcaseOutline class="w-4 h-4" />
                    Total Assets
                </div>
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                    {assets.length}
                </div>
            </Card>
            <!-- Active Positions Card -->
            <Card class="p-6 hover:shadow-lg transition-shadow duration-200">
                <div
                    class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-2"
                >
                    <ChartPieOutline class="w-4 h-4" />
                    Active Positions
                </div>
                <div class="text-3xl font-bold text-gray-900 dark:text-white">
                    {positions.length}
                </div>
            </Card>
            <!-- Total Valuation Card (주요 지표: 강조 스타일) -->
            <Card
                class="p-6 bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/20 dark:to-gray-800 hover:shadow-lg transition-shadow duration-200 border-primary-200 dark:border-primary-700"
            >
                <div
                    class="flex items-center gap-2 text-sm text-primary-700 dark:text-primary-300 mb-2"
                >
                    <DollarOutline class="w-4 h-4" />
                    Total Valuation
                </div>
                <div
                    class="text-3xl font-bold text-primary-900 dark:text-primary-100"
                >
                    {formatCurrency(portfolioSummary.total_value)}
                </div>
            </Card>
            <!-- Portfolio Return Card (주요 지표: 색상 + 화살표) -->
            <Card class="p-6 hover:shadow-lg transition-shadow duration-200">
                <div
                    class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-2"
                >
                    {#if portfolioSummary.total_pl_stats.percent >= 0}
                        <ArrowUpOutline class="w-4 h-4 text-green-500" />
                    {:else}
                        <ArrowDownOutline class="w-4 h-4 text-red-500" />
                    {/if}
                    Portfolio Return
                </div>
                <div
                    class="flex items-center gap-2 text-3xl font-bold {getColorClass(
                        portfolioSummary.total_pl_stats.percent,
                    )}"
                >
                    {#if portfolioSummary.total_pl_stats.percent >= 0}
                        <span class="text-green-500">▲</span>
                    {:else}
                        <span class="text-red-500">▼</span>
                    {/if}
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
            <!-- Quick Actions (Expanded) -->
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Quick Actions
                </h2>
                <div class="grid grid-cols-2 gap-2">
                    <Button
                        href="/assets"
                        class="w-full text-white focus:ring-2 focus:ring-primary-500"
                    >
                        <BriefcaseOutline class="w-4 h-4 mr-2" />
                        Manage Assets
                    </Button>
                    <Button
                        href="/positions"
                        color="alternative"
                        class="w-full focus:ring-2 focus:ring-primary-500"
                    >
                        <ChartPieOutline class="w-4 h-4 mr-2" />
                        Positions
                    </Button>
                    <Button
                        href="/transactions"
                        color="light"
                        class="w-full focus:ring-2 focus:ring-primary-500"
                    >
                        <PlusOutline class="w-4 h-4 mr-2" />
                        Transactions
                    </Button>
                    <Button
                        color="light"
                        class="w-full focus:ring-2 focus:ring-primary-500"
                        disabled
                    >
                        <FileExportOutline class="w-4 h-4 mr-2" />
                        Export (Soon)
                    </Button>
                    <Button
                        href="/social/leaderboard"
                        color="light"
                        class="w-full col-span-2 focus:ring-2 focus:ring-primary-500"
                    >
                        <ClipboardListOutline class="w-4 h-4 mr-2" />
                        Weekly Leaderboard
                    </Button>
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

        <!-- Recent Activity & Insights Section (Mock/Placeholder) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-8">
            <!-- Recent Activity Panel -->
            <Card class="p-6">
                <h2
                    class="text-xl font-bold text-gray-900 dark:text-white mb-4"
                >
                    Recent Activity
                </h2>
                <div class="space-y-3">
                    <p class="text-sm text-gray-500 dark:text-gray-400 italic">
                        No recent transactions to display. Add your first
                        transaction!
                    </p>
                    <!-- Placeholder for future transaction list -->
                    <!--
                    <div class="flex items-center justify-between py-2 border-b border-gray-200 dark:border-gray-700">
                        <div class="flex items-center gap-2">
                            <span class="text-green-500">BUY</span>
                            <span class="font-medium">AAPL</span>
                        </div>
                        <span class="text-sm text-gray-500">10 shares @ $150</span>
                    </div>
                    -->
                </div>
            </Card>

            <!-- AI Insights Panel -->
            <Card
                class="p-6 bg-gradient-to-br from-blue-50 to-white dark:from-blue-900/20 dark:to-gray-800 border-blue-200 dark:border-blue-700"
            >
                <h2
                    class="text-xl font-bold text-blue-900 dark:text-blue-100 mb-4"
                >
                    AI Insights
                </h2>
                <div class="space-y-3">
                    <p class="text-sm text-blue-700 dark:text-blue-300">
                        💡 <strong>Coming Soon:</strong> AI-powered recommendations
                        for portfolio rebalancing, risk warnings, and investment
                        opportunities.
                    </p>
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                        Stay tuned for personalized insights based on your
                        portfolio performance.
                    </p>
                </div>
            </Card>
        </div>
    {/if}
    <ShareModal bind:open={shareModal} />
</div>
