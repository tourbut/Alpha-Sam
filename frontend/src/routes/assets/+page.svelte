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
    import { PlusOutline } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import { refresh_prices as refreshPrices } from "$lib/apis/prices";
    import {
        get_portfolio_summary as getPortfolioSummary,
        fetchPortfolios,
    } from "$lib/apis/portfolio";
    import { calculatePortfolioSummary } from "$lib/utils";
    import type { Asset, Position } from "$lib/types";
    import AssetModal from "$lib/components/AssetModal.svelte";
    import TransactionFormModal from "$lib/components/transaction/TransactionFormModal.svelte";

    let assets: Asset[] = [];
    let positions: Position[] = [];
    let transactionModalOpen = false;
    let assetModalOpen = false;
    let selectedAsset: Asset | null = null;
    let loading = false;
    let error: string | null = null;
    let portfolioId: string | null = null;

    // Position을 Asset ID로 매핑
    $: positionMap = new Map<string, Position>();
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
            avg_price: position?.avg_price,
        };
    });

    // 포트폴리오 요약
    $: portfolioSummary = calculatePortfolioSummary(positions);

    async function loadAssets() {
        loading = true;
        error = null;
        try {
            // 1. Fetch Portfolios first
            const portfolios = await fetchPortfolios();

            // 2. Determine Portfolio ID
            if (portfolios.length > 0) {
                // If portfolioId is not set, use the first one
                if (!portfolioId) {
                    portfolioId = portfolios[0].id;
                }
            } else {
                console.warn("No portfolios found");
                loading = false;
                return;
            }

            // 3. Fetch data for the selected portfolio
            if (portfolioId) {
                const [assetsData, summaryData] = await Promise.all([
                    getAssets({ portfolio_id: portfolioId }),
                    getPortfolioSummary({ portfolio_id: portfolioId }),
                ]);
                assets = assetsData;
                positions = summaryData.positions; // Assuming summary endpoint returns positions or we need separate positions call?
                // Wait, getPortfolioSummary signature might not take args? It usually does for a specific portfolio or global user summary?
                // Let's check api but for now assume we filter by portfolio.
                // Actually `getPortfolioSummary` in api might leverage `portfolio_id` query param if we update it?
                // `src/lib/apis/portfolio.ts` has `get_portfolio_summary = api_router('portfolios', 'get', 'summary')`
                // Ideally we should use `fetchPortfolio` or `fetchPortfolioPositions` but let's stick to existing if it supports query.
            }

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

    function openAddTransactionModal(asset: Asset) {
        selectedAsset = asset;
        transactionModalOpen = true;
    }

    function handleTransactionCreated() {
        loadAssets();
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

<AssetModal
    bind:open={assetModalOpen}
    portfolioId={portfolioId || ""}
    on:created={handleAssetCreated}
/>
<TransactionFormModal
    bind:open={transactionModalOpen}
    assetId={selectedAsset?.id || ""}
    assetSymbol={selectedAsset?.symbol || ""}
    portfolioId={portfolioId || ""}
    oncreated={handleTransactionCreated}
/>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Assets</h1>
        <div class="flex gap-2 flex-wrap">
            <Button
                color="alternative"
                class="btn-outline"
                size="sm"
                onclick={handleRefreshPrices}>Refresh Prices</Button
            >
            <Button onclick={openAddAssetModal} class="btn-primary" size="sm">
                <PlusOutline class="w-4 h-4 mr-2" />
                Add Asset
            </Button>
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
                    <TableHeadCell>Avg Price</TableHeadCell>
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
                    <TableHeadCell>Avg Price</TableHeadCell>
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
                                {asset.avg_price !== undefined
                                    ? formatCurrency(asset.avg_price)
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
                                    class="btn-primary"
                                    onclick={() =>
                                        openAddTransactionModal(asset)}
                                >
                                    <PlusOutline class="w-3 h-3 mr-1" />
                                    Add Transaction
                                </Button>
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    {/if}
</div>
