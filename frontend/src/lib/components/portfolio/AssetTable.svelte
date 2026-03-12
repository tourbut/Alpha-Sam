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
    import { Button } from "flowbite-svelte";
    import { PieChart } from "lucide-svelte";
    import DataTable, {
        type ColumnDef,
    } from "$lib/components/common/DataTable.svelte";

    let {
        assets = [],
        onViewTransactions,
    }: {
        assets: AssetRow[];
        onViewTransactions?: (assetId: string) => void;
    } = $props();

    // 수량 0 종목 표시 여부 (기본값: 숨김)
    let showZeroQuantity = $state(false);

    // 필터링된 자산 목록 (파생 상태)
    let filteredAssets = $derived(
        showZeroQuantity ? assets : assets.filter((a) => a.quantity > 0),
    );

    let columns: ColumnDef<AssetRow>[] = [
        { key: "symbol", label: "Asset" },
        { key: "quantity", label: "Quantity", align: "right" },
        { key: "avgPrice", label: "Avg Price", align: "right" },
        { key: "currentPrice", label: "Current Price", align: "right" },
        { key: "totalValue", label: "Total Value", align: "right" },
        { key: "change", label: "Change", align: "right" },
        { key: "realizedPl", label: "Realized P/L", align: "right" },
        { key: "actions", label: "Actions", align: "center", sortable: false },
    ];
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
    <DataTable data={filteredAssets} {columns}>
        {#snippet customCell(asset, colKey)}
            {#if colKey === "symbol"}
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
            {:else if colKey === "quantity"}
                {asset.quantity}
            {:else if colKey === "avgPrice"}
                ${asset.avgPrice.toLocaleString()}
            {:else if colKey === "currentPrice"}
                ${asset.currentPrice.toLocaleString()}
            {:else if colKey === "totalValue"}
                <span class="font-semibold"
                    >${asset.totalValue.toLocaleString()}</span
                >
            {:else if colKey === "change"}
                <span
                    class={asset.change >= 0
                        ? "text-accent-600 dark:text-accent-400"
                        : "text-red-600 dark:text-red-400"}
                >
                    {asset.change >= 0 ? "+" : ""}{asset.change.toFixed(2)}%
                </span>
            {:else if colKey === "realizedPl"}
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
            {:else if colKey === "actions"}
                <Button
                    size="xs"
                    color="light"
                    onclick={() => onViewTransactions?.(asset.id)}
                >
                    View Transactions
                </Button>
            {/if}
        {/snippet}
    </DataTable>
{/if}
