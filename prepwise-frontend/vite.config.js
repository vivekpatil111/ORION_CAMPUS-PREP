import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5000,        // 👈 YAHI PORT FIX HAI
    strictPort: true,  // 👈 agar 5000 busy hua to start hi nahi hoga
    host: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
});
