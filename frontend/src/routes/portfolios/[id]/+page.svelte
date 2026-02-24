<script lang="ts">
  import { page } from "$app/state";
  import { portfolioStore } from "$lib/stores/portfolio.svelte";
  import { onMount } from "svelte";
  import { fetchPortfolioSummary } from "$lib/apis/portfolio";
  import type { PortfolioSummary } from "$lib/types/portfolio";
  import {
    Button,
    Card,
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Spinner,
    Alert,
  } from "flowbite-svelte";
  import {
    Plus,
    ArrowLeft,
    PieChart,
    Info,
    DollarSign,
    TrendingUp,
    TrendingDown,
    Briefcase,
  } from "lucide-svelte";
  import AssetModal from "$lib/components/AssetModal.svelte";
  import { goto } from "$app/navigation";

  // 자산 데이터 인터페이스 정의
  interface AssetRow {
    id: string;
    symbol: string;
    name: string;
    quantity: number;
    avgPrice: number;
    currentPrice: number;
    totalValue: number;
    change: number;
  }

  let openAssetModal = $state(false);
  let portfolioId = $derived(page.params.id);
  let currentPortfolio = $derived(
    portfolioStore.portfolios.find((p) => p.id === portfolioId),
  );

  // 명시적 타입 지정으로 never[] 추론 문제 해결
  let assets: AssetRow[] = $state([]);
  let summary: PortfolioSummary | null = $state(null);
  let loading = $state(false);
  let error: string | null = $state(null);

  onMount(async () => {
    if (!currentPortfolio) {
      // If direct navigation, load portfolios to find name, etc.
      // (Ideally we should fetch specific portfolio details too if list is empty)
      await portfolioStore.loadPortfolios();
    }
    await loadAssets();
  });

  async function loadAssets() {
    // portfolioId가 없으면 로딩하지 않음
    if (!portfolioId) {
      error = "Portfolio ID가 없습니다.";
      return;
    }

    loading = true;
    error = null;
    try {
      const data = await fetchPortfolioSummary(portfolioId);

      summary = {
        totalValuation: data.summary.total_value || 0,
        totalProfitLoss: data.summary.total_pl || 0,
        totalReturnRate: data.summary.total_pl_stats?.percent || 0,
        totalInvested: data.summary.total_cost || 0,
        realizedProfitLoss: data.summary.realized_pl || 0,
      };

      // Map API response (snake_case) to UI format (camelCase)
      assets = data.positions.map((p: any) => ({
        id: p.asset_id,
        symbol: p.asset_symbol,
        name: p.asset_name,
        quantity: p.quantity,
        avgPrice: p.avg_price,
        currentPrice: p.current_price || p.avg_price, // fallback
        totalValue:
          p.valuation || p.quantity * (p.current_price || p.avg_price),
        change: p.return_rate || 0,
      }));
    } catch (e: any) {
      console.error("Failed to load assets:", e);
      error = e.message || "Failed to load assets";
    } finally {
      loading = false;
    }
  }

  function viewAssetTransactions(assetId: string) {
    goto(`/portfolios/${portfolioId}/assets/${assetId}`);
  }

  function goBack() {
    goto("/portfolios");
  }
</script>

