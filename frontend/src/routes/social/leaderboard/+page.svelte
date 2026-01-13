<script lang="ts">
    import { onMount } from "svelte";
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Badge,
        Card,
        Spinner,
    } from "flowbite-svelte";
    import { socialStore } from "$lib/stores/social.svelte";
    import {
        UserCircleOutline,
        ChartMixedDollarOutline,
    } from "flowbite-svelte-icons";

    onMount(() => {
        socialStore.loadLeaderboard();
    });

    function getRankBadge(rank: number) {
        if (rank === 1) return { color: "yellow", text: "Gold" };
        if (rank === 2) return { color: "gray", text: "Silver" };
        if (rank === 3) return { color: "red", text: "Bronze" }; // 사실상 구리색 느낌
        return null;
    }
</script>

<div class="container mx-auto p-4 max-w-4xl">
    <div class="flex flex-col items-center mb-10 text-center">
        <ChartMixedDollarOutline class="w-16 h-16 text-primary-500 mb-4" />
        <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-2">
            Weekly Leaderboard
        </h1>
        <p class="text-gray-500 dark:text-gray-400">
            이번 주 최고의 누적 수익률을 기록한 투자자들입니다.
        </p>
    </div>

    {#if socialStore.loading}
        <div class="flex justify-center py-20">
            <Spinner size="12" />
        </div>
    {:else}
        <Card class="p-0 overflow-hidden border-none shadow-xl">
            <Table hoverable={true}>
                <TableHead class="bg-gray-50 dark:bg-gray-700">
                    <TableHeadCell>Rank</TableHeadCell>
                    <TableHeadCell>Investor</TableHeadCell>
                    <TableHeadCell class="text-right">PnL %</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each socialStore.leaderboard as entry}
                        <TableBodyRow class="text-base">
                            <TableBodyCell class="font-bold w-24">
                                <div class="flex items-center gap-2">
                                    {entry.rank}
                                    {#if getRankBadge(entry.rank)}
                                        <Badge
                                            color={getRankBadge(entry.rank)!
                                                .color as any}
                                            rounded
                                        >
                                            {getRankBadge(entry.rank)!.text}
                                        </Badge>
                                    {/if}
                                </div>
                            </TableBodyCell>
                            <TableBodyCell>
                                <div class="flex items-center gap-3">
                                    <UserCircleOutline
                                        class="w-6 h-6 text-gray-400"
                                    />
                                    <span
                                        class="font-medium text-gray-900 dark:text-white"
                                    >
                                        {entry.nickname}
                                    </span>
                                </div>
                            </TableBodyCell>
                            <TableBodyCell
                                class="text-right font-mono font-bold text-green-500"
                            >
                                +{entry.pnl_percent.toFixed(2)}%
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </Card>

        <div
            class="mt-8 p-6 bg-primary-50 dark:bg-primary-900/20 rounded-2xl border border-primary-100 dark:border-primary-800 flex items-center gap-4"
        >
            <ChartMixedDollarOutline class="w-10 h-10 text-primary-500" />
            <div>
                <h4
                    class="font-bold text-primary-900 dark:text-primary-100 italic"
                >
                    "당신의 포트폴리오도 리더보드에 올리고 싶으신가요?"
                </h4>
                <p class="text-sm text-primary-700 dark:text-primary-300">
                    프로필 설정에서 '리더보드 공개'를 활성화하면 자동으로 랭킹에
                    집계됩니다.
                </p>
            </div>
        </div>
    {/if}
</div>
