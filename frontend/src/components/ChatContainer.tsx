// src/components/ChatContainer.tsx
import React, { useState, useEffect, useRef } from 'react';
import { InputArea } from '@/components/ui/InputArea';
import { Card } from '@/components/ui/Card';
import { ChatBubble } from '@/components/ui/ChatBubble';
import { SendButton } from '@/components/ui/SendButton';
import styles from './ChatContainer.module.css';

import { getChatMessages, sendChatMessage } from '@/lib/utils';
import { ChatMessage, Chat } from '@/lib/types';

interface ChatContainerProps {
    chat: Chat | null;   // We pass the chat from parent
    userId?: number;     // Optionally, we can pass userId from parent if we don’t store it in ChatContainer
}

const ChatContainer: React.FC<ChatContainerProps> = ({ chat, userId }) => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const bottomRef = useRef<HTMLDivElement>(null);

    // 1) Fetch existing messages when the chat becomes available
    useEffect(() => {

        async function loadMessages() {
            try {
                if (!chat) return;
                const chatMessages = await getChatMessages(chat.chat_id);
                setMessages(chatMessages);
            } catch (error) {
                console.error('Error loading chat messages:', error);
            }
        }

        loadMessages();
    }, [chat]);

    // 2) Scroll to the bottom of the chat whenever messages change
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // 3) Handle sending a new user message
    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !chat || !userId || isLoading) return;

        setIsLoading(true);

        try {
            // Send the user message to the backend
            const newMessages = await sendChatMessage(chat.chat_id, userId, input);
            // The response is an array of messages: user message + assistant message.

            // Merge these new messages into our local array
            setMessages((prev) => [...prev, ...newMessages]);

            // Clear input field
            setInput('');
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card className={styles.chatContainer} data-testid="chat-container">
            <div className={styles.messagesArea}>
                {messages.map((message) => (
                    <ChatBubble
                        key={message.message_id}
                        content={message.message_text}
                        variant={message.sender_type === 'user' ? 'user' : 'system'}
                        dataTestId={'chat-bubble'}
                    />
                ))}
                {/* Scroll sentinel */}
                <div ref={bottomRef}></div>
            </div>

            {/* Input area */}
            <div className={styles.inputArea}>
                <form onSubmit={handleSend} className={styles.inputContainer}>
                    <InputArea
                        onChange={(e) => setInput(e.target.value)}
                        value={input}
                        placeholder="Type a message..."
                        disabled={isLoading || !chat || !userId}
                        data-testid="chat-input"
                    />
                    <SendButton size="lg" disabled={!chat || !userId || isLoading} />
                </form>
            </div>
        </Card>
    );
};

export default ChatContainer;
