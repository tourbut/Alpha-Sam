<script lang="ts">
    import { Modal, Button, Fileupload, Label, Spinner } from "flowbite-svelte";
    import { uploadTossPortfolio } from "$lib/apis/portfolio";
    import { FileText, CheckCircle, AlertCircle } from "lucide-svelte";

    let { open = $bindable(false), onuploaded } = $props<{
        open: boolean;
        onuploaded: () => void;
    }>();

    let files = $state<FileList | undefined>();
    let isLoading = $state(false);
    let error = $state<string | null>(null);
    let successMessage = $state<string | null>(null);

    function resetState() {
        files = undefined;
        isLoading = false;
        error = null;
        successMessage = null;
    }

    $effect(() => {
        if (open) {
            resetState();
        }
    });

    async function handleUpload() {
        if (!files || files.length === 0) {
            error = "파일을 선택해주세요.";
            return;
        }

        const file = files[0];
        if (file.type !== "application/pdf") {
            error = "PDF 파일만 업로드 가능합니다.";
            return;
        }

        isLoading = true;
        error = null;
        successMessage = null;

        try {
            const formData = new FormData();
            formData.append("file", file);

            const result = await uploadTossPortfolio(formData);

            successMessage = result.message || "성공적으로 업로드되었습니다.";

            // Notify parent to refresh list
            if (onuploaded) {
                onuploaded();
            }

            // Close modal after brief delay on success
            setTimeout(() => {
                open = false;
            }, 2000);
        } catch (err: any) {
            console.error("Upload failed", err);
            error = err.message || "업로드 중 오류가 발생했습니다.";
        } finally {
            isLoading = false;
        }
    }
</script>

<Modal
    title="토스증권 포트폴리오 업로드"
    bind:open
    size="sm"
    outsideclose={!isLoading}
>
    {#if successMessage}
        <div class="flex flex-col items-center justify-center py-6 text-center">
            <div
                class="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mb-4"
            >
                <CheckCircle
                    class="w-8 h-8 text-green-500 dark:text-green-400"
                />
            </div>
            <h3
                class="text-lg font-medium text-neutral-900 dark:text-neutral-100"
            >
                {successMessage}
            </h3>
            <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                포트폴리오 화면으로 이동합니다...
            </p>
        </div>
    {:else}
        <form
            class="flex flex-col space-y-6"
            onsubmit={(e) => {
                e.preventDefault();
                handleUpload();
            }}
        >
            <div>
                <Label class="mb-2">거래내역서 PDF 파일</Label>
                <Fileupload bind:files accept=".pdf" disabled={isLoading} />
                <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                    토스증권 앱에서 발급받은 '거래내역서.pdf' 파일을
                    업로드해주세요.
                </p>
            </div>

            {#if error}
                <div
                    class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 flex flex-row items-center"
                    role="alert"
                >
                    <AlertCircle class="w-4 h-4 mr-2" />
                    <span class="font-medium">{error}</span>
                </div>
            {/if}

            <div class="flex justify-end gap-3">
                <Button
                    color="alternative"
                    onclick={() => (open = false)}
                    disabled={isLoading}
                >
                    취소
                </Button>
                <Button
                    type="submit"
                    class="btn-primary"
                    disabled={isLoading || !files}
                >
                    {#if isLoading}
                        <Spinner class="mr-3" size="4" />
                        업로드 중...
                    {:else}
                        <FileText class="w-4 h-4 mr-2" />
                        업로드 및 파싱
                    {/if}
                </Button>
            </div>
        </form>
    {/if}
</Modal>
