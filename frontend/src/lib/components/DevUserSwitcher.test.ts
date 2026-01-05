import { render, fireEvent, screen } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import DevUserSwitcher from './DevUserSwitcher.svelte';
import { devUser, DEV_USERS } from '$lib/stores/devUser';

// Mock $lib/stores/devUser
vi.mock('$lib/stores/devUser', () => {
    const { writable } = require('svelte/store');
    const store = writable({ id: 1, name: 'User 1 (Admin)', role: 'admin' });
    return {
        devUser: {
            ...store,
            switchUser: vi.fn()
        },
        DEV_USERS: [
            { id: 1, name: 'User 1 (Admin)', role: 'admin' },
            { id: 2, name: 'User 2 (Tester)', role: 'tester' }
        ]
    };
});

// Mock element.animate for JSDOM
// @ts-ignore
if (typeof Element !== 'undefined' && !Element.prototype.animate) {
    // @ts-ignore
    Element.prototype.animate = () => ({
        finished: Promise.resolve(),
        onfinish: null,
        cancel: () => { },
        play: () => { },
        pause: () => { },
        reverse: () => { },
    });
}

describe('DevUserSwitcher', () => {
    it('should render the current user name', () => {
        render(DevUserSwitcher);
        expect(screen.getByText('User 1 (Admin)')).toBeInTheDocument();
    });

    it('should open dropdown when clicked', async () => {
        render(DevUserSwitcher);
        const button = screen.getByRole('button');
        await fireEvent.click(button);
        expect(screen.getByText('Switch User')).toBeInTheDocument();
    });

    it('should call switchUser when a user is selected', async () => {
        render(DevUserSwitcher);
        const button = screen.getByRole('button');
        await fireEvent.click(button);

        const user2Button = screen.getByText('User 2 (Tester)');
        await fireEvent.click(user2Button);

        expect(devUser.switchUser).toHaveBeenCalledWith(2);
    });
});
