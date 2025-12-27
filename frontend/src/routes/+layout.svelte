<script lang="ts">
  import "../app.css";
  import { page } from "$app/stores";
  import {
    Navbar,
    NavBrand,
    NavLi,
    NavUl,
    NavHamburger,
  } from "flowbite-svelte";

  import Footer from "$lib/components/Footer.svelte";
  import { onMount } from "svelte";
  import { auth } from "$lib/stores/auth";
  import { Button } from "flowbite-svelte";
  import { goto } from "$app/navigation";
  import { browser } from "$app/environment";

  let hidden = true; // Mobile menu hidden by default
  function toggle() {
    hidden = !hidden;
  }

  onMount(() => {
    auth.initialize();
  });

  $: if (browser && !$auth.isAuthenticated) {
    const publicRoutes = ["/login", "/signup"];
    // Simple check. In real app, might want match logic or use layout groups.
    if (!publicRoutes.includes($page.url.pathname)) {
      // Redirect to login
      goto("/login");
    }
  }

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
        <NavLi href="/settings">Settings</NavLi>
        <NavLi class="cursor-pointer" onclick={handleLogout}>Logout</NavLi>
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
</div>
