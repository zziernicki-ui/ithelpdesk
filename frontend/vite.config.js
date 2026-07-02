import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    // Emit the compiled site into the folder FastAPI will serve.
    outDir: "../static",
    emptyOutDir: true,
  },
  server: {
    // During local dev (npm run dev), forward API calls to the
    // FastAPI server so the same relative URLs work as in production.
    proxy: {
      "/search": "http://localhost:8000",
      "/health": "http://localhost:8000",
    },
  },
});
