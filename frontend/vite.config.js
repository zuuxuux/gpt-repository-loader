import { defineConfig } from 'vite'

export default defineConfig({
  envDir: '.',
  server: {
    watch: {
      usePolling: true
    }
  }
})