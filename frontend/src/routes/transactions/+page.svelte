<script lang="ts">
    import { onMount } from "svelte";
    import { Button, Modal, Label, Input, Select } from "flowbite-svelte";
    import { get_transactions as getTransactions } from "$lib/apis/transactions";
    import { createTransaction, fetchPortfolios } from "$lib/apis/portfolio";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import type { Transaction, Asset, CreateTransaction } from "$lib/types";
    import { auth } from "$lib/stores/auth.svelte";
    import { goto } from "$app/navigation";
    import { goto } from "$app/navigation";
    import { PlusOutline, RefreshOutline } from "flowbite-svelte-icons";
    import { APP_NAME } from "$lib/constants";

    let transactions: Transaction[] = [];
    let assets: Asset[] = [];
    let loading = true;
    let error: string | null = null;

    // Modal state
    let formModal = false;
    let submitting = false;

    // Form state
    let selectedAssetId: string | null = null;
    let portfolioId: string | null = null;
    let type: "BUY" | "SELL" = "BUY";
    let quantity: number = 0;
    let price: number = 0;

    let assetOptions: { value: string; name: string }[] = [];

    async function loadData() {
        loading = true;
        try {
            const [txs, assetList, portfolios] = await Promise.all([
                getTransactions({ skip: 0, limit: 50 }),
                getAssets(),
                fetchPortfolios(),
            ]);
            transactions = txs;
            assets = assetList;
            if (portfolios.length > 0) {
                portfolioId = portfolios[0].id;
            }
            assetOptions = assets.map((a) => ({
                value: a.id,
                name: `${a.symbol} (${a.name})`,
            }));
        } catch (e) {
            console.error("Error loading data", e);
            error = "Failed to load transactions.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        if (!auth.isAuthenticated) {
            goto("/login");
            return;
        }
        loadData();
    });

    async function handleSubmit() {
        if (!selectedAssetId || quantity <= 0 || price <= 0) {
            alert("Please fill all fields correctly.");
            return;
        }

        submitting = true;
        try {
            if (!portfolioId) {
                alert("No portfolio found.");
                return;
            }
            // createTransaction은 단일 TransactionCreate 객체를 받음
            await createTransaction({
                portfolio_id: portfolioId,
                asset_id: selectedAssetId,
                type: type,
                quantity: Number(quantity),
                price: Number(price),
            });
            formModal = false;
            // Reset form
            quantity = 0;
            price = 0;
            // Reload list
            await loadData();
        } catch (e) {
            console.error(e);
            alert("Failed to create transaction.");
            error = "Failed to create transaction.";
        } finally {
            submitting = false;
        }
    }

    function formatDate(isoString: string) {
        if (!isoString) return "-";
        const date = new Date(isoString);
        if (isNaN(date.getTime())) return isoString || "-";
        return date.toLocaleString();
    }

    function getAssetSymbol(id: string) {
        const asset = assets.find((a) => a.id === id);
        return asset ? asset.symbol : `ID: ${id}`;
    }

    function formatCurrency(value: number | undefined): string {
        if (value === undefined || value === null) return "-";
        return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
</script>

<svelte:head>
    <title>Transactions - {APP_NAME}</title>
</svelte:head>

<div class="max-w-[1400px] mx-auto p-5">
    <!-- 헤더 영역 -->
    <div
        class="flex justify-between items-center mb-8 pb-5 border-b border-neutral-200 dark:border-neutral-700"
    >
        <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">
            Transactions
        </h1>
        <Button
            onclick={() => (formModal = true)}
            class="btn-primary"
            size="sm"
        >
            <PlusOutline class="w-4 h-4 mr-2" />
            Add Transaction
        </Button>
    </div>

    {#if loading}
        <div class="text-center py-8 text-neutral-500">Loading...</div>
    {:else if error}
        <div class="text-center py-8 text-red-500">{error}</div>
    {:else}
        <!-- 테이블 컨테이너 - theme-preview 스타일 적용 -->
        <div class="table-container overflow-x-auto">
            <table class="w-full">
                <thead>
                    <tr>
                        <th class="table-header">Date</th>
                        <th class="table-header">Type</th>
                        <th class="table-header">Asset</th>
                        <th class="table-header text-right">Quantity</th>
                        <th class="table-header text-right">Price</th>
                        <th class="table-header text-right">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {#each transactions as tx}
                        <tr class="table-row-hover">
                            <td class="table-cell"
                                >{formatDate(tx.timestamp)}</td
                            >
                            <td class="table-cell">
                                <span
                                    class="badge {tx.type === 'BUY'
                                        ? 'badge-success'
                                        : 'badge-error'}"
                                >
                                    {tx.type}
                                </span>
                            </td>
                            <td class="table-cell font-medium">
                                {getAssetSymbol(tx.asset_id)}
                            </td>
                            <td class="table-cell text-right">
                                {tx.quantity.toLocaleString(undefined, {
                                    maximumFractionDigits: 8,
                                })}
                            </td>
                            <td class="table-cell text-right">
                                {formatCurrency(tx.price)}
                            </td>
                            <td class="table-cell text-right font-semibold">
                                {tx.total_amount
                                    ? formatCurrency(tx.total_amount)
                                    : "-"}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>

        {#if transactions.length === 0}
            <div
                class="text-center py-8 text-neutral-500 dark:text-neutral-400"
            >
                No transactions found. Click "Add Transaction" to create one.
            </div>
        {/if}
    {/if}

    <!-- Add Transaction Modal -->
    <Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
        <form
            class="flex flex-col space-y-6"
            on:submit|preventDefault={handleSubmit}
        >
            <h3 class="text-xl font-semibold text-neutral-900 dark:text-white">
                Add Transaction
            </h3>

            <Label>
                <span
                    class="text-sm font-medium text-neutral-700 dark:text-neutral-300"
                    >Select Asset</span
                >
                <Select
                    items={assetOptions}
                    bind:value={selectedAssetId}
                    required
                    class="mt-2"
                />
            </Label>

            <Label>
                <span
                    class="text-sm font-medium text-neutral-700 dark:text-neutral-300"
                    >Type</span
                >
                <Select
                    items={[
                        { value: "BUY", name: "Buy" },
                        { value: "SELL", name: "Sell" },
                    ]}
                    bind:value={type}
                    required
                    class="mt-2"
                />
            </Label>

            <Label>
                <span
                    class="text-sm font-medium text-neutral-700 dark:text-neutral-300"
                    >Quantity</span
                >
                <Input
                    type="number"
                    step="0.00000001"
                    bind:value={quantity}
                    required
                    placeholder="0.0"
                    class="mt-2 input"
                />
            </Label>

            <Label>
                <span
                    class="text-sm font-medium text-neutral-700 dark:text-neutral-300"
                    >Price per Unit ($)</span
                >
                <Input
                    type="number"
                    step="0.01"
                    bind:value={price}
                    required
                    placeholder="0.00"
                    class="mt-2 input"
                />
            </Label>

            <Button
                type="submit"
                class="btn-primary w-full"
                disabled={submitting}
            >
                {#if submitting}
                    <RefreshOutline class="w-4 h-4 mr-2 animate-spin" />
                    Submitting...
                {:else}
                    <PlusOutline class="w-4 h-4 mr-2" />
                    Confirm Transaction
                {/if}
            </Button>
        </form>
    </Modal>
</div>
