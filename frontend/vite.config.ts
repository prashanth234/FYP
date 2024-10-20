import { defineConfig, splitVendorChunkPlugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    splitVendorChunkPlugin()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      // '/static': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000',
      '/graphql': 'http://127.0.0.1:8000'
    }
  },
  test: {
    globals: true,
    environment: 'jsdom'
  }
})
