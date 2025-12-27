<script lang="ts">
    import { Modal, Label, Input, Button, Select } from "flowbite-svelte";
    import {
        createPosition,
        updatePosition,
        type PositionCreate,
        type PositionUpdate,
        type Asset,
    } from "$lib/api";
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
    let quantity = "";
    let buyPrice = "";
    let buyDate = "";
    let error: string | null = null;
    let loading = false;

    // 모달이 열릴 때 초기화
    $: if (open) {
        if (position) {
            // 수정 모드
            selectedAssetId = position.asset_id;
            quantity = position.quantity.toString();
            buyPrice = position.buy_price.toString();
            buyDate = position.buy_date || "";
        } else if (asset) {
            // 특정 Asset에 대한 Position 추가
            selectedAssetId = asset.id;
            quantity = "";
            buyPrice = "";
            buyDate = "";
        } else {
            // 새 Position 추가 (Asset 선택 필요)
            selectedAssetId = null;
            quantity = "";
            buyPrice = "";
            buyDate = "";
        }
        error = null;
    }

    function resetForm() {
        selectedAssetId = null;
        quantity = "";
        buyPrice = "";
        buyDate = "";
        error = null;
    }

    function validateForm(): boolean {
        if (!selectedAssetId) {
            error = "Please select an asset";
            return false;
        }

        const qty = parseFloat(quantity);
        if (isNaN(qty) || qty < 0) {
            error = "Quantity must be 0 or greater";
            return false;
        }

        const price = parseFloat(buyPrice);
        if (isNaN(price) || price <= 0) {
            error = "Buy price must be greater than 0";
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
            if (position) {
                // 수정 모드
                const updateData: PositionUpdate = {
                    quantity: parseFloat(quantity),
                    buy_price: parseFloat(buyPrice),
                    buy_date: buyDate || undefined,
                };
                await updatePosition(position.id, updateData);
            } else {
                // 생성 모드
                const newPosition: PositionCreate = {
                    asset_id: selectedAssetId!,
                    quantity: parseFloat(quantity),
                    buy_price: parseFloat(buyPrice),
                    buy_date: buyDate || undefined,
                };
                await createPosition(newPosition);
            }

            dispatch("created");
            open = false;
            resetForm();
        } catch (err: any) {
            console.error("Failed to save position:", err);
            error = err.message || "Failed to save position";
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
    title={position ? "Edit Position" : "Add Position"}
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
            <span>Quantity</span>
            <Input
                type="number"
                step="any"
                min="0"
                bind:value={quantity}
                placeholder="0.0"
                required
            />
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Amount of asset you own (must be 0 or greater)
            </p>
        </Label>

        <Label>
            <span>Buy Price</span>
            <Input
                type="number"
                step="any"
                min="0.01"
                bind:value={buyPrice}
                placeholder="0.00"
                required
            />
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Price per unit when you bought (must be greater than 0)
            </p>
        </Label>

        <Label>
            <span>Buy Date (Optional)</span>
            <Input type="date" bind:value={buyDate} />
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Date when you purchased this asset
            </p>
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
                {loading ? "Saving..." : position ? "Update" : "Create"}
            </Button>
        </div>
    </form>
</Modal>
