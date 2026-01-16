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
        if (value === undefined || value === null || isNaN(value))
            return "0.00%";
        return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
    }

    function getColorClass(value: number | undefined): string {
        if (value === undefined || value === null || isNaN(value))
            return "text-gray-900 dark:text-white";
        if (value < 0) return "text-red-600 dark:text-red-400";
        if (value > 0) return "text-green-600 dark:text-green-400";
        return "text-gray-900 dark:text-white";
    }
</script>

<svelte:head>
    <title>Portfolio Dashboard - Alpha-Sam</title>
</svelte:head>

<!-- 대시보드 콘텐츠 (사이드바는 +layout.svelte에서 처리) -->
<div class="space-y-5">
    <!-- 헤더 영역 -->
    <div
        class="flex justify-between items-center pb-5 border-b border-neutral-200 dark:border-neutral-700"
    >
        <h1 class="text-2xl font-bold text-primary-600 dark:text-primary-400">
            Portfolio Dashboard
        </h1>
        <div class="flex gap-3">
            <Button
                color="alternative"
                size="sm"
                onclick={() => (shareModal = true)}
                aria-label="Share portfolio"
                class="btn-outline"
            >
                <ShareNodesOutline class="w-4 h-4 mr-2" />
                Share
            </Button>
            <Button
                size="sm"
                onclick={handleRefresh}
                disabled={refreshing}
                aria-label="Refresh prices and data"
                class="btn-primary"
            >
                <RefreshOutline
                    class="w-4 h-4 mr-2 {refreshing ? 'animate-spin' : ''}"
                />
                {#if refreshing}
                    Refreshing...
                {:else}
                    Refresh
                {/if}
            </Button>
        </div>
    </div>

    {#if loading}
        <div class="text-center py-8">
            <p class="text-neutral-500 dark:text-neutral-400">Loading...</p>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <Button onclick={loadData} class="btn-primary">Retry</Button>
        </div>
    {:else}
        <!-- Stat Cards 섹션 -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
            <!-- Total Assets Card -->
            <div class="card">
                <div class="card-title flex items-center gap-2">
                    <BriefcaseOutline class="w-4 h-4" />
                    Total Assets
                </div>
                <div class="card-value">{assets.length}</div>
                <div class="card-change">✓ Registered assets</div>
            </div>

            <!-- Active Positions Card -->
            <div class="card">
                <div class="card-title flex items-center gap-2">
                    <ChartPieOutline class="w-4 h-4" />
                    Active Positions
                </div>
                <div class="card-value">{positions.length}</div>
                <div class="card-change">✓ Diversified holdings</div>
            </div>

            <!-- Total Valuation Card -->
            <div
                class="card bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/20 dark:to-neutral-800 border-primary-200 dark:border-primary-700"
            >
                <div
                    class="card-title flex items-center gap-2 text-primary-700 dark:text-primary-300"
                >
                    <DollarOutline class="w-4 h-4" />
                    Total Valuation
                </div>
                <div
                    class="text-3xl font-bold text-primary-900 dark:text-primary-100 mb-3"
                >
                    {formatCurrency(portfolioSummary.total_value)}
                </div>
            </div>

            <!-- Portfolio Return Card -->
            <div class="card">
                <div class="card-title flex items-center gap-2">
                    {#if portfolioSummary.total_pl_stats.percent >= 0}
                        <ArrowUpOutline class="w-4 h-4 text-accent-500" />
                    {:else}
                        <ArrowDownOutline class="w-4 h-4 text-red-500" />
                    {/if}
                    Portfolio Return
                </div>
                <div
                    class="flex items-center gap-2 text-3xl font-bold mb-3 {getColorClass(
                        portfolioSummary.total_pl_stats.percent,
                    )}"
                >
                    {#if portfolioSummary.total_pl_stats.percent >= 0}
                        <span class="badge badge-success"
                            >▲ {formatPercent(
                                portfolioSummary.total_pl_stats.percent,
                            )}</span
                        >
                    {:else}
                        <span class="badge badge-error"
                            >▼ {formatPercent(
                                portfolioSummary.total_pl_stats.percent,
                            )}</span
                        >
                    {/if}
                </div>
            </div>
        </div>

        <!-- 차트 섹션 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card class="card p-6">
                <h2 class="card-title text-lg normal-case">Allocation</h2>
                <PortfolioDistributionChart {positions} />
            </Card>
            <Card class="card p-6">
                <h2 class="card-title text-lg normal-case">
                    Performance (Value)
                </h2>
                <PortfolioHistoryChart {history} />
            </Card>
        </div>

        <!-- Quick Actions & Summary 섹션 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Quick Actions -->
            <Card class="card p-6">
                <h2 class="card-title text-lg normal-case mb-4">
                    Quick Actions
                </h2>
                <div class="grid grid-cols-2 gap-3">
                    <Button
                        href="/assets"
                        class="btn-primary w-full justify-center"
                    >
                        <BriefcaseOutline class="w-4 h-4 mr-2" />
                        Assets
                    </Button>
                    <Button
                        href="/positions"
                        class="btn-outline w-full justify-center"
                    >
                        <ChartPieOutline class="w-4 h-4 mr-2" />
                        Positions
                    </Button>
                    <Button
                        href="/transactions"
                        class="btn-outline w-full justify-center"
                    >
                        <PlusOutline class="w-4 h-4 mr-2" />
                        Transactions
                    </Button>
                    <Button class="btn-outline w-full justify-center" disabled>
                        <FileExportOutline class="w-4 h-4 mr-2" />
                        Export (Soon)
                    </Button>
                    <Button
                        href="/social/leaderboard"
                        class="btn-outline w-full justify-center col-span-2"
                    >
                        <ClipboardListOutline class="w-4 h-4 mr-2" />
                        Weekly Leaderboard
                    </Button>
                </div>
            </Card>

            <!-- Portfolio Summary -->
            <Card class="card p-6">
                <h2 class="card-title text-lg normal-case mb-4">
                    Portfolio Summary
                </h2>
                <div class="space-y-3">
                    <div
                        class="flex justify-between items-center py-2 border-b border-neutral-200 dark:border-neutral-700"
                    >
                        <span class="text-neutral-500 dark:text-neutral-400"
                            >Total Invested</span
                        >
                        <span
                            class="font-semibold text-neutral-900 dark:text-white"
                        >
                            {formatCurrency(portfolioSummary.total_cost)}
                        </span>
                    </div>
                    <div
                        class="flex justify-between items-center py-2 border-b border-neutral-200 dark:border-neutral-700"
                    >
                        <span class="text-neutral-500 dark:text-neutral-400"
                            >Current Value</span
                        >
                        <span
                            class="font-semibold text-neutral-900 dark:text-white"
                        >
                            {formatCurrency(portfolioSummary.total_value)}
                        </span>
                    </div>
                    <div class="flex justify-between items-center py-2">
                        <span class="text-neutral-500 dark:text-neutral-400"
                            >Total P/L</span
                        >
                        <span
                            class="font-semibold {getColorClass(
                                portfolioSummary.total_pl,
                            )}"
                        >
                            {formatCurrency(portfolioSummary.total_pl)}
                        </span>
                    </div>
                </div>
            </Card>
        </div>

        <!-- Recent Activity & Insights 섹션 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <!-- Recent Activity Panel -->
            <Card class="card p-6">
                <h2 class="card-title text-lg normal-case mb-4">
                    Recent Activity
                </h2>
                <div class="space-y-3">
                    <p
                        class="text-sm text-neutral-500 dark:text-neutral-400 italic"
                    >
                        No recent transactions to display. Add your first
                        transaction!
                    </p>
                </div>
            </Card>

            <!-- AI Insights Panel -->
            <Card
                class="card p-6 bg-gradient-to-br from-blue-50 to-white dark:from-blue-900/20 dark:to-neutral-800 border-blue-200 dark:border-blue-700"
            >
                <h2
                    class="card-title text-lg normal-case text-blue-700 dark:text-blue-300 mb-4"
                >
                    AI Insights
                </h2>
                <div class="space-y-3">
                    <p class="text-sm text-blue-700 dark:text-blue-300">
                        💡 <strong>Coming Soon:</strong> AI-powered recommendations
                        for portfolio rebalancing, risk warnings, and investment
                        opportunities.
                    </p>
                    <p class="text-xs text-neutral-500 dark:text-neutral-400">
                        Stay tuned for personalized insights based on your
                        portfolio performance.
                    </p>
                </div>
            </Card>
        </div>
    {/if}

    <ShareModal bind:open={shareModal} />
</div>
