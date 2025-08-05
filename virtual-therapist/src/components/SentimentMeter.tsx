'use client';

import { SentimentAnalysis } from '@/types';
import { getSentimentColor, getSentimentEmoji } from '@/utils/sentimentAnalysis';

interface SentimentMeterProps {
  sentiment: SentimentAnalysis;
}

export default function SentimentMeter({ sentiment }: SentimentMeterProps) {
  const getIntensityColor = (intensity: number) => {
    if (intensity > 0.7) return 'bg-red-500';
    if (intensity > 0.4) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getMeterPosition = (score: number) => {
    // Convert score from -1 to 1 range to 0 to 100 percentage
    return ((score + 1) / 2) * 100;
  };

  return (
    <div className="bg-white rounded-lg p-4 border border-gray-100">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-700">Current Sentiment</h3>
        <div className="flex items-center space-x-2">
          <span className="text-lg">{getSentimentEmoji(sentiment)}</span>
          <span className={`text-sm font-medium capitalize ${getSentimentColor(sentiment)}`}>
            {sentiment.label}
          </span>
        </div>
      </div>

      {/* Sentiment Meter */}
      <div className="relative mb-4">
        <div className="w-full h-2 bg-gray-200 rounded-full">
          <div 
            className="h-2 bg-gradient-to-r from-red-400 via-yellow-400 to-green-400 rounded-full"
          />
        </div>
        <div 
          className="absolute top-0 w-3 h-3 bg-white border-2 border-gray-600 rounded-full transform -translate-y-0.5 -translate-x-1.5"
          style={{ left: `${getMeterPosition(sentiment.score)}%` }}
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Negative</span>
          <span>Neutral</span>
          <span>Positive</span>
        </div>
      </div>

      {/* Intensity Indicator */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-600">Intensity</span>
        <div className="flex items-center space-x-2">
          <div className="w-20 h-2 bg-gray-200 rounded-full">
            <div 
              className={`h-2 rounded-full ${getIntensityColor(sentiment.intensity)}`}
              style={{ width: `${sentiment.intensity * 100}%` }}
            />
          </div>
          <span className="text-sm text-gray-600">
            {Math.round(sentiment.intensity * 100)}%
          </span>
        </div>
      </div>

      {/* Detected Emotions */}
      {sentiment.emotions.length > 0 && (
        <div>
          <span className="text-sm text-gray-600 mb-2 block">Detected Emotions</span>
          <div className="flex flex-wrap gap-2">
            {sentiment.emotions.map((emotion, index) => (
              <div
                key={index}
                className="flex items-center space-x-1 px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs"
              >
                <span className="capitalize">{emotion.emotion}</span>
                <span className="text-blue-500">
                  {Math.round(emotion.confidence * 100)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}