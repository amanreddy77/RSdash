/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Aura light theme — white + blacks
        stone: '#ffffff', // page background (white)
        cream: '#111111', // primary text (near black)
        warm: '#000000',  // primary accent/button (black)
        warmSoft: '#1f2933',
        accentSoft: '#e5e7eb',
      },
      fontFamily: {
        serif: ['var(--font-cormorant)', 'ui-serif', 'Georgia', 'serif'],
      },
      boxShadow: {
        'aura-card': '0 18px 40px rgba(15,23,42,0.20)',
      },
      borderRadius: {
        aura: '1.5rem',
      },
    },
  },
  plugins: [],
};
