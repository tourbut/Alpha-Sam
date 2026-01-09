<script lang="ts">
  import "../app.css";
  import AppNavbar from "$lib/components/common/AppNavbar.svelte";
  import Footer from "$lib/components/Footer.svelte";
  import AssetModal from "$lib/components/AssetModal.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth.svelte";
  import ChatWidget from "$lib/components/chat/ChatWidget.svelte";

  let openAssetModal = $state(false);

  onMount(() => {
    if (!auth.isAuthenticated) {
      auth.initialize();
    }
  });
</script>

<div
  class="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-200"
>
  <AppNavbar bind:openAssetModal />

  <main class="flex-grow pt-20">
    <slot />
  </main>

  <Footer />
  <ChatWidget />
  <AssetModal bind:open={openAssetModal} />
</div>
