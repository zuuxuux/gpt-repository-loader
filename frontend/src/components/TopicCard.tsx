import React from "react";
import { ThumbsUp, ThumbsDown } from "lucide-react";
import styles from './TopicCard.module.css';

export interface Metric {
  label: string;
  value: number;
}

export interface TopicData {
  title: string;
  metrics: Metric[];
}

interface TopicCardProps {
  topic: TopicData;
  onThumbsUp?: () => void;
  onThumbsDown?: () => void;
}

interface ProgressBarProps {
  label: string;
  value: number;
  color: string;
}

const METRIC_COLORS = [
  'rgb(168 85 247)',  // Purple
  'rgb(59 130 246)',  // Blue
  'rgb(251 191 36)'   // Amber
];

const ProgressBar: React.FC<ProgressBarProps> = ({ label, value, color }) => {
  const toPercent = (val: number): string => `${Math.min(Math.max(val, 0), 100)}%`;

  return (
    <div className={styles.progressContainer}>
      <p className={styles.progressLabel}>{label}:</p>
      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ 
            width: toPercent(value),
            backgroundColor: color
          }}
        />
      </div>
    </div>
  );
};

const MetricsSection: React.FC<{ metrics: Metric[] }> = ({ metrics }) => (
  <div className={styles.metricsContainer}>
    {metrics.map((metric, index) => (
      <ProgressBar
        key={metric.label}
        label={metric.label}
        value={metric.value}
        color={METRIC_COLORS[index % METRIC_COLORS.length]}
      />
    ))}
  </div>
);

const TopicCard: React.FC<TopicCardProps> = ({ 
  topic,
  onThumbsUp,
  onThumbsDown
}) => {
  return (
    <div className={styles.cardContainer}>
      <div className={styles.card}>
        <h3 className={styles.title}>{topic.title}</h3>
        <div className={styles.dividerContainer}>
          <div className={styles.divider}></div>
          <div className={styles.thumbContainer}>
            <button onClick={onThumbsUp} className={styles.thumbButton}>
              <ThumbsUp size={20} />
            </button>
            <button onClick={onThumbsDown} className={styles.thumbButton}>
              <ThumbsDown size={20} />
            </button>
          </div>
        </div>
        <MetricsSection metrics={topic.metrics} />
      </div>
    </div>
  );
};

export default TopicCard;