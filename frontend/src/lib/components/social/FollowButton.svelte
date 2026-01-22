<script lang="ts">
    import { Button } from "flowbite-svelte";
    import {
        UserAddOutline,
        UserRemoveOutline,
        CheckOutline,
    } from "flowbite-svelte-icons";
    import { followUser, unfollowUser } from "$lib/apis/social";

    // Flowbite-Svelte Button 타입 정의
    type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
    type ButtonColor = "primary" | "light" | "dark" | "alternative" | "red" | "green" | "yellow" | "purple";

    interface Props {
        userId: string;
        initialIsFollowing?: boolean;
        size?: ButtonSize;
        onToggle?: (isFollowing: boolean) => void;
    }

    let {
        userId,
        initialIsFollowing = false,
        size = "sm" as ButtonSize,
        onToggle = () => {},
    }: Props = $props();

    let isFollowing = $state(initialIsFollowing);
    let isLoading = $state(false);

    async function toggleFollow() {
        if (!userId) return;

        isLoading = true;
        try {
            if (isFollowing) {
                await unfollowUser(userId);
                isFollowing = false;
            } else {
                await followUser(userId);
                isFollowing = true;
            }
            onToggle(isFollowing);
        } catch (error) {
            console.error("Follow action failed:", error);
            alert("작업을 처리하는 중 오류가 발생했습니다.");
        } finally {
            isLoading = false;
        }
    }

    // 버튼 색상: 팔로우 중이면 light, 아니면 primary
    let btnColor: ButtonColor = $derived(isFollowing ? "light" : "primary");
</script>

<Button
    {size}
    color={btnColor}
    outline={isFollowing}
    disabled={isLoading}
    onclick={toggleFollow}
    class="gap-2 transition-all duration-200"
>
    {#if isLoading}
        <span class="animate-pulse">Loading...</span>
    {:else if isFollowing}
        <CheckOutline class="w-4 h-4" />
        <span class="hidden sm:inline">Following</span>
    {:else}
        <UserAddOutline class="w-4 h-4" />
        <span>Follow</span>
    {/if}
</Button>
