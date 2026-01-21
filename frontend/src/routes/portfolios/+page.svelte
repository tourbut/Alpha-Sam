<script lang="ts">
  /**
   * Portfolios 페이지
   * 와이어프레임 기준으로 리디자인:
   * - 그리드 레이아웃 (auto-fill, minmax 350px)
   * - PortfolioCard 컴포넌트 사용
   * - 빈 상태 UI
   * - Lazy loaded chart
   * - 실제 API 데이터 연동
   */
  import { portfolioStore } from "$lib/stores/portfolio.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth.svelte";
  import { Button, Card, Spinner } from "flowbite-svelte";
  import { Plus, Wallet, AlertCircle } from "lucide-svelte";
  import CreatePortfolioModal from "$lib/components/portfolio/CreatePortfolioModal.svelte";
  import PortfolioCard from "$lib/components/portfolio/PortfolioCard.svelte";
  import { goto } from "$app/navigation";
  import type { PortfolioWithAssets } from "$lib/types";
  import { fetchPortfoliosWithAssets } from "$lib/apis/portfolio";

  // Lazy load chart component
  let PortfolioPieChart: any = $state(null);

  let openCreateModal = $state(false);
  let portfoliosWithAssets = $state<PortfolioWithAssets[]>([]);
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  onMount(async () => {
    if (auth.isAuthenticated) {
      portfolioStore.loadPortfolios();

      // 실제 API 호출로 포트폴리오 + 자산 요약 정보 조회
      try {
        isLoading = true;
        error = null;
        portfoliosWithAssets = await fetchPortfoliosWithAssets();
      } catch (err) {
        console.error("Failed to load portfolios with assets:", err);
        error = "포트폴리오 목록을 불러오는데 실패했습니다.";
        portfoliosWithAssets = [];
      } finally {
        isLoading = false;
      }

      // Lazy load chart component only when portfolios exist
      if (portfoliosWithAssets.length > 0) {
        const module = await import(
          "$lib/components/portfolio/PortfolioPieChart.svelte"
        );
        PortfolioPieChart = module.default;
      }
    } else {
      isLoading = false;
    }
  });

  function viewPortfolio(id: string) {
    goto(`/portfolios/${id}`);
  }
</script>

<svelte:head>
  <title>Portfolios | Alpha-Sam</title>
</svelte:head>

<div class="space-y-6">
  <!-- 페이지 헤더: 타이틀 + 부제 + 생성 버튼 -->
  <header
    class="flex items-center justify-between pb-4 border-b-2 border-dashed border-neutral-200 dark:border-neutral-700"
  >
    <div>
      <h1 class="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
        Portfolios
      </h1>
      <p class="text-neutral-600 dark:text-neutral-400 mt-1">
        Manage your portfolios, assets, and transactions
      </p>
    </div>
    <Button
      class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg"
      onclick={() => (openCreateModal = true)}
    >
      <Plus class="w-4 h-4 mr-2" />
      Create Portfolio
    </Button>
  </header>

  <!-- 로딩 상태 -->
  {#if isLoading}
    <div class="col-span-full flex items-center justify-center py-16">
      <Spinner size="12" class="text-primary-600" />
      <span class="ml-3 text-neutral-600 dark:text-neutral-400"
        >포트폴리오 로딩 중...</span
      >
    </div>
  {:else if error}
    <!-- 에러 상태 -->
    <div class="col-span-full">
      <Card
        class="text-center py-16 border-2 border-dashed border-red-300 dark:border-red-600 bg-red-50 dark:bg-red-900/20"
      >
        <div
          class="w-20 h-20 mx-auto mb-6 rounded-full bg-red-100 dark:bg-red-800 flex items-center justify-center"
        >
          <AlertCircle class="w-10 h-10 text-red-400 dark:text-red-500" />
        </div>
        <h3 class="text-xl font-semibold text-red-900 dark:text-red-100 mb-2">
          오류 발생
        </h3>
        <p class="text-red-600 dark:text-red-400 mb-6 max-w-md mx-auto">
          {error}
        </p>
        <Button color="red" onclick={() => window.location.reload()}>
          다시 시도
        </Button>
      </Card>
    </div>
  {:else}
    <!-- 포트폴리오 그리드 (와이어프레임 기준: auto-fill, minmax 350px) -->
    <div
      class="grid gap-6"
      style="grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));"
    >
      {#each portfoliosWithAssets as portfolio (portfolio.id)}
        <PortfolioCard
          {portfolio}
          isCurrent={portfolio.id === portfolioStore.selectedPortfolioId}
          ChartComponent={PortfolioPieChart}
          onclick={() => viewPortfolio(portfolio.id)}
          onManageClick={() => viewPortfolio(portfolio.id)}
        />
      {:else}
        <!-- 빈 상태 UI -->
        <div class="col-span-full">
          <Card
            class="text-center py-16 border-2 border-dashed border-neutral-300 dark:border-neutral-600"
          >
            <div
              class="w-20 h-20 mx-auto mb-6 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center"
            >
              <Wallet
                class="w-10 h-10 text-neutral-400 dark:text-neutral-500"
              />
            </div>
            <h3
              class="text-xl font-semibold text-neutral-900 dark:text-neutral-100 mb-2"
            >
              No portfolios yet
            </h3>
            <p
              class="text-neutral-600 dark:text-neutral-400 mb-6 max-w-md mx-auto"
            >
              Create your first portfolio to start tracking your assets
            </p>
            <Button
              class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
              onclick={() => (openCreateModal = true)}
            >
              <Plus class="w-4 h-4 mr-2" />
              Create Portfolio
            </Button>
          </Card>
        </div>
      {/each}
    </div>
  {/if}
</div>

<CreatePortfolioModal bind:open={openCreateModal} />
