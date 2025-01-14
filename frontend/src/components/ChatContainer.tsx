import React, { useState, useRef, useEffect } from 'react'
import { InputArea } from "@/components/ui/InputArea"
import { Card } from "@/components/ui/Card"
import { ChatBubble } from "@/components/ui/ChatBubble"
import { SendButton } from "@/components/ui/SendButton"
import styles from './ChatContainer.module.css'

interface Message {
  id: string
  content: string
  sender: 'user' | 'system'
  timestamp: Date
}

const defaultMessages: Message[] = [
  {
    id: '1',
    content: 'Hi John, what was the highlight of your week?',
    sender: 'system',
    timestamp: new Date()
  }
]

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(defaultMessages)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // The sentinel <div> at the bottom of the messages
  const bottomRef = useRef<HTMLDivElement>(null)

  // Whenever we update messages, scroll the sentinel into view
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate sending message to server
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await response.json()

      // Add system message
      const systemMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        sender: 'system',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, systemMessage])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className={styles.chatContainer} data-testid="chat-container">
      {/* Our scrollable messages area */}
      <div className={styles.messagesArea}>
        {messages.map((message) => (
          <ChatBubble
            key={message.id}
            content={message.content}
            variant={message.sender}
          />
        ))}

        {/* Sentinel that we scroll to when new messages come in */}
        <div ref={bottomRef}></div>
      </div>

      {/* Fixed input area at bottom of the card */}
      <div className={styles.inputArea}>
        <form onSubmit={handleSend} className={styles.inputContainer}>
        <InputArea
          onChange={(e) => setInput(e.target.value)}
          value={input}
          placeholder="Type a message..."
          disabled={isLoading}
        />
          <SendButton 
            size="lg"
            disabled={false}
          />
        </form>
      </div>
    </Card>
  )
}

export default ChatContainer
