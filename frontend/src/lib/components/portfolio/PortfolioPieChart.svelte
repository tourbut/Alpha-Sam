<script lang="ts">
  import { onMount } from "svelte";
  import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from "chart.js";

  interface Asset {
    symbol: string;
    name: string;
    value: number;
    percentage: number;
  }

  let { assets = [] }: { assets: Asset[] } = $props();

  let canvasElement: HTMLCanvasElement;
  let chart: Chart | null = null;

  onMount(() => {
    // Register only required components for doughnut chart
    Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

    const colors = [
      "#2774AE", // primary-600
      "#00416A", // secondary-500
      "#2E8B57", // accent-500
      "#F59E0B", // warning
      "#EF4444", // error
      "#6B7280", // neutral-500
      "#8B5CF6", // purple
      "#EC4899", // pink
    ];

    const ctx = canvasElement.getContext("2d");
    if (ctx) {
      chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: assets.map((a) => a.symbol),
          datasets: [
            {
              data: assets.map((a) => a.percentage),
              backgroundColor: colors.slice(0, assets.length),
              borderWidth: 2,
              borderColor: "#ffffff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              enabled: true,
              callbacks: {
                label: function (context) {
                  const asset = assets[context.dataIndex];
                  return `${asset.symbol}: $${asset.value.toLocaleString()} (${asset.percentage.toFixed(1)}%)`;
                },
              },
            },
          },
          cutout: "60%",
        },
      });
    }

    return () => {
      if (chart) {
        chart.destroy();
      }
    };
  });

  $effect(() => {
    if (chart && assets) {
      const colors = [
        "#2774AE",
        "#00416A",
        "#2E8B57",
        "#F59E0B",
        "#EF4444",
        "#6B7280",
        "#8B5CF6",
        "#EC4899",
      ];

      chart.data.labels = assets.map((a) => a.symbol);
      chart.data.datasets[0].data = assets.map((a) => a.percentage);
      chart.data.datasets[0].backgroundColor = colors.slice(0, assets.length);
      chart.update();
    }
  });
</script>

<div class="relative w-full max-w-[200px] mx-auto">
  <canvas bind:this={canvasElement}></canvas>
</div>
