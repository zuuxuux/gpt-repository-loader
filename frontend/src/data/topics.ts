// src/data/topics.ts
import { TopicData } from '../components/TopicCard';

export const mockTopics: TopicData[] = [
  {
    title: "The Impact of Artificial Intelligence on Modern Healthcare",
    metrics: [
      { label: "Clarity", value: 85 },
      { label: "Impact", value: 95 },
      { label: "Innovation", value: 90 }
    ]
  },
  {
    title: "Sustainable Urban Development in Growing Cities",
    metrics: [
      { label: "Feasibility", value: 75 },
      { label: "Environmental Impact", value: 88 },
      { label: "Social Benefit", value: 92 }
    ]
  },
  {
    title: "The Future of Remote Work and Digital Collaboration",
    metrics: [
      { label: "Relevance", value: 95 },
      { label: "Practicality", value: 82 },
      { label: "Economic Impact", value: 78 }
    ]
  }
];