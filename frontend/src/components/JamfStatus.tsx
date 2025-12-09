import React, { useState } from 'react';
import type { JamfCredentials } from '../types';
import { ExecutionService } from '../services/ExecutionService';
import './JamfStatus.css';

interface JamfStatusProps {
  onCredentialsChange?: (credentials: JamfCredentials | null) => void;
}

const JamfStatus: React.FC<JamfStatusProps> = ({ onCredentialsChange }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [url, setUrl] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTesting, setIsTesting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const validateUrl = (urlString: string): boolean => {
    try {
      const urlObj = new URL(urlString);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  };

  /* eslint-disable @typescript-eslint/no-unused-vars */
  const handleConnect = () => {
    if (!url || !username || !password) return;
    if (!validateUrl(url)) return;

    const credentials: JamfCredentials = {
      url: url.trim(),
      username: username.trim(),
      password: password,
    };

    setIsConnected(true);
    onCredentialsChange?.(credentials);
    setIsExpanded(false);
  };
  /* eslint-enable @typescript-eslint/no-unused-vars */

  const handleTestConnection = async () => {
    if (!url || !username || !password) return;
    if (!validateUrl(url)) return;

    setIsTesting(true);
    
    try {
      const credentials: JamfCredentials = {
        url: url.trim(),
        username: username.trim(),
        password: password,
      };

      const result = await ExecutionService.verifyAuth(credentials);

      if (result.success) {
        setIsConnected(true);
        onCredentialsChange?.(credentials);
        setIsExpanded(false);
      } else {
        alert(`Connection Failed: ${result.error || 'Unknown error'}`);
        setIsConnected(false);
      }
    } catch (error) {
      alert(`Connection Failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
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
    onCredentialsChange?.(null);
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
                onChange={(e) => setUrl(e.target.value)}
                onClick={(e) => e.stopPropagation()}
              />
            </div>

            <div className="form-field">
              <label>Username</label>
              <input
                type="text"
                placeholder="admin@company.com"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
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
                  onChange={(e) => setPassword(e.target.value)}
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

            <div className="dropdown-actions">
              <button
                className="btn-test"
                onClick={(e) => {
                  e.stopPropagation();
                  handleTestConnection();
                }}
                disabled={!url || !username || !password || isTesting}
              >
                {isTesting ? '⏳ Testing...' : '🔍 Test & Connect'}
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
