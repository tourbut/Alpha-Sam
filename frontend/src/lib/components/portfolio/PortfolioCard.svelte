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
    size="xl"
    class="!max-w-none w-full w-full !max-w-none cursor-pointer hover:shadow-lg transition-all duration-300 p-6 bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-900 border-0 shadow-sm hover:shadow-md"
    {onclick}
>
    <!-- 카드 헤더: 아이콘 + 이름 + 뱃지 -->
    <div class="flex items-start justify-between mb-5">
        <div class="flex items-center gap-3">
            <div
                class="w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/40 flex items-center justify-center"
            >
                <Wallet
                    class="w-5 h-5 text-primary-600 dark:text-primary-400"
                />
            </div>
            <div>
                <h3
                    class="text-base font-semibold text-neutral-900 dark:text-neutral-100"
                >
                    {portfolio.name}
                </h3>
                {#if isCurrent}
                    <Badge color="blue" class="text-xs mt-1">Current</Badge>
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
            <Dropdown placement="bottom-end" class="list-none">
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
            class="text-sm text-neutral-600 dark:text-neutral-400 mb-3 line-clamp-1"
        >
            {portfolio.description}
        </p>
    {/if}

    <!-- 날짜 정보 -->
    <div class="text-xs text-neutral-500 dark:text-neutral-400 mb-4">
        {#if portfolio.created_at}
            Created {new Date(portfolio.created_at).toLocaleDateString()}
        {/if}
    </div>

    <!-- Total Value 통계 영역 -->
    <div class="mb-5">
        <div
            class="text-xs text-neutral-500 dark:text-neutral-400 uppercase tracking-wide mb-1 font-medium"
        >
            Total Value
        </div>
        <div class="text-3xl font-bold text-primary-600 dark:text-primary-400">
            ${portfolio.totalValue?.toLocaleString() ?? "0"}
        </div>
    </div>

    <!-- Lazy Loaded Pie Chart -->
    <div class="mb-5">
        {#if ChartComponent && portfolio.assets?.length > 0}
            <ChartComponent assets={portfolio.assets} />
        {:else if portfolio.assets?.length > 0}
            <div
                class="w-full max-w-[160px] h-[160px] mx-auto flex items-center justify-center text-neutral-400 dark:text-neutral-500 text-xs rounded-lg bg-neutral-100/50 dark:bg-neutral-700/30"
            >
                Loading chart...
            </div>
        {:else}
            <div
                class="w-full max-w-[160px] h-[160px] mx-auto flex items-center justify-center text-neutral-400 dark:text-neutral-500 text-xs rounded-lg bg-neutral-100/50 dark:bg-neutral-700/30"
            >
                No assets yet
            </div>
        {/if}
    </div>

    <!-- 자산 분배 리스트 -->
    {#if portfolio.assets && portfolio.assets.length > 0}
        <div class="mb-5">
            <AssetBreakdownList assets={portfolio.assets} maxItems={3} />
        </div>
    {/if}

    <!-- 카드 푸터: Asset Count + Manage Button -->
    <div
        class="flex flex-col gap-3 pt-4 border-t border-neutral-200 dark:border-neutral-700"
    >
        <div class="text-xs text-neutral-500 dark:text-neutral-400 font-medium">
            {portfolio.assets?.length ?? 0}
            {portfolio.assets?.length === 1 ? "asset" : "assets"}
        </div>
        <Button
            size="sm"
            class="w-full !text-center !gap-1.5 btn-primary"
            onclick={(e: MouseEvent) => {
                e.stopPropagation();
                onManageClick?.(e);
            }}
        >
            <span>Manage Assets</span>
            <ArrowRight class="w-3.5 h-3.5" />
        </Button>
    </div>
</Card>
