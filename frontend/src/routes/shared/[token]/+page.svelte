<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { fetchSharedPortfolio } from "$lib/apis/portfolio";
    import type { PortfolioShared } from "$lib/types";
    import {
        Card,
        Spinner,
        Badge,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
    } from "flowbite-svelte";
    import PortfolioDistributionChart from "$lib/components/PortfolioDistributionChart.svelte";
    import { formatCurrency, formatPercent, getColorClass } from "$lib/utils"; // utility helper 필요

    let token = $page.params.token as string;
    let portfolio: PortfolioShared | null = $state(null);
    let loading = $state(true);
    let error = $state("");

    onMount(async () => {
        try {
            portfolio = await fetchSharedPortfolio(token);
        } catch (e) {
            error = "포트폴리오를 찾을 수 없거나 접근 권한이 없습니다.";
        } finally {
            loading = false;
        }
    });
</script>

<div class="container mx-auto px-4 py-8 max-w-6xl">
    {#if loading}
        <div class="text-center py-20">
            <Spinner size="12" color="blue" />
            <p class="mt-4 text-gray-500">포트폴리오 불러오는 중...</p>
        </div>
    {:else if error}
        <div class="text-center py-20">
            <h2
                class="text-2xl font-bold text-gray-700 dark:text-gray-300 mb-2"
            >
                Error
            </h2>
            <p class="text-red-500">{error}</p>
        </div>
    {:else if portfolio}
        <header
            class="mb-8 text-center sm:text-left border-b border-gray-200 dark:border-gray-700 pb-6"
        >
            <div
                class="flex flex-col sm:flex-row justify-between items-center gap-4"
            >
                <div>
                    <h1
                        class="text-3xl font-bold text-gray-900 dark:text-white mb-2"
                    >
                        {portfolio.name}
                    </h1>
                    <p class="text-gray-500 dark:text-gray-400">
                        Owner: <span class="font-medium text-primary-600"
                            >{portfolio.owner_nickname || "Unknown"}</span
                        >
                    </p>
                    {#if portfolio.description}
                        <p class="text-sm text-gray-400 mt-2 max-w-2xl">
                            {portfolio.description}
                        </p>
                    {/if}
                </div>
                <div class="flex gap-2">
                    <Badge color="blue" large>{portfolio.visibility}</Badge>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
                <Card class="text-center sm:text-left p-4">
                    <h3
                        class="text-gray-500 text-sm font-medium uppercase mb-1"
                    >
                        Total Value
                    </h3>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">
                        {formatCurrency(portfolio.total_value || 0)}
                    </p>
                </Card>
                <Card class="text-center sm:text-left p-4">
                    <h3
                        class="text-gray-500 text-sm font-medium uppercase mb-1"
                    >
                        Return Rate
                    </h3>
                    <p
                        class={`text-2xl font-bold ${getColorClass(portfolio.return_rate || 0)}`}
                    >
                        {formatPercent(portfolio.return_rate || 0)}
                    </p>
                </Card>
                <Card class="text-center sm:text-left p-4">
                    <h3
                        class="text-gray-500 text-sm font-medium uppercase mb-1"
                    >
                        Assets
                    </h3>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">
                        {portfolio.positions?.length || 0}
                    </p>
                </Card>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Asset Allocation Chart -->
            <div class="lg:col-span-1">
                <Card>
                    <h3 class="text-lg font-bold mb-4">Asset Allocation</h3>
                    <div class="h-64">
                        <!-- Chart Component Reuse -->
                        <!-- Note: Needs check if chart component accepts data props or fetches itself. 
                              Usually charts fetch themselves in this project, need to check. 
                              Let's assume we need to pass data or rewrite chart for shared usage.
                              Checking PortfolioDistributionChart.svelte... -->
                        <PortfolioDistributionChart
                            positions={portfolio.positions}
                        />
                    </div>
                </Card>
            </div>

            <!-- Positions Table -->
            <div class="lg:col-span-2">
                <Card class="w-full">
                    <h3 class="text-lg font-bold mb-4">Holdings</h3>
                    <Table hoverable>
                        <TableHead>
                            <TableHeadCell>Symbol</TableHeadCell>
                            <TableHeadCell>Name</TableHeadCell>
                            <TableHeadCell class="text-right"
                                >Price</TableHeadCell
                            >
                            <TableHeadCell class="text-right"
                                >Quantity</TableHeadCell
                            >
                            <TableHeadCell class="text-right"
                                >Value</TableHeadCell
                            >
                        </TableHead>
                        <TableBody>
                            {#each portfolio.positions as pos}
                                <TableBodyRow>
                                    <TableBodyCell
                                        class="font-medium text-gray-900 dark:text-white"
                                    >
                                        {pos.asset_symbol}
                                    </TableBodyCell>
                                    <TableBodyCell
                                        >{pos.asset_name}</TableBodyCell
                                    >
                                    <TableBodyCell class="text-right"
                                        >{formatCurrency(
                                            pos.current_price || 0,
                                        )}</TableBodyCell
                                    >
                                    <TableBodyCell class="text-right"
                                        >{pos.quantity}</TableBodyCell
                                    >
                                    <TableBodyCell class="text-right"
                                        >{formatCurrency(
                                            pos.valuation || 0,
                                        )}</TableBodyCell
                                    >
                                </TableBodyRow>
                            {/each}
                        </TableBody>
                    </Table>
                </Card>
            </div>
        </div>
    {/if}
</div>
