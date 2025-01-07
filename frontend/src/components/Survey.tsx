import { Card } from "@/components/ui/card"
import styles from "./Survey.module.css"
import { useState } from "react"
import { RatingScale } from "@/components/ui/RatingScale" // <— new import
// import { RatingScale } from "@/components/ui/RatingScale" // <— new import

interface SurveyProps {
  userName: string
}

export function Survey({ userName }: SurveyProps) {
  const [currentStep, setCurrentStep] = useState(1)
  const totalSteps = 3

  // Example numeric rating
  const [riskTolerance, setRiskTolerance] = useState<string>("")

  return (
    <Card className="p-6 max-w-xl mx-auto mt-20">
      <div className={styles.header}>
        <div className={styles.title}>Hi {userName},</div>
        <p className={styles.subtitle}>
          Congratulations on making the smart choice for your career &mdash; 
          you&apos;re on the path to success!
        </p>
        <p className={styles.subtitle}>
          While we&apos;re loading your information, 
          we have a few questions so we can get to know you a little better:
        </p>
      </div>

      <div className={styles.progressRow}>
        <div className={styles.stepInfo}>
          {currentStep}/{totalSteps}
        </div>
      </div>

      <div className={styles.questionRow}>
        <label className={styles.questionText}>
          I am willing to take risks to achieve my goals
        </label>
      </div>

      <div className="flex flex-col items-center gap-2">
        <span className="text-sm text-gray-500">Strongly Disagree</span>
        <RatingScale
          name="risk"
          value={riskTolerance}
          onChange={setRiskTolerance}
        />
        <span className="text-sm text-gray-500">Strongly Agree</span>
      </div>
    </Card>
  )
}
