import { SentimentAnalysis, TherapeuticResponse } from '@/types';

interface ResponseTemplate {
  condition: (sentiment: SentimentAnalysis, text: string) => boolean;
  responses: string[];
  technique: string;
  suggestions: string[];
}

const responseTemplates: ResponseTemplate[] = [
  // Anxious/Worried responses
  {
    condition: (sentiment, text) => 
      sentiment.emotions.some(e => e.emotion === 'anxious') || 
      text.includes('worried') || text.includes('anxiety'),
    responses: [
      "I can hear that you're feeling anxious right now. That's completely understandable, and you're not alone in feeling this way.",
      "Anxiety can feel overwhelming, but remember that these feelings are temporary and manageable.",
      "It sounds like you're experiencing some worry. Let's work through this together."
    ],
    technique: "Anxiety Management",
    suggestions: [
      "Try the 4-7-8 breathing technique: Inhale for 4, hold for 7, exhale for 8",
      "Practice grounding: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
      "Challenge anxious thoughts: Ask yourself 'Is this thought realistic? What evidence do I have?'",
      "Consider writing down your worries to externalize them"
    ]
  },
  
  // Sad/Depressed responses
  {
    condition: (sentiment, text) => 
      sentiment.emotions.some(e => e.emotion === 'sad') || 
      sentiment.score < -0.4,
    responses: [
      "I'm sorry you're going through a difficult time. Your feelings are valid, and it's okay to feel sad.",
      "It takes courage to share these feelings. You've taken an important step by reaching out.",
      "Depression can make everything feel heavy, but you don't have to carry this burden alone."
    ],
    technique: "Cognitive Behavioral Therapy",
    suggestions: [
      "Try to identify one small activity that usually brings you joy, even if it doesn't feel appealing right now",
      "Practice self-compassion: Speak to yourself as you would to a good friend",
      "Consider keeping a mood journal to track patterns and triggers",
      "Engage in gentle physical activity, even just a short walk"
    ]
  },
  
  // Angry/Frustrated responses
  {
    condition: (sentiment, text) => 
      sentiment.emotions.some(e => e.emotion === 'angry'),
    responses: [
      "I can sense your frustration. Anger is a normal emotion, and it's okay to feel this way.",
      "It sounds like something really important to you has been affected. Let's explore this together.",
      "Your anger is telling us something important. Let's understand what's underneath it."
    ],
    technique: "Anger Management",
    suggestions: [
      "Take slow, deep breaths to activate your body's relaxation response",
      "Try the STOP technique: Stop, Take a breath, Observe your feelings, Proceed mindfully",
      "Express your feelings through writing or physical exercise",
      "Identify the underlying need or value that's been threatened"
    ]
  },
  
  // Hopeless responses
  {
    condition: (sentiment, text) => 
      sentiment.emotions.some(e => e.emotion === 'hopeless') ||
      text.includes('hopeless') || text.includes('give up'),
    responses: [
      "I hear how hopeless you're feeling right now. These feelings are real, but they don't define your future.",
      "When everything feels dark, it's hard to see any light. But you've reached out today, and that shows incredible strength.",
      "Hopelessness can feel all-consuming, but it's a feeling, not a fact. Let's work together to find some small steps forward."
    ],
    technique: "Hope Restoration",
    suggestions: [
      "Focus on just the next hour or day, rather than the overwhelming big picture",
      "Recall a time when you overcame a challenge - what strengths did you use?",
      "Consider reaching out to a trusted friend, family member, or mental health professional",
      "Practice gratitude for one small thing, even if it feels difficult"
    ]
  },
  
  // Positive/Happy responses
  {
    condition: (sentiment, text) => 
      sentiment.score > 0.3 || sentiment.emotions.some(e => e.emotion === 'happy'),
    responses: [
      "It's wonderful to hear some positivity in your message! These moments of joy are important to acknowledge.",
      "I'm glad you're experiencing some happiness. How does it feel to share this positive moment?",
      "Your positive energy comes through clearly. These feelings are just as valid and important as the difficult ones."
    ],
    technique: "Positive Psychology",
    suggestions: [
      "Take a moment to savor this positive feeling - really notice how it feels in your body",
      "Consider what contributed to this positive moment - can you recreate similar conditions?",
      "Share this positive experience with someone you care about",
      "Write about this moment in a gratitude journal"
    ]
  },
  
  // Confused/Uncertain responses
  {
    condition: (sentiment, text) => 
      sentiment.emotions.some(e => e.emotion === 'confused') ||
      text.includes('don\'t know') || text.includes('confused'),
    responses: [
      "It's completely normal to feel confused or uncertain. Life can be complex, and clarity often comes gradually.",
      "Confusion can be uncomfortable, but it's often a sign that you're processing something important.",
      "Not knowing what to do next is a very human experience. Let's explore this uncertainty together."
    ],
    technique: "Mindful Exploration",
    suggestions: [
      "Try writing down all your thoughts without judgment - sometimes clarity emerges from the process",
      "Break down the situation into smaller, more manageable parts",
      "Consider what your values are telling you about this situation",
      "Talk through your thoughts with someone you trust"
    ]
  },
  
  // Default empathetic response
  {
    condition: () => true,
    responses: [
      "Thank you for sharing your thoughts with me. I'm here to listen and support you.",
      "I appreciate you opening up. Your feelings and experiences matter.",
      "It takes courage to express your inner thoughts. How are you feeling right now?"
    ],
    technique: "Active Listening",
    suggestions: [
      "Take a few deep breaths and notice how you're feeling in this moment",
      "Consider what you need most right now - rest, connection, or perhaps some gentle activity",
      "Remember that seeking support is a sign of strength, not weakness",
      "Be patient and compassionate with yourself as you navigate your feelings"
    ]
  }
];

export function generateTherapeuticResponse(sentiment: SentimentAnalysis, userMessage: string): TherapeuticResponse {
  // Find the first matching template
  const template = responseTemplates.find(t => t.condition(sentiment, userMessage.toLowerCase()));
  
  if (!template) {
    // Fallback to default
    const defaultTemplate = responseTemplates[responseTemplates.length - 1];
    return {
      message: defaultTemplate.responses[Math.floor(Math.random() * defaultTemplate.responses.length)],
      technique: defaultTemplate.technique,
      suggestions: defaultTemplate.suggestions
    };
  }
  
  return {
    message: template.responses[Math.floor(Math.random() * template.responses.length)],
    technique: template.technique,
    suggestions: template.suggestions
  };
}

export const dailyAffirmations = [
  "You are worthy of love and respect, exactly as you are.",
  "Every day is a new opportunity to grow and learn.",
  "Your feelings are valid, and it's okay to experience them fully.",
  "You have overcome challenges before, and you have the strength to do it again.",
  "Progress, not perfection, is what matters.",
  "You deserve compassion, especially from yourself.",
  "Your mental health journey is unique and valid.",
  "Small steps forward are still steps forward.",
  "You are not alone in your struggles.",
  "Your vulnerability is a sign of courage, not weakness."
];

export function getDailyAffirmation(): string {
  const today = new Date().getDate();
  return dailyAffirmations[today % dailyAffirmations.length];
}