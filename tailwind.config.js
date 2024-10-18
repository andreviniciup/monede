/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',  // Adicione isso para suportar arquivos Python com tags de template Django
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
