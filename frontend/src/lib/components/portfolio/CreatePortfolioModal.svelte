<script lang="ts">
    import { Modal, Label, Input, Button, Textarea } from "flowbite-svelte";
    import { portfolioStore } from "$lib/stores/portfolio.svelte";

    let { open = $bindable(false) } = $props();

    let name = $state("");
    let description = $state("");
    let currency = $state("USD");
    let loading = $state(false);

    async function handleSubmit() {
        loading = true;
        try {
            await portfolioStore.addPortfolio({
                name,
                description,
                currency,
            });
            open = false;
            name = "";
            description = "";
        } catch (e) {
            alert("Failed to create portfolio");
        } finally {
            loading = false;
        }
    }
</script>

<Modal
    bind:open
    title="Create New Portfolio"
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
        <Button type="submit" class="w-full1" disabled={loading}>
            {loading ? "Creating..." : "Create Portfolio"}
        </Button>
    </form>
</Modal>
