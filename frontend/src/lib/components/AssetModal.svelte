<script lang="ts">
    import {
        Button,
        Modal,
        Label,
        Input,
        Select,
        Helper,
    } from "flowbite-svelte";
    import { create_asset as createAsset } from "$lib/apis/assets";
    import { createEventDispatcher } from "svelte";

    export let open = false;

    const dispatch = createEventDispatcher();

    let symbol = "";
    let name = "";
    let category = "";
    let loading = false;
    let error: string | null = null;

    const categories = [
        { value: "Stock", name: "Stock" },
        { value: "Crypto", name: "Crypto" },
        { value: "ETF", name: "ETF" },
        { value: "Cash", name: "Cash" },
        { value: "Other", name: "Other" },
    ];

    async function handleSubmit() {
        loading = true;
        error = null;
        try {
            await createAsset({
                symbol,
                name,
                category,
            });
            dispatch("created");
            open = false;
            resetForm();
        } catch (e: any) {
            console.error(e);
            error = e.response?.data?.detail || "Failed to create asset";
        } finally {
            loading = false;
        }
    }

    function resetForm() {
        symbol = "";
        name = "";
        category = "";
        error = null;
    }
</script>

<Modal bind:open title="Add New Asset" autoclose={false}>
    <form
        on:submit|preventDefault={handleSubmit}
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
            <Helper class="text-sm mt-2"
                >Unique identifier for the asset.</Helper
            >
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
            <Button color="alternative" on:click={() => (open = false)}
                >Cancel</Button
            >
            <Button type="submit" disabled={loading}
                >{loading ? "Creating..." : "Create Asset"}</Button
            >
        </div>
    </form>
</Modal>
