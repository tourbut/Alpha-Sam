<script lang="ts">
    import { Modal, Button, Toggle, Label, Input, Helper } from "flowbite-svelte";
    import { socialStore } from "$lib/stores/social.svelte";
    import { ShareNodesOutline, ClipboardCleanOutline, ChevronRightOutline } from "flowbite-svelte-icons";

    let { open = $bindable(false) } = $props();
    
    let shareUrl = $state("");
    let isCreating = $state(false);
    let copied = $state(false);

    async function handleCreateLink() {
        isCreating = true;
        try {
            shareUrl = await socialStore.createShareLink();
        } finally {
            isCreating = false;
        }
    }

    function copyToClipboard() {
        if (!shareUrl) return;
        navigator.clipboard.writeText(shareUrl);
        copied = true;
        setTimeout(() => copied = false, 2000);
    }
</script>

<Modal title="Share Your Portfolio" bind:open size="md">
    <div class="space-y-6">
        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
            당신의 포트폴리오 성과를 세상에 공유하세요. 개인 정보보호를 위해 공유 항목을 세밀하게 제어할 수 있습니다.
        </p>

        <div class="space-y-4 bg-gray-50 dark:bg-gray-800 p-4 rounded-lg border border-gray-100 dark:border-gray-700">
            <h3 class="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <ShareNodesOutline class="w-5 h-5 text-primary-600" />
                공유 설정
            </h3>
            
            <div class="flex items-center justify-between">
                <Label for="show-pnl" class="text-sm">수익률(PnL%) 공개</Label>
                <Toggle id="show-pnl" bind:checked={socialStore.shareSettings.show_pnl} color="green" />
            </div>
            
            <div class="flex items-center justify-between">
                <Label for="show-weights" class="text-sm">종목 비중 공개</Label>
                <Toggle id="show-weights" bind:checked={socialStore.shareSettings.show_weights} color="blue" />
            </div>

            <div class="flex items-center justify-between">
                <div>
                    <Label for="show-amounts" class="text-sm">실제 자산 금액 공개</Label>
                    <Helper class="text-xs text-red-500">주의: 실제 보유 수량과 가치가 노출됩니다.</Helper>
                </div>
                <Toggle id="show-amounts" bind:checked={socialStore.shareSettings.show_amounts} color="red" />
            </div>
        </div>

        {#if !shareUrl}
            <Button class="w-full" on:click={handleCreateLink} disabled={isCreating}>
                {#if isCreating}
                    공유 링크 생성 중...
                {:else}
                    공유 링크 생성하기
                {/if}
            </Button>
        {:else}
            <div class="space-y-2">
                <Label>공유 링크</Label>
                <div class="flex gap-2">
                    <Input value={shareUrl} readonly class="bg-gray-100 dark:bg-gray-700" />
                    <Button color="alternative" on:click={copyToClipboard} class="shrink-0">
                        {#if copied}
                            Copied!
                        {:else}
                            <ClipboardCleanOutline class="w-5 h-5" />
                        {/if}
                    </Button>
                </div>
                <p class="text-xs text-gray-500">이 링크를 가진 사람만 당신의 포트폴리오를 볼 수 있습니다.</p>
            </div>
        {/if}
    </div>
    
    <svelte:fragment slot="footer">
        <Button color="alternative" on:click={() => open = false}>닫기</Button>
    </svelte:fragment>
</Modal>
