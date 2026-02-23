<script lang="ts">
    import {
        Footer,
        FooterCopyright,
        FooterLinkGroup,
        FooterLink,
    } from "flowbite-svelte";
    import { APP_NAME } from "$lib/constants";
</script>

<Footer
    class="mt-auto rounded-none shadow-none border-t border-neutral-200 dark:border-neutral-700"
>
    <div class="w-full flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div
            class="w-full flex flex-col sm:flex-row sm:items-center sm:justify-between"
        >
            <FooterCopyright
                href="/"
                by={APP_NAME}
                year={new Date().getFullYear()}
            />
            <FooterLinkGroup
                class="flex flex-wrap items-center justify-center sm:justify-end text-sm text-neutral-500 dark:text-neutral-400"
            >
                <FooterLink href="/">About</FooterLink>
                <FooterLink href="/">Privacy Policy</FooterLink>
                <FooterLink href="/">Licensing</FooterLink>
                <FooterLink href="/">Contact</FooterLink>
            </FooterLinkGroup>
        </div>
    </div>
</Footer>
