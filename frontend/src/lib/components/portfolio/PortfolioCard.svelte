<script lang="ts">
    /**
     * PortfolioCard.svelte
     * 포트폴리오 정보를 표시하는 카드 컴포넌트
     * 와이어프레임 기준: 아이콘 + 이름 + 뱃지 + Total Value + 차트 + 자산 분배 + 푸터
     */
    import {
        Card,
        Button,
        Badge,
        Dropdown,
        DropdownItem,
    } from "flowbite-svelte";
    import {
        Wallet,
        ArrowRight,
        MoreVertical,
        Edit2,
        Trash2,
    } from "lucide-svelte";
    import AssetBreakdownList from "./AssetBreakdownList.svelte";
    import type { PortfolioAsset, PortfolioWithAssets } from "$lib/types";

    let {
        portfolio,
        isCurrent = false,
        ChartComponent = null,
        onclick,
        onManageClick,
        onedit,
        ondelete,
    }: {
        portfolio: PortfolioWithAssets;
        isCurrent?: boolean;
        ChartComponent?: any;
        onclick?: () => void;
        onManageClick?: (e: MouseEvent) => void;
        onedit?: () => void;
        ondelete?: () => void;
    } = $props();
</script>

<Card
    class="cursor-pointer hover:shadow-xl transition-all duration-300 hover:scale-[1.02] hover:border-primary-300 dark:hover:border-primary-600 p-6"
    {onclick}
>
    <!-- 카드 헤더: 아이콘 + 이름 + 뱃지 -->
    <div class="flex items-start justify-between mb-4">
        <div class="flex items-center gap-3">
            <div
                class="w-12 h-12 rounded-full bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900 dark:to-primary-800 flex items-center justify-center shadow-sm"
            >
                <Wallet
                    class="w-6 h-6 text-primary-600 dark:text-primary-400"
                />
            </div>
            <div>
                <h3
                    class="text-lg font-semibold text-neutral-900 dark:text-neutral-100"
                >
                    {portfolio.name}
                </h3>
                {#if isCurrent}
                    <Badge color="purple" class="text-xs">Current</Badge>
                {/if}
            </div>
        </div>

        <div class="relative">
            <Button
                color="light"
                class="!p-2 -mr-2"
                size="xs"
                onclick={(e: MouseEvent) => e.stopPropagation()}
            >
                <MoreVertical class="w-5 h-5 text-neutral-500" />
            </Button>
            <Dropdown placement="bottom-end">
                <DropdownItem
                    onclick={(e) => {
                        e.stopPropagation();
                        onedit?.();
                    }}
                >
                    <div class="flex items-center gap-2">
                        <Edit2 class="w-4 h-4" /> Edit
                    </div>
                </DropdownItem>
                <DropdownItem
                    onclick={(e) => {
                        e.stopPropagation();
                        ondelete?.();
                    }}
                    class="text-red-600 hover:text-red-700 dark:text-red-500 dark:hover:text-red-400"
                >
                    <div class="flex items-center gap-2">
                        <Trash2 class="w-4 h-4" /> Delete
                    </div>
                </DropdownItem>
            </Dropdown>
        </div>
    </div>

    <!-- 설명 -->
    {#if portfolio.description}
        <p
            class="text-sm text-neutral-600 dark:text-neutral-400 mb-4 line-clamp-2"
        >
            {portfolio.description}
        </p>
    {/if}

    <!-- Total Value 통계 영역 -->
    <div
        class="mb-4 p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg border border-dashed border-neutral-200 dark:border-neutral-700"
    >
        <div
            class="text-xs text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mb-1"
        >
            Total Value
        </div>
        <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">
            ${portfolio.totalValue?.toLocaleString() ?? "0"}
        </div>
    </div>

    <!-- Lazy Loaded Pie Chart -->
    <div class="mb-4">
        {#if ChartComponent && portfolio.assets?.length > 0}
            <svelte:component this={ChartComponent} assets={portfolio.assets} />
        {:else if portfolio.assets?.length > 0}
            <div
                class="w-full max-w-[180px] h-[180px] mx-auto flex items-center justify-center text-neutral-400 dark:text-neutral-500 text-sm border-2 border-dashed border-neutral-200 dark:border-neutral-700 rounded-lg bg-neutral-50 dark:bg-neutral-800"
            >
                Loading chart...
            </div>
        {:else}
            <div
                class="w-full max-w-[180px] h-[180px] mx-auto flex items-center justify-center text-neutral-400 dark:text-neutral-500 text-sm border-2 border-dashed border-neutral-200 dark:border-neutral-700 rounded-lg bg-neutral-50 dark:bg-neutral-800"
            >
                No assets yet
            </div>
        {/if}
    </div>

    <!-- 자산 분배 리스트 -->
    {#if portfolio.assets && portfolio.assets.length > 0}
        <div class="mb-4">
            <AssetBreakdownList assets={portfolio.assets} maxItems={3} />
        </div>
    {/if}

    <!-- 카드 푸터 -->
    <div
        class="flex items-center justify-between pt-4 border-t-2 border-neutral-200 dark:border-neutral-700"
    >
        <div class="text-xs text-neutral-500 dark:text-neutral-400">
            {portfolio.assets?.length ?? 0} assets
        </div>
        <Button
            size="xs"
            color="light"
            class="hover:bg-primary-50 dark:hover:bg-primary-900"
            onclick={(e: MouseEvent) => {
                e.stopPropagation();
                onManageClick?.(e);
            }}
        >
            Manage Assets
            <ArrowRight class="w-3 h-3 ml-1" />
        </Button>
    </div>
</Card>
