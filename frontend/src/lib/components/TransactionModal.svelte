<script lang="ts">
	import { Modal, Label, Input, Button, Select } from "flowbite-svelte";
	import { createEventDispatcher } from "svelte";
	import type { Asset } from "$lib/types";
	import type { TransactionCreate } from "$lib/apis/portfolio";
	import { createTransaction } from "$lib/apis/portfolio";

	export let open = false;
	export let asset: Asset | null = null;
	export let assets: Asset[] = [];
	export let portfolioId: string = ""; // TODO: 실제 Portfolio ID 사용

	const dispatch = createEventDispatcher();

	let selectedAssetId: string | null = null;
	let transactionType: "BUY" | "SELL" = "BUY";
	let quantity = "";
	let price = "";
	let executedAt = "";
	let error: string | null = null;
	let loading = false;

	// 모달이 열릴 때 초기화
	$: if (open) {
		if (asset) {
			selectedAssetId = asset.id;
		} else {
			selectedAssetId = null;
		}
		transactionType = "BUY";
		quantity = "";
		price = "";
		executedAt = new Date().toISOString().split("T")[0]; // 오늘 날짜
		error = null;
	}

	function resetForm() {
		selectedAssetId = null;
		transactionType = "BUY";
		quantity = "";
		price = "";
		executedAt = "";
		error = null;
	}

	function validateForm(): boolean {
		if (!selectedAssetId) {
			error = "자산을 선택해주세요";
			return false;
		}

		const qty = parseFloat(quantity);
		if (isNaN(qty) || qty <= 0) {
			error = "수량은 0보다 커야 합니다";
			return false;
		}

		const priceValue = parseFloat(price);
		if (isNaN(priceValue) || priceValue <= 0) {
			error = "가격은 0보다 커야 합니다";
			return false;
		}

		return true;
	}

	async function handleSubmit() {
		if (!validateForm()) {
			return;
		}

		loading = true;
		error = null;

		try {
			const transactionData: TransactionCreate = {
				asset_id: selectedAssetId!,
				type: transactionType,
				quantity: parseFloat(quantity),
				price: parseFloat(price),
				executed_at: executedAt || undefined,
			};

			await createTransaction(portfolioId, transactionData);

			dispatch("created");
			open = false;
			resetForm();
		} catch (err: any) {
			console.error("Failed to create transaction:", err);
			error = err.message || "거래 추가에 실패했습니다";
		} finally {
			loading = false;
		}
	}

	function handleClose() {
		open = false;
		resetForm();
	}
</script>

<Modal bind:open title="거래 추가" autoclose={false} onclose={handleClose}>
	<form
		class="flex flex-col space-y-6"
		on:submit|preventDefault={handleSubmit}
	>
		{#if error}
			<div
				class="p-4 mb-4 text-sm text-red-800 bg-red-50 dark:bg-red-800/50 dark:text-red-400 rounded-lg"
			>
				{error}
			</div>
		{/if}

		{#if !asset}
			<Label>
				<span>자산</span>
				<Select
					class="mt-2"
					items={assets.map((a) => ({
						value: a.id,
						name: `${a.symbol} - ${a.name}`,
					}))}
					bind:value={selectedAssetId}
					required
				>
					<option value="">자산 선택</option>
				</Select>
			</Label>
		{:else}
			<Label>
				<span>자산</span>
				<Input
					type="text"
					value={`${asset.symbol} - ${asset.name}`}
					disabled
					readonly
				/>
			</Label>
		{/if}

		<Label>
			<span>거래 유형</span>
			<Select class="mt-2" bind:value={transactionType} required>
				<option value="BUY">매수 (BUY)</option>
				<option value="SELL">매도 (SELL)</option>
			</Select>
		</Label>

		<Label>
			<span>수량</span>
			<Input
				type="number"
				step="any"
				min="0.0001"
				bind:value={quantity}
				placeholder="0.0"
				required
			/>
			<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
				거래할 수량
			</p>
		</Label>

		<Label>
			<span>가격</span>
			<Input
				type="number"
				step="any"
				min="0.01"
				bind:value={price}
				placeholder="0.00"
				required
			/>
			<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
				단위당 거래 가격
			</p>
		</Label>

		<Label>
			<span>거래 날짜 (선택사항)</span>
			<Input type="date" bind:value={executedAt} />
			<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
				거래가 실행된 날짜 (기본값: 오늘)
			</p>
		</Label>

		<div class="flex gap-2 justify-end">
			<Button
				color="alternative"
				type="button"
				onclick={handleClose}
				disabled={loading}
			>
				취소
			</Button>
			<Button type="submit" disabled={loading}>
				{loading ? "저장 중..." : "거래 추가"}
			</Button>
		</div>
	</form>
</Modal>
