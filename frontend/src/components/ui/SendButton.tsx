import React from 'react';
import { ArrowUp } from 'lucide-react';
import styles from './SendButton.module.css';

type ButtonSize = 'sm' | 'md' | 'lg';

interface SendButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: ButtonSize;
}

const SendButton: React.FC<SendButtonProps> = ({
  onClick,
  size = 'md',
  disabled = false,
  ...props
}) => {
  // Apply both the base sendButton class and size variant
  const classNames = `${styles.sendButton} ${styles[size]}`;

  return (
    <button
      className={classNames}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {/* Lucide-React up arrow icon */}
      <ArrowUp className={styles.icon} />
    </button>
  );
};

export {SendButton};
