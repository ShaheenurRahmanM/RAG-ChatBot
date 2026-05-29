/**
 * ChatBox Component
 * Main component for managing chat messages and interactions
 */

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import MessageBubble from './MessageBubble';
import SourceList from './SourceList';
import Loader from './Loader';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending message
  const handleSendMessage = async (e) => {
    e.preventDefault();

    // Validate input
    if (!input.trim()) {
      setError('Please enter a question');
      return;
    }

    // Add user message to chat
    const userMessage = {
      text: input,
      isUser: true,
      sources: [],
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setError('');
    setLoading(true);

    try {
      // Call backend API
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        question: input,
      });

      // Add AI response to chat
      const aiMessage = {
        text: response.data.answer,
        isUser: false,
        sources: response.data.sources || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      // Handle errors
      let errorMessage = 'Failed to get response from the server';

      if (err.response) {
        errorMessage = err.response.data?.detail || err.response.statusText;
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);

      // Add error message to chat
      const errorMsg = {
        text: `❌ ${errorMessage}`,
        isUser: false,
        sources: [],
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbox">
      {/* Chat messages container */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p className="empty-state-text">
              👋 Welcome! Ask me anything about company policies and documents.
            </p>
            <p className="empty-state-subtext">
              Example: &quot;What is the leave policy?&quot;
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message-wrapper ${msg.isUser ? 'user-message' : 'ai-message'}`}
          >
            <MessageBubble message={msg.text} isUser={msg.isUser} />
            {!msg.isUser && msg.sources && msg.sources.length > 0 && (
              <SourceList sources={msg.sources} />
            )}
          </div>
        ))}

        {loading && <Loader />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form onSubmit={handleSendMessage} className="chat-input-form">
        {error && <div className="error-message">{error}</div>}
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setError('')}
            placeholder="Ask a question..."
            className="chat-input"
            disabled={loading}
            autoFocus
          />
          <button
            type="submit"
            className="send-button"
            disabled={loading || !input.trim()}
            title="Send message"
          >
            {loading ? '⏳' : '➤'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatBox;
