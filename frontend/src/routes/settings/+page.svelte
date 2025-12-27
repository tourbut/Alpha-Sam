<script lang="ts">
    import {
        Card,
        Button,
        Label,
        Input,
        Heading,
        Alert,
        Toggle,
        Skeleton,
    } from "flowbite-svelte";
    import { auth } from "$lib/stores/auth";
    import {
        updateProfile,
        changePassword,
        getNotificationSettings,
        updateNotificationSettings,
    } from "$lib/api";
    import { onMount, onDestroy } from "svelte";
    import type { Unsubscriber } from "svelte/store";

    let email = "";
    let nickname = "";

    // Profile Form State
    let updateProfileMessage = "";
    let updateProfileError = false;

    // Password Form State
    let currentPassword = "";
    let newPassword = "";
    let confirmPassword = "";
    let changePasswordMessage = "";
    let changePasswordError = false;

    // Notification Settings State
    let notificationSettings: any = null;
    let notificationMessage = "";
    let notificationError = false;
    let updatingSettings = false;

    async function handleToggleChange() {
        if (!notificationSettings || updatingSettings) return;

        updatingSettings = true;
        notificationMessage = "";

        try {
            await updateNotificationSettings({
                daily_report_enabled: notificationSettings.daily_report_enabled,
                price_alert_enabled: notificationSettings.price_alert_enabled,
            });
            notificationMessage = "Preferences updated automatically.";
            notificationError = false;

            // Clear message after 3 seconds
            setTimeout(() => {
                if (
                    notificationMessage === "Preferences updated automatically."
                ) {
                    notificationMessage = "";
                }
            }, 3000);
        } catch (e) {
            notificationError = true;
            notificationMessage = "Failed to update preferences.";
            // Revert on failure might be complex without original state,
            // but for now we just show error.
        } finally {
            updatingSettings = false;
        }
    }

    let unsubscribe: Unsubscriber;

    async function loadNotificationSettings() {
        try {
            notificationSettings = await getNotificationSettings();
        } catch (e) {
            console.error("Failed to load settings:", e);
        }
    }

    onMount(() => {
        loadNotificationSettings();
        unsubscribe = auth.subscribe((state) => {
            if (state.user) {
                email = state.user.email;
                nickname = state.user.nickname || "";
            }
        });
    });

    onDestroy(() => {
        if (unsubscribe) unsubscribe();
    });

    async function handleUpdateProfile() {
        updateProfileMessage = "";
        updateProfileError = false;
        try {
            await updateProfile({ nickname });
            // Update local store
            auth.updateUser({ nickname });
            updateProfileMessage = "Profile updated successfully.";
        } catch (e) {
            updateProfileError = true;
            updateProfileMessage = "Failed to update profile.";
            console.error(e);
        }
    }

    async function handleChangePassword() {
        changePasswordMessage = "";
        changePasswordError = false;

        if (newPassword !== confirmPassword) {
            changePasswordError = true;
            changePasswordMessage = "New passwords do not match.";
            return;
        }

        try {
            await changePassword({
                current_password: currentPassword,
                new_password: newPassword,
            });
            changePasswordMessage = "Password changed successfully.";
            // Clear fields
            currentPassword = "";
            newPassword = "";
            confirmPassword = "";
        } catch (e) {
            changePasswordError = true;
            changePasswordMessage =
                "Failed to change password. Please check your current password.";
            console.error(e);
        }
    }
</script>

