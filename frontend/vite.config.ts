import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    // @ts-ignore - allow all hosts for preview
    allowedHosts: true as any,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    },
    hmr: {
      clientPort: 443,
    },
    cors: true,
    headers: {
      'X-Frame-Options': 'ALLOWALL'
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    // @ts-ignore
    allowedHosts: true as any,
    cors: true,
  }
})