<div class="space-y-6">
  <div
    class="flex items-center gap-2 text-sm text-neutral-600 dark:text-neutral-400"
  >
    <button
      onclick={goBack}
      class="hover:text-primary-600 dark:hover:text-primary-400"
    >
      <ArrowLeft class="w-4 h-4 inline mr-1" />
      Back to Portfolios
    </button>
  </div>

  <div class="flex items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
        {currentPortfolio?.name || "Portfolio"}
      </h1>
      <p class="text-neutral-600 dark:text-neutral-400 mt-1">
        Manage assets and track performance
      </p>
    </div>
    <Button
      class="btn-primary"
      size="sm"
      onclick={() => (openAssetModal = true)}
    >
      <Plus class="w-4 h-4 mr-2" />
      Add Asset
    </Button>
  </div>

  {#if loading}
    <div class="flex justify-center py-12">
      <Spinner size="12" color="purple" />
    </div>
  {:else if error}
    <Alert color="red" class="mb-4">
      <span class="font-medium">Error!</span>
      {error}
    </Alert>
  {:else}
    <!-- Summary Section -->
    {#if summary}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card class="!max-w-none w-full p-4" size="md">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-neutral-500">Total Value</span
            >
            <Briefcase class="w-4 h-4 text-primary-500" />
          </div>
          <div class="text-2xl font-bold">
            ${summary.totalValuation.toLocaleString()}
          </div>
        </Card>

        <Card class="!max-w-none w-full p-4" size="md">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-neutral-500"
              >Total Profit/Loss</span
            >
            {#if summary.totalProfitLoss >= 0}
              <TrendingUp class="w-4 h-4 text-green-500" />
            {:else}
              <TrendingDown class="w-4 h-4 text-red-500" />
            {/if}
          </div>
          <div
            class="text-2xl font-bold {summary.totalProfitLoss >= 0
              ? 'text-green-600'
              : 'text-red-600'}"
          >
            {summary.totalProfitLoss >= 0
              ? "+"
              : ""}${summary.totalProfitLoss.toLocaleString()}
            <span class="text-sm font-normal text-neutral-500 ml-1">
              ({summary.totalReturnRate.toFixed(2)}%)
            </span>
          </div>
        </Card>

        <Card class="!max-w-none w-full p-4" size="md">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-neutral-500"
              >Realized Profit</span
            >
            <DollarSign class="w-4 h-4 text-blue-500" />
          </div>
          <div
            class="text-2xl font-bold {summary.realizedProfitLoss >= 0
              ? 'text-blue-600'
              : 'text-red-600'}"
          >
            {summary.realizedProfitLoss >= 0
              ? "+"
              : ""}${summary.realizedProfitLoss.toLocaleString()}
          </div>
        </Card>

        <Card class="!max-w-none w-full p-4" size="md">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-neutral-500"
              >Total Invested</span
            >
            <div class="w-4 h-4 text-neutral-400">IV</div>
          </div>
          <div
            class="text-2xl font-bold text-neutral-700 dark:text-neutral-300"
          >
            ${summary.totalInvested.toLocaleString()}
          </div>
        </Card>
      </div>
    {/if}

    {#if assets.length > 0}
      <Card class="!max-w-none w-full mt-6">
        <div class="overflow-x-auto">
          <Table hoverable={true}>
            <TableHead>
              <TableHeadCell>Asset</TableHeadCell>
              <TableHeadCell class="text-right">Quantity</TableHeadCell>
              <TableHeadCell class="text-right">Avg Price</TableHeadCell>
              <TableHeadCell class="text-right">Current Price</TableHeadCell>
              <TableHeadCell class="text-right">Total Value</TableHeadCell>
              <TableHeadCell class="text-right">Change</TableHeadCell>
              <TableHeadCell class="text-center">Actions</TableHeadCell>
            </TableHead>
            <TableBody>
              {#each assets as asset}
                <TableBodyRow>
                  <TableBodyCell>
                    <div class="flex items-center gap-2">
                      <div
                        class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center"
                      >
                        <PieChart
                          class="w-4 h-4 text-primary-600 dark:text-primary-400"
                        />
                      </div>
                      <div>
                        <div
                          class="font-semibold text-neutral-900 dark:text-neutral-100"
                        >
                          {asset.symbol}
                        </div>
                        <div
                          class="text-xs text-neutral-500 dark:text-neutral-400"
                        >
                          {asset.name}
                        </div>
                      </div>
                    </div>
                  </TableBodyCell>
                  <TableBodyCell class="text-right"
                    >{asset.quantity}</TableBodyCell
                  >
                  <TableBodyCell class="text-right"
                    >${asset.avgPrice.toLocaleString()}</TableBodyCell
                  >
                  <TableBodyCell class="text-right"
                    >${asset.currentPrice.toLocaleString()}</TableBodyCell
                  >
                  <TableBodyCell class="text-right font-semibold">
                    ${asset.totalValue.toLocaleString()}
                  </TableBodyCell>
                  <TableBodyCell class="text-right">
                    <span
                      class={asset.change >= 0
                        ? "text-accent-600 dark:text-accent-400"
                        : "text-red-600 dark:text-red-400"}
                    >
                      {asset.change >= 0 ? "+" : ""}{asset.change.toFixed(2)}%
                    </span>
                  </TableBodyCell>
                  <TableBodyCell class="text-center">
                    <Button
                      size="xs"
                      color="light"
                      onclick={() => viewAssetTransactions(asset.id)}
                    >
                      View Transactions
                    </Button>
                  </TableBodyCell>
                </TableBodyRow>
              {/each}
            </TableBody>
          </Table>
        </div>
      </Card>
    {:else}
      <Card class="!max-w-none w-full text-center py-12">
        <PieChart
          class="w-16 h-16 mx-auto mb-4 text-neutral-300 dark:text-neutral-600"
        />
        <h3
          class="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2"
        >
          No assets yet
        </h3>
        <p class="text-neutral-600 dark:text-neutral-400 mb-4">
          Add your first asset to start tracking your portfolio
        </p>
        <Button
          class="btn-primary"
          size="sm"
          onclick={() => (openAssetModal = true)}
        >
          <Plus class="w-4 h-4 mr-2" />
          Add Asset
        </Button>
      </Card>
    {/if}
  {/if}
</div>

<AssetModal bind:open={openAssetModal} {portfolioId} on:created={loadAssets} />
