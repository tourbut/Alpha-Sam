<script lang="ts">
  import { page } from "$app/state";
  import { Button, Card, Spinner, Alert } from "flowbite-svelte";
  import { Plus, ArrowLeft, DollarSign, Edit, Trash2 } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import DataTable, {
    type ColumnDef,
  } from "$lib/components/common/DataTable.svelte";
  import { onMount } from "svelte";
  import {
    fetchPortfolioAsset,
    fetchPortfolioAssetTransactions,
  } from "$lib/apis/portfolio";
  import { delete_transaction } from "$lib/apis/transactions";
  import type { AssetSummary, AssetTransaction, Asset } from "$lib/types";
  import TransactionFormModal from "$lib/components/transaction/TransactionFormModal.svelte";
  import EditAssetModal from "$lib/components/EditAssetModal.svelte";
  import EditTransactionModal from "$lib/components/transaction/EditTransactionModal.svelte";

  let portfolioId = $derived(page.params.id);
  let assetId = $derived(page.params.assetId);

  let asset: AssetSummary | null = $state(null);
  let transactions: AssetTransaction[] = $state([]);
  let loading = $state(true);
  let error: string | null = $state(null);

  // Modal State
  let showModal = $state(false);
  let showEditAssetModal = $state(false);
  let showEditTransactionModal = $state(false);
  let selectedTransaction: AssetTransaction | null = $state(null);

  onMount(async () => {
    await loadData();
  });

  async function loadData() {
    // ID가 없으면 로딩하지 않음
    if (!portfolioId || !assetId) {
      error = "Portfolio ID 또는 Asset ID가 없습니다.";
      loading = false;
      return;
    }

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

  function openAddTransaction() {
    showModal = true;
  }

  async function handleDeleteTransaction(id: string) {
    if (
      !confirm(
        "정말로 이 트랜잭션을 삭제하시겠습니까? 잔고와 수익률이 변경됩니다.",
      )
    )
      return;
    try {
      await delete_transaction({ id });
      await loadData();
    } catch (e: any) {
      alert(e.message || "Failed to delete transaction");
    }
  }

  // 거래 내역 셀 렌더링을 정의
  // 현금 자산일 경우와 아닐 경우 컬럼이 다르므로 이를 여기서 계산합니다.
  let columns = $derived.by(() => {
    if (!asset) return [];

    if (asset.category === "cash") {
      return [
        { key: "date", label: "Date" },
        { key: "type", label: "Type" },
        { key: "quantity", label: "Amount", align: "right" },
        { key: "fee", label: "Fee", align: "right" },
        { key: "actions", label: "Action", align: "center", sortable: false },
      ] as ColumnDef<AssetTransaction>[];
    } else {
      return [
        { key: "date", label: "Date" },
        { key: "type", label: "Type" },
        { key: "quantity", label: "Quantity", align: "right" },
        { key: "price", label: "Price", align: "right" },
        { key: "total", label: "Total", align: "right" },
        { key: "fee", label: "Fee", align: "right" },
        { key: "actions", label: "Action", align: "center", sortable: false },
      ] as ColumnDef<AssetTransaction>[];
    }
  });
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
      <Spinner size="12" color="purple" />
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
      <div class="flex gap-2">
        <Button
          color="alternative"
          size="sm"
          onclick={() => (showEditAssetModal = true)}
        >
          <Edit class="w-4 h-4 mr-2" />
          Edit Asset
        </Button>
        <Button class="btn-primary" size="sm" onclick={openAddTransaction}>
          <Plus class="w-4 h-4 mr-2" />
          Add Transaction
        </Button>
      </div>
    </div>

    <!-- Asset Summary -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Card size="xl" class="!max-w-none w-full">
        <div class="!max-w-none w-full card-title">Quantity</div>
        <div class="card-value">{asset.quantity}</div>
      </Card>
      <Card size="xl" class="!max-w-none w-full">
        <div class="!max-w-none w-full card-title">Avg Price</div>
        <div class="card-value">${asset.avg_price.toLocaleString()}</div>
      </Card>
      <Card size="xl" class="!max-w-none w-full">
        <div class="!max-w-none w-full card-title">Current Price</div>
        <div class="card-value">
          ${asset.current_price
            ? asset.current_price.toLocaleString()
            : asset.avg_price.toLocaleString()}
        </div>
      </Card>
      <Card size="xl" class="!max-w-none w-full">
        <div class="!max-w-none w-full card-title">Total Value</div>
        <div class="card-value">
          ${asset.total_value.toLocaleString()}
        </div>
      </Card>
    </div>

    <!-- Transactions Table -->
    {#if transactions.length > 0}
      <Card size="xl" class="!max-w-none w-full">
        <h2
          class="!max-w-none w-full text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-4"
        >
          Transactions
        </h2>
        <DataTable data={transactions} {columns}>
          {#snippet customCell(tx, colKey)}
            {#if colKey === "date"}
              {new Date(tx.date).toLocaleDateString()}
            {:else if colKey === "type"}
              <span
                class={tx.type.toLowerCase() === "buy"
                  ? "badge badge-success"
                  : "badge badge-error"}
              >
                {tx.type.toUpperCase()}
              </span>
            {:else if colKey === "quantity"}
              {#if asset?.category === "cash"}
                {tx.quantity.toLocaleString()}
              {:else}
                {tx.quantity}
              {/if}
            {:else if colKey === "price"}
              ${tx.price.toLocaleString()}
            {:else if colKey === "total"}
              <span class="font-semibold">${tx.total.toLocaleString()}</span>
            {:else if colKey === "fee"}
              {tx.fee ? `$${tx.fee}` : "-"}
            {:else if colKey === "actions"}
              <div class="flex items-center justify-center gap-2">
                <button
                  class="text-neutral-500 hover:text-primary-600"
                  onclick={() => {
                    selectedTransaction = tx;
                    showEditTransactionModal = true;
                  }}
                >
                  <Edit class="w-4 h-4" />
                </button>
                <button
                  class="text-neutral-500 hover:text-red-600"
                  onclick={() => handleDeleteTransaction(tx.id)}
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            {/if}
          {/snippet}
        </DataTable>
      </Card>
    {:else}
      <Card class="!max-w-none w-full text-center py-12">
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
        <Button class="btn-primary" size="sm" onclick={openAddTransaction}>
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

<!-- Add Transaction Modal -->
<TransactionFormModal
  bind:open={showModal}
  {assetId}
  assetSymbol={asset?.symbol || ""}
  {portfolioId}
  oncreated={loadData}
/>

{#if asset}
  <EditAssetModal
    bind:open={showEditAssetModal}
    asset={{
      id: asset.asset_id,
      symbol: asset.symbol,
      name: asset.name,
      category: (asset as any).category || "Stock",
    }}
    onupdated={loadData}
  />
{/if}

<EditTransactionModal
  bind:open={showEditTransactionModal}
  transaction={selectedTransaction}
  assetSymbol={asset?.symbol || ""}
  isCashAsset={asset?.category === "cash"}
  onupdated={loadData}
/>
