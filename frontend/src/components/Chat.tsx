import React, { useState, useRef, useEffect, useCallback } from 'react';
import type { Message } from '../types';
import { ExecutionService } from '../services/ExecutionService';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './Chat.css';

interface ChatProps {
  selectedRecipe?: string | null;
  onRecipeUsed?: () => void;
}

const Chat: React.FC<ChatProps> = ({ selectedRecipe, onRecipeUsed }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = useCallback(async (messageContent: string) => {
    if (!messageContent.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageContent.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await ExecutionService.generateHCL({
        prompt: userMessage.content,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.success ? response.hcl : `Error: ${response.error}`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  // Handle selected recipe from cookbook
  useEffect(() => {
    if (selectedRecipe) {
      sendMessage(selectedRecipe);
      if (onRecipeUsed) {
        onRecipeUsed();
      }
    }
  }, [selectedRecipe, onRecipeUsed, sendMessage]);

  const handleSend = () => {
    sendMessage(input);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">💬</div>
            <h2 className="empty-state-title">Start a Conversation</h2>
            <p className="empty-state-description">
              Describe the Jamf configuration you need, and I'll generate the Terraform HCL for you.
            </p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.role}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-role">
                      {message.role === 'user' ? 'You' : 'Assistant'}
                    </span>
                    <span className="message-timestamp">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  <div className="message-text">
                    {message.role === 'assistant' ? (
                      <SyntaxHighlighter
                        language="hcl"
                        style={vscDarkPlus}
                        customStyle={{
                          margin: 0,
                          borderRadius: 'var(--radius-md)',
                          fontSize: '0.875rem',
                          background: 'var(--color-bg-tertiary)',
                        }}
                      >
                        {message.content}
                      </SyntaxHighlighter>
                    ) : (
                      message.content
                    )}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="loading-indicator">
                    <span>Generating HCL</span>
                    <div className="loading-dots">
                      <div className="loading-dot"></div>
                      <div className="loading-dot"></div>
                      <div className="loading-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            ref={textareaRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your Jamf configuration... (Shift+Enter for new line)"
            rows={1}
            disabled={isLoading}
          />
          <button
            className="chat-send-button"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <span>Send</span>
            <span>↑</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
