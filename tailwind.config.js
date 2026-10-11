/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        extend: {
            colors: {
                rail: {
                    blue: '#0a2a5d',
                    navy: '#071b3d',
                    sky: '#eaf3ff',
                    orange: '#ff7a1a',
                    soft: '#f3f8ff',
                }
            },
            boxShadow: {
                soft: '0 20px 60px rgba(11, 46, 97, 0.12)',
            }
        }
    },
    plugins: [],
};