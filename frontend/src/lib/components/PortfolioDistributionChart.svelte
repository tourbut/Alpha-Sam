<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";
    import type { Position } from "$lib/types";

    export let positions: Position[] = [];

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    // React to positions changes
    $: if (chart && positions) {
        updateChart();
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: [],
                datasets: [
                    {
                        data: [],
                        backgroundColor: [
                            "#3B82F6", // Blue
                            "#10B981", // Green
                            "#F59E0B", // Yellow
                            "#EF4444", // Red
                            "#8B5CF6", // Purple
                            "#EC4899", // Pink
                            "#6366F1", // Indigo
                            "#14B8A6", // Teal
                        ],
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "right",
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                        },
                    },
                    title: {
                        display: false,
                        text: "Portfolio Allocation",
                    },
                },
            },
        });

        updateChart();
    });

    onDestroy(() => {
        if (chart) chart.destroy();
    });

    function updateChart() {
        if (!chart) return;

        const allocation: Record<string, number> = {};

        positions.forEach((p) => {
            const symbol = p.asset_symbol || `Asset ${p.asset_id}`;
            // Use valuation if available, otherwise 0.
            // Note: Valuation might be null/undefined if price fetching failed.
            const value = p.valuation ?? 0;
            allocation[symbol] = (allocation[symbol] || 0) + value;
        });

        chart.data.labels = Object.keys(allocation);
        chart.data.datasets[0].data = Object.values(allocation);
        chart.update();
    }
</script>

<div class="relative h-64 w-full">
    <canvas bind:this={canvas}></canvas>
</div>
