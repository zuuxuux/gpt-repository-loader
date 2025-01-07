import * as React from "react"
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group"
import { cn } from "@/lib/utils"

/**
 * RadioGroup is the root wrapper, analogous to a <form> for radio buttons.
 * - `orientation="vertical" | "horizontal"` from Radix UI
 * - `value` holds the currently-selected value
 * - `onValueChange` is your change handler
 */
const RadioGroup = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Root>
>(({ className, children, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Root
      ref={ref}
      className={cn("flex gap-2", className)}
      {...props}
    >
      {children}
    </RadioGroupPrimitive.Root>
  )
})
RadioGroup.displayName = "RadioGroup"

/**
 * RadioGroupItem is each individual radio “button.”
 * - `value` is the unique key for that radio
 */
const RadioGroupItem = React.forwardRef<
  React.ElementRef<typeof RadioGroupPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Item>
>(({ className, children, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Item
      ref={ref}
      className={cn(
        // Tailwind or your own classes:
        "relative flex h-5 w-5 items-center justify-center rounded-full border border-border bg-background text-foreground " +
          "data-[state=checked]:border-primary data-[state=checked]:bg-primary/20 " +
          "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 " +
          "disabled:pointer-events-none disabled:opacity-50",
        className
      )}
      {...props}
    >
      {/* The checked indicator inside the radio circle */}
      <RadioGroupPrimitive.Indicator
        className={cn(
          "flex h-2.5 w-2.5 items-center justify-center rounded-full bg-primary"
        )}
      />
      {children}
    </RadioGroupPrimitive.Item>
  )
})
RadioGroupItem.displayName = "RadioGroupItem"

export { RadioGroup, RadioGroupItem }
