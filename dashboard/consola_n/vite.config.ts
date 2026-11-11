import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";
import { viteSingleFile } from "vite-plugin-singlefile";

// Modo «pagina»: todo en un único index.html para publicarlo como página con enlace.
export default defineConfig(({ mode }) => ({
  plugins: mode === "pagina" ? [react(), viteSingleFile()] : [react()],
  resolve: { alias: { "@": path.resolve(__dirname, "src") } },
  build: { outDir: mode === "pagina" ? "dist-pagina" : "dist", chunkSizeWarningLimit: 3000 },
  test: { include: ["pruebas/unit/**/*.test.ts"], environment: "node" },
}));
