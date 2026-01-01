<script lang="ts">
    import {
        Modal,
        Label,
        Input,
        Button,
        Select,
        Badge,
    } from "flowbite-svelte";
    import {
        createAsset,
        searchSymbol,
        type SymbolSearchResult,
    } from "$lib/api";
    import { createEventDispatcher } from "svelte";
    import { fade } from "svelte/transition";

    export let open = false;

    let symbol = "";
    let name = "";
    let category = "";

    // Search state
    let searchQuery = "";
    let searchResults: SymbolSearchResult[] = [];
    let isSearching = false;
    let showDropdown = false;
    let searchTimeout: NodeJS.Timeout;

    const dispatch = createEventDispatcher();

    const categories = [
        { value: "Crypto", name: "Crypto" },
        { value: "Stock", name: "Stock" },
        { value: "Cash", name: "Cash" },
    ];

    $: if (!open) {
        // Reset state when modal closes
        symbol = "";
        name = "";
        category = "";
        searchQuery = "";
        searchResults = [];
        showDropdown = false;
    }

    $: symbol = searchQuery ? searchQuery.toUpperCase() : "";

    function handleInput() {
        const query = searchQuery;

        clearTimeout(searchTimeout);

        if (!query || query.length < 2) {
            searchResults = [];
            showDropdown = false;
            return;
        }

        isSearching = true;
        showDropdown = true;
        searchTimeout = setTimeout(async () => {
            try {
                searchResults = await searchSymbol(query);
            } catch (e) {
                console.error("Search failed", e);
                searchResults = [];
            } finally {
                isSearching = false;
            }
        }, 500);
    }

    function selectSymbol(result: SymbolSearchResult) {
        symbol = result.symbol;
        searchQuery = result.symbol;
        if (result.longname) {
            name = result.longname;
        } else if (result.shortname) {
            name = result.shortname;
        }

        // Simple heuristic for category mapping
        if (
            result.quoteType === "CRYPTOCURRENCY" ||
            result.quoteType === "CRYPTO"
        ) {
            category = "Crypto";
        } else if (result.quoteType === "EQUITY") {
            category = "Stock";
        } else {
            // Default based on exchange or manual mapped
            category = "Stock";
        }

        showDropdown = false;
    }

    async function handleSubmit() {
        try {
            await createAsset({ symbol, name, category });
            dispatch("created");
            open = false;
            symbol = "";
            name = "";
            category = "";
        } catch (error) {
            console.error("Failed to create asset:", error);
            alert("Failed to create asset");
        }
    }
</script>

<Modal bind:open title="Add New Asset" autoclose={false}>
    <form
        class="flex flex-col space-y-6"
        on:submit|preventDefault={handleSubmit}
    >
        <div class="relative">
            <Label>
                <span>Symbol (Search)</span>
                <Input
                    type="text"
                    bind:value={searchQuery}
                    on:input={handleInput}
                    on:focus={() => (showDropdown = searchResults.length > 0)}
                    placeholder="Search e.g. AAPL, BTC"
                    required
                    autocomplete="off"
                />
            </Label>

            {#if showDropdown && (searchResults.length > 0 || isSearching)}
                <div
                    class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto"
                    transition:fade={{ duration: 100 }}
                >
                    {#if isSearching}
                        <div
                            class="p-3 text-center text-gray-500 dark:text-gray-400"
                        >
                            Searching...
                        </div>
                    {:else}
                        <ul class="py-1">
                            {#each searchResults as result}
                                <li>
                                    <button
                                        type="button"
                                        class="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-white flex justify-between items-center"
                                        on:click={() => selectSymbol(result)}
                                    >
                                        <span class="font-bold"
                                            >{result.symbol}</span
                                        >
                                        <span
                                            class="text-sm text-gray-500 dark:text-gray-400 truncate max-w-[60%]"
                                            >{result.longname ||
                                                result.shortname ||
                                                ""}</span
                                        >
                                    </button>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </div>
            {/if}
        </div>
        <Label>
            <span>Name</span>
            <Input
                type="text"
                bind:value={name}
                placeholder="Bitcoin"
                required
            />
        </Label>
        <Label>
            <span>Category</span>
            <Select
                class="mt-2"
                items={categories}
                bind:value={category}
                required
            />
        </Label>
        <Button type="submit">Create Asset</Button>
    </form>
</Modal>
