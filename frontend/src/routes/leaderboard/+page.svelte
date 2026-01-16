<script lang="ts">
    import { onMount } from "svelte";
    import { getLeaderboard } from "$lib/apis/social";
    import type { LeaderboardEntry } from "$lib/types";
    import {
        Card,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Badge,
        Spinner,
    } from "flowbite-svelte";
    import { formatCurrency, formatPercent, getColorClass } from "$lib/utils";

    let leaderboard: LeaderboardEntry[] = $state([]);
    let loading = $state(true);
    let error = $state("");

    onMount(async () => {
        try {
            leaderboard = await getLeaderboard();
        } catch (e) {
            error = "리더보드를 불러오는 데 실패했습니다.";
            console.error(e);
        } finally {
            loading = false;
        }
    });

    const getRankBadgeColor = (
        rank: number,
    ): "yellow" | "gray" | "red" | "purple" => {
        if (rank === 1) return "yellow";
        if (rank === 2) return "gray"; // Silver
        if (rank === 3) return "red"; // Bronzeish
        return "purple";
    };
</script>

<div class="container mx-auto px-4 py-8 max-w-5xl">
    <div class="mb-8 text-center sm:text-left">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Leaderboard
        </h1>
        <p class="text-gray-500 dark:text-gray-400">
            Top performers based on portfolio returns. (Updated Hourly)
        </p>
    </div>

    {#if loading}
        <div class="flex justify-center py-20">
            <Spinner size="10" color="purple" />
        </div>
    {:else if error}
        <div class="text-center text-red-500 py-10">
            {error}
        </div>
    {:else}
        <Card class="w-full">
            <Table hoverable>
                <TableHead>
                    <TableHeadCell class="w-20 text-center">Rank</TableHeadCell>
                    <TableHeadCell>User</TableHeadCell>
                    <TableHeadCell class="text-right">Return Rate</TableHeadCell
                    >
                    <TableHeadCell class="text-right">Total Value</TableHeadCell
                    >
                </TableHead>
                <TableBody>
                    {#each leaderboard as entry}
                        <TableBodyRow class="cursor-pointer">
                            <TableBodyCell class="text-center font-bold">
                                {#if entry.rank <= 3}
                                    <Badge
                                        color={getRankBadgeColor(entry.rank)}
                                        rounded
                                        class="w-8 h-8 flex items-center justify-center mx-auto text-lg"
                                    >
                                        {entry.rank}
                                    </Badge>
                                {:else}
                                    <span class="text-gray-500"
                                        >{entry.rank}</span
                                    >
                                {/if}
                            </TableBodyCell>
                            <TableBodyCell>
                                <div
                                    class="font-medium text-gray-900 dark:text-white"
                                >
                                    {entry.nickname}
                                </div>
                            </TableBodyCell>
                            <TableBodyCell class="text-right font-bold text-lg">
                                <span class={getColorClass(entry.return_rate)}>
                                    {formatPercent(entry.return_rate)}
                                </span>
                            </TableBodyCell>
                            <TableBodyCell class="text-right text-gray-500">
                                {formatCurrency(entry.total_value)}
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </Card>
    {/if}
</div>
