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

    export interface ColumnDef<T> {
        key: string;
        label: string;
        sortable?: boolean;
        align?: "left" | "center" | "right";
    }
</script>

<script lang="ts">
    import {
        Table,
        TableBody,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        TableBodyCell,
    } from "flowbite-svelte";
    import type { Snippet } from "svelte";

    type T = $$Generic<Record<string, any>>;

    let {
        data = [],
        columns = [],
        customCell,
    }: {
        data: T[];
        columns: ColumnDef<T>[];
        customCell?: Snippet<[T, string]>;
    } = $props();

    let sortBy = $state<string | null>(null);
    let sortOrder = $state<"asc" | "desc">("asc");

    let sortedData = $derived.by(() => {
        if (!sortBy) return data;

        const sorted = [...data];
        sorted.sort((a, b) => {
            const aValue = a[sortBy!];
            const bValue = b[sortBy!];

            if (typeof aValue === "number" && typeof bValue === "number") {
                return sortOrder === "asc" ? aValue - bValue : bValue - aValue;
            }

            const aStr = String(aValue ?? "").toLowerCase();
            const bStr = String(bValue ?? "").toLowerCase();
            return sortOrder === "asc"
                ? aStr.localeCompare(bStr)
                : bStr.localeCompare(aStr);
        });

        return sorted;
    });

    function handleSort(key: string, sortable?: boolean) {
        if (sortable === false) return;
        if (sortBy === key) {
            sortOrder = sortOrder === "asc" ? "desc" : "asc";
        } else {
            sortBy = key;
            sortOrder = "asc";
        }
    }

    function getSortIcon(key: string) {
        if (sortBy !== key) return null;
        return sortOrder === "asc" ? "↑" : "↓";
    }

    function getAlignClass(align?: "left" | "center" | "right") {
        if (align === "right") return "text-right";
        if (align === "center") return "text-center";
        return "text-left";
    }
</script>

<div class="w-full overflow-hidden">
    <Table hoverable={true}>
        <TableHead>
            {#each columns as col}
                <TableHeadCell
                    class="{col.sortable !== false
                        ? 'cursor-pointer hover:bg-neutral-100 dark:hover:bg-neutral-700 select-none transition-colors'
                        : ''} {getAlignClass(col.align)}"
                    onclick={() => handleSort(col.key, col.sortable)}
                >
                    <div
                        class="flex items-center gap-2 {col.align === 'right'
                            ? 'justify-end'
                            : col.align === 'center'
                              ? 'justify-center'
                              : ''}"
                    >
                        <span>{col.label}</span>
                        {#if getSortIcon(col.key)}
                            <span class="text-xs font-semibold"
                                >{getSortIcon(col.key)}</span
                            >
                        {/if}
                    </div>
                </TableHeadCell>
            {/each}
        </TableHead>

        <TableBody>
            {#each sortedData as row}
                <TableBodyRow>
                    {#each columns as col}
                        <TableBodyCell
                            class="{getAlignClass(col.align)} whitespace-nowrap"
                        >
                            {#if customCell}
                                {@render customCell(row, col.key)}
                            {:else}
                                {row[col.key]}
                            {/if}
                        </TableBodyCell>
                    {/each}
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</div>
