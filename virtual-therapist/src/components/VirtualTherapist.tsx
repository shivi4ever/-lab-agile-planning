'use client';

import { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Send, Heart, Brain, BookOpen, TrendingUp } from 'lucide-react';
import { Message, SentimentAnalysis, UserSession } from '@/types';
import { analyzeSentiment, getSentimentColor, getSentimentEmoji } from '@/utils/sentimentAnalysis';
import { generateTherapeuticResponse, getDailyAffirmation } from '@/utils/therapeuticResponses';
import ChatMessage from './ChatMessage';
import SentimentMeter from './SentimentMeter';
import MoodJournal from './MoodJournal';
import SentimentTrends from './SentimentTrends';
import PrivacyNotice from './PrivacyNotice';

export default function VirtualTherapist() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentSentiment, setCurrentSentiment] = useState<SentimentAnalysis | null>(null);
  const [activeTab, setActiveTab] = useState<'chat' | 'journal' | 'trends'>('chat');
  const [session, setSession] = useState<UserSession>({
    id: uuidv4(),
    startTime: new Date(),
    messages: [],
    moodEntries: [],
    sentimentHistory: []
  });
  const [showPrivacyNotice, setShowPrivacyNotice] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    // Welcome message
    const welcomeMessage: Message = {
      id: uuidv4(),
      content: `Hello! I'm here to provide a safe, supportive space for you to express your thoughts and feelings. I'm an AI companion designed to offer empathetic responses and evidence-based coping strategies.

Today's affirmation: "${getDailyAffirmation()}"

How are you feeling today? Feel free to share whatever is on your mind.`,
      sender: 'therapist',
      timestamp: new Date()
    };
    
    setMessages([welcomeMessage]);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: uuidv4(),
      content: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    // Analyze sentiment
    const sentiment = analyzeSentiment(inputText);
    userMessage.sentiment = sentiment;
    setCurrentSentiment(sentiment);

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Generate therapeutic response
    setTimeout(() => {
      const therapeuticResponse = generateTherapeuticResponse(sentiment, inputText);
      
      const therapistMessage: Message = {
        id: uuidv4(),
        content: therapeuticResponse.message,
        sender: 'therapist',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, therapistMessage]);

      // Add suggestions as a follow-up message
      if (therapeuticResponse.suggestions.length > 0) {
        setTimeout(() => {
          const suggestionsMessage: Message = {
            id: uuidv4(),
            content: `Here are some ${therapeuticResponse.technique} techniques that might help:\n\n${therapeuticResponse.suggestions.map((s, i) => `${i + 1}. ${s}`).join('\n')}`,
            sender: 'therapist',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, suggestionsMessage]);
          setIsTyping(false);
        }, 1500);
      } else {
        setIsTyping(false);
      }
    }, 1000);

    // Update session
    setSession(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      sentimentHistory: [...prev.sentimentHistory, sentiment]
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (showPrivacyNotice) {
    return <PrivacyNotice onAccept={() => setShowPrivacyNotice(false)} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-sm rounded-t-2xl p-6 border-b border-blue-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Virtual Therapist</h1>
                <p className="text-gray-600">Your AI companion for mental wellness</p>
              </div>
            </div>
            
            {currentSentiment && (
              <div className="flex items-center space-x-2">
                <span className="text-2xl">{getSentimentEmoji(currentSentiment)}</span>
                <div className="text-right">
                  <div className={`font-medium ${getSentimentColor(currentSentiment)}`}>
                    {currentSentiment.label}
                  </div>
                  <div className="text-sm text-gray-500">
                    {currentSentiment.emotions[0]?.emotion || 'neutral'}
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Navigation Tabs */}
          <div className="flex space-x-1 mt-4">
            {[
              { id: 'chat', label: 'Chat', icon: Brain },
              { id: 'journal', label: 'Mood Journal', icon: BookOpen },
              { id: 'trends', label: 'Trends', icon: TrendingUp }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 hover:bg-blue-50'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white/80 backdrop-blur-sm rounded-b-2xl min-h-[600px] flex flex-col">
          {activeTab === 'chat' && (
            <>
              {/* Chat Messages */}
              <div className="flex-1 p-6 overflow-y-auto max-h-[500px]">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                  {isTyping && (
                    <div className="flex items-center space-x-2 text-gray-500">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <Heart className="w-4 h-4 text-white" />
                      </div>
                      <div className="bg-gray-100 rounded-2xl px-4 py-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              </div>

              {/* Sentiment Meter */}
              {currentSentiment && (
                <div className="px-6 py-2 border-t border-blue-100">
                  <SentimentMeter sentiment={currentSentiment} />
                </div>
              )}

              {/* Input Area */}
              <div className="p-6 border-t border-blue-100">
                <div className="flex space-x-4">
                  <textarea
                    ref={inputRef}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Share your thoughts and feelings..."
                    className="flex-1 p-4 border border-gray-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[60px] max-h-[120px]"
                    rows={2}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputText.trim() || isTyping}
                    className="px-6 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-2 text-center">
                  Press Enter to send, Shift+Enter for new line
                </p>
              </div>
            </>
          )}

          {activeTab === 'journal' && (
            <MoodJournal session={session} onUpdateSession={setSession} />
          )}

          {activeTab === 'trends' && (
            <SentimentTrends session={session} />
          )}
        </div>
      </div>
    </div>
  );
}