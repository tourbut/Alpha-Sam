<script lang="ts">
  import "../app.css";
  import {
    Navbar,
    NavBrand,
    NavLi,
    NavUl,
    NavHamburger,
    Button,
  } from "flowbite-svelte";

  import Footer from "$lib/components/Footer.svelte";
  import AssetModal from "$lib/components/AssetModal.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import DevUserSwitcher from "$lib/components/DevUserSwitcher.svelte";

  let hidden = true; // Mobile menu hidden by default
  let openAssetModal = false;

  function toggle() {
    hidden = !hidden;
  }

  onMount(() => {
    auth.initialize();
  });

  function handleLogout() {
    auth.logout();
    goto("/login");
  }
</script>

<div class="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900">
  <Navbar
    fluid={true}
    class="fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600"
  >
    <NavBrand href="/">
      <span
        class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
        >Alpha-Sam</span
      >
    </NavBrand>
    <NavHamburger onclick={toggle} class="md:hidden" />
    <NavUl {hidden} class="w-full md:block md:w-auto">
      {#if $auth.isAuthenticated}
        <NavLi href="/">Dashboard</NavLi>
        <NavLi href="/assets">Assets</NavLi>
        <NavLi href="/positions">Positions</NavLi>
        <div class="flex items-center space-x-4 md:ml-4">
          <Button size="xs" on:click={() => (openAssetModal = true)}
            >Add Asset</Button
          >
          {#if $auth.user}
            <span class="text-sm font-medium text-gray-900 dark:text-white">
              Hello, {$auth.user.nickname || $auth.user.email}
            </span>
          {/if}
          <NavLi class="cursor-pointer" on:click={handleLogout}>Logout</NavLi>
        </div>
        <NavLi href="/settings">Settings</NavLi>
      {:else}
        <NavLi href="/login">Login</NavLi>
        <NavLi href="/signup">Sign up</NavLi>
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
