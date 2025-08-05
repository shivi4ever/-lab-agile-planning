'use client';

import { UserSession } from '@/types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, Calendar, BarChart3 } from 'lucide-react';

interface SentimentTrendsProps {
  session: UserSession;
}

export default function SentimentTrends({ session }: SentimentTrendsProps) {
  // Prepare data for sentiment chart
  const sentimentData = session.sentimentHistory.map((sentiment, index) => ({
    index: index + 1,
    sentiment: sentiment.score,
    intensity: sentiment.intensity,
    label: sentiment.label
  }));

  // Prepare data for mood entries chart
  const moodData = session.moodEntries.map((entry, index) => ({
    index: index + 1,
    mood: entry.mood,
    date: new Date(entry.date).toLocaleDateString()
  }));

  // Calculate emotion frequency
  const emotionFrequency = session.sentimentHistory.reduce((acc, sentiment) => {
    sentiment.emotions.forEach(emotion => {
      acc[emotion.emotion] = (acc[emotion.emotion] || 0) + 1;
    });
    return acc;
  }, {} as Record<string, number>);

  const emotionData = Object.entries(emotionFrequency)
    .map(([emotion, count]) => ({ emotion, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8);

  const getAverageSentiment = () => {
    if (session.sentimentHistory.length === 0) return 0;
    const sum = session.sentimentHistory.reduce((acc, s) => acc + s.score, 0);
    return sum / session.sentimentHistory.length;
  };

  const getAverageMood = () => {
    if (session.moodEntries.length === 0) return 0;
    const sum = session.moodEntries.reduce((acc, entry) => acc + entry.mood, 0);
    return sum / session.moodEntries.length;
  };

  const getMoodTrend = () => {
    if (moodData.length < 2) return 'stable';
    const recent = moodData.slice(-3);
    const older = moodData.slice(-6, -3);
    
    if (recent.length === 0 || older.length === 0) return 'stable';
    
    const recentAvg = recent.reduce((acc, d) => acc + d.mood, 0) / recent.length;
    const olderAvg = older.reduce((acc, d) => acc + d.mood, 0) / older.length;
    
    if (recentAvg > olderAvg + 0.5) return 'improving';
    if (recentAvg < olderAvg - 0.5) return 'declining';
    return 'stable';
  };

  const formatTooltipValue = (value: number, name: string) => {
    if (name === 'sentiment') {
      return [value.toFixed(2), 'Sentiment Score'];
    }
    if (name === 'mood') {
      return [value, 'Mood Rating'];
    }
    return [value, name];
  };

  return (
    <div className="p-6 h-full overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center space-x-3 mb-6">
          <TrendingUp className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-800">Emotional Trends</h2>
        </div>

        {session.sentimentHistory.length === 0 && session.moodEntries.length === 0 ? (
          <div className="text-center py-12">
            <BarChart3 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-500 mb-2">No data available yet</h3>
            <p className="text-gray-400">Start chatting and journaling to see your emotional trends over time.</p>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Average Sentiment</p>
                    <p className={`text-2xl font-bold ${
                      getAverageSentiment() > 0.1 ? 'text-green-600' :
                      getAverageSentiment() < -0.1 ? 'text-red-600' : 'text-yellow-600'
                    }`}>
                      {getAverageSentiment() > 0 ? '+' : ''}{getAverageSentiment().toFixed(2)}
                    </p>
                  </div>
                  <div className="text-2xl">
                    {getAverageSentiment() > 0.1 ? '😊' : 
                     getAverageSentiment() < -0.1 ? '😔' : '😐'}
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Average Mood</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {getAverageMood().toFixed(1)}/10
                    </p>
                  </div>
                  <div className="text-2xl">📊</div>
                </div>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Mood Trend</p>
                    <p className={`text-lg font-bold capitalize ${
                      getMoodTrend() === 'improving' ? 'text-green-600' :
                      getMoodTrend() === 'declining' ? 'text-red-600' : 'text-blue-600'
                    }`}>
                      {getMoodTrend()}
                    </p>
                  </div>
                  <div className="text-2xl">
                    {getMoodTrend() === 'improving' ? '📈' :
                     getMoodTrend() === 'declining' ? '📉' : '➡️'}
                  </div>
                </div>
              </div>
            </div>

            {/* Sentiment Over Time */}
            {sentimentData.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Sentiment Over Time</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={sentimentData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="index" 
                        label={{ value: 'Message Number', position: 'insideBottom', offset: -10 }}
                      />
                      <YAxis 
                        domain={[-1, 1]}
                        label={{ value: 'Sentiment Score', angle: -90, position: 'insideLeft' }}
                      />
                      <Tooltip formatter={formatTooltipValue} />
                      <Line 
                        type="monotone" 
                        dataKey="sentiment" 
                        stroke="#3B82F6" 
                        strokeWidth={2}
                        dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Mood Journal Trends */}
            {moodData.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Mood Journal Trends</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={moodData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="index"
                        label={{ value: 'Journal Entry', position: 'insideBottom', offset: -10 }}
                      />
                      <YAxis 
                        domain={[1, 10]}
                        label={{ value: 'Mood Rating', angle: -90, position: 'insideLeft' }}
                      />
                      <Tooltip formatter={formatTooltipValue} />
                      <Line 
                        type="monotone" 
                        dataKey="mood" 
                        stroke="#10B981" 
                        strokeWidth={2}
                        dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Emotion Frequency */}
            {emotionData.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Most Common Emotions</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={emotionData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="emotion" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#8B5CF6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Insights */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Insights & Patterns</h3>
              <div className="space-y-2 text-gray-700">
                {session.sentimentHistory.length > 0 && (
                  <p>
                    • You've shared {session.sentimentHistory.length} messages with an average sentiment of{' '}
                    <span className="font-medium">
                      {getAverageSentiment() > 0.1 ? 'positive' : 
                       getAverageSentiment() < -0.1 ? 'negative' : 'neutral'}
                    </span>
                  </p>
                )}
                {session.moodEntries.length > 0 && (
                  <p>
                    • Your mood journal shows {session.moodEntries.length} entries with an average rating of{' '}
                    <span className="font-medium">{getAverageMood().toFixed(1)}/10</span>
                  </p>
                )}
                {emotionData.length > 0 && (
                  <p>
                    • Your most frequently expressed emotion is{' '}
                    <span className="font-medium capitalize">{emotionData[0].emotion}</span>
                  </p>
                )}
                <p>
                  • Remember: These patterns can help you understand your emotional journey, but every feeling is valid and temporary.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}