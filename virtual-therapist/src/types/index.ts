export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'therapist';
  timestamp: Date;
  sentiment?: SentimentAnalysis;
}

export interface SentimentAnalysis {
  score: number; // -1 to 1 (negative to positive)
  label: string; // 'positive', 'negative', 'neutral'
  emotions: EmotionAnalysis[];
  intensity: number; // 0 to 1
}

export interface EmotionAnalysis {
  emotion: string;
  confidence: number;
}

export interface MoodEntry {
  id: string;
  date: Date;
  mood: number; // 1-10 scale
  notes: string;
  sentiment: SentimentAnalysis;
}

export interface TherapeuticResponse {
  message: string;
  technique: string;
  suggestions: string[];
}

export interface UserSession {
  id: string;
  startTime: Date;
  messages: Message[];
  moodEntries: MoodEntry[];
  sentimentHistory: SentimentAnalysis[];
}