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
  } from "flowbite-svelte";
  import { Plus, ArrowLeft, DollarSign } from "lucide-svelte";
  import { goto } from "$app/navigation";

  let portfolioId = $derived(page.params.id);
  let assetId = $derived(page.params.assetId);

  // Mock data - replace with actual API call
  let asset = $state({
    symbol: "BTC",
    name: "Bitcoin",
    quantity: 0.5,
    avgPrice: 45000,
    currentPrice: 48000,
  });

  let transactions = $state([
    {
      id: 1,
      type: "buy",
      date: "2024-01-15",
      quantity: 0.3,
      price: 43000,
      total: 12900,
      fee: 10,
    },
    {
      id: 2,
      type: "buy",
      date: "2024-02-10",
      quantity: 0.2,
      price: 48000,
      total: 9600,
      fee: 8,
    },
  ]);

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
      <div class="card-value">${asset.avgPrice.toLocaleString()}</div>
    </Card>
    <Card>
      <div class="card-title">Current Price</div>
      <div class="card-value">${asset.currentPrice.toLocaleString()}</div>
    </Card>
    <Card>
      <div class="card-title">Total Value</div>
      <div class="card-value">
        ${(asset.quantity * asset.currentPrice).toLocaleString()}
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
                    class={tx.type === "buy"
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
                <TableBodyCell>${tx.fee}</TableBodyCell>
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
</div>
