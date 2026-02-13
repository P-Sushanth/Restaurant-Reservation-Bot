/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#d97706", // amber-600
                secondary: "#92400e", // amber-800
            }
        },
    },
    plugins: [],
}
