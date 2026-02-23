<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";
    import type { PortfolioHistoryResponse } from "$lib/types";

    let { data = [] }: { data: PortfolioHistoryResponse[] } = $props();

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $effect(() => {
        if (chart && data) {
            updateChartData();
        }
    });

    function updateChartData() {
        if (!data || data.length === 0) return;

        const sorted = [...data].sort(
            (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
        );

        const labels = sorted.map((h) => new Date(h.date).toLocaleDateString());
        const dataValue = sorted.map((h) => h.total_value);
        const dataCash = sorted.map((h) => h.uninvested_cash);

        chart.data.labels = labels;
        chart.data.datasets[0].data = dataValue;
        if (chart.data.datasets[1]) {
            chart.data.datasets[1].data = dataCash;
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
                        borderColor: "#10B981",
                        backgroundColor: "rgba(16, 185, 129, 0.1)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                    },
                    {
                        label: "Uninvested Cash ($)",
                        data: [],
                        borderColor: "#9CA3AF",
                        borderDash: [5, 5],
                        backgroundColor: "transparent",
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
                        },
                    },
                },
                scales: {
                    y: {
                        beginAtZero: false,
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
