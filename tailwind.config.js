/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './*/index.html', './js/**/*.js', './scripts/**/*.py'],
  theme: {
    extend: {
      colors: {
        ocean: {
          50:  '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        pr: {
          50:  '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
        },
        sand: {
          50:  '#fefdf8',
          100: '#fdf8ed',
          200: '#faefd4',
        }
      },
      fontFamily: {
        display: ['Outfit', 'system-ui', 'sans-serif'],
        body:    ['Source Sans 3', 'system-ui', 'sans-serif'],
      },
    }
  },
  plugins: [],
};
