import { useState } from 'react';
import { InputArea } from "@/components/ui/InputArea"
import { Card } from "@/components/ui/Card"
import { ScrollArea } from "@/components/ui/ScrollArea"
import { ChatBubble } from "@/components/ui/ChatBubble"
import { SendButton } from "@/components/ui/SendButton";
import styles from './ChatContainer.module.css';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'system';
  timestamp: Date;
}

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      content: input,
      sender: 'user' as const,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      const systemMessage = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: 'system' as const,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, systemMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className={styles.container}>
      <ScrollArea className={styles.scrollArea}>
      {messages.map((message) => (
        <ChatBubble
          key={message.id}
          content={message.content}
          variant={message.sender}
        />
      ))}
      </ScrollArea>
      <div className={styles.inputArea}>
        <form onSubmit={handleSend} className={styles.inputContainer}>
          <InputArea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            disabled={isLoading}
          />
          <SendButton 
            onClick={() => console.log('Sending...')}
            size="lg"
            disabled={false}
          />
        </form>
      </div>
    </Card>
  );
};

export default ChatContainer;