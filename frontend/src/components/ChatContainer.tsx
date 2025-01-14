import React, { useState, useEffect, useRef } from 'react'
import { InputArea } from "@/components/ui/InputArea"
import { Card } from "@/components/ui/Card"
import { ChatBubble } from "@/components/ui/ChatBubble"
import { SendButton } from "@/components/ui/SendButton"
import styles from './ChatContainer.module.css'

// Import your new utils & types
import { getChatMessages } from '@/lib/utils'
import { ChatMessage, Chat } from '@/lib/types'

interface ChatContainerProps {
  chat: Chat | null; // We'll pass in the chat object from the parent (e.g., App.tsx)
}

const ChatContainer: React.FC<ChatContainerProps> = ({ chat }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const bottomRef = useRef<HTMLDivElement>(null)

  // On mount or when chat changes, load the messages
  useEffect(() => {

    async function loadMessages() {
      try {
        if (!chat) return;
        const chatMessages = await getChatMessages(chat.chat_id)
        setMessages(chatMessages)
      } catch (error) {
        console.error('Error loading chat messages:', error)
      }
    }

    loadMessages()
  }, [chat])

  // Scroll to bottom when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !chat || isLoading) return

    // TODO: In a later step, we will call the POST /api/chats/:chat_id/messages endpoint
    // to add this new message and fetch the result. For now, we can just log or stub it out.

    console.log('Sending message:', input)
    setInput('')

    // We'll handle sending to the server in a future commit
  }

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
        {/* Sentinel for scrolling */}
        <div ref={bottomRef}></div>
      </div>

      {/* Input area */}
      <div className={styles.inputArea}>
        <form onSubmit={handleSend} className={styles.inputContainer}>
          <InputArea
            onChange={(e) => setInput(e.target.value)}
            value={input}
            placeholder="Type a message..."
            disabled={isLoading || !chat}
            data-testid="chat-input"
          />
          <SendButton
            size="lg"
            disabled={!chat}
          />
        </form>
      </div>
    </Card>
  )
}

export default ChatContainer
