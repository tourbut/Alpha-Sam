<script lang="ts">
  import "../app.css";
  import {
    Navbar,
    NavBrand,
    NavLi,
    NavUl,
    NavHamburger,
    Button,
    DarkMode,
  } from "flowbite-svelte";

  import Footer from "$lib/components/Footer.svelte";
  import AssetModal from "$lib/components/AssetModal.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth.svelte";
  import { goto } from "$app/navigation";
  import DevUserSwitcher from "$lib/components/DevUserSwitcher.svelte";

  let hidden = true; // Mobile menu hidden by default
  let openAssetModal = false;

  function toggle() {
    hidden = !hidden;
  }

  onMount(() => {
    if (!auth.isAuthenticated) {
      auth.initialize();
    }
  });

  function handleLogout() {
    auth.logout();
    goto("/login");
  }
</script>

<div
  class="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-200"
>
  <Navbar
    fluid={true}
    class="fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600 px-4 py-2.5 bg-white dark:bg-gray-800"
  >
    <NavBrand href="/">
      <span
        class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
        >Alpha-Sam</span
      >
    </NavBrand>

    <div class="flex items-center md:order-2 space-x-3">
      <DarkMode
        class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5"
      />

      {#if auth.isAuthenticated}
        <Button
          size="sm"
          class="bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l text-white focus:ring-4 focus:outline-none focus:ring-purple-200 dark:focus:ring-purple-800"
          on:click={() => (openAssetModal = true)}
        >
          + Add Asset
        </Button>
        {#if auth.user}
          <div
            class="hidden lg:flex items-center gap-2 text-sm font-medium text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full border border-gray-200 dark:border-gray-600"
          >
            <span>👤 {auth.user.nickname || auth.user.email}</span>
          </div>
        {/if}
        <Button
          size="xs"
          color="light"
          class="border-0 hidden md:block"
          onclick={handleLogout}>Logout</Button
        >
      {:else}
        <div class="flex items-center gap-2">
          <Button href="/login" size="xs">Login</Button>
          <Button href="/signup" size="xs" color="alternative">Sign up</Button>
        </div>
      {/if}
      <NavHamburger onclick={toggle} class="md:hidden" />
    </div>

    <NavUl
      {hidden}
      class="justify-between hidden w-full md:flex md:w-auto md:order-1"
    >
      {#if auth.isAuthenticated}
        <NavLi href="/">Dashboard</NavLi>
        <NavLi href="/assets">Assets</NavLi>
        <NavLi href="/positions">Positions</NavLi>
        <NavLi href="/settings">Settings</NavLi>
        <NavLi href="#" class="cursor-pointer md:hidden" onclick={handleLogout}
          >Logout</NavLi
        >
      {:else}
        <NavLi href="/login" class="md:hidden">Login</NavLi>
        <NavLi href="/signup" class="md:hidden">Sign up</NavLi>
      {/if}
    </NavUl>
  </Navbar>

  <main class="flex-grow pt-20">
    <slot />
  </main>

  <Footer />
  <DevUserSwitcher />
  <AssetModal bind:open={openAssetModal} />
</div>
