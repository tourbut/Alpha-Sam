<script lang="ts">
    import {
        Modal,
        Label,
        Input,
        Button,
        Select,
        Radio,
    } from "flowbite-svelte";
    import { create_transaction as createTransaction } from "$lib/apis/transactions";
    import type { Asset } from "$lib/types";
    import { createEventDispatcher } from "svelte";

    export let open = false;
    export let asset: Asset | null = null;
    export let assets: Asset[] = [];
    export let position: {
        id: number;
        asset_id: number;
        quantity: number;
        buy_price: number;
        buy_date?: string;
    } | null = null;

    const dispatch = createEventDispatcher();

    let selectedAssetId: number | null = null;
    let type: "BUY" | "SELL" = "BUY";
    let quantity = "";
    let price = "";
    let error: string | null = null;
    let loading = false;

    // 모달이 열릴 때 초기화
    $: if (open) {
        if (position) {
            // Pre-fill asset if adding a trade from an existing position row
            selectedAssetId = position.asset_id;
            type = "BUY";
            quantity = "";
            price = "";
        } else if (asset) {
            selectedAssetId = asset.id;
            type = "BUY";
            quantity = "";
            price = "";
        } else {
            selectedAssetId = null;
            type = "BUY";
            quantity = "";
            price = "";
        }
        error = null;
    }

    function resetForm() {
        selectedAssetId = null;
        type = "BUY";
        quantity = "";
        price = "";
        error = null;
    }

    function validateForm(): boolean {
        if (!selectedAssetId) {
            error = "Please select an asset";
            return false;
        }

        const qty = parseFloat(quantity);
        if (isNaN(qty) || qty <= 0) {
            error = "Quantity must be greater than 0";
            return false;
        }

        const p = parseFloat(price);
        if (isNaN(p) || p <= 0) {
            error = "Price must be greater than 0";
            return false;
        }

        return true;
    }

    async function handleSubmit() {
        if (!validateForm()) {
            return;
        }

        loading = true;
        error = null;

        try {
            await createTransaction({
                asset_id: Number(selectedAssetId),
                type,
                quantity: parseFloat(quantity),
                price: parseFloat(price),
            });

            dispatch("created");
            open = false;
            resetForm();
        } catch (err: any) {
            console.error("Failed to save transaction:", err);
            error = err.message || "Failed to save transaction";
        } finally {
            loading = false;
        }
    }

    function handleClose() {
        open = false;
        resetForm();
    }
</script>

<Modal
    bind:open
    title="Add Transaction"
    autoclose={false}
    onclose={handleClose}
>
    <form
        class="flex flex-col space-y-6"
        on:submit|preventDefault={handleSubmit}
    >
        {#if error}
            <div
                class="p-4 mb-4 text-sm text-red-800 bg-red-50 dark:bg-red-800/50 dark:text-red-400 rounded-lg"
            >
                {error}
            </div>
        {/if}

        {#if !asset}
            <Label>
                <span>Asset</span>
                <Select
                    class="mt-2"
                    items={assets.map((a) => ({
                        value: a.id.toString(),
                        name: `${a.symbol} - ${a.name}`,
                    }))}
                    bind:value={selectedAssetId}
                    required
                >
                    <option value="">Select an asset</option>
                </Select>
            </Label>
        {:else}
            <Label>
                <span>Asset</span>
                <Input
                    type="text"
                    value={`${asset.symbol} - ${asset.name}`}
                    disabled
                    readonly
                />
            </Label>
        {/if}

        <Label>
            <span>Type</span>
            <div class="flex gap-4 mt-2">
                <Radio name="type" bind:group={type} value="BUY">Buy</Radio>
                <Radio name="type" bind:group={type} value="SELL">Sell</Radio>
            </div>
        </Label>

        <Label>
            <span>Quantity</span>
            <Input
                type="number"
                step="any"
                min="0.00000001"
                bind:value={quantity}
                placeholder="0.0"
                required
            />
        </Label>

        <Label>
            <span>Price</span>
            <Input
                type="number"
                step="any"
                min="0.01"
                bind:value={price}
                placeholder="0.00"
                required
            />
        </Label>

        <div class="flex gap-2 justify-end">
            <Button
                color="alternative"
                type="button"
                onclick={handleClose}
                disabled={loading}
            >
                Cancel
            </Button>
            <Button type="submit" disabled={loading}>
                {loading ? "Saving..." : "Record Transaction"}
            </Button>
        </div>
    </form>
</Modal>
