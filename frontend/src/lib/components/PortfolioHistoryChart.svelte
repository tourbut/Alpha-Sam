<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";
    import type { PortfolioHistory } from "$lib/types";

    export let history: PortfolioHistory[] = [];

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $: if (chart && history) {
        updateChartData();
    }

    function updateChartData() {
        if (!history || history.length === 0) return;

        // Sort by date ascending
        const sorted = [...history].sort(
            (a, b) =>
                new Date(a.timestamp).getTime() -
                new Date(b.timestamp).getTime(),
        );

        const labels = sorted.map((h) =>
            new Date(h.timestamp).toLocaleDateString(),
        );
        const dataValue = sorted.map((h) => h.total_value);
        const dataCost = sorted.map((h) => h.total_cost);

        chart.data.labels = labels;
        chart.data.datasets[0].data = dataValue;
        if (chart.data.datasets[1]) {
            chart.data.datasets[1].data = dataCost;
        } else {
            // Should be initialized in onMount, but handle update if needed
        }
        chart.update();
    }

    onMount(() => {
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "Total Value ($)",
                        data: [],
                        borderColor: "#10B981", // Emerald 500
                        backgroundColor: "rgba(16, 185, 129, 0.1)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                    },
                    {
                        label: "Total Cost ($)",
                        data: [],
                        borderColor: "#9CA3AF", // Gray 400
                        borderDash: [5, 5],
                        backgroundColor: "rgba(156, 163, 175, 0.1)",
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                    title: {
                        display: false,
                    },
                    tooltip: {
                        mode: "index",
                        intersect: false,
                        callbacks: {
                            label: function (context: any) {
                                let label = context.dataset.label || "";
                                if (label) {
                                    label += ": ";
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat("en-US", {
                                        style: "currency",
                                        currency: "USD",
                                    }).format(context.parsed.y);
                                }
                                return label;
                            },
                            afterBody: function (tooltipItems: any[]) {
                                const valueItem = tooltipItems.find(
                                    (i: any) => i.datasetIndex === 0,
                                );
                                const costItem = tooltipItems.find(
                                    (i: any) => i.datasetIndex === 1,
                                );

                                if (valueItem && costItem) {
                                    const value = valueItem.parsed.y;
                                    const cost = costItem.parsed.y;
                                    const pl = value - cost;
                                    const plPercent =
                                        cost > 0 ? (pl / cost) * 100 : 0;

                                    return `P/L: ${new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(pl)} (${plPercent.toFixed(2)}%)`;
                                }
                                return "";
                            },
                        },
                    },
                },
                scales: {
                    y: {
                        beginAtZero: false, // Value unlikely to be 0
                        grid: {
                            color: "rgba(0, 0, 0, 0.05)",
                        },
                    },
                    x: {
                        grid: {
                            display: false,
                        },
                    },
                },
                interaction: {
                    mode: "nearest",
                    axis: "x",
                    intersect: false,
                },
            },
        });
    });

    onDestroy(() => {
        if (chart) chart.destroy();
    });
</script>

<div class="relative h-64 w-full">
    <canvas bind:this={canvas}></canvas>
</div>
