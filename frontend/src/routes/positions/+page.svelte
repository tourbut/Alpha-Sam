<script lang="ts">
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Button,
    } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { calculatePortfolioSummary } from "$lib/utils";
    import type { Position } from "$lib/types";
    import TransactionFormModal from "$lib/components/transaction/TransactionFormModal.svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";

    let transactionModalOpen = $state(false);
    let selectedPosition: Position | null = $state(null);
    let selectedAssetId = $state(0);
    let selectedAssetSymbol = $state("");

    // Use store positions
    let positions = $derived(portfolioStore.positions);
    let loading = $derived(portfolioStore.loading);

    // 포트폴리오 요약
    let portfolioSummary = $derived(calculatePortfolioSummary(positions));

    onMount(() => {
        // AppNavbar loads portfolios which triggers loading positions for default.
        // If we landed here directly and store is empty, Navbar logic will handle it,
        // but we can ensure load if auth is ready.
        if (portfolioStore.selectedPortfolioId) {
            portfolioStore.loadPositions(portfolioStore.selectedPortfolioId);
        }
    });

    function openAddTransactionModal() {
        selectedAssetId = 0;
        selectedAssetSymbol = "";
        transactionModalOpen = true;
    }

    function openTradeModal(position: Position) {
        selectedAssetId = position.asset_id;
        selectedAssetSymbol = position.asset_symbol || "";
        transactionModalOpen = true;
    }

    function formatCurrency(value: number | undefined): string {
        if (value === undefined || value === null) return "-";
        return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function formatPercent(value: number | undefined): string {
        if (value === undefined || value === null) return "-";
        return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
    }
</script>

<TransactionFormModal
    bind:open={transactionModalOpen}
    assetId={selectedAssetId}
    assetSymbol={selectedAssetSymbol}
/>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            {#if portfolioStore.selectedPortfolio}
                {portfolioStore.selectedPortfolio.name} Positions
            {:else}
                Positions
            {/if}
        </h1>
        <Button onclick={openAddTransactionModal}>Add Transaction</Button>
    </div>

    {#if loading}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">Loading positions...</p>
        </div>
    {:else if positions.length === 0}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">
                No positions found. Record your first transaction to get start.
            </p>
        </div>
    {:else}
        <div class="overflow-x-auto">
            <Table shadow>
                <TableHead>
                    <TableHeadCell>Asset</TableHeadCell>
                    <TableHeadCell>Symbol</TableHeadCell>
                    <TableHeadCell>Category</TableHeadCell>
                    <TableHeadCell>Quantity</TableHeadCell>
                    <TableHeadCell>Avg Price</TableHeadCell>
                    <!-- Renamed from Buy Price -->
                    <TableHeadCell>Current Price</TableHeadCell>
                    <TableHeadCell>Valuation</TableHeadCell>
                    <TableHeadCell>Profit/Loss</TableHeadCell>
                    <TableHeadCell>Return Rate</TableHeadCell>
                    <TableHeadCell>Actions</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each positions as position (position.id)}
                        <TableBodyRow>
                            <TableBodyCell
                                class="font-medium text-gray-900 dark:text-white"
                            >
                                {position.asset_name || "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class="font-medium text-gray-900 dark:text-white"
                            >
                                {position.asset_symbol || "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                >{position.asset_category || "-"}</TableBodyCell
                            >
                            <TableBodyCell>
                                {position.quantity.toLocaleString(undefined, {
                                    maximumFractionDigits: 8,
                                })}
                            </TableBodyCell>
                            <TableBodyCell>
                                <!-- Using avg_price or fallback to buy_price for legacy -->
                                {formatCurrency(
                                    position.avg_price || position.buy_price,
                                )}
                            </TableBodyCell>
                            <TableBodyCell>
                                {position.current_price
                                    ? formatCurrency(position.current_price)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                {position.valuation !== undefined
                                    ? formatCurrency(position.valuation)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={position.profit_loss !== undefined &&
                                position.profit_loss < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : position.profit_loss !== undefined &&
                                        position.profit_loss > 0
                                      ? "text-green-600 dark:text-green-400"
                                      : ""}
                            >
                                {position.profit_loss !== undefined
                                    ? `${position.profit_loss >= 0 ? "+" : ""}${formatCurrency(position.profit_loss)}`
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={position.return_rate !== undefined &&
                                position.return_rate < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : position.return_rate !== undefined &&
                                        position.return_rate > 0
                                      ? "text-green-600 dark:text-green-400"
                                      : ""}
                            >
                                {position.return_rate !== undefined
                                    ? formatPercent(position.return_rate)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                <div class="flex gap-2">
                                    <Button
                                        size="xs"
                                        color="alternative"
                                        onclick={() => openTradeModal(position)}
                                    >
                                        Trade
                                    </Button>
                                </div>
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>

        {#if positions.length > 0}
            <div class="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
                <!-- Summary Section Reuse -->
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        Total Valuation
                    </div>
                    <div
                        class="text-xl font-bold text-gray-900 dark:text-white"
                    >
                        {formatCurrency(portfolioSummary.totalValuation)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        Total Invested
                    </div>
                    <div
                        class="text-xl font-bold text-gray-900 dark:text-white"
                    >
                        {formatCurrency(portfolioSummary.totalInvested)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        Total Profit/Loss
                    </div>
                    <div
                        class="text-xl font-bold {portfolioSummary.totalProfitLoss <
                        0
                            ? 'text-red-600 dark:text-red-400'
                            : portfolioSummary.totalProfitLoss > 0
                              ? 'text-green-600 dark:text-green-400'
                              : 'text-gray-900 dark:text-white'}"
                    >
                        {formatCurrency(portfolioSummary.totalProfitLoss)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        Portfolio Return
                    </div>
                    <div
                        class="text-xl font-bold {portfolioSummary.totalReturnRate <
                        0
                            ? 'text-red-600 dark:text-red-400'
                            : portfolioSummary.totalReturnRate > 0
                              ? 'text-green-600 dark:text-green-400'
                              : 'text-gray-900 dark:text-white'}"
                    >
                        {formatPercent(portfolioSummary.totalReturnRate)}
                    </div>
                </div>
            </div>
        {/if}
    {/if}
</div>
