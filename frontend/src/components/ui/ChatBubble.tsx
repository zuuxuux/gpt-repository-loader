// src/components/ui/ChatBubble.tsx
import React from 'react';
import styles from './ChatBubble.module.css';

interface ChatBubbleProps {
  content: string;
  variant: 'system' | 'user';
  dataTestId: string;
  className?: string;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ 
  content, 
  variant,
  dataTestId,
  className = '' 
}) => {
  return (
    <div data-testid={dataTestId} className={`${styles.message} ${styles[variant]} ${className}`}>
      <div className={styles.chatBubbleBorder}>
        <div className={styles.messageContent}>
          {content}
        </div>
      </div>
    </div>
  );
};

export default ChatBubble;