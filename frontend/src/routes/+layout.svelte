<script lang="ts">
  import "../app.css";
  import AppNavbar from "$lib/components/common/AppNavbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import AssetModal from "$lib/components/AssetModal.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth.svelte";
  import ChatWidget from "$lib/components/chat/ChatWidget.svelte";
  import { page } from "$app/state";
  import {
    HomeOutline,
    ClipboardListOutline,
    CogOutline,
    WalletSolid,
  } from "flowbite-svelte-icons";

  let openAssetModal = $state(false);

  // 사이드바 네비게이션 아이템 (전역 적용)
  const navItems = [
    { href: "/", label: "Dashboard", icon: HomeOutline },
    { href: "/portfolios", label: "Portfolios", icon: WalletSolid },
    {
      href: "/social/leaderboard",
      label: "Leaderboard",
      icon: ClipboardListOutline,
    },
    { href: "/settings", label: "Settings", icon: CogOutline },
  ];

  let finalNavItems = $derived.by(() => {
    const items = [...navItems];
    if (auth.user?.is_superuser) {
      items.push({
        href: "/admin/assets",
        label: "System Admin",
        icon: CogOutline, // Or specific icon
      });
    }
    return items;
  });

  // 사이드바를 표시하지 않을 경로 목록
  const noSidebarPaths = ["/login", "/signup"];

  // 현재 경로가 사이드바를 표시해야 하는지 확인
  let showSidebar = $derived(
    auth.isAuthenticated && !noSidebarPaths.includes(page.url.pathname),
  );

  onMount(() => {
    if (!auth.isAuthenticated) {
      auth.initialize();
    }
  });
</script>

<div
  class="flex flex-col min-h-screen w-full bg-neutral-50 dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100 transition-colors duration-200 overflow-x-hidden"
>
  <AppNavbar />

  <!-- 메인 영역: 사이드바 + 콘텐츠 (인증된 사용자에게만 사이드바 표시) -->
  {#if showSidebar}
    <main class="flex-grow w-full overflow-visible pt-20">
      <div class="max-w-[1400px] mx-auto p-5">
        <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-5">
          <!-- 사이드바 네비게이션 -->
          <aside class="sidebar hidden lg:block">
            {#each finalNavItems as item}
              <a
                href={item.href}
                class="nav-item flex items-center gap-3 {page.url.pathname ===
                item.href
                  ? 'active'
                  : ''}"
              >
                <svelte:component this={item.icon} class="w-5 h-5" />
                {item.label}
              </a>
            {/each}
          </aside>

          <!-- 페이지 콘텐츠 -->
          <div class="min-w-0">
            <slot />
          </div>
        </div>
      </div>
    </main>
  {:else}
    <!-- 로그인/회원가입 페이지는 사이드바 없이 전체 너비 사용 -->
    <main class="flex-grow w-full overflow-visible pt-20">
      <slot />
    </main>
  {/if}

  <Footer />
  <ChatWidget />
  <AssetModal bind:open={openAssetModal} />
</div>
