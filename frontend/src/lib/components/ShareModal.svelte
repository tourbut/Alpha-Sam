<script lang="ts">
    import {
        Modal,
        Button,
        Toggle,
        Label,
        Input,
        Helper,
        Select,
        Badge,
    } from "flowbite-svelte";
    import {
        ShareNodesOutline,
        ClipboardCleanOutline,
        LinkOutline,
        GlobeOutline,
        LockOpenOutline,
        LockSolid,
    } from "flowbite-svelte-icons";
    import { PortfolioVisibility } from "$lib/types";
    import { updatePortfolioVisibility } from "$lib/apis/portfolio";
    import { onMount } from "svelte";

    let {
        open = $bindable(false),
        portfolioId = 0,
        currentVisibility = "PRIVATE",
        shareToken = null,
    } = $props();

    let visibility = $state(currentVisibility);
    let token = $state(shareToken);
    let isLoading = $state(false);
    let copied = $state(false);

    let shareUrl = $derived(
        token ? `${window.location.origin}/shared/${token}` : "",
    );

    const visibilityOptions = [
        {
            value: PortfolioVisibility.PRIVATE,
            name: "비공개 (Private)",
            description: "나만 볼 수 있습니다.",
        },
        {
            value: PortfolioVisibility.LINK_ONLY,
            name: "링크 공유 (Link Only)",
            description: "링크를 가진 사람만 볼 수 있습니다.",
        },
        {
            value: PortfolioVisibility.PUBLIC,
            name: "전체 공개 (Public)",
            description: "누구나 볼 수 있고 리더보드에 등록됩니다.",
        },
    ];

    async function handleUpdate() {
        isLoading = true;
        try {
            const updated = await updatePortfolioVisibility(
                portfolioId,
                visibility as PortfolioVisibility,
            );
            visibility = updated.visibility;
            token = updated.share_token;
            // Parent needs to know? Maybe dispatch event or just rely on local state update
        } catch (e) {
            console.error(e);
            alert("설정 변경 중 오류가 발생했습니다.");
        } finally {
            isLoading = false;
        }
    }

    function copyToClipboard() {
        if (!shareUrl) return;
        navigator.clipboard.writeText(shareUrl);
        copied = true;
        setTimeout(() => (copied = false), 2000);
    }

    // Sync props to internal state when modal opens/props change
    $effect(() => {
        visibility = currentVisibility;
        token = shareToken;
    });
</script>

<Modal title="포트폴리오 공유 설정" bind:open size="md">
    <div class="space-y-6">
        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
            포트폴리오의 공개 범위를 설정하고 링크를 공유하세요.
        </p>

        <div
            class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 space-y-4"
        >
            <h3
                class="font-semibold text-gray-900 dark:text-white flex items-center gap-2"
            >
                {#if visibility === PortfolioVisibility.PRIVATE}
                    <LockSolid class="w-5 h-5 text-gray-500" />
                {:else if visibility === PortfolioVisibility.LINK_ONLY}
                    <LinkOutline class="w-5 h-5 text-blue-500" />
                {:else}
                    <GlobeOutline class="w-5 h-5 text-green-500" />
                {/if}
                공개 범위 설정
            </h3>

            <div class="grid gap-3">
                {#each visibilityOptions as option}
                    <div
                        class="flex items-center ps-4 border border-gray-200 rounded-sm dark:border-gray-700"
                    >
                        <input
                            bind:group={visibility}
                            type="radio"
                            name="visibility"
                            value={option.value}
                            class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        />
                        <label
                            for="visibility-radio"
                            class="w-full py-4 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                        >
                            {option.name}
                            <p
                                class="text-xs font-normal text-gray-500 dark:text-gray-400 mt-0.5"
                            >
                                {option.description}
                            </p>
                        </label>
                    </div>
                {/each}
            </div>

            <Button
                class="w-full mt-2"
                onclick={handleUpdate}
                disabled={isLoading ||
                    (visibility === currentVisibility && token === shareToken)}
            >
                {isLoading ? "저장 중..." : "설정 저장"}
            </Button>
        </div>

        {#if visibility !== PortfolioVisibility.PRIVATE && shareUrl}
            <div
                class="space-y-2 pt-4 border-t border-gray-200 dark:border-gray-700"
            >
                <Label>공유 링크</Label>
                <div class="flex gap-2">
                    <Input
                        value={shareUrl}
                        readonly
                        class="bg-gray-100 dark:bg-gray-700"
                    />
                    <Button
                        color="alternative"
                        onclick={copyToClipboard}
                        class="shrink-0"
                    >
                        {#if copied}
                            Copied!
                        {:else}
                            <ClipboardCleanOutline class="w-5 h-5" />
                        {/if}
                    </Button>
                </div>
                <Helper class="text-xs text-gray-500">
                    {#if visibility === PortfolioVisibility.LINK_ONLY}
                        이 링크를 가진 사람만 접근할 수 있습니다.
                    {:else}
                        공개된 링크이며, 리더보드 등에도 노출될 수 있습니다.
                    {/if}
                </Helper>
            </div>
        {/if}
    </div>
</Modal>
