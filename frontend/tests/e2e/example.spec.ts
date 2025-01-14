import { test, expect } from '@playwright/test';

test('landing page loads and shows a welcome message', async ({ page }) => {
  // Navigate to the home page (using the baseURL in the config)
  await page.goto('/');

  // Check for some text or element on the landing page
  // e.g., a heading or a unique element ID
  const chatContainer = page.locator('[data-testid="chat-container"]');
    await expect(chatContainer).toBeVisible();

});
