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

test('chat flow: user sends a message and sees assistant response', async ({ page }) => {
    // 1) Go to the home page
    await page.goto('/');
  
    // 2) Wait for the user and chat to be initialized (e.g. "Logged in as John Doe" text)
    // Adjust the exact text as your UI displays. This ensures user creation is done.
    await expect(page.getByText(/Logged in as/i)).toBeVisible();
    await expect(page.getByText(/Chat ID:/i)).toBeVisible();
  
    // 3) Verify the chat container is present
    const chatContainer = page.locator('[data-testid="chat-container"]');
    await expect(chatContainer).toBeVisible();
  
    // 4) Fill in a new message in the chat input
    const input = page.locator('[data-testid="chat-input"]');
    await input.fill('Hello, from Playwright!');
  
    // 5) Click send
    const sendButton = page.locator('[data-testid="send-button"]');
    await sendButton.click();
  
    // 6) The user’s message should appear as the last chat bubble
    const chatBubbles = page.locator('[data-testid="chat-bubble"]');
    await expect(chatBubbles.last()).toHaveText('Hello, from Playwright!');
  
    // 7) Wait for the assistant’s response. The backend inserts it automatically.
    //    We assume it’s appended after the user’s bubble, so we wait for the count to increase by at least 2 from the time of sending.
    //    Or we can specifically wait for a new message that is not the user’s text.
    //    Here's a simple approach: wait for the text "Responding to: Hello, from Playwright!"
    //    because DummyProvider returns "Responding to: <input_message>"
    await expect(
      page.locator('[data-testid="chat-bubble"]', { hasText: 'Responding to: Hello, from Playwright!' })
    ).toBeVisible();
  
    // Optional: further validations, e.g. check that there's now an additional bubble
    // or that the text specifically matches "Responding to: Hello, from Playwright!"
  });
