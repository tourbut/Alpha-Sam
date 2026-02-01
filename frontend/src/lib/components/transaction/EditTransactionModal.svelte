<script lang="ts">
    import { Modal, Label, Input, Button, Select } from "flowbite-svelte";
    import { update_transaction } from "$lib/apis/transactions";
    import { RefreshOutline, EditOutline } from "flowbite-svelte-icons";
    import type { AssetTransaction, TransactionUpdate } from "$lib/types";

    let {
        open = $bindable(false),
        transaction = $bindable(null) as AssetTransaction | null,
        assetSymbol = "",
        onupdated = () => {},
    } = $props<{
        open: boolean;
        transaction: AssetTransaction | null;
        assetSymbol: string;
        onupdated?: () => void;
    }>();

    let type = $state("BUY");
    let quantity = $state(0);
    let price = $state(0);
    let date = $state("");
    let loading = $state(false);
    let error: string | null = $state(null);

    const types = [
        { value: "BUY", name: "Buy" },
        { value: "SELL", name: "Sell" },
    ];

    $effect(() => {
        if (open && transaction) {
            type = transaction.type.toUpperCase();
            quantity = transaction.quantity;
            price = transaction.price;

            // Convert ISO string to datetime-local format (YYYY-MM-DDTHH:MM)
            const d = new Date(transaction.date);
            const tzOffset = d.getTimezoneOffset() * 60000;
            date = new Date(d.getTime() - tzOffset).toISOString().slice(0, 16);

            error = null;
        }
    });

    async function handleSubmit() {
        if (!transaction) return;

        if (quantity <= 0 || price <= 0) {
            alert("Quantity and Price must be positive.");
            return;
        }

        loading = true;
        error = null;
        try {
            const updateData: TransactionUpdate = {
                type: type as "BUY" | "SELL",
                quantity,
                price,
                executed_at: new Date(date).toISOString(),
            };

            await update_transaction({
                id: transaction.id,
                ...updateData,
            });

            onupdated?.();
            open = false;
        } catch (e: any) {
            console.error(e);
            error = e.message || "Failed to update transaction";
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title="Edit Transaction ({assetSymbol})"
    size="lg"
    autoclose={false}
    class="w-full"
    outsideclose={true}
>
    <form
        onsubmit={(e) => {
            e.preventDefault();
            handleSubmit();
        }}
        class="flex flex-col space-y-6"
    >
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

        {#if error}
            <div class="text-red-600 text-sm">{error}</div>
        {/if}

        <div class="flex justify-end gap-2">
            <Button color="alternative" onclick={() => (open = false)}
                >Cancel</Button
            >
            <Button type="submit" class="btn-primary" disabled={loading}>
                {#if loading}
                    <RefreshOutline class="w-4 h-4 mr-2 animate-spin" />
                    Updating...
                {:else}
                    <EditOutline class="w-4 h-4 mr-2" />
                    Update Transaction
                {/if}
            </Button>
        </div>
    </form>
</Modal>
