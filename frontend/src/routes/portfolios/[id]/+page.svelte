<script lang="ts">
  import { page } from "$app/state";
  import { portfolioStore } from "$lib/stores/portfolio.svelte";
  import { onMount } from "svelte";
  import { fetchPortfolioPositions } from "$lib/apis/portfolio";
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
  import { Plus, ArrowLeft, PieChart, Info } from "lucide-svelte";
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
      const positions = await fetchPortfolioPositions(portfolioId);
      // Map API response (snake_case) to UI format (camelCase)
      assets = positions.map((p: any) => ({
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
  {:else if assets.length > 0}
    <Card>
      <div class="overflow-x-auto">
        <Table hoverable={true}>
          <TableHead>
            <TableHeadCell>Asset</TableHeadCell>
            <TableHeadCell>Quantity</TableHeadCell>
            <TableHeadCell>Avg Price</TableHeadCell>
            <TableHeadCell>Current Price</TableHeadCell>
            <TableHeadCell>Total Value</TableHeadCell>
            <TableHeadCell>Change</TableHeadCell>
            <TableHeadCell>Actions</TableHeadCell>
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
                <TableBodyCell>{asset.quantity}</TableBodyCell>
                <TableBodyCell>${asset.avgPrice.toLocaleString()}</TableBodyCell
                >
                <TableBodyCell
                  >${asset.currentPrice.toLocaleString()}</TableBodyCell
                >
                <TableBodyCell class="font-semibold">
                  ${asset.totalValue.toLocaleString()}
                </TableBodyCell>
                <TableBodyCell>
                  <span
                    class={asset.change >= 0
                      ? "text-accent-600 dark:text-accent-400"
                      : "text-red-600 dark:text-red-400"}
                  >
                    {asset.change >= 0 ? "+" : ""}{asset.change.toFixed(2)}%
                  </span>
                </TableBodyCell>
                <TableBodyCell>
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
    <Card class="text-center py-12">
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
</div>

<AssetModal bind:open={openAssetModal} {portfolioId} />
