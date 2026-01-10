<script lang="ts">
    import { onMount } from "svelte";
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Button,
        Modal,
        Label,
        Input,
        Select,
        Helper,
    } from "flowbite-svelte";
    import {
        get_transactions as getTransactions,
        create_transaction as createTransaction,
    } from "$lib/apis/transactions";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import type { Transaction, Asset, CreateTransaction } from "$lib/types";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";

    let transactions: Transaction[] = [];
    let assets: Asset[] = [];
    let loading = true;
    let error: string | null = null;

    // Modal state
    let formModal = false;
    let submitting = false;

    // Form state
    let selectedAssetId: number | null = null;
    let type: "BUY" | "SELL" = "BUY";
    let quantity: number = 0;
    let price: number = 0;

    let assetOptions: { value: number; name: string }[] = [];

    async function loadData() {
        loading = true;
        try {
            const [txs, assetList] = await Promise.all([
                getTransactions(0, 50),
                getAssets(),
            ]);
            transactions = txs;
            assets = assetList;
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
        if (!$auth.isAuthenticated) {
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
            await createTransaction({
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
            error = "Failed to create transaction."; // Display error in UI if possible but alert is fine for now
        } finally {
            submitting = false;
        }
    }

    function formatDate(isoString: string) {
        return new Date(isoString).toLocaleString();
    }

    function getAssetSymbol(id: number) {
        const asset = assets.find((a) => a.id === id);
        return asset ? asset.symbol : `ID: ${id}`;
    }
</script>

<div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Transactions
        </h1>
        <Button on:click={() => (formModal = true)}>Add Transaction</Button>
    </div>

    {#if loading}
        <div class="text-center py-8 text-gray-500">Loading...</div>
    {:else if error}
        <div class="text-center py-8 text-red-500">{error}</div>
    {:else}
        <Table hoverable={true}>
            <TableHead>
                <TableHeadCell>Date</TableHeadCell>
                <TableHeadCell>Type</TableHeadCell>
                <TableHeadCell>Asset</TableHeadCell>
                <TableHeadCell>Quantity</TableHeadCell>
                <TableHeadCell>Price</TableHeadCell>
                <TableHeadCell>Total</TableHeadCell>
            </TableHead>
            <TableBody>
                {#each transactions as tx}
                    <TableBodyRow>
                        <TableBodyCell>{formatDate(tx.timestamp)}</TableBodyCell
                        >
                        <TableBodyCell>
                            <span
                                class={tx.type === "BUY"
                                    ? "text-green-600 font-bold"
                                    : "text-red-600 font-bold"}
                            >
                                {tx.type}
                            </span>
                        </TableBodyCell>
                        <TableBodyCell
                            >{getAssetSymbol(tx.asset_id)}</TableBodyCell
                        >
                        <TableBodyCell>{tx.quantity}</TableBodyCell>
                        <TableBodyCell
                            >${tx.price.toLocaleString()}</TableBodyCell
                        >
                        <TableBodyCell
                            >${tx.total_amount
                                ? tx.total_amount.toLocaleString()
                                : "-"}</TableBodyCell
                        >
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>

        {#if transactions.length === 0}
            <div class="text-center py-8 text-gray-500">
                No transactions found.
            </div>
        {/if}
    {/if}

    <Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
        <form
            class="flex flex-col space-y-6"
            on:submit|preventDefault={handleSubmit}
        >
            <h3 class="text-xl font-medium text-gray-900 dark:text-white">
                Add Transaction
            </h3>

            <Label>
                <span>Select Asset</span>
                <Select
                    items={assetOptions}
                    bind:value={selectedAssetId}
                    required
                    class="mt-2"
                />
            </Label>

            <Label>
                <span>Type</span>
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
                <span>Quantity</span>
                <Input
                    type="number"
                    step="0.00000001"
                    bind:value={quantity}
                    required
                    placeholder="0.0"
                    class="mt-2"
                />
            </Label>

            <Label>
                <span>Price per Unit ($)</span>
                <Input
                    type="number"
                    step="0.01"
                    bind:value={price}
                    required
                    placeholder="0.00"
                    class="mt-2"
                />
            </Label>

            <Button type="submit" class="w-full" disabled={submitting}>
                {submitting ? "Submitting..." : "Confirm Transaction"}
            </Button>
        </form>
    </Modal>
</div>
