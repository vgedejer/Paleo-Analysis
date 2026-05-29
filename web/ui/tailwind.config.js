/** @type {import('tailwindcss').Config} */
export default {
  // `content` tells Tailwind which files to scan for class names so it can
  // tree-shake unused styles out of the production CSS bundle. If a class
  // isn't found here at build time, it won't exist in the output.
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // A small domain palette so components reference `bg-fossil-700`
        // instead of magic hex strings scattered across the codebase.
        fossil: {
          50: "#f6f5f0",
          100: "#e8e4d8",
          700: "#5c5340",
          900: "#2e2a20",
        },
      },
    },
  },
  plugins: [],
};
