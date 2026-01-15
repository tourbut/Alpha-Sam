<script lang="ts">
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
    } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { get_portfolio_summary as getPortfolioSummary } from "$lib/apis/portfolio";
    import { calculatePortfolioSummary } from "$lib/utils";
    import type { Position } from "$lib/types";

    let positions: Position[] = [];
    let loading = false;
    let error: string | null = null;

    // 포트폴리오 요약
    $: portfolioSummary = calculatePortfolioSummary(positions);

    async function loadData() {
        loading = true;
        error = null;
        try {
            const summaryData = await getPortfolioSummary();
            positions = summaryData.positions;
        } catch (e) {
            console.error("Error loading positions:", e);
            error = "Failed to load positions";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadData();
    });

    function formatCurrency(value: number | undefined): string {
        if (value === undefined || value === null) return "-";
        return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function formatPercent(value: number | undefined): string {
        if (value === undefined || value === null) return "-";
        return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
    }
</script>

<svelte:head>
    <title>Positions - Alpha-Sam</title>
</svelte:head>

<div class="max-w-[1400px] mx-auto p-5">
    <!-- 헤더 영역 -->
    <div
        class="flex justify-between items-center mb-8 pb-5 border-b border-neutral-200 dark:border-neutral-700"
    >
        <div>
            <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">
                Positions
            </h1>
            <p class="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
                읽기 전용 - Transaction을 추가하여 Position을 변경하세요
            </p>
        </div>
    </div>

    {#if loading}
        <div class="text-center py-8">
            <p class="text-neutral-500 dark:text-neutral-400">
                Loading positions...
            </p>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400">{error}</p>
        </div>
    {:else if positions.length === 0}
        <div class="text-center py-8">
            <p class="text-neutral-500 dark:text-neutral-400">
                No positions found. Add transactions to create positions.
            </p>
        </div>
    {:else}
        <!-- 테이블 컨테이너 - theme-preview 스타일 적용 -->
        <div class="table-container overflow-x-auto">
            <table class="w-full">
                <thead>
                    <tr>
                        <th class="table-header">Asset</th>
                        <th class="table-header">Symbol</th>
                        <th class="table-header">Category</th>
                        <th class="table-header text-right">Quantity</th>
                        <th class="table-header text-right">Avg Price</th>
                        <th class="table-header text-right">Current Price</th>
                        <th class="table-header text-right">Valuation</th>
                        <th class="table-header text-right">Profit/Loss</th>
                        <th class="table-header text-right">Return</th>
                    </tr>
                </thead>
                <tbody>
                    {#each positions as position (position.asset_id)}
                        <tr class="table-row-hover">
                            <td
                                class="table-cell font-semibold text-neutral-900 dark:text-white"
                            >
                                {position.asset_name || "-"}
                            </td>
                            <td class="table-cell font-medium">
                                {position.asset_symbol || "-"}
                            </td>
                            <td class="table-cell">
                                {position.asset_category || "-"}
                            </td>
                            <td class="table-cell text-right">
                                {position.quantity.toLocaleString(undefined, {
                                    maximumFractionDigits: 8,
                                })}
                            </td>
                            <td class="table-cell text-right">
                                {formatCurrency(position.avg_price)}
                            </td>
                            <td class="table-cell text-right">
                                {position.current_price
                                    ? formatCurrency(position.current_price)
                                    : "-"}
                            </td>
                            <td class="table-cell text-right font-medium">
                                {position.valuation !== undefined
                                    ? formatCurrency(position.valuation)
                                    : "-"}
                            </td>
                            <td class="table-cell text-right">
                                {#if position.profit_loss !== undefined}
                                    <span
                                        class="badge {position.profit_loss >= 0
                                            ? 'badge-success'
                                            : 'badge-error'}"
                                    >
                                        {position.profit_loss >= 0
                                            ? "+"
                                            : ""}{formatCurrency(
                                            position.profit_loss,
                                        )}
                                    </span>
                                {:else}
                                    -
                                {/if}
                            </td>
                            <td class="table-cell text-right">
                                {#if position.return_rate !== undefined}
                                    <span
                                        class="badge {position.return_rate >= 0
                                            ? 'badge-success'
                                            : 'badge-error'}"
                                    >
                                        {formatPercent(position.return_rate)}
                                    </span>
                                {:else}
                                    -
                                {/if}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        <!-- Summary Cards -->
        {#if positions.length > 0}
            <div class="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="card">
                    <div class="card-title">Total Valuation</div>
                    <div class="card-value text-2xl">
                        {formatCurrency(portfolioSummary.totalValuation)}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Total Invested</div>
                    <div class="card-value text-2xl">
                        {formatCurrency(portfolioSummary.totalInvested)}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Total P/L</div>
                    <div
                        class="text-2xl font-bold mb-3 {portfolioSummary.totalProfitLoss <
                        0
                            ? 'text-red-600 dark:text-red-400'
                            : portfolioSummary.totalProfitLoss > 0
                              ? 'text-accent-600 dark:text-accent-400'
                              : 'text-neutral-900 dark:text-white'}"
                    >
                        {formatCurrency(portfolioSummary.totalProfitLoss)}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Portfolio Return</div>
                    <div>
                        <span
                            class="badge {portfolioSummary.totalReturnRate >= 0
                                ? 'badge-success'
                                : 'badge-error'} text-base"
                        >
                            {formatPercent(portfolioSummary.totalReturnRate)}
                        </span>
                    </div>
                </div>
            </div>
        {/if}
    {/if}
</div>
