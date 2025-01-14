import { test, expect } from '@playwright/test';

test('chat flow: default message + sending user message', async ({ page }) => {
      // Listen for console events from the browser
    page.on('console', (msg) => {
        console.log(`Browser console: ${msg.type()}: ${msg.text()}`);
    });
    // 1) Go to the home/chat page (baseURL is set in your playwright.config.ts)
    await page.goto('/');
    console.log('page.url()', page.url());  
    // 2) Verify the default message is present
    const defaultMessage = page.locator('[data-testid="default-message"]');
    await expect(defaultMessage).toBeVisible();
    await expect(defaultMessage).toHaveText('Hi John, what was the highlight of your week?');

    // 3) Type a new message in the chat input
    const input = page.locator('[data-testid="chat-input"]');
    await input.fill('This is a new message');

    // 4) Click the send button
    const sendButton = page.locator('[data-testid="send-button"]');

    console.log('sendButton:', sendButton);
    await sendButton.click();

    // 5) Check that the newly sent message appears
    //    Here, we assume each message bubble has data-testid="chat-bubble"
    const allBubbles = page.locator('[data-testid="chat-bubble"]');
    await expect(allBubbles.last()).toHaveText('This is a new message');
});
