import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

export default defineConfig({
    plugins: [
        svelte({ hot: false }),
    ],
    resolve: {
        conditions: ['browser']
    },
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}'],
        environment: 'jsdom',
        globals: true,
        setupFiles: ['./vitest-setup.ts'],
        alias: {
            '$lib': path.resolve('./src/lib'),
            '$app/environment': path.resolve('./src/lib/mocks/app-environment.ts'),
            '$app': path.resolve('./.svelte-kit/runtime/app'),
        }
    }
});
