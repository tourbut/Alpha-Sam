<script lang="ts">
  import { page } from "$app/state";
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
  import { Plus, ArrowLeft, DollarSign } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import {
    fetchPortfolioAsset,
    fetchPortfolioAssetTransactions,
  } from "$lib/apis/portfolio";
  import type { AssetSummary, AssetTransaction } from "$lib/types";

  let portfolioId = $derived(page.params.id);
  let assetId = $derived(page.params.assetId);

  let asset: AssetSummary | null = $state(null);
  let transactions: AssetTransaction[] = $state([]);
  let loading = $state(true);
  let error = $state(null);

  onMount(async () => {
    await loadData();
  });

  async function loadData() {
    loading = true;
    error = null;
    try {
      const [assetRes, txRes] = await Promise.all([
        fetchPortfolioAsset(portfolioId, assetId),
        fetchPortfolioAssetTransactions(portfolioId, assetId),
      ]);
      asset = assetRes;
      transactions = txRes;
    } catch (e: any) {
      console.error("Failed to load data:", e);
      error = e.message || "Failed to load asset data";
    } finally {
      loading = false;
    }
  }

  function goBack() {
    goto(`/portfolios/${portfolioId}`);
  }

  function addTransaction() {
    // TODO: Implement add transaction modal
    alert("Add transaction feature coming soon!");
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
      Back to Assets
    </button>
  </div>

  {#if loading}
    <div class="flex justify-center py-12">
      <Spinner size="lg" color="purple" />
    </div>
  {:else if error}
    <Alert color="red" class="mb-4">
      <span class="font-medium">Error!</span>
      {error}
    </Alert>
  {:else if asset}
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
          {asset.symbol} - {asset.name}
        </h1>
        <p class="text-neutral-600 dark:text-neutral-400 mt-1">
          Transaction history and performance
        </p>
      </div>
      <Button
        class="bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l text-white"
        onclick={addTransaction}
      >
        <Plus class="w-4 h-4 mr-2" />
        Add Transaction
      </Button>
    </div>

    <!-- Asset Summary -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card>
        <div class="card-title">Quantity</div>
        <div class="card-value">{asset.quantity}</div>
      </Card>
      <Card>
        <div class="card-title">Avg Price</div>
        <div class="card-value">${asset.avg_price.toLocaleString()}</div>
      </Card>
      <Card>
        <div class="card-title">Current Price</div>
        <div class="card-value">
          ${asset.current_price
            ? asset.current_price.toLocaleString()
            : asset.avg_price.toLocaleString()}
        </div>
      </Card>
      <Card>
        <div class="card-title">Total Value</div>
        <div class="card-value">
          ${asset.total_value.toLocaleString()}
        </div>
      </Card>
    </div>

    <!-- Transactions Table -->
    {#if transactions.length > 0}
      <Card>
        <h2
          class="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-4"
        >
          Transactions
        </h2>
        <div class="overflow-x-auto">
          <Table hoverable={true}>
            <TableHead>
              <TableHeadCell>Date</TableHeadCell>
              <TableHeadCell>Type</TableHeadCell>
              <TableHeadCell>Quantity</TableHeadCell>
              <TableHeadCell>Price</TableHeadCell>
              <TableHeadCell>Total</TableHeadCell>
              <TableHeadCell>Fee</TableHeadCell>
            </TableHead>
            <TableBody>
              {#each transactions as tx}
                <TableBodyRow>
                  <TableBodyCell>
                    {new Date(tx.date).toLocaleDateString()}
                  </TableBodyCell>
                  <TableBodyCell>
                    <span
                      class={tx.type.toLowerCase() === "buy"
                        ? "badge badge-success"
                        : "badge badge-error"}
                    >
                      {tx.type.toUpperCase()}
                    </span>
                  </TableBodyCell>
                  <TableBodyCell>{tx.quantity}</TableBodyCell>
                  <TableBodyCell>${tx.price.toLocaleString()}</TableBodyCell>
                  <TableBodyCell class="font-semibold">
                    ${tx.total.toLocaleString()}
                  </TableBodyCell>
                  <TableBodyCell>{tx.fee ? `$${tx.fee}` : "-"}</TableBodyCell>
                </TableBodyRow>
              {/each}
            </TableBody>
          </Table>
        </div>
      </Card>
    {:else}
      <Card class="text-center py-12">
        <DollarSign
          class="w-16 h-16 mx-auto mb-4 text-neutral-300 dark:text-neutral-600"
        />
        <h3
          class="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2"
        >
          No transactions yet
        </h3>
        <p class="text-neutral-600 dark:text-neutral-400 mb-4">
          Add your first transaction to start tracking this asset
        </p>
        <Button
          class="bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l text-white"
          onclick={addTransaction}
        >
          <Plus class="w-4 h-4 mr-2" />
          Add Transaction
        </Button>
      </Card>
    {/if}
  {:else}
    <Alert color="yellow" class="mb-4">
      <span class="font-medium">Warning!</span> Asset not found.
    </Alert>
  {/if}
</div>
