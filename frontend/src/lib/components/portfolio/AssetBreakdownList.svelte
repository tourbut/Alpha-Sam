<script lang="ts">
  /**
   * AssetBreakdownList.svelte
   * 포트폴리오 내 자산 분배 비율을 표시하는 리스트 컴포넌트
   * 와이어프레임 기준: 색상 도트 + 자산명 + 비율%
   */
  interface Asset {
    symbol: string;
    name: string;
    value: number;
    percentage: number;
  }

  let { assets = [], maxItems = 5 }: { assets: Asset[]; maxItems?: number } = $props();

  // 일관된 색상 팔레트
  const ASSET_COLORS = [
    "#2774AE", // primary-600
    "#00416A", // secondary-500
    "#2E8B57", // accent-500
    "#F59E0B", // warning
    "#EF4444", // error
    "#6B7280", // neutral-500
    "#8B5CF6", // purple
    "#EC4899", // pink
  ];

  function getAssetColor(index: number): string {
    return ASSET_COLORS[index % ASSET_COLORS.length];
  }

  // 표시할 자산 목록 (maxItems 제한)
  $effect(() => {
    // 반응형 처리
  });
</script>

<div class="space-y-2">
  {#each assets.slice(0, maxItems) as asset, index}
    <div class="flex items-center justify-between text-sm py-1 border-b border-neutral-100 dark:border-neutral-700 last:border-b-0">
      <div class="flex items-center gap-2">
        <div
          class="w-3 h-3 rounded-full border-2 border-neutral-200 dark:border-neutral-600"
          style="background-color: {getAssetColor(index)}"
        ></div>
        <span class="text-neutral-700 dark:text-neutral-300 font-medium">
          {asset.symbol}
        </span>
      </div>
      <span class="font-semibold text-neutral-900 dark:text-neutral-100">
        {asset.percentage.toFixed(1)}%
      </span>
    </div>
  {/each}
  {#if assets.length > maxItems}
    <div class="text-xs text-neutral-500 dark:text-neutral-400 text-center pt-1">
      +{assets.length - maxItems} more assets
    </div>
  {/if}
</div>
