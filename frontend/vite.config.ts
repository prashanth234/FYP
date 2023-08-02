import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/static': 'http://localhost:8000',
      '/media': 'http://localhost:8000'
    }
  },
  test: {
    globals: true,
    environment: 'jsdom'
  }
})
