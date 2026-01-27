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
        Card,
        Spinner,
        Alert,
    } from "flowbite-svelte";
    import {
        Plus,
        Trash2,
        PieChart,
        Activity,
        AlertCircle,
    } from "lucide-svelte";
    import {
        get_admin_assets,
        create_admin_asset,
        delete_admin_asset,
        toggle_admin_asset,
    } from "$lib/apis/admin";
    import type { AdminAsset, AdminAssetCreate } from "$lib/types";

    let assets: AdminAsset[] = $state([]);
    let loading = $state(false);
    let error = $state("");

    // Modal State
    let formModal = $state(false);
    let deleteModal = $state(false);
    let selectedAsset: AdminAsset | null = $state(null);
    let newAsset: AdminAssetCreate = $state({
        symbol: "",
        name: "",
        type: "STOCK",
        is_active: true,
    });

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

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <div>
            <h1
                class="text-3xl font-bold text-neutral-900 dark:text-neutral-100"
            >
                System Assets Management
            </h1>
            <p class="text-neutral-600 dark:text-neutral-400 mt-1">
                Manage global assets for price collection and system
                availability
            </p>
        </div>
        <Button
            class="btn-primary"
            size="sm"
            onclick={() => (formModal = true)}
        >
            <Plus class="w-4 h-4 mr-2" />
            Add Asset
        </Button>
    </div>

    {#if loading}
        <div class="flex justify-center py-12">
            <Spinner size="12" color="purple" />
        </div>
    {:else if error}
        <div class="mb-4">
            <Alert color="red">
                <span class="font-medium">Error!</span>
                {error}
            </Alert>
        </div>
    {:else if assets.length > 0}
        <Card>
            <div class="overflow-x-auto">
                <Table hoverable={true}>
                    <TableHead>
                        <TableHeadCell>Asset</TableHeadCell>
                        <TableHeadCell>Type</TableHeadCell>
                        <TableHeadCell>Status</TableHeadCell>
                        <TableHeadCell class="text-right"
                            >Last Update</TableHeadCell
                        >
                        <TableHeadCell class="text-center"
                            >Actions</TableHeadCell
                        >
                    </TableHead>
                    <TableBody>
                        {#each assets as asset}
                            <TableBodyRow>
                                <TableBodyCell>
                                    <div class="flex items-center gap-2">
                                        <div
                                            class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center"
                                        >
                                            <PieChart
                                                class="w-4 h-4 text-primary-600 dark:text-primary-400"
                                            />
                                        </div>
                                        <div>
                                            <div
                                                class="font-semibold text-neutral-900 dark:text-neutral-100"
                                            >
                                                {asset.symbol}
                                            </div>
                                            <div
                                                class="text-xs text-neutral-500 dark:text-neutral-400"
                                            >
                                                {asset.name}
                                            </div>
                                        </div>
                                    </div>
                                </TableBodyCell>
                                <TableBodyCell>
                                    <span
                                        class="text-sm font-medium text-gray-900 dark:text-gray-300"
                                    >
                                        {asset.type}
                                    </span>
                                </TableBodyCell>
                                <TableBodyCell>
                                    <Button
                                        color={asset.is_active
                                            ? "green"
                                            : "red"}
                                        size="xs"
                                        outline
                                        class="!p-1.5"
                                        onclick={() => handleToggle(asset)}
                                    >
                                        <Activity class="w-3 h-3 mr-1" />
                                        {asset.is_active
                                            ? "Active"
                                            : "Inactive"}
                                    </Button>
                                </TableBodyCell>
                                <TableBodyCell class="text-right text-gray-500">
                                    {new Date(
                                        asset.updated_at,
                                    ).toLocaleString()}
                                </TableBodyCell>
                                <TableBodyCell class="text-center">
                                    <Button
                                        color="red"
                                        size="xs"
                                        outline
                                        onclick={() => openDeleteModal(asset)}
                                    >
                                        <Trash2 class="w-3 h-3" />
                                    </Button>
                                </TableBodyCell>
                            </TableBodyRow>
                        {/each}
                    </TableBody>
                </Table>
            </div>
        </Card>
    {:else}
        <Card class="text-center py-12">
            <PieChart
                class="w-16 h-16 mx-auto mb-4 text-neutral-300 dark:text-neutral-600"
            />
            <h3
                class="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-2"
            >
                No assets configured
            </h3>
            <p class="text-neutral-600 dark:text-neutral-400 mb-4">
                Add assets to start monitoring prices and availability
            </p>
            <Button
                class="btn-primary"
                size="sm"
                onclick={() => (formModal = true)}
            >
                <Plus class="w-4 h-4 mr-2" />
                Add Asset
            </Button>
        </Card>
    {/if}
</div>

<!-- Add Modal -->
<Modal
    bind:open={formModal}
    title="Add New System Asset"
    autoclose={false}
    size="lg"
>
    <form
        class="space-y-4"
        onsubmit={(e) => {
            e.preventDefault();
            handleAdd();
        }}
    >
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
            <Button color="alternative" onclick={() => (formModal = false)}
                >Cancel</Button
            >
            <Button type="submit" class="btn-primary">List Asset</Button>
        </div>
    </form>
</Modal>

<!-- Delete Confirm Modal -->
<Modal bind:open={deleteModal} size="xs" autoclose={false}>
    <div class="text-center">
        <AlertCircle
            class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200"
        />
        <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Are you sure you want to remove {selectedAsset?.symbol}?
        </h3>
        <Button color="red" class="mr-2" onclick={handleDelete}
            >Yes, I'm sure</Button
        >
        <Button color="alternative" onclick={() => (deleteModal = false)}
            >No, cancel</Button
        >
    </div>
</Modal>
