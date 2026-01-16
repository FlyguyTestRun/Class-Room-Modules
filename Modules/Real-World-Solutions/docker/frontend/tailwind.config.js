/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        'zzz-blue': '#1e40af',
        'zzz-green': '#059669'
      }
    }
  },
  plugins: []
}
