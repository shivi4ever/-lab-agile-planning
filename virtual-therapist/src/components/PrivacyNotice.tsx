'use client';

import { Shield, Heart, AlertTriangle, Check } from 'lucide-react';

interface PrivacyNoticeProps {
  onAccept: () => void;
}

export default function PrivacyNotice({ onAccept }: PrivacyNoticeProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-2xl bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Virtual Therapist</h1>
          <p className="text-gray-600">Privacy & Ethical Use Notice</p>
        </div>

        <div className="space-y-6">
          {/* Important Notice */}
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
              <div>
                <h3 className="font-semibold text-amber-800 mb-1">Important Notice</h3>
                <p className="text-amber-700 text-sm">
                  This AI companion is designed to provide emotional support and coping strategies, 
                  but it is <strong>not a replacement for professional mental health care</strong>. 
                  If you're experiencing a mental health crisis, please contact a mental health professional 
                  or crisis hotline immediately.
                </p>
              </div>
            </div>
          </div>

          {/* Privacy Features */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <Heart className="w-5 h-5 text-red-500 mr-2" />
              Your Privacy Matters
            </h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <Check className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-700">
                    <strong>Local Processing:</strong> All sentiment analysis and data processing 
                    happens locally in your browser. Your conversations never leave your device.
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Check className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-700">
                    <strong>No Data Storage:</strong> We don't store your conversations, mood entries, 
                    or personal information on any servers. Everything is kept private on your device.
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Check className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-gray-700">
                    <strong>Anonymous Usage:</strong> No personal identification is required or collected. 
                    You remain completely anonymous while using this service.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Ethical Guidelines */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">Ethical Use Guidelines</h3>
            <div className="space-y-2 text-gray-700">
              <p>• This tool provides general emotional support and evidence-based coping strategies</p>
              <p>• Responses are generated using established therapeutic techniques (CBT, mindfulness)</p>
              <p>• The AI cannot diagnose mental health conditions or prescribe treatments</p>
              <p>• For serious mental health concerns, please consult qualified professionals</p>
              <p>• Use this as a supplement to, not a replacement for, professional care</p>
            </div>
          </div>

          {/* Crisis Resources */}
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="font-semibold text-red-800 mb-2">Crisis Resources</h3>
            <div className="text-red-700 text-sm space-y-1">
              <p><strong>National Suicide Prevention Lifeline:</strong> 988</p>
              <p><strong>Crisis Text Line:</strong> Text HOME to 741741</p>
              <p><strong>International:</strong> Visit findahelpline.com for local resources</p>
            </div>
          </div>

          {/* Consent */}
          <div className="border-t pt-6">
            <p className="text-gray-600 text-sm mb-4">
              By continuing, you acknowledge that you have read and understood this privacy notice 
              and agree to use this tool responsibly as a supportive resource alongside appropriate 
              professional care when needed.
            </p>
            <button
              onClick={onAccept}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-colors"
            >
              I Understand - Continue to Virtual Therapist
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}