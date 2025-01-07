import * as React from "react"
import { RadioGroup, RadioGroupItem } from "./RadioGroup"
import { cn } from "@/lib/utils"

interface RatingScaleProps {
  name?: string
  /** Array of numeric (or string) labels, e.g. [1,2,3,4,5] */
  scale?: (number | string)[]
  value?: string
  onChange?: (val: string) => void
  className?: string
}

/**
 * RatingScale is a higher-level component that takes a list of numbers/labels and
 * renders them horizontally. Good for quick 1–5 or 1–10 “agreement” scales.
 */
export function RatingScale({
  name,
  scale = [1, 2, 3, 4, 5],
  value,
  onChange,
  className,
}: RatingScaleProps) {
  return (
    <RadioGroup
      name={name}
      value={value}
      onValueChange={onChange}
      orientation="horizontal"
      className={cn("items-center justify-center gap-4", className)}
    >
      {scale.map((item) => (
        <label
          key={item}
          className="flex cursor-pointer flex-col items-center gap-1 text-sm"
        >
          <RadioGroupItem value={String(item)} />
          <span>{item}</span>
        </label>
      ))}
    </RadioGroup>
  )
}
