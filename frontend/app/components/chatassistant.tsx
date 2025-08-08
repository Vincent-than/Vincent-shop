'use client';

import { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, X, Bot, User, Sparkles } from 'lucide-react';
import { api } from '../lib/api';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  currency: string;
  category: string;
  brand: string;
  image_url: string;
  rating: number;
  review_count: number;
  tags: string[];
  similarity_score?: number;
}

interface ChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  products?: Product[];
  intent?: string;
}

export default function ChatAssistant() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      text: "Hi! 👋 I'm your AI shopping assistant. I can help you find products, compare options, and answer questions. What are you looking for today?",
      isUser: false,
      timestamp: new Date(),
      intent: 'greeting'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await api.post('/api/chat', { 
        message: inputMessage,
        user_id: 'user_123' 
      });

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data.message,
        isUser: false,
        timestamp: new Date(),
        products: response.data.products || [],
        intent: response.data.intent
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I'm having trouble right now. Please try again!",
        isUser: false,
        timestamp: new Date(),
        intent: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const quickQuestions = [
    "Find wireless headphones under $200",
    "Recommend a good laptop for students",
    "Compare iPhone vs Samsung phones",
    "Show me comfortable running shoes"
  ];

  return (
    <>
      {/* Chat Button - 3D Floating */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-purple-600 to-pink-600 text-white p-4 rounded-full shadow-2xl hover:shadow-3xl transform transition-all duration-300 hover:scale-110 hover:-translate-y-2 group"
        style={{
          background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #c084fc 100%)',
          boxShadow: '0 20px 40px rgba(139, 92, 246, 0.4), 0 0 20px rgba(139, 92, 246, 0.3)'
        }}
      >
        <div className="relative">
          <MessageSquare className="h-6 w-6 group-hover:animate-pulse" />
          <Sparkles className="absolute -top-1 -right-1 h-3 w-3 text-yellow-300 animate-ping" />
        </div>
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed inset-0 z-40 flex items-end justify-end p-4">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black/20 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Chat Container */}
          <div 
            className="relative bg-white rounded-2xl shadow-2xl w-96 h-[600px] flex flex-col transform transition-all duration-500 animate-in slide-in-from-bottom-4"
            style={{
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 20px 40px rgba(139, 92, 246, 0.15)'
            }}
          >
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-4 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="bg-white/20 p-2 rounded-full">
                    <Bot className="h-5 w-5" />
                  </div>
                  <div>
                    <h3 className="font-bold">AI Shopping Assistant</h3>
                    <p className="text-purple-100 text-sm">Online • Ready to help</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] ${message.isUser ? 'order-2' : 'order-1'}`}>
                    {/* Message Bubble */}
                    <div className={`p-3 rounded-2xl ${
                      message.isUser 
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white ml-auto' 
                        : 'bg-gray-100 text-gray-800'
                    } shadow-md`}>
                      <div className="flex items-start space-x-2">
                        {!message.isUser && (
                          <Bot className="h-4 w-4 mt-1 text-purple-600" />
                        )}
                        <div className="flex-1">
                          <p className="text-sm leading-relaxed whitespace-pre-line">{message.text}</p>
                        </div>
                        {message.isUser && (
                          <User className="h-4 w-4 mt-1 text-white/80" />
                        )}
                      </div>
                    </div>

                    {/* Product Cards for AI responses */}
                    {!message.isUser && message.products && message.products.length > 0 && (
                      <div className="mt-3 space-y-2">
                        {message.products.slice(0, 3).map((product) => (
                          <div key={product.id} className="bg-white border rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow">
                            <div className="flex items-center space-x-3">
                              <img
                                src={product.image_url}
                                alt={product.name}
                                className="w-12 h-12 object-cover rounded-lg"
                              />
                              <div className="flex-1">
                                <h4 className="font-semibold text-sm text-gray-900">{product.name}</h4>
                                <p className="text-xs text-gray-600">{product.brand}</p>
                                <div className="flex items-center justify-between mt-1">
                                  <span className="font-bold text-blue-600">{formatPrice(product.price)}</span>
                                  <span className="text-xs text-yellow-600">⭐ {product.rating}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Timestamp */}
                    <p className="text-xs text-gray-500 mt-1 px-2">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-3 rounded-2xl shadow-md">
                    <div className="flex items-center space-x-2">
                      <Bot className="h-4 w-4 text-purple-600" />
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Questions */}
            {messages.length <= 1 && (
              <div className="p-4 border-t bg-gray-50">
                <p className="text-xs text-gray-600 mb-2">Quick questions:</p>
                <div className="space-y-1">
                  {quickQuestions.slice(0, 2).map((question) => (
                    <button
                      key={question}
                      onClick={() => {
                        setInputMessage(question);
                        setTimeout(() => sendMessage(), 100);
                      }}
                      className="w-full text-left text-xs text-blue-600 hover:text-blue-800 p-2 hover:bg-blue-50 rounded transition-colors"
                    >
                      💬 {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t bg-white rounded-b-2xl">
              <div className="flex items-center space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Ask me anything about products..."
                  className="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white p-3 rounded-xl transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}