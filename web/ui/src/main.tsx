import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { AppProviders } from "@/app/providers";
import App from "@/App";
import "@/index.css";

/**
 * The application entry point — the equivalent of your FastAPI `main.py`
 * composition root. It finds the `#root` div, creates a React root, and renders
 * the component tree into it. This is the ONE place we touch the real DOM
 * directly; everything else is declarative.
 *
 * <StrictMode> is a dev-only wrapper that intentionally double-invokes certain
 * functions (component bodies, effects) to surface impure code and missing
 * effect cleanups early. If something runs twice in development and breaks,
 * StrictMode is doing its job — it has no effect in production builds.
 */
const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Root element #root not found in index.html");

createRoot(rootElement).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>,
);
