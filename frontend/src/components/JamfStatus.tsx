import React, { useState } from 'react';
import type { JamfCredentials } from '../types';
import { ExecutionService } from '../services/ExecutionService';
import './JamfStatus.css';

interface JamfStatusProps {
  onCredentialsChange?: (credentials: JamfCredentials | null) => void;
}

interface ConnectionFeedback {
  type: 'error' | 'success';
  title: string;
  message: string;
  hint?: string;
}

const JamfStatus: React.FC<JamfStatusProps> = ({ onCredentialsChange }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [url, setUrl] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [feedback, setFeedback] = useState<ConnectionFeedback | null>(null);

  const validateUrl = (urlString: string): boolean => {
    try {
      const urlObj = new URL(urlString);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  };

  const parseErrorMessage = (error: string): ConnectionFeedback => {
    const lowerError = error.toLowerCase();
    
    if (lowerError.includes('401') || lowerError.includes('authentication failed')) {
      return {
        type: 'error',
        title: '❌ Authentication Failed',
        message: 'The username or password is incorrect.',
        hint: 'Double-check your credentials and ensure this account has API access.'
      };
    }
    if (lowerError.includes('404')) {
      return {
        type: 'error',
        title: '❌ Server Not Found',
        message: 'Could not reach the Jamf Pro API at this URL.',
        hint: 'Verify the URL format (e.g., https://yourcompany.jamfcloud.com)'
      };
    }
    if (lowerError.includes('connection') || lowerError.includes('network') || lowerError.includes('fetch')) {
      return {
        type: 'error',
        title: '❌ Connection Error',
        message: 'Unable to connect to the Jamf Pro server.',
        hint: 'Check your network connection and ensure the URL is accessible.'
      };
    }
    if (lowerError.includes('timeout')) {
      return {
        type: 'error',
        title: '⏱️ Connection Timeout',
        message: 'The server took too long to respond.',
        hint: 'The server may be busy. Please try again in a moment.'
      };
    }
    
    return {
      type: 'error',
      title: '❌ Connection Failed',
      message: error || 'An unexpected error occurred.',
      hint: 'Please verify your credentials and try again.'
    };
  };

  const handleTestConnection = async () => {
    if (!url || !username || !password) return;
    if (!validateUrl(url)) {
      setFeedback({
        type: 'error',
        title: '❌ Invalid URL',
        message: 'Please enter a valid Jamf Pro URL.',
        hint: 'Example: https://yourcompany.jamfcloud.com'
      });
      return;
    }

    setIsTesting(true);
    setFeedback(null);
    
    try {
      const credentials: JamfCredentials = {
        url: url.trim(),
        username: username.trim(),
        password: password,
      };

      const result = await ExecutionService.verifyAuth(credentials);

      if (result.success) {
        setFeedback({
          type: 'success',
          title: '✅ Connected Successfully!',
          message: 'Your Jamf Pro instance is now linked.',
        });
        setIsConnected(true);
        onCredentialsChange?.(credentials);
        
        // Auto-close after success
        setTimeout(() => {
          setIsExpanded(false);
          setFeedback(null);
        }, 1500);
      } else {
        setFeedback(parseErrorMessage(result.error || 'Unknown error'));
        setIsConnected(false);
      }
    } catch (error) {
      setFeedback(parseErrorMessage(error instanceof Error ? error.message : 'Unknown error'));
      setIsConnected(false);
    } finally {
      setIsTesting(false);
    }
  };

  const handleDisconnect = () => {
    setUrl('');
    setUsername('');
    setPassword('');
    setIsConnected(false);
    setIsExpanded(false);
    setFeedback(null);
    onCredentialsChange?.(null);
  };

  const handleInputChange = () => {
    // Clear feedback when user starts typing
    if (feedback) {
      setFeedback(null);
    }
  };

  return (
    <div className="jamf-status-wrapper">
      <div
        className={`jamf-status ${isConnected ? 'connected' : 'disconnected'}`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className={`status-indicator ${isConnected ? 'online' : 'offline'}`}></div>
        <span>Jamf Pro {isConnected ? 'Connected' : 'Disconnected'}</span>
      </div>

      {isExpanded && (
        <div className="jamf-status-dropdown">
          <div className="dropdown-header">
            <h3>🔐 Jamf Pro Credentials</h3>
            <button
              className="close-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(false);
                setFeedback(null);
              }}
            >
              ✕
            </button>
          </div>

          <div className="dropdown-form">
            <div className="form-field">
              <label>Jamf Pro URL</label>
              <input
                type="text"
                placeholder="https://your-instance.jamfcloud.com"
                value={url}
                onChange={(e) => { setUrl(e.target.value); handleInputChange(); }}
                onClick={(e) => e.stopPropagation()}
              />
            </div>

            <div className="form-field">
              <label>Username</label>
              <input
                type="text"
                placeholder="admin@company.com"
                value={username}
                onChange={(e) => { setUsername(e.target.value); handleInputChange(); }}
                onClick={(e) => e.stopPropagation()}
                autoComplete="username"
              />
            </div>

            <div className="form-field">
              <label>Password</label>
              <div className="password-field">
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); handleInputChange(); }}
                  onClick={(e) => e.stopPropagation()}
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowPassword(!showPassword);
                  }}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            {/* Inline Feedback */}
            {feedback && (
              <div className={`connection-feedback ${feedback.type}`}>
                <div className="feedback-title">{feedback.title}</div>
                <div className="feedback-message">{feedback.message}</div>
                {feedback.hint && <div className="feedback-hint">{feedback.hint}</div>}
              </div>
            )}

            <div className="dropdown-actions">
              <button
                className={`btn-test ${isTesting ? 'testing' : ''}`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleTestConnection();
                }}
                disabled={!url || !username || !password || isTesting}
              >
                {isTesting ? (
                  <>
                    <span className="testing-spinner"></span>
                    Verifying...
                  </>
                ) : (
                  '🔍 Test & Connect'
                )}
              </button>
              {isConnected && (
                <button
                  className="btn-disconnect"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDisconnect();
                  }}
                >
                  🗑️ Disconnect
                </button>
              )}
            </div>

            <div className="dropdown-info">
              <small>Session-only • Never persisted to disk</small>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JamfStatus;
