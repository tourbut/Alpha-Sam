<script lang="ts">
    import {
        Footer,
        FooterCopyright,
        FooterLinkGroup,
        FooterLink,
    } from "flowbite-svelte";
</script>

<Footer
    class="mt-auto rounded-none shadow-none border-t border-gray-200 dark:border-gray-700"
>
    <div class="w-full text-center">
        <div
            class="w-full justify-between sm:flex sm:items-center sm:justify-between"
        >
            <FooterCopyright
                href="/"
                by="Alpha-Sam"
                year={new Date().getFullYear()}
            />
            <FooterLinkGroup
                class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
            >
                <FooterLink href="/">About</FooterLink>
                <FooterLink href="/">Privacy Policy</FooterLink>
                <FooterLink href="/">Licensing</FooterLink>
                <FooterLink href="/">Contact</FooterLink>
            </FooterLinkGroup>
        </div>
    </div>
</Footer>
