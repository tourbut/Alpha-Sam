<script lang="ts">
    import { Modal, Label, Input, Button, Select } from "flowbite-svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";
    import { createTransaction } from "$lib/apis/portfolio";
    import { get_assets as getAssets } from "$lib/apis/assets";
    import { onMount } from "svelte";

    let { open = $bindable(false), assetId = 0, assetSymbol = "" } = $props();

    let type = $state("BUY");
    let quantity = $state(0);
    let price = $state(0);
    let date = $state("");
    let loading = $state(false);
    let assets = $state<any[]>([]);
    let selectedAssetId = $state(0);

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
        if (!portfolioStore.selectedPortfolioId) {
            alert("Please select a portfolio first.");
            return;
        }
        const finalAssetId = assetId || selectedAssetId;
        if (!finalAssetId) {
            alert("Please select an asset");
            return;
        }

        if (quantity <= 0 || price <= 0) {
            alert("Quantity and Price must be positive.");
            return;
        }

        loading = true;
        try {
            await createTransaction(portfolioStore.selectedPortfolioId, {
                asset_id: finalAssetId,
                type: type as "BUY" | "SELL",
                quantity,
                price,
                executed_at: new Date(date).toISOString(),
            });
            open = false;
            await portfolioStore.loadPositions(
                portfolioStore.selectedPortfolioId,
            );
            quantity = 0;
            price = 0;
            if (!assetId) selectedAssetId = 0;
        } catch (e: any) {
            alert(
                "Failed to create transaction: " +
                    (e.response?.data?.detail || e.message),
            );
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title={assetId ? `Add Transaction (${assetSymbol})` : "Add New Transaction"}
    size="xs"
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
        <Label class="space-y-2">
            <span>Date & Time</span>
            <Input type="datetime-local" bind:value={date} required />
        </Label>

        <Button type="submit" class="w-full" disabled={loading}>
            {loading ? "Processing..." : "Add Transaction"}
        </Button>
    </form>
</Modal>
