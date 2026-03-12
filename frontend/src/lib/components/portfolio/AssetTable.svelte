<script module lang="ts">
    export interface AssetRow {
        id: string;
        symbol: string;
        name: string;
        quantity: number;
        avgPrice: number;
        currentPrice: number;
        totalValue: number;
        change: number;
        realizedPl: number;
    }
</script>

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
    import { PieChart } from "lucide-svelte";

    let {
        assets = [],
        onViewTransactions,
    }: {
        assets: AssetRow[];
        onViewTransactions?: (assetId: string) => void;
    } = $props();

    // 수량 0 종목 표시 여부 (기본값: 숨김)
    let showZeroQuantity = $state(false);
    // 정렬 상태
    let sortBy = $state<keyof AssetRow | null>(null);
    let sortOrder = $state<"asc" | "desc">("asc");

    // 필터링된 자산 목록 (파생 상태)
    let filteredAssets = $derived(
        showZeroQuantity ? assets : assets.filter((a) => a.quantity > 0),
    );

    // 정렬된 자산 목록 (파생 상태)
    let sortedAssets = $derived.by(() => {
        if (!sortBy) return filteredAssets;

        const sorted = [...filteredAssets];
        sorted.sort((a, b) => {
            const aValue = a[sortBy!];
            const bValue = b[sortBy!];

            // 숫자 비교
            if (typeof aValue === "number" && typeof bValue === "number") {
                return sortOrder === "asc"
                    ? (aValue as number) - (bValue as number)
                    : (bValue as number) - (aValue as number);
            }

            // 문자 비교
            const aStr = String(aValue).toLowerCase();
            const bStr = String(bValue).toLowerCase();
            return sortOrder === "asc"
                ? aStr.localeCompare(bStr)
                : bStr.localeCompare(aStr);
        });

        return sorted;
    });

    function handleSort(column: keyof AssetRow) {
        if (sortBy === column) {
            sortOrder = sortOrder === "asc" ? "desc" : "asc";
        } else {
            sortBy = column;
            sortOrder = "asc";
        }
    }

    function getSortIcon(column: keyof AssetRow) {
        if (sortBy !== column) return null;
        return sortOrder === "asc" ? "↑" : "↓";
    }
</script>

<!-- 수량 0 종목 표시 토글 -->
<div
    class="flex items-center gap-2 px-4 pt-4 pb-2 border-b border-neutral-100 dark:border-neutral-700"
>
    <input
        type="checkbox"
        id="show-zero-quantity"
        bind:checked={showZeroQuantity}
        class="w-4 h-4 rounded border-gray-300 text-primary-600 cursor-pointer"
    />
    <label
        for="show-zero-quantity"
        class="text-sm text-neutral-600 dark:text-neutral-400 cursor-pointer select-none"
    >
        수량 0 종목 보기
    </label>
    {#if !showZeroQuantity}
        <span class="text-xs text-neutral-400 dark:text-neutral-500 ml-1">
            (전량 매도 종목 숨김 중)
        </span>
    {/if}
</div>

{#if filteredAssets.length === 0 && assets.length > 0}
    <div class="text-center py-8 text-neutral-500 dark:text-neutral-400">
        <p class="text-sm">수량이 있는 종목이 없습니다.</p>
        <p class="text-xs mt-1">
            "수량 0 종목 보기"를 체크하면 전량 매도된 종목을 확인할 수 있습니다.
        </p>
    </div>
{:else}
    <div class="w-full overflow-hidden">
        <Table hoverable={true}>
            <TableHead>
                <TableHeadCell
                    class="cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("symbol")}
                >
                    <div class="flex items-center gap-2">
                        <span>Asset</span>
                        {#if getSortIcon("symbol")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("symbol")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("quantity")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Quantity</span>
                        {#if getSortIcon("quantity")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("quantity")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("avgPrice")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Avg Price</span>
                        {#if getSortIcon("avgPrice")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("avgPrice")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("currentPrice")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Current Price</span>
                        {#if getSortIcon("currentPrice")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("currentPrice")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("totalValue")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Total Value</span>
                        {#if getSortIcon("totalValue")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("totalValue")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("change")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Change</span>
                        {#if getSortIcon("change")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("change")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell
                    class="text-right cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors"
                    onclick={() => handleSort("realizedPl")}
                >
                    <div class="flex items-center justify-end gap-2">
                        <span>Realized P/L</span>
                        {#if getSortIcon("realizedPl")}
                            <span class="text-xs font-semibold"
                                >{getSortIcon("realizedPl")}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
                <TableHeadCell class="text-center">Actions</TableHeadCell>
            </TableHead>
            <TableBody>
                {#each sortedAssets as asset}
                    <TableBodyRow>
                        <TableBodyCell>
                            <div class="flex items-center gap-2">
                                <div
                                    class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center flex-shrink-0"
                                >
                                    <PieChart
                                        class="w-4 h-4 text-primary-600 dark:text-primary-400"
                                    />
                                </div>
                                <div class="min-w-0">
                                    <div
                                        class="font-semibold text-neutral-900 dark:text-neutral-100 truncate"
                                    >
                                        {asset.symbol}
                                    </div>
                                    <div
                                        class="text-xs text-neutral-500 dark:text-neutral-400 truncate"
                                    >
                                        {asset.name}
                                    </div>
                                </div>
                            </div>
                        </TableBodyCell>
                        <TableBodyCell class="text-right whitespace-nowrap"
                            >{asset.quantity}</TableBodyCell
                        >
                        <TableBodyCell class="text-right whitespace-nowrap"
                            >${asset.avgPrice.toLocaleString()}</TableBodyCell
                        >
                        <TableBodyCell class="text-right whitespace-nowrap"
                            >${asset.currentPrice.toLocaleString()}</TableBodyCell
                        >
                        <TableBodyCell
                            class="text-right font-semibold whitespace-nowrap"
                        >
                            ${asset.totalValue.toLocaleString()}
                        </TableBodyCell>
                        <TableBodyCell class="text-right whitespace-nowrap">
                            <span
                                class={asset.change >= 0
                                    ? "text-accent-600 dark:text-accent-400"
                                    : "text-red-600 dark:text-red-400"}
                            >
                                {asset.change >= 0
                                    ? "+"
                                    : ""}{asset.change.toFixed(2)}%
                            </span>
                        </TableBodyCell>
                        <TableBodyCell class="text-right whitespace-nowrap">
                            <span
                                class={asset.realizedPl === 0
                                    ? "text-neutral-500 dark:text-neutral-400"
                                    : asset.realizedPl > 0
                                      ? "text-blue-600 dark:text-blue-400"
                                      : "text-red-600 dark:text-red-400"}
                            >
                                {asset.realizedPl === 0
                                    ? "$0.00"
                                    : (asset.realizedPl > 0 ? "+" : "") +
                                      "$" +
                                      asset.realizedPl.toFixed(2)}
                            </span>
                        </TableBodyCell>
                        <TableBodyCell class="text-center whitespace-nowrap">
                            <Button
                                size="xs"
                                color="light"
                                onclick={() => onViewTransactions?.(asset.id)}
                            >
                                View Transactions
                            </Button>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>
    </div>
{/if}
