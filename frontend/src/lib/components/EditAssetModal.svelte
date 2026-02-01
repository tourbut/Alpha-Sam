<script lang="ts">
    import { Button, Modal, Label, Input, Select } from "flowbite-svelte";
    import { RefreshOutline, EditOutline } from "flowbite-svelte-icons";
    import { update_asset } from "$lib/apis/assets";
    import type { Asset, AssetUpdate } from "$lib/types";

    let {
        open = $bindable(false),
        asset = $bindable(undefined) as unknown as Asset, // Force type (or handle null)
        onupdated = () => {},
    } = $props<{
        open: boolean;
        asset: Asset | undefined; // Allow undefined initially
        onupdated?: () => void;
    }>();

    let symbol = $state("");
    let name = $state("");
    let category = $state("");
    let loading = $state(false);
    let error: string | null = $state(null);

    const categories = [
        { value: "Stock", name: "Stock" },
        { value: "Crypto", name: "Crypto" },
        { value: "ETF", name: "ETF" },
        { value: "Cash", name: "Cash" },
        { value: "Other", name: "Other" },
    ];

    $effect(() => {
        if (open && asset) {
            symbol = asset.symbol;
            name = asset.name;
            category = asset.category || "Stock";
            error = null;
        }
    });

    async function handleSubmit() {
        if (!asset) return;

        loading = true;
        error = null;
        try {
            const updateData: AssetUpdate = {
                symbol,
                name,
                category,
            };
            await update_asset({
                id: asset.id,
                ...updateData,
            });
            onupdated?.();
            open = false;
        } catch (e: any) {
            console.error(e);
            error = e.message || "Failed to update asset";
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title="Edit Asset"
    autoclose={false}
    size="lg"
    class="w-full"
    outsideclose={true}
>
    <form
        onsubmit={(e) => {
            e.preventDefault();
            handleSubmit();
        }}
        class="flex flex-col space-y-4"
    >
        <div>
            <Label for="symbol" class="mb-2">Symbol / Ticker</Label>
            <Input
                type="text"
                id="symbol"
                placeholder="AAPL"
                required
                bind:value={symbol}
            />
        </div>

        <div>
            <Label for="name" class="mb-2">Asset Name</Label>
            <Input
                type="text"
                id="name"
                placeholder="Apple Inc."
                required
                bind:value={name}
            />
        </div>

        <div>
            <Label for="category" class="mb-2">Category</Label>
            <Select
                id="category"
                items={categories}
                bind:value={category}
                required
                placeholder="Select category"
            />
        </div>

        {#if error}
            <div class="text-red-600 text-sm">{error}</div>
        {/if}

        <div class="flex justify-end gap-2">
            <Button color="alternative" onclick={() => (open = false)}
                >Cancel</Button
            >
            <Button type="submit" disabled={loading} class="btn-primary">
                {#if loading}
                    <RefreshOutline class="w-4 h-4 mr-2 animate-spin" />
                    Updating...
                {:else}
                    <EditOutline class="w-4 h-4 mr-2" />
                    Update Asset
                {/if}
            </Button>
        </div>
    </form>
</Modal>
