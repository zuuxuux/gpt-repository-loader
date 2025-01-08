import * as React from "react"
import { cn } from "@/lib/utils"
import styles from "./InputArea.module.css"
import TextareaAutosize from "react-textarea-autosize"

type InputAreaProps = React.ComponentProps<typeof TextareaAutosize>

export const InputArea: React.FC<InputAreaProps> = ({ className, ...props }) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      e.currentTarget.form?.requestSubmit()
    }
  }

  return (
    <TextareaAutosize
      autoFocus
      onKeyDown={handleKeyDown}
      minRows={1}
      maxRows={10}
      className={cn(styles.input, className)}
      {...props}
    />
  )
}
