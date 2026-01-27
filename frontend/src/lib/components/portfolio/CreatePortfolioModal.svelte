<script lang="ts">
    import { Modal, Label, Input, Button, Textarea } from "flowbite-svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";
    import {
        PlusOutline,
        RefreshOutline,
        PenOutline,
    } from "flowbite-svelte-icons";
    import type { Portfolio } from "$lib/types";

    let {
        open = $bindable(false),
        oncreated,
        initialData = null,
    }: {
        open?: boolean;
        oncreated?: () => void;
        initialData?: {
            id: string;
            name: string;
            description?: string;
            currency?: string;
        } | null;
    } = $props();

    let name = $state("");
    let description = $state("");
    let currency = $state("USD");
    let loading = $state(false);

    // Watch for open/initialData changes to reset/fill form
    $effect(() => {
        if (open) {
            if (initialData) {
                name = initialData.name;
                description = initialData.description || "";
                currency = initialData.currency || "USD";
            } else {
                name = "";
                description = "";
            }
        }
    });

    async function handleSubmit() {
        loading = true;
        try {
            if (initialData) {
                await portfolioStore.editPortfolio(initialData.id, {
                    name,
                    description,
                    currency,
                });
            } else {
                await portfolioStore.addPortfolio({
                    name,
                    description,
                    currency,
                });
            }
            open = false;
            if (oncreated) oncreated();
        } catch (e) {
            alert(
                initialData
                    ? "Failed to update portfolio"
                    : "Failed to create portfolio",
            );
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title={initialData ? "Edit Portfolio" : "Create New Portfolio"}
    size="lg"
    autoclose={false}
    class="w-auto mx-auto"
>
    <form
        class="flex flex-col space-y-6"
        onsubmit={(e) => {
            e.preventDefault();
            handleSubmit();
        }}
    >
        <Label class="space-y-2">
            <span>Portfolio Name</span>
            <Input
                type="text"
                name="name"
                bind:value={name}
                required
                placeholder="My Portfolio"
            />
        </Label>
        <Label class="space-y-2">
            <span>Description</span>
            <Textarea
                name="description"
                bind:value={description}
                placeholder="Investment goals..."
                class="w-full"
            />
        </Label>
        <Label class="space-y-2">
            <span>Currency</span>
            <Input type="text" name="currency" bind:value={currency} disabled />
        </Label>
        <Button type="submit" class="w-full btn-primary" disabled={loading}>
            {#if loading}
                <RefreshOutline class="w-4 h-4 mr-2 animate-spin" />
                {initialData ? "Updating..." : "Creating..."}
            {:else if initialData}
                <PenOutline class="w-4 h-4 mr-2" />
                Update Portfolio
            {:else}
                <PlusOutline class="w-4 h-4 mr-2" />
                Create Portfolio
            {/if}
        </Button>
    </form>
</Modal>
