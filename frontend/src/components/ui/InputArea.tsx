import * as React from "react"
import { cn } from "@/lib/utils"
import styles from './InputArea.module.css'

const InputArea = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(styles.input, className)}
        ref={ref}
        {...props}
      />
    )
  }
)
InputArea.displayName = "Input"

export { InputArea }