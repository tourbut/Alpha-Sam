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
    import { 
        getPositions, 
        deletePosition,
        calculatePortfolioSummary,
        type Position 
    } from "$lib/api";
    import PositionModal from "$lib/components/PositionModal.svelte";
    import { getAssets } from "$lib/api";

    let positions: Position[] = [];
    let assets: any[] = [];
    let positionModalOpen = false;
    let selectedPosition: Position | null = null;
    let loading = false;
    let error: string | null = null;

    // 포트폴리오 요약
    $: portfolioSummary = calculatePortfolioSummary(positions);

    async function loadData() {
        loading = true;
        error = null;
        try {
            const [positionsData, assetsData] = await Promise.all([
                getPositions(),
                getAssets()
            ]);
            console.log('Loaded positions:', positionsData);
            positions = positionsData;
            assets = assetsData;
        } catch (e) {
            console.error('Error loading positions:', e);
            error = 'Failed to load positions';
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadData();
    });

    function openAddPositionModal() {
        selectedPosition = null;
        positionModalOpen = true;
    }

    function openEditPositionModal(position: Position) {
        selectedPosition = position;
        positionModalOpen = true;
    }

    async function handleDeletePosition(position: Position) {
        if (!confirm(`Are you sure you want to delete position for ${position.asset_symbol || 'this asset'}?`)) {
            return;
        }

        try {
            await deletePosition(position.id);
            await loadData();
        } catch (e: any) {
            console.error('Error deleting position:', e);
            alert(`Failed to delete position: ${e.message}`);
        }
    }

    function handlePositionCreated() {
        loadData();
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

<PositionModal 
    bind:open={positionModalOpen} 
    {assets}
    position={selectedPosition ? {
        id: selectedPosition.id,
        asset_id: selectedPosition.asset_id,
        quantity: selectedPosition.quantity,
        buy_price: selectedPosition.buy_price,
        buy_date: selectedPosition.buy_date
    } : null}
    on:created={handlePositionCreated} 
/>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Positions</h1>
        <Button onclick={openAddPositionModal}>Add Position</Button>
    </div>

    {#if loading}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">Loading positions...</p>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400">{error}</p>
        </div>
    {:else if positions.length === 0}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">No positions found. Add your first position to get started.</p>
        </div>
    {:else}
        <div class="overflow-x-auto">
            <Table shadow>
                <TableHead>
                    <TableHeadCell>Asset</TableHeadCell>
                    <TableHeadCell>Symbol</TableHeadCell>
                    <TableHeadCell>Category</TableHeadCell>
                    <TableHeadCell>Quantity</TableHeadCell>
                    <TableHeadCell>Buy Price</TableHeadCell>
                    <TableHeadCell>Current Price</TableHeadCell>
                    <TableHeadCell>Valuation</TableHeadCell>
                    <TableHeadCell>Profit/Loss</TableHeadCell>
                    <TableHeadCell>Return Rate</TableHeadCell>
                    <TableHeadCell>Actions</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each positions as position (position.id)}
                        <TableBodyRow>
                            <TableBodyCell class="font-medium text-gray-900 dark:text-white">
                                {position.asset_name || "-"}
                            </TableBodyCell>
                            <TableBodyCell class="font-medium text-gray-900 dark:text-white">
                                {position.asset_symbol || "-"}
                            </TableBodyCell>
                            <TableBodyCell>{position.asset_category || "-"}</TableBodyCell>
                            <TableBodyCell>
                                {position.quantity.toLocaleString(undefined, { maximumFractionDigits: 8 })}
                            </TableBodyCell>
                            <TableBodyCell>
                                {formatCurrency(position.buy_price)}
                            </TableBodyCell>
                            <TableBodyCell>
                                {position.current_price ? formatCurrency(position.current_price) : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                {position.valuation !== undefined ? formatCurrency(position.valuation) : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={position.profit_loss !== undefined && position.profit_loss < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : position.profit_loss !== undefined && position.profit_loss > 0
                                    ? "text-green-600 dark:text-green-400"
                                    : ""}
                            >
                                {position.profit_loss !== undefined 
                                    ? `${position.profit_loss >= 0 ? "+" : ""}${formatCurrency(position.profit_loss)}`
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={position.return_rate !== undefined && position.return_rate < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : position.return_rate !== undefined && position.return_rate > 0
                                    ? "text-green-600 dark:text-green-400"
                                    : ""}
                            >
                                {position.return_rate !== undefined ? formatPercent(position.return_rate) : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                <div class="flex gap-2">
                                    <Button 
                                        size="xs" 
                                        color="alternative"
                                        onclick={() => openEditPositionModal(position)}
                                    >
                                        Edit
                                    </Button>
                                    <Button 
                                        size="xs" 
                                        color="red"
                                        onclick={() => handleDeletePosition(position)}
                                    >
                                        Delete
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
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Valuation</div>
                    <div class="text-xl font-bold text-gray-900 dark:text-white">
                        {formatCurrency(portfolioSummary.totalValuation)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Invested</div>
                    <div class="text-xl font-bold text-gray-900 dark:text-white">
                        {formatCurrency(portfolioSummary.totalInvested)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Profit/Loss</div>
                    <div class="text-xl font-bold {portfolioSummary.totalProfitLoss < 0 ? 'text-red-600 dark:text-red-400' : portfolioSummary.totalProfitLoss > 0 ? 'text-green-600 dark:text-green-400' : 'text-gray-900 dark:text-white'}">
                        {formatCurrency(portfolioSummary.totalProfitLoss)}
                    </div>
                </div>
                <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">Portfolio Return</div>
                    <div class="text-xl font-bold {portfolioSummary.totalReturnRate < 0 ? 'text-red-600 dark:text-red-400' : portfolioSummary.totalReturnRate > 0 ? 'text-green-600 dark:text-green-400' : 'text-gray-900 dark:text-white'}">
                        {formatPercent(portfolioSummary.totalReturnRate)}
                    </div>
                </div>
            </div>
        {/if}
    {/if}
</div>

