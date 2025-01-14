import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/e2e',       // Directory where your E2E tests live
  timeout: 30_000,           // 30 seconds per test
  use: {
    headless: true,          // Run in headless mode; set false if you want a visible browser
    baseURL: 'http://localhost:5173', 
    // ^ If your front-end dev server is on port 5173 (Vite default) or 3000 (CRA), adjust accordingly
  },
});
