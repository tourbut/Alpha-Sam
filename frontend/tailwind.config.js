import flowbitePlugin from 'flowbite/plugin'

/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Trusted Professional Theme - Rich Cerulean Blue
                primary: {
                    50: '#D7E8F6',
                    100: '#AFD2ED',
                    200: '#86BBE4',
                    300: '#5EA5DB',
                    400: '#368ED1',
                    500: '#2774AE',
                    600: '#216191',
                    700: '#1A4D74',
                    800: '#143A57',
                    900: '#0D273A'
                },
                secondary: {
                    50: '#BCE5FF',
                    100: '#79CCFF',
                    200: '#36B2FF',
                    300: '#0095F1',
                    400: '#006BAE',
                    500: '#00416A',
                    600: '#003759',
                    700: '#002C47',
                    800: '#002136',
                    900: '#001624'
                },
                accent: {
                    50: '#E8F5E9',
                    100: '#C8E6C9',
                    200: '#A5D6A7',
                    300: '#81C784',
                    400: '#66BB6A',
                    500: '#2E8B57',
                    600: '#2E7D50',
                    700: '#27613D',
                    800: '#1B5E20',
                    900: '#0D3818'
                },
                neutral: {
                    50: '#F9FAFB',
                    100: '#F3F4F6',
                    200: '#E5E7EB',
                    300: '#D1D5DB',
                    400: '#9CA3AF',
                    500: '#6B7280',
                    600: '#4B5563',
                    700: '#374151',
                    800: '#1F2937',
                    900: '#111827'
                }
            },
            fontFamily: {
                sans: ['Montserrat', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                mono: ['Menlo', 'monospace']
            },
            spacing: {
                xs: '0.25rem',
                sm: '0.5rem',
                md: '1rem',
                lg: '1.5rem',
                xl: '2rem',
                '2xl': '3rem',
                '3xl': '4rem'
            }
        }
    },
    plugins: [flowbitePlugin]
};