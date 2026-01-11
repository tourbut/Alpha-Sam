import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import SettingsPage from './+page.svelte';
import * as usersApi from '$lib/apis/users';
import { auth } from '$lib/stores/auth.svelte';

// Mock $lib/apis/users
vi.mock('$lib/apis/users', async () => {
    const actual = await vi.importActual('$lib/apis/users');
    return {
        ...actual,
        get_notification_settings: vi.fn(),
        update_notification_settings: vi.fn(),
        update_me: vi.fn(),
        change_password: vi.fn()
    };
});

// Mock $lib/stores/auth
vi.mock('$lib/stores/auth', () => {
    const { writable } = require('svelte/store');
    return {
        auth: {
            subscribe: writable({ user: { email: 'test@example.com', nickname: 'Tester' } }).subscribe,
            updateUser: vi.fn()
        }
    };
});

describe('Settings Page', () => {
    const mockSettings = {
        user_id: 1,
        daily_report_enabled: true,
        price_alert_enabled: false
    };

    beforeEach(() => {
        vi.clearAllMocks();
        (usersApi.get_notification_settings as any).mockResolvedValue(mockSettings);
    });

    it('should load and display notification settings', async () => {
        render(SettingsPage);

        await waitFor(() => {
            expect(usersApi.get_notification_settings).toHaveBeenCalled();
        });

        const dailyToggle = screen.getByLabelText(/Daily Portfolio Report/i) as HTMLInputElement;
        const priceToggle = screen.getByLabelText(/Price Alerts/i) as HTMLInputElement;

        expect(dailyToggle.checked).toBe(true);
        expect(priceToggle.checked).toBe(false);
    });

    it('should call updateNotificationSettings when toggle is clicked', async () => {
        vi.useFakeTimers();
        (usersApi.update_notification_settings as any).mockResolvedValue({ ...mockSettings, price_alert_enabled: true });

        render(SettingsPage);

        // Wait for settings to load
        await waitFor(() => {
            expect(usersApi.get_notification_settings).toHaveBeenCalled();
        });

        const input = screen.getByLabelText(/Price Alerts/i);

        await fireEvent.click(input);

        // Fast-forward time for setTimeout(..., 0)
        vi.runAllTimers();

        await waitFor(() => {
            expect(usersApi.update_notification_settings).toHaveBeenCalled();
        });

        expect(screen.getByText(/Preferences updated automatically/i)).toBeTruthy();
        vi.useRealTimers();
    });
});
