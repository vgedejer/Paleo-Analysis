// PostCSS is the CSS build pipeline Tailwind plugs into. Vite runs this
// automatically. `tailwindcss` expands @tailwind directives; `autoprefixer`
// adds vendor prefixes (-webkit-, etc.) for browser compatibility.
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
