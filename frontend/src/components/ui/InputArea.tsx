import * as React from "react"
import { cn } from "@/lib/utils"
import styles from './InputArea.module.css'
import TextareaAutosize from 'react-textarea-autosize'


const InputArea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => {

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        // Submit logic
      }
    }
  
    return (
      <TextareaAutosize
        placeholder="Type a message..."
        onKeyDown={handleKeyDown}
        minRows={1}
        maxRows={10}
        style={{
          width: '100%',
          boxSizing: 'border-box',
          resize: 'none',
        }}
        className={cn(styles.input, className)}
      />
    )
  }
)
InputArea.displayName = "InputArea"

export { InputArea }
