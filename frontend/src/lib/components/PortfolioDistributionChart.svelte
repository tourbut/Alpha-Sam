<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";
    import type { AssetAllocationResponse } from "$lib/types";

    let { data = [] }: { data: AssetAllocationResponse[] } = $props();

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $effect(() => {
        if (chart && data) {
            updateChart();
        }
    });

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
                            "#3B82F6",
                            "#10B981",
                            "#F59E0B",
                            "#EF4444",
                            "#8B5CF6",
                            "#EC4899",
                            "#6366F1",
                            "#14B8A6",
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

        chart.data.labels = data.map(
            (d) => `${d.ticker} (${d.percentage.toFixed(1)}%)`,
        );
        chart.data.datasets[0].data = data.map((d) => d.total_value);
        chart.update();
    }
</script>

<div class="relative h-64 w-full">
    <canvas bind:this={canvas}></canvas>
</div>
