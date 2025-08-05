'use client';

import { Message } from '@/types';
import { Heart, User } from 'lucide-react';
import { getSentimentColor, getSentimentEmoji } from '@/utils/sentimentAnalysis';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex items-start space-x-2 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser 
            ? 'bg-blue-500' 
            : 'bg-gradient-to-r from-blue-500 to-purple-600'
        }`}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Heart className="w-4 h-4 text-white" />
          )}
        </div>
        
        {/* Message Content */}
        <div className={`rounded-2xl px-4 py-3 ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          <div className="whitespace-pre-wrap text-sm leading-relaxed">
            {message.content}
          </div>
          
          {/* Timestamp and Sentiment */}
          <div className={`flex items-center justify-between mt-2 text-xs ${
            isUser ? 'text-blue-100' : 'text-gray-500'
          }`}>
            <span>
              {message.timestamp.toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </span>
            
            {message.sentiment && isUser && (
              <div className="flex items-center space-x-1">
                <span>{getSentimentEmoji(message.sentiment)}</span>
                <span className="capitalize">
                  {message.sentiment.label}
                </span>
              </div>
            )}
          </div>
          
          {/* Emotions (for user messages) */}
          {message.sentiment && isUser && message.sentiment.emotions.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {message.sentiment.emotions.slice(0, 2).map((emotion, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-blue-400 text-blue-50 rounded-full text-xs capitalize"
                >
                  {emotion.emotion}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}