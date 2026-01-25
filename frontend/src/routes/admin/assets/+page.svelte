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
        Badge,
        Indicator,
    } from "flowbite-svelte";
    import {
        PlusOutline,
        TrashBinSolid,
        ExclamationCircleSolid,
    } from "flowbite-svelte-icons";
    import {
        get_admin_assets,
        create_admin_asset,
        delete_admin_asset,
        toggle_admin_asset,
    } from "$lib/apis/admin";
    import type { AdminAsset, AdminAssetCreate } from "$lib/types";

    let assets: AdminAsset[] = [];
    let loading = false;
    let error = "";

    // Modal State
    let formModal = false;
    let deleteModal = false;
    let selectedAsset: AdminAsset | null = null;
    let newAsset: AdminAssetCreate = {
        symbol: "",
        name: "",
        type: "STOCK",
        is_active: true,
    };

    const typeOptions = [
        { value: "STOCK", name: "Stock" },
        { value: "CRYPTO", name: "Crypto" },
        { value: "FOREX", name: "Forex" },
        { value: "INDEX", name: "Index" },
    ];

    async function loadAssets() {
        loading = true;
        try {
            assets = await get_admin_assets({});
        } catch (e) {
            error = "Failed to load assets: " + e;
        } finally {
            loading = false;
        }
    }

    async function handleAdd() {
        try {
            await create_admin_asset(newAsset);
            formModal = false;
            newAsset = { symbol: "", name: "", type: "STOCK", is_active: true }; // Reset
            await loadAssets();
        } catch (e: any) {
            alert("Error creating asset: " + (e.detail || e.message));
        }
    }

    async function handleDelete() {
        if (!selectedAsset) return;
        try {
            await delete_admin_asset({ id: selectedAsset.id });
            deleteModal = false;
            selectedAsset = null;
            await loadAssets();
        } catch (e: any) {
            alert("Error deleting asset: " + (e.detail || e.message));
        }
    }

    async function handleToggle(asset: AdminAsset) {
        try {
            await toggle_admin_asset({ id: asset.id });
            await loadAssets(); // Refresh to see update
        } catch (e: any) {
            alert("Error toggling asset: " + (e.detail || e.message));
        }
    }

    function openDeleteModal(asset: AdminAsset) {
        selectedAsset = asset;
        deleteModal = true;
    }

    onMount(() => {
        loadAssets();
    });
</script>

<div class="space-y-4">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold dark:text-white">
            System Assets Management
        </h1>
        <Button on:click={() => (formModal = true)}>
            <PlusOutline class="w-3.5 h-3.5 mr-2" />
            Add Asset
        </Button>
    </div>

    {#if loading}
        <p class="dark:text-gray-400">Loading...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <Table hoverable={true} shadow>
            <TableHead>
                <TableHeadCell>Symbol</TableHeadCell>
                <TableHeadCell>Name</TableHeadCell>
                <TableHeadCell>Type</TableHeadCell>
                <TableHeadCell>Status</TableHeadCell>
                <TableHeadCell>Last Update</TableHeadCell>
                <TableHeadCell>Actions</TableHeadCell>
            </TableHead>
            <TableBody>
                {#each assets as asset}
                    <TableBodyRow>
                        <TableBodyCell class="font-medium"
                            >{asset.symbol}</TableBodyCell
                        >
                        <TableBodyCell>{asset.name}</TableBodyCell>
                        <TableBodyCell>{asset.type}</TableBodyCell>
                        <TableBodyCell>
                            <Button
                                color={asset.is_active ? "green" : "red"}
                                size="xs"
                                outline
                                on:click={() => handleToggle(asset)}
                            >
                                {asset.is_active ? "Active" : "Inactive"}
                            </Button>
                        </TableBodyCell>
                        <TableBodyCell
                            >{new Date(
                                asset.updated_at,
                            ).toLocaleString()}</TableBodyCell
                        >
                        <TableBodyCell>
                            <Button
                                color="red"
                                size="xs"
                                on:click={() => openDeleteModal(asset)}
                            >
                                <TrashBinSolid class="w-3 h-3" />
                            </Button>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>
    {/if}
</div>

<!-- Add Modal -->
<Modal bind:open={formModal} title="Add New System Asset" autoclose={false}>
    <form class="space-y-4" on:submit|preventDefault={handleAdd}>
        <Label class="space-y-2">
            <span>Symbol (Ticker)</span>
            <Input
                type="text"
                placeholder="e.g. AAPL, BTC-USD"
                bind:value={newAsset.symbol}
                required
            />
            <p class="text-xs text-gray-500">
                For Crypto, use Yahoo Finance format (e.g. BTC-USD)
            </p>
        </Label>
        <Label class="space-y-2">
            <span>Name</span>
            <Input
                type="text"
                placeholder="Asset Name"
                bind:value={newAsset.name}
                required
            />
        </Label>
        <Label class="space-y-2">
            <span>Type</span>
            <Select items={typeOptions} bind:value={newAsset.type} required />
        </Label>
        <div class="flex justify-end gap-2">
            <Button color="alternative" on:click={() => (formModal = false)}
                >Cancel</Button
            >
            <Button type="submit">List Asset</Button>
        </div>
    </form>
</Modal>

<!-- Delete Confirm Modal -->
<Modal bind:open={deleteModal} size="xs" autoclose={false}>
    <div class="text-center">
        <ExclamationCircleSolid
            class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200"
        />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Are you sure you want to remove {selectedAsset?.symbol}?
        </h3>
        <Button color="red" class="mr-2" on:click={handleDelete}
            >Yes, I'm sure</Button
        >
        <Button color="alternative" on:click={() => (deleteModal = false)}
            >No, cancel</Button
        >
    </div>
</Modal>
