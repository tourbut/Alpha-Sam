<script lang="ts">
    import {
        Modal,
        Label,
        Input,
        Button,
        Select,
        Alert,
    } from "flowbite-svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";
    import { createTransaction } from "$lib/apis/portfolio";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import { onMount } from "svelte";

    let {
        open = $bindable(false),
        assetId = "",
        assetSymbol = "",
        portfolioId = "",
        oncreated = () => {},
    } = $props();

    let type = $state("BUY");
    let quantity = $state<number | undefined>(undefined);
    let price = $state<number | undefined>(undefined);
    let amount = $state<number | undefined>(undefined);
    let date = $state("");
    let loading = $state(false);
    let errorMessage = $state("");
    let assets = $state<any[]>([]);
    let selectedAssetId = $state("");
    let isCashAsset = $derived(
        assets.find(a => a.id === (assetId || selectedAssetId))?.category === "cash"
    );

    const types = [
        { value: "BUY", name: "Buy" },
        { value: "SELL", name: "Sell" },
    ];

    $effect(() => {
        if (open) {
            if (!date) {
                const now = new Date();
                const tzOffset = now.getTimezoneOffset() * 60000;
                date = new Date(now.getTime() - tzOffset)
                    .toISOString()
                    .slice(0, 16);
            }
            if (assetId) {
                selectedAssetId = assetId;
            } else if (assets.length === 0) {
                loadAssets();
            }
        }
    });

    async function loadAssets() {
        try {
            assets = await getAssets();
        } catch (e) {
            console.error("Failed to load assets", e);
        }
    }

    async function handleSubmit() {
        const targetPortfolioId =
            portfolioId || portfolioStore.selectedPortfolioId;

        if (!targetPortfolioId) {
            errorMessage = "Please select a portfolio first.";
            return;
        }
        const finalAssetId = assetId || selectedAssetId;
        if (!finalAssetId) {
            errorMessage = "Please select an asset";
            return;
        }

        if (isCashAsset) {
            if (amount === undefined || amount <= 0) {
                errorMessage = "Amount must be positive.";
                return;
            }
        } else {
            if (quantity === undefined || price === undefined || quantity <= 0 || price <= 0) {
                errorMessage = "Quantity and Price must be positive.";
                return;
            }
        }

        loading = true;
        errorMessage = "";
        try {
            await createTransaction({
                portfolio_id: targetPortfolioId,
                asset_id: finalAssetId,
                type: type as "BUY" | "SELL",
                quantity: isCashAsset ? undefined : quantity,
                price: isCashAsset ? undefined : price,
                amount: isCashAsset ? amount : undefined,
                executed_at: new Date(date).toISOString(),
            });
            open = false;
            // Removed specific portfolioStore call to genericize, or keep it if needed.
            // Better to rely on callback for page-specific refresh logic.
            if (oncreated) oncreated();

            await portfolioStore.loadPositions(
                portfolioStore.selectedPortfolioId || portfolioId,
            );
            quantity = undefined;
            price = undefined;
            amount = undefined;
            if (!assetId) selectedAssetId = "";
        } catch (e: any) {
            errorMessage =
                e.response?.data?.detail ||
                e.message ||
                "Failed to create transaction";
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title={assetId ? `Add Transaction (${assetSymbol})` : "Add New Transaction"}
    size="lg"
    autoclose={false}
    class="w-full"
>
    <form
        class="flex flex-col space-y-6"
        onsubmit={(e) => {
            e.preventDefault();
            handleSubmit();
        }}
    >
        {#if errorMessage}
            <Alert color="red" class="mb-4">{errorMessage}</Alert>
        {/if}

        {#if !assetId}
            <Label class="space-y-2">
                <span>Select Asset</span>
                <Select
                    items={assets.map((a) => ({
                        value: a.id,
                        name: `${a.symbol} - ${a.name}`,
                    }))}
                    bind:value={selectedAssetId}
                    required
                    placeholder="Select an asset"
                />
            </Label>
        {/if}

        <Label class="space-y-2">
            <span>Type</span>
            <Select items={types} bind:value={type} />
        </Label>

        {#if isCashAsset}
            <Label class="space-y-2">
                <span>Amount</span>
                <Input
                    type="number"
                    bind:value={amount}
                    min="0.00000001"
                    step="0.00000001"
                    required
                />
            </Label>
        {:else}
            <Label class="space-y-2">
                <span>Quantity</span>
                <Input
                    type="number"
                    bind:value={quantity}
                    min="0.00000001"
                    step="0.00000001"
                    required
                />
            </Label>
            <Label class="space-y-2">
                <span>Price per Unit</span>
                <Input
                    type="number"
                    bind:value={price}
                    min="0.00000001"
                    step="0.00000001"
                    required
                />
            </Label>
        {/if}

        <Label class="space-y-2">
            <span>Date & Time</span>
            <Input type="datetime-local" bind:value={date} required />
        </Label>

        <Button type="submit" class="w-full btn-primary" disabled={loading}>
            {loading ? "Processing..." : "Add Transaction"}
        </Button>
    </form>
</Modal>
