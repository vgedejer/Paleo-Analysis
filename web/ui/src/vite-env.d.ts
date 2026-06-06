/// <reference types="vite/client" />

// Typed access to our custom env vars via `import.meta.env.VITE_*`.
// Mirrors .env.example — keep them in sync.
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
