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
        // Landing-page palette — the dark "natural history archive" theme from
        // the Figma mockup. Namespaced under `paleo` so it never collides with
        // the light `fossil` palette (app views) or Tailwind's built-in `amber`.
        paleo: {
          bg: "#16130f", // deep shale ground
          panel: "#1b1710", // card / section surface
          panel2: "#211c14", // raised surface
          line: "#38301f", // hairline borders
          cream: "#e2d5b8", // primary text
          dim: "#9a8f74", // muted labels / captions
          accent: "#c17f3a", // amber accent
          // Period-specific accents used for era tags & the timeline bar.
          triassic: "#c8763c",
          jurassic: "#6fa08b",
          cretaceous: "#c9a24a",
          // Diet color-coding on specimen cards.
          carnivore: "#c17f3a",
          herbivore: "#7ba05b",
          piscivore: "#5f8fa8",
        },
      },
      fontFamily: {
        // Display faces loaded in index.html. `mono` is intentionally overridden
        // to Space Mono — the app doesn't use the default mono stack anywhere.
        cinzel: ['"Cinzel"', "serif"],
        crimson: ['"Crimson Pro"', "Georgia", "serif"],
        mono: ['"Space Mono"', "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
