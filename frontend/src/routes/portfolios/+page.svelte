<script lang="ts">
  /**
   * Portfolios 페이지
   * 와이어프레임 기준으로 리디자인:
   * - 그리드 레이아웃 (auto-fill, minmax 350px)
   * - PortfolioCard 컴포넌트 사용
   * - 빈 상태 UI
   * - Lazy loaded chart
   */
  import { portfolioStore } from "$lib/stores/portfolio.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth.svelte";
  import { Button, Card } from "flowbite-svelte";
  import { Plus, Wallet } from "lucide-svelte";
  import CreatePortfolioModal from "$lib/components/portfolio/CreatePortfolioModal.svelte";
  import PortfolioCard from "$lib/components/portfolio/PortfolioCard.svelte";
  import { goto } from "$app/navigation";
  import type { PortfolioWithAssets } from "$lib/types";

  // Lazy load chart component
  let PortfolioPieChart: any = $state(null);

  let openCreateModal = $state(false);
  let portfoliosWithAssets = $state<PortfolioWithAssets[]>([]);

  onMount(async () => {
    if (auth.isAuthenticated) {
      portfolioStore.loadPortfolios();

      // TODO: Replace with actual API call to get portfolios with asset breakdown
      // For now, using mock data as per wireframe
      portfoliosWithAssets = [
        {
          id: 1,
          name: "Main Portfolio",
          description: "Primary investment portfolio",
          created_at: "2024-01-15",
          totalValue: 45000,
          assets: [
            { symbol: "BTC", name: "Bitcoin", value: 24000, percentage: 53.3 },
            { symbol: "ETH", name: "Ethereum", value: 15000, percentage: 33.3 },
            { symbol: "SOL", name: "Solana", value: 6000, percentage: 13.3 },
          ],
        },
        {
          id: 2,
          name: "Retirement Fund",
          description: "Long-term investment strategy",
          created_at: "2024-02-10",
          totalValue: 75000,
          assets: [
            { symbol: "BTC", name: "Bitcoin", value: 40000, percentage: 53.3 },
            { symbol: "ETH", name: "Ethereum", value: 25000, percentage: 33.3 },
            { symbol: "ADA", name: "Cardano", value: 10000, percentage: 13.3 },
          ],
        },
      ];

      // Lazy load chart component only when portfolios exist
      if (portfoliosWithAssets.length > 0) {
        const module = await import(
          "$lib/components/portfolio/PortfolioPieChart.svelte"
        );
        PortfolioPieChart = module.default;
      }
    }
  });

  function viewPortfolio(id: number) {
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
            <Wallet class="w-10 h-10 text-neutral-400 dark:text-neutral-500" />
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
</div>

<CreatePortfolioModal bind:open={openCreateModal} />
