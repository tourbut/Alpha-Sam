<script lang="ts">
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Button,
        Card,
        Tooltip,
        Badge,
        Skeleton,
    } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import {
        getAssets,
        refreshPrices,
        getPositions,
        calculatePortfolioSummary,
        deletePosition,
        type Asset,
        type Position,
    } from "$lib/api";
    import AssetModal from "$lib/components/AssetModal.svelte";
    import PositionModal from "$lib/components/PositionModal.svelte";

    let assets: Asset[] = [];
    let positions: Position[] = [];
    let assetModalOpen = false;
    let positionModalOpen = false;
    let selectedAsset: Asset | null = null;
    let loading = false;
    let error: string | null = null;

    // Position을 Asset ID로 매핑
    $: positionMap = new Map<number, Position>();
    positions.forEach((pos) => {
        positionMap.set(pos.asset_id, pos);
    });

    // Asset에 Position 정보 병합
    $: assetsWithPositions = assets.map((asset) => {
        const position = positionMap.get(asset.id);
        return {
            ...asset,
            valuation: position?.valuation,
            profit_loss: position?.profit_loss,
            return_rate: position?.return_rate,
            quantity: position?.quantity,
            buy_price: position?.buy_price,
            position_id: position?.id,
        };
    });

    // 포트폴리오 요약
    $: portfolioSummary = calculatePortfolioSummary(positions);

    async function loadAssets() {
        loading = true;
        error = null;
        try {
            const [assetsData, positionsData] = await Promise.all([
                getAssets(),
                getPositions(),
            ]);
            console.log("Loaded assets:", assetsData);
            console.log("Loaded positions:", positionsData);
            assets = assetsData;
            positions = positionsData;
            if (assets.length === 0) {
                console.warn("No assets found");
            }
        } catch (e) {
            console.error("Error loading data:", e);
            error = "Failed to load data";
        } finally {
            loading = false;
        }
    }

    async function handleRefreshPrices() {
        try {
            await refreshPrices();
            await loadAssets();
        } catch (e) {
            console.error(e);
            alert("Failed to refresh prices");
        }
    }

    onMount(() => {
        loadAssets();
    });

    function openAddAssetModal() {
        assetModalOpen = true;
    }

    function handleAssetCreated() {
        loadAssets();
    }

    function openAddPositionModal(asset: Asset) {
        selectedAsset = asset;
        positionModalOpen = true;
    }

    function handlePositionCreated() {
        loadAssets();
    }

    async function handleDeletePosition(positionId: number) {
        if (!confirm("Are you sure you want to delete this position?")) {
            return;
        }
        try {
            await deletePosition(positionId);
            await loadAssets();
        } catch (e) {
            console.error(e);
            alert("Failed to delete position");
        }
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

<AssetModal bind:open={assetModalOpen} on:created={handleAssetCreated} />
<PositionModal
    bind:open={positionModalOpen}
    {assets}
    asset={selectedAsset}
    on:created={handlePositionCreated}
/>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Assets</h1>
        <div class="flex gap-2 flex-wrap">
            <Button color="alternative" onclick={handleRefreshPrices}
                >Refresh Prices</Button
            >
            <Button onclick={openAddAssetModal}>Add Asset</Button>
        </div>
    </div>

    {#if loading}
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            {#each Array(4) as _}
                <Card class="p-4">
                    <Skeleton class="h-4 w-24 mb-2" />
                    <Skeleton class="h-8 w-20" />
                </Card>
            {/each}
        </div>
    {:else if positions.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card class="p-4">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Total Valuation
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                    {formatCurrency(portfolioSummary.totalValuation)}
                </div>
            </Card>
            <Card class="p-4">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Total Invested
                </div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">
                    {formatCurrency(portfolioSummary.totalInvested)}
                </div>
            </Card>
            <Card class="p-4">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Total Profit/Loss
                </div>
                <div
                    class="text-2xl font-bold {portfolioSummary.totalProfitLoss <
                    0
                        ? 'text-red-600 dark:text-red-400'
                        : portfolioSummary.totalProfitLoss > 0
                          ? 'text-green-600 dark:text-green-400'
                          : 'text-gray-900 dark:text-white'}"
                >
                    {formatCurrency(portfolioSummary.totalProfitLoss)}
                </div>
            </Card>
            <Card class="p-4">
                <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Portfolio Return
                </div>
                <div
                    class="text-2xl font-bold {portfolioSummary.totalReturnRate <
                    0
                        ? 'text-red-600 dark:text-red-400'
                        : portfolioSummary.totalReturnRate > 0
                          ? 'text-green-600 dark:text-green-400'
                          : 'text-gray-900 dark:text-white'}"
                >
                    {formatPercent(portfolioSummary.totalReturnRate)}
                </div>
            </Card>
        </div>
    {/if}

    {#if loading}
        <div class="overflow-x-auto">
            <Table shadow>
                <TableHead>
                    <TableHeadCell>Symbol</TableHeadCell>
                    <TableHeadCell>Name</TableHeadCell>
                    <TableHeadCell>Category</TableHeadCell>
                    <TableHeadCell>Current Price</TableHeadCell>
                    <TableHeadCell>Quantity</TableHeadCell>
                    <TableHeadCell>Buy Price</TableHeadCell>
                    <TableHeadCell>Valuation</TableHeadCell>
                    <TableHeadCell>Profit/Loss</TableHeadCell>
                    <TableHeadCell>Return Rate</TableHeadCell>
                    <TableHeadCell>Action</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each Array(5) as _}
                        <TableBodyRow>
                            <TableBodyCell
                                ><Skeleton class="h-4 w-16" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-32" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-20" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-20" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-16" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-20" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-24" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-24" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-4 w-16" /></TableBodyCell
                            >
                            <TableBodyCell
                                ><Skeleton class="h-6 w-20" /></TableBodyCell
                            >
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    {:else if error}
        <div class="text-center py-8">
            <p class="text-red-600 dark:text-red-400">{error}</p>
        </div>
    {:else if assets.length === 0}
        <div class="text-center py-8">
            <p class="text-gray-600 dark:text-gray-400">
                No assets found. Add your first asset to get started.
            </p>
        </div>
    {:else}
        <div class="overflow-x-auto">
            <Table shadow>
                <TableHead>
                    <TableHeadCell>Symbol</TableHeadCell>
                    <TableHeadCell>Name</TableHeadCell>
                    <TableHeadCell>Category</TableHeadCell>
                    <TableHeadCell>Current Price</TableHeadCell>
                    <TableHeadCell>Quantity</TableHeadCell>
                    <TableHeadCell>Buy Price</TableHeadCell>
                    <TableHeadCell>Valuation</TableHeadCell>
                    <TableHeadCell>Profit/Loss</TableHeadCell>
                    <TableHeadCell>Return Rate</TableHeadCell>
                    <TableHeadCell>Action</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each assetsWithPositions as asset (asset.id)}
                        <TableBodyRow>
                            <TableBodyCell
                                class="font-medium text-gray-900 dark:text-white flex items-center"
                                ><span transition:fade={{ duration: 300 }}
                                    >{asset.symbol}</span
                                >
                                {#if asset.owner_id}
                                    <Badge color="green" class="ml-2"
                                        >Private</Badge
                                    >
                                {:else}
                                    <Badge color="blue" class="ml-2"
                                        >Global</Badge
                                    >
                                {/if}
                            </TableBodyCell>
                            <TableBodyCell>{asset.name}</TableBodyCell>
                            <TableBodyCell
                                >{asset.category || "-"}</TableBodyCell
                            >
                            <TableBodyCell>
                                {asset.latest_price
                                    ? formatCurrency(asset.latest_price)
                                    : "-"}
                                {#if asset.latest_price && asset.latest_price_updated_at}
                                    <Tooltip>
                                        Updated: {new Date(
                                            asset.latest_price_updated_at,
                                        ).toLocaleString()}
                                    </Tooltip>
                                {/if}
                            </TableBodyCell>
                            <TableBodyCell>
                                {asset.quantity !== undefined
                                    ? asset.quantity.toLocaleString(undefined, {
                                          maximumFractionDigits: 8,
                                      })
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                {asset.buy_price !== undefined
                                    ? formatCurrency(asset.buy_price)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                {asset.valuation !== undefined
                                    ? formatCurrency(asset.valuation)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={asset.profit_loss !== undefined &&
                                asset.profit_loss < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : asset.profit_loss !== undefined &&
                                        asset.profit_loss > 0
                                      ? "text-green-600 dark:text-green-400"
                                      : ""}
                            >
                                {asset.profit_loss !== undefined
                                    ? `${asset.profit_loss >= 0 ? "+" : ""}${formatCurrency(asset.profit_loss)}`
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell
                                class={asset.return_rate !== undefined &&
                                asset.return_rate < 0
                                    ? "text-red-600 dark:text-red-400"
                                    : asset.return_rate !== undefined &&
                                        asset.return_rate > 0
                                      ? "text-green-600 dark:text-green-400"
                                      : ""}
                            >
                                {asset.return_rate !== undefined
                                    ? formatPercent(asset.return_rate)
                                    : "-"}
                            </TableBodyCell>
                            <TableBodyCell>
                                <Button
                                    size="xs"
                                    color={asset.position_id
                                        ? "alternative"
                                        : "blue"}
                                    onclick={() => openAddPositionModal(asset)}
                                    class="mr-2"
                                >
                                    {asset.position_id ? "Edit" : "Add"}
                                </Button>
                                {#if asset.position_id}
                                    <Button
                                        size="xs"
                                        color="red"
                                        onclick={() =>
                                            handleDeletePosition(
                                                asset.position_id!,
                                            )}
                                    >
                                        Delete
                                    </Button>
                                {/if}
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    {/if}
</div>
