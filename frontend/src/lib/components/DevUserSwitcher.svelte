<script lang="ts">
    import { devUser, DEV_USERS } from "$lib/stores/devUser";
    import { slide } from "svelte/transition";

    // Only show in dev mode normally, but for now we show it always or check env
    // import { dev } from '$app/environment';

    let isOpen = false;

    function toggleDropdown() {
        isOpen = !isOpen;
    }

    function selectUser(id: number) {
        devUser.switchUser(id);
        isOpen = false;
        // Optional: Reload page to ensure all data is re-fetched with new user ID
        window.location.reload();
    }
</script>

<div class="fixed bottom-4 right-4 z-50 font-sans">
    <div class="relative">
        <button
            on:click={toggleDropdown}
            class="flex items-center space-x-2 bg-gray-800 text-white px-4 py-2 rounded-full shadow-lg hover:bg-gray-700 transition-colors border border-gray-600"
        >
            <span
                class="text-xs font-bold bg-blue-500 px-1.5 py-0.5 rounded text-white"
                >DEV</span
            >
            <span class="text-sm font-medium">{$devUser.name}</span>
            <svg
                class="w-4 h-4 ml-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                />
            </svg>
        </button>

        {#if isOpen}
            <div
                transition:slide={{ duration: 300, axis: "y" }}
                class="absolute bottom-full right-0 mb-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden"
            >
                <div class="bg-gray-50 px-3 py-2 border-b border-gray-100">
                    <p
                        class="text-xs font-semibold text-gray-500 uppercase tracking-wider"
                    >
                        Switch User
                    </p>
                </div>
                <ul class="py-1">
                    {#each DEV_USERS as user}
                        <li>
                            <button
                                on:click={() => selectUser(user.id)}
                                class="w-full text-left px-4 py-2 text-sm hover:bg-blue-50 flex items-center justify-between
                                {$devUser.id === user.id
                                    ? 'text-blue-600 font-semibold bg-blue-50'
                                    : 'text-gray-700'}"
                            >
                                <span>{user.name}</span>
                                {#if $devUser.id === user.id}
                                    <svg
                                        class="w-4 h-4 text-blue-500"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M5 13l4 4L19 7"
                                        />
                                    </svg>
                                {/if}
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</div>
