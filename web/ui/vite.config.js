import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        // Mirror the `@/*` alias from tsconfig.json so the bundler and the type
        // checker agree on what `@/features/genera` resolves to.
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        port: 5173,
        /**
         * DEV-ONLY PROXY.
         *
         * In development the React app runs on :5173 and FastAPI on :8000 — two
         * different origins, so the browser would block requests as cross-origin
         * (CORS). Instead of configuring CORS on the backend just for local dev,
         * we proxy: the browser talks only to :5173, and Vite forwards anything
         * starting with `/api` to the FastAPI server.
         *
         * Net effect: frontend code always fetches a same-origin relative URL
         * (`/api/v1/genera`), and this config decides where that physically goes.
         * In production you'd serve both behind one reverse proxy (nginx, etc.),
         * so the same relative URL keeps working with no code change.
         */
        proxy: {
            "/api": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
        },
    },
});
