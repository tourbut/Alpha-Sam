import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import SettingsPage from './+page.svelte';
import * as api from '$lib/api';
import { auth } from '$lib/stores/auth';

// Mock $lib/api
vi.mock('$lib/api', async () => {
    const actual = await vi.importActual('$lib/api');
    return {
        ...actual,
        getNotificationSettings: vi.fn(),
        updateNotificationSettings: vi.fn(),
        updateProfile: vi.fn(),
        changePassword: vi.fn()
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
        (api.getNotificationSettings as any).mockResolvedValue(mockSettings);
    });

    it('should load and display notification settings', async () => {
        render(SettingsPage);

        await waitFor(() => {
            expect(api.getNotificationSettings).toHaveBeenCalled();
        });

        const dailyToggle = screen.getByLabelText(/Daily Portfolio Report/i) as HTMLInputElement;
        const priceToggle = screen.getByLabelText(/Price Alerts/i) as HTMLInputElement;

        expect(dailyToggle.checked).toBe(true);
        expect(priceToggle.checked).toBe(false);
    });

    it('should call updateNotificationSettings when toggle is clicked', async () => {
        (api.updateNotificationSettings as any).mockResolvedValue({ ...mockSettings, price_alert_enabled: true });

        render(SettingsPage);

        // Wait for settings to load
        await waitFor(() => {
            expect(api.getNotificationSettings).toHaveBeenCalled();
        });

        // Toggle elements in Flowbite-Svelte are often nested.
        // We find the label and click its parent or the input inside.
        const priceToggleLabel = screen.getByText(/Price Alerts/i);
        const priceToggleContainer = priceToggleLabel.closest('label');
        const input = priceToggleContainer?.querySelector('input');

        if (input) {
            await fireEvent.click(input);

            await waitFor(() => {
                expect(api.updateNotificationSettings).toHaveBeenCalled();
            }, { timeout: 2000 });

            expect(screen.getByText(/Preferences updated automatically/i)).toBeTruthy();
        } else {
            throw new Error('Toggle input not found');
        }
    });
});
