'use client';

import { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Calendar, Plus, Save } from 'lucide-react';
import { UserSession, MoodEntry } from '@/types';
import { analyzeSentiment } from '@/utils/sentimentAnalysis';

interface MoodJournalProps {
  session: UserSession;
  onUpdateSession: (session: UserSession) => void;
}

export default function MoodJournal({ session, onUpdateSession }: MoodJournalProps) {
  const [selectedMood, setSelectedMood] = useState(5);
  const [notes, setNotes] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const moodEmojis = ['😢', '😔', '😐', '🙂', '😊', '😄', '🥰', '😍', '🤩', '🌟'];
  const moodLabels = [
    'Very Sad', 'Sad', 'Down', 'Okay', 'Good', 
    'Happy', 'Very Happy', 'Joyful', 'Ecstatic', 'Amazing'
  ];

  const handleSaveMoodEntry = () => {
    if (!notes.trim()) return;

    const sentiment = analyzeSentiment(notes);
    const newEntry: MoodEntry = {
      id: uuidv4(),
      date: new Date(),
      mood: selectedMood + 1, // Convert to 1-10 scale
      notes,
      sentiment
    };

    const updatedSession = {
      ...session,
      moodEntries: [...session.moodEntries, newEntry]
    };

    onUpdateSession(updatedSession);
    setNotes('');
    setSelectedMood(5);
    setIsAdding(false);
  };

  const getDailyCheckIn = () => {
    const prompts = [
      "How are you feeling today? What emotions are you experiencing?",
      "What's one thing you're grateful for right now?",
      "What challenged you today, and how did you handle it?",
      "Describe your energy level and what might be affecting it.",
      "What's one small thing that brought you joy today?",
      "How would you rate your stress level, and what's contributing to it?",
      "What's something you learned about yourself today?"
    ];
    
    const today = new Date().getDay();
    return prompts[today];
  };

  return (
    <div className="p-6 h-full">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Calendar className="w-6 h-6 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-800">Mood Journal</h2>
          </div>
          <button
            onClick={() => setIsAdding(!isAdding)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>New Entry</span>
          </button>
        </div>

        {/* Daily Check-in Prompt */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Daily Check-in</h3>
          <p className="text-gray-700 italic">"{getDailyCheckIn()}"</p>
        </div>

        {/* Add New Entry Form */}
        {isAdding && (
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">How are you feeling?</h3>
            
            {/* Mood Selector */}
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">Mood (1-10)</span>
                <span className="text-sm font-medium text-gray-800">
                  {moodLabels[selectedMood]} {moodEmojis[selectedMood]}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="9"
                value={selectedMood}
                onChange={(e) => setSelectedMood(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Very Sad</span>
                <span>Amazing</span>
              </div>
            </div>

            {/* Notes */}
            <div className="mb-4">
              <label className="block text-sm text-gray-600 mb-2">
                Notes (How are you feeling? What's on your mind?)
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Describe your feelings, thoughts, or experiences..."
                className="w-full p-3 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={4}
              />
            </div>

            <div className="flex space-x-3">
              <button
                onClick={handleSaveMoodEntry}
                disabled={!notes.trim()}
                className="flex items-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Save className="w-4 h-4" />
                <span>Save Entry</span>
              </button>
              <button
                onClick={() => setIsAdding(false)}
                className="px-4 py-2 text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Mood Entries */}
        <div className="space-y-4">
          {session.moodEntries.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-500 mb-2">No journal entries yet</h3>
              <p className="text-gray-400">Start tracking your mood and thoughts to see patterns over time.</p>
            </div>
          ) : (
            session.moodEntries
              .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
              .map((entry) => (
                <div key={entry.id} className="bg-white rounded-lg border border-gray-200 p-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{moodEmojis[entry.mood - 1]}</span>
                      <div>
                        <div className="font-medium text-gray-800">
                          {moodLabels[entry.mood - 1]} ({entry.mood}/10)
                        </div>
                        <div className="text-sm text-gray-500">
                          {new Date(entry.date).toLocaleDateString()} at{' '}
                          {new Date(entry.date).toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-500">Sentiment</div>
                      <div className={`font-medium capitalize ${
                        entry.sentiment.score > 0.1 ? 'text-green-600' :
                        entry.sentiment.score < -0.1 ? 'text-red-600' : 'text-yellow-600'
                      }`}>
                        {entry.sentiment.label}
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-gray-700 whitespace-pre-wrap">
                    {entry.notes}
                  </div>
                  
                  {entry.sentiment.emotions.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {entry.sentiment.emotions.slice(0, 3).map((emotion, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs capitalize"
                        >
                          {emotion.emotion}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
          )}
        </div>
      </div>
    </div>
  );
}