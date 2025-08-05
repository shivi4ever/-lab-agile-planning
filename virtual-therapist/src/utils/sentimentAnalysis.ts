import Sentiment from 'sentiment';
import { SentimentAnalysis, EmotionAnalysis } from '@/types';

const sentiment = new Sentiment();

// Emotion keywords mapping
const emotionKeywords = {
  happy: ['happy', 'joy', 'excited', 'elated', 'cheerful', 'delighted', 'pleased', 'glad', 'euphoric', 'blissful'],
  sad: ['sad', 'depressed', 'down', 'blue', 'melancholy', 'gloomy', 'dejected', 'despondent', 'sorrowful', 'grief'],
  anxious: ['anxious', 'worried', 'nervous', 'stressed', 'panic', 'fear', 'scared', 'terrified', 'apprehensive', 'uneasy'],
  angry: ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated', 'livid', 'enraged', 'hostile'],
  hopeless: ['hopeless', 'despair', 'helpless', 'worthless', 'defeated', 'lost', 'trapped', 'overwhelmed', 'powerless'],
  grateful: ['grateful', 'thankful', 'blessed', 'appreciative', 'fortunate', 'lucky'],
  lonely: ['lonely', 'isolated', 'alone', 'abandoned', 'disconnected', 'solitary'],
  confident: ['confident', 'strong', 'capable', 'empowered', 'self-assured', 'determined'],
  confused: ['confused', 'lost', 'uncertain', 'unclear', 'bewildered', 'puzzled'],
  peaceful: ['peaceful', 'calm', 'serene', 'tranquil', 'relaxed', 'content']
};

export function analyzeSentiment(text: string): SentimentAnalysis {
  const result = sentiment.analyze(text);
  const normalizedScore = Math.max(-1, Math.min(1, result.score / 10)); // Normalize to -1 to 1
  
  let label = 'neutral';
  if (normalizedScore > 0.1) label = 'positive';
  else if (normalizedScore < -0.1) label = 'negative';
  
  const emotions = detectEmotions(text.toLowerCase());
  const intensity = Math.abs(normalizedScore);
  
  return {
    score: normalizedScore,
    label,
    emotions,
    intensity
  };
}

function detectEmotions(text: string): EmotionAnalysis[] {
  const detectedEmotions: EmotionAnalysis[] = [];
  
  Object.entries(emotionKeywords).forEach(([emotion, keywords]) => {
    const matches = keywords.filter(keyword => text.includes(keyword));
    if (matches.length > 0) {
      const confidence = Math.min(1, matches.length / keywords.length * 2);
      detectedEmotions.push({
        emotion,
        confidence
      });
    }
  });
  
  // Sort by confidence and return top 3
  return detectedEmotions
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, 3);
}

export function getSentimentColor(sentiment: SentimentAnalysis): string {
  if (sentiment.score > 0.3) return 'text-green-600';
  if (sentiment.score < -0.3) return 'text-red-600';
  return 'text-yellow-600';
}

export function getSentimentEmoji(sentiment: SentimentAnalysis): string {
  if (sentiment.score > 0.5) return '😊';
  if (sentiment.score > 0.2) return '🙂';
  if (sentiment.score > -0.2) return '😐';
  if (sentiment.score > -0.5) return '😔';
  return '😢';
}