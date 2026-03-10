<script lang="ts">
    import {
        Modal,
        Button,
        Fileupload,
        Label,
        Spinner,
        Select,
    } from "flowbite-svelte";
    import { uploadPortfolio } from "$lib/apis/portfolio";
    import { FileText, CheckCircle, AlertCircle } from "lucide-svelte";

    let {
        open = $bindable(false),
        onuploaded,
        portfolioId = null,
    } = $props<{
        open: boolean;
        onuploaded: () => void;
        portfolioId?: string | null;
    }>();

    let files = $state<FileList | undefined>();
    let provider = $state<string>("toss");
    let isLoading = $state(false);
    let error = $state<string | null>(null);
    let successMessage = $state<string | null>(null);

    let providers = [
        { value: "toss", name: "토스증권 (PDF)" },
        { value: "common", name: "알파샘 공통양식 (CSV)" },
    ];

    function resetState() {
        files = undefined;
        provider = "toss";
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
        if (provider === "toss" && file.type !== "application/pdf") {
            error = "토스증권은 PDF 파일만 업로드 가능합니다.";
            return;
        }
        if (
            provider === "common" &&
            !file.name.toLowerCase().endsWith(".csv")
        ) {
            error = "공통양식은 CSV 파일만 업로드 가능합니다.";
            return;
        }

        isLoading = true;
        error = null;
        successMessage = null;

        try {
            const formData = new FormData();
            formData.append("file", file);

            const result = await uploadPortfolio(
                provider,
                formData,
                portfolioId || undefined,
            );

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
    title="거래내역 포트폴리오 업로드"
    bind:open
    size="lg"
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
                <Label class="mb-2">증권사/양식 선택</Label>
                <Select
                    items={providers}
                    bind:value={provider}
                    class="mb-4"
                    disabled={isLoading}
                />

                <Label class="mb-2">거래내역서 파일</Label>
                <Fileupload
                    bind:files
                    accept={provider === "toss" ? ".pdf" : ".csv"}
                    disabled={isLoading}
                />
                <div
                    class="mt-2 text-sm text-neutral-500 dark:text-neutral-400"
                >
                    {#if provider === "toss"}
                        토스증권 앱에서 발급받은 '거래내역서.pdf' 파일을
                        업로드해주세요.
                    {:else}
                        <div class="flex items-center gap-2">
                            <span
                                >알파샘 공통양식으로 작성된 .csv 파일을
                                업로드해주세요. 양식에 맞추어 작성되어야 파싱이
                                가능합니다.</span
                            >
                            <Button
                                size="xs"
                                color="alternative"
                                href="/data/sample_common_format.csv"
                                download>샘플 양식 다운로드</Button
                            >
                        </div>
                    {/if}
                </div>
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
                    disabled={isLoading}>취소</Button
                >
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
