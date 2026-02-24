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
    import { auth } from "$lib/stores/auth.svelte";
    import {
        update_me as updateProfile,
        change_password as changePassword,
        get_notification_settings as getNotificationSettings,
        update_notification_settings as updateNotificationSettings,
    } from "$lib/apis/users";
    import { onMount, onDestroy } from "svelte";

    let email = $state("");
    let nickname = $state("");
    let isPublicLeaderboard = $state(false);

    // Profile Form State
    let updateProfileMessage = $state("");
    let updateProfileError = $state(false);

    // Password Form State
    let currentPassword = $state("");
    let newPassword = $state("");
    let confirmPassword = $state("");
    let changePasswordMessage = $state("");
    let changePasswordError = $state(false);

    // Notification Settings State
    let notificationSettings: any = $state(null);
    let notificationMessage = $state("");
    let notificationError = $state(false);
    let updatingSettings = $state(false);
    let settingsLoading = $state(true);

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

    async function loadNotificationSettings() {
        try {
            settingsLoading = true;
            notificationSettings = await getNotificationSettings();
        } catch (e) {
            console.error("Failed to load settings:", e);
        } finally {
            settingsLoading = false;
        }
    }

    onMount(() => {
        loadNotificationSettings();
    });

    $effect(() => {
        if (auth.user) {
            email = auth.user.email;
            nickname = auth.user.nickname || "";
            isPublicLeaderboard = auth.user.is_public_leaderboard || false;
        }
    });

    async function handleUpdateProfile() {
        updateProfileMessage = "";
        updateProfileError = false;
        try {
            await updateProfile({ 
                nickname, 
                is_public_leaderboard: isPublicLeaderboard 
            });
            // Update local store
            auth.updateUser({ 
                nickname, 
                is_public_leaderboard: isPublicLeaderboard 
            });
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

<div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-6 pb-4 border-b-2 border-dashed border-neutral-200 dark:border-neutral-700">
        <h1 class="text-3xl font-bold text-neutral-900 dark:text-neutral-100">Settings</h1>
        <p class="text-neutral-600 dark:text-neutral-400 mt-1">Manage your account, security, and preferences</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Profile Settings Card -->
        <Card class="!max-w-none w-full border border-neutral-200 dark:border-neutral-700 bg-gradient-to-br from-neutral-50 to-white dark:from-neutral-800/50 dark:to-neutral-800 h-fit p-6">
            <h5
                class="mb-2 text-lg font-semibold text-neutral-900 dark:text-neutral-100"
            >
                Profile Settings
            </h5>
            <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-6 pb-4 border-b border-neutral-200 dark:border-neutral-700">Update your basic account information</p>
            
            <form
                class="flex flex-col space-y-5"
                onsubmit={(e) => {
                    e.preventDefault();
                    handleUpdateProfile();
                }}
            >
                <div>
                    <Label for="email" class="mb-2 text-neutral-700 dark:text-neutral-300">Email Address</Label>
                    <Input
                        type="email"
                        id="email"
                        bind:value={email}
                        disabled
                        readonly
                        class="bg-neutral-100 dark:bg-neutral-700 cursor-not-allowed opacity-60"
                    />
                    <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-1.5">Cannot be changed - contact support if you need assistance</p>
                </div>
                <div>
                    <Label for="nickname" class="mb-2 text-neutral-700 dark:text-neutral-300">Nickname</Label>
                    <Input
                        type="text"
                        id="nickname"
                        placeholder="Enter your nickname (optional)"
                        bind:value={nickname}
                    />
                </div>
                
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pt-4 border-t border-neutral-200 dark:border-neutral-700">
                    <Label for="public-leaderboard" class="mb-0 cursor-pointer flex-1">
                        <span class="block text-base font-medium text-neutral-900 dark:text-neutral-100 mb-1">Public Leaderboard</span>
                        <p class="text-sm text-neutral-600 dark:text-neutral-400">
                            Allow others to see your nickname and portfolio performance on the leaderboard.
                        </p>
                    </Label>
                    <div class="flex-shrink-0">
                        <Toggle
                            id="public-leaderboard"
                            bind:checked={isPublicLeaderboard}
                        />
                    </div>
                </div>

                {#if updateProfileMessage}
                    <Alert
                        color={updateProfileError ? "red" : "green"}
                        class="mt-4 flex items-center gap-2 font-medium"
                    >
                        <span>{updateProfileError ? "⚠️" : "✓"}</span>
                        {updateProfileMessage}
                    </Alert>
                {/if}

                <Button type="submit" class="w-full btn-primary mt-2">Save Profile</Button>
            </form>
        </Card>

        <!-- Security Settings Card -->
        <Card class="!max-w-none w-full border border-amber-200 dark:border-amber-800 bg-gradient-to-br from-amber-50 to-white dark:from-amber-900/20 dark:to-neutral-800 h-fit p-6">
            <div class="inline-block bg-amber-100 dark:bg-amber-900/40 text-amber-900 dark:text-amber-200 px-3 py-1 rounded-full text-xs font-semibold mb-4">
                🔒 IMPORTANT
            </div>
            <h5
                class="mb-2 text-lg font-semibold text-neutral-900 dark:text-neutral-100"
            >
                Security Settings
            </h5>
            <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-6 pb-4 border-b border-amber-200 dark:border-amber-800">We recommend using a strong, unique password for your account</p>
            <form
                class="flex flex-col space-y-5"
                onsubmit={(e) => {
                    e.preventDefault();
                    handleChangePassword();
                }}
            >
                <div>
                    <Label for="current-password" class="mb-2 text-neutral-700 dark:text-neutral-300"
                        >Current Password</Label
                    >
                    <Input
                        type="password"
                        id="current-password"
                        placeholder="Enter current password"
                        required
                        bind:value={currentPassword}
                    />
                </div>
                <div>
                    <Label for="new-password" class="mb-2 text-neutral-700 dark:text-neutral-300">New Password</Label>
                    <Input
                        type="password"
                        id="new-password"
                        placeholder="Enter new password"
                        required
                        bind:value={newPassword}
                    />
                </div>
                <div>
                    <Label for="confirm-password" class="mb-2 text-neutral-700 dark:text-neutral-300"
                        >Confirm New Password</Label
                    >
                    <Input
                        type="password"
                        id="confirm-password"
                        placeholder="Confirm new password"
                        required
                        bind:value={confirmPassword}
                    />
                </div>

                {#if changePasswordMessage}
                    <Alert
                        color={changePasswordError ? "red" : "green"}
                        class="mt-4 flex items-center gap-2 font-medium"
                    >
                        <span>{changePasswordError ? "⚠️" : "✓"}</span>
                        {changePasswordMessage}
                    </Alert>
                {/if}

                <Button type="submit" class="w-full btn-primary mt-2">Change Password</Button>
            </form>
        </Card>

        <!-- Notification Settings Card -->
        <Card class="!max-w-none w-full border border-neutral-200 dark:border-neutral-700 bg-gradient-to-br from-neutral-50 to-white dark:from-neutral-800/50 dark:to-neutral-800 lg:col-span-2 p-6">
            <h5
                class="mb-2 text-lg font-semibold text-neutral-900 dark:text-neutral-100"
            >
                Notification Settings
            </h5>
            <p class="text-sm text-neutral-600 dark:text-neutral-400 mb-6 pb-4 border-b border-neutral-200 dark:border-neutral-700">Choose what updates you want to receive via email</p>
            <form
                class="flex flex-col space-y-5 transition-opacity duration-200"
                class:opacity-50={updatingSettings}
                onsubmit={(e) => {
                    e.preventDefault();
                }}
            >
                {#if !settingsLoading && notificationSettings}
                    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                        <Label for="daily-report" class="mb-0 cursor-pointer flex-1">
                            <span
                                class="block text-base font-medium text-neutral-900 dark:text-neutral-100 mb-1"
                                >Daily Portfolio Report</span
                            >
                            <p class="text-sm text-neutral-600 dark:text-neutral-400">
                                Receive a daily summary of your portfolio
                                performance.
                            </p>
                        </Label>
                        <div class="flex-shrink-0">
                            <Toggle
                                id="daily-report"
                                bind:checked={
                                    notificationSettings.daily_report_enabled
                                }
                                disabled={updatingSettings}
                                onclick={() => setTimeout(handleToggleChange, 0)}
                                class={updatingSettings ? "opacity-60 cursor-not-allowed" : ""}
                            />
                        </div>
                    </div>

                    <div
                        class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 pt-4 border-t border-neutral-200 dark:border-neutral-700"
                    >
                        <Label for="price-alerts" class="mb-0 cursor-pointer flex-1">
                            <span
                                class="block text-base font-medium text-neutral-900 dark:text-neutral-100 mb-1"
                                >Price Alerts</span
                            >
                            <p class="text-sm text-neutral-600 dark:text-neutral-400">
                                Get notified when assets hit your target price.
                            </p>
                        </Label>
                        <div class="flex-shrink-0">
                            <Toggle
                                id="price-alerts"
                                bind:checked={
                                    notificationSettings.price_alert_enabled
                                }
                                disabled={updatingSettings}
                                onclick={() => setTimeout(handleToggleChange, 0)}
                                class={updatingSettings ? "opacity-60 cursor-not-allowed" : ""}
                            />
                        </div>
                    </div>
                {:else if settingsLoading}
                    <div class="space-y-4 py-2">
                        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4">
                            <div class="space-y-2 flex-1">
                                <Skeleton class="h-5 w-1/2" />
                                <Skeleton class="h-3 w-full" />
                                <Skeleton class="h-3 w-4/5" />
                            </div>
                            <Skeleton class="h-6 w-12 rounded-full flex-shrink-0" />
                        </div>
                        <div
                            class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-4 pt-4 border-t border-neutral-200 dark:border-neutral-700"
                        >
                            <div class="space-y-2 flex-1">
                                <Skeleton class="h-5 w-1/3" />
                                <Skeleton class="h-3 w-full" />
                                <Skeleton class="h-3 w-3/4" />
                            </div>
                            <Skeleton class="h-6 w-12 rounded-full flex-shrink-0" />
                        </div>
                    </div>
                {/if}

                {#if notificationMessage}
                    <Alert
                        color={notificationError ? "red" : "green"}
                        class="mt-4 flex items-center gap-2 font-medium"
                    >
                        <span>{notificationError ? "⚠️" : "✓"}</span>
                        {notificationMessage}
                    </Alert>
                {/if}
            </form>
        </Card>
    </div>
</div>
