// src/components/ui/ChatBubble.tsx
import React from 'react';
import styles from './ChatBubble.module.css';

interface ChatBubbleProps {
  content: string;
  variant: 'system' | 'user';
  className?: string;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ 
  content, 
  variant,
  className = '' 
}) => {
  return (
    <div className={`${styles.message} ${styles[variant]} ${className}`}>
      <div className={styles.gradientBorder}>
        <div className={styles.messageContent}>
          {content}
        </div>
      </div>
    </div>
  );
};

export default ChatBubble;