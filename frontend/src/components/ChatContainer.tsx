import styles from './ChatContainer.module.css';
import React, { useState } from 'react';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"

interface Message {
    id: string;
    content: string;
    sender: 'user' | 'bot';
}

const ChatContainer = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = {
            id: Date.now().toString(),
            content: input,
            sender: 'user' as const
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            });

            const data = await response.json();
            const botMessage = {
                id: (Date.now() + 1).toString(),
                content: data.response,
                sender: 'bot' as const
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <Card className={styles.container}>
            <ScrollArea className={styles.scrollArea}>
                {messages.map((message) => (
                    <div key={message.id} className={`${styles.message} ${message.sender === 'user' ? styles.userMessage : styles.botMessage}`}>
                        <Card className={message.sender === 'user' ? 'bg-primary' : 'bg-muted'}>
                            <CardContent className="p-3">{message.content}</CardContent>
                        </Card>
                    </div>
                ))}
            </ScrollArea>
            <form onSubmit={handleSend} className={styles.inputForm}>
                <div className={styles.inputContainer}>
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                    />
                    <Button type="submit">Send</Button>
                </div>
            </form>
        </Card>
    );
};

export default ChatContainer;