<div class="container mx-auto px-4 py-8">
    <Heading tag="h2" class="mb-4">User Settings</Heading>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Profile Settings Card -->
        <Card>
            <h5
                class="mb-4 text-xl font-bold tracking-tight text-gray-900 dark:text-white"
            >
                Profile Settings
            </h5>
            <form
                class="flex flex-col space-y-4"
                on:submit|preventDefault={handleUpdateProfile}
            >
                <div>
                    <Label for="email" class="mb-2">Email</Label>
                    <Input
                        type="email"
                        id="email"
                        bind:value={email}
                        disabled
                        readonly
                        class="bg-gray-100 dark:bg-gray-600"
                    />
                </div>
                <div>
                    <Label for="nickname" class="mb-2">Nickname</Label>
                    <Input
                        type="text"
                        id="nickname"
                        placeholder="Enter your nickname"
                        bind:value={nickname}
                    />
                </div>

                {#if updateProfileMessage}
                    <Alert
                        color={updateProfileError ? "red" : "green"}
                        class="mt-2"
                    >
                        {updateProfileMessage}
                    </Alert>
                {/if}

                <Button type="submit" class="w-full">Save Profile</Button>
            </form>
        </Card>

        <!-- Security Settings Card -->
        <Card>
            <h5
                class="mb-4 text-xl font-bold tracking-tight text-gray-900 dark:text-white"
            >
                Security Settings
            </h5>
            <form
                class="flex flex-col space-y-4"
                on:submit|preventDefault={handleChangePassword}
            >
                <div>
                    <Label for="current-password" class="mb-2"
                        >Current Password</Label
                    >
                    <Input
                        type="password"
                        id="current-password"
                        placeholder="••••••••"
                        required
                        bind:value={currentPassword}
                    />
                </div>
                <div>
                    <Label for="new-password" class="mb-2">New Password</Label>
                    <Input
                        type="password"
                        id="new-password"
                        placeholder="••••••••"
                        required
                        bind:value={newPassword}
                    />
                </div>
                <div>
                    <Label for="confirm-password" class="mb-2"
                        >Confirm New Password</Label
                    >
                    <Input
                        type="password"
                        id="confirm-password"
                        placeholder="••••••••"
                        required
                        bind:value={confirmPassword}
                    />
                </div>

                {#if changePasswordMessage}
                    <Alert
                        color={changePasswordError ? "red" : "green"}
                        class="mt-2"
                    >
                        {changePasswordMessage}
                    </Alert>
                {/if}

                <Button type="submit" class="w-full">Change Password</Button>
            </form>
        </Card>

        <!-- Notification Settings Card -->
        <Card>
            <h5
                class="mb-4 text-xl font-bold tracking-tight text-gray-900 dark:text-white"
            >
                Notification Settings
            </h5>
            <form
                class="flex flex-col space-y-4"
                on:submit|preventDefault={() => {}}
            >
                {#if notificationSettings}
                    <div class="flex justify-between items-center">
                        <Label for="daily-report" class="mb-0 cursor-pointer">
                            <span
                                class="text-base font-medium text-gray-900 dark:text-gray-300"
                                >Daily Portfolio Report</span
                            >
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                Receive a daily summary of your portfolio
                                performance.
                            </p>
                        </Label>
                        <Toggle
                            id="daily-report"
                            bind:checked={
                                notificationSettings.daily_report_enabled
                            }
                            disabled={updatingSettings}
                            on:click={() => setTimeout(handleToggleChange, 0)}
                        />
                    </div>

                    <div
                        class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700"
                    >
                        <Label for="price-alerts" class="mb-0 cursor-pointer">
                            <span
                                class="text-base font-medium text-gray-900 dark:text-gray-300"
                                >Price Alerts</span
                            >
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                Get notified when assets hit your target price.
                            </p>
                        </Label>
                        <Toggle
                            id="price-alerts"
                            bind:checked={
                                notificationSettings.price_alert_enabled
                            }
                            disabled={updatingSettings}
                            on:click={() => setTimeout(handleToggleChange, 0)}
                        />
                    </div>
                {:else}
                    <div class="space-y-4 py-2">
                        <div class="flex justify-between items-center">
                            <div class="space-y-2 w-3/4">
                                <Skeleton class="h-4 w-1/2" />
                                <Skeleton class="h-3 w-full" />
                            </div>
                            <Skeleton class="h-6 w-10 rounded-full" />
                        </div>
                        <div
                            class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700"
                        >
                            <div class="space-y-2 w-3/4">
                                <Skeleton class="h-4 w-1/2" />
                                <Skeleton class="h-3 w-full" />
                            </div>
                            <Skeleton class="h-6 w-10 rounded-full" />
                        </div>
                    </div>
                {/if}

                {#if notificationMessage}
                    <Alert
                        color={notificationError ? "red" : "green"}
                        class="mt-4"
                    >
                        {notificationMessage}
                    </Alert>
                {/if}
            </form>
        </Card>
    </div>
</div>
