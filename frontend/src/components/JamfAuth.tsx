import React, { useState } from 'react';
import type { JamfCredentials, AuthStatus } from '../types';
import './JamfAuth.css';

interface JamfAuthProps {
  onCredentialsChange?: (credentials: JamfCredentials | null) => void;
}

const JamfAuth: React.FC<JamfAuthProps> = ({ onCredentialsChange }) => {
  const [url, setUrl] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<AuthStatus>('idle');
  const [message, setMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const validateUrl = (urlString: string): boolean => {
    try {
      const urlObj = new URL(urlString);
      return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
      return false;
    }
  };

  const handleSetCredentials = () => {
    // Validate inputs
    if (!url || !username || !password) {
      setStatus('error');
      setMessage('All fields are required');
      return;
    }

    if (!validateUrl(url)) {
      setStatus('error');
      setMessage('Invalid URL format. Must start with http:// or https://');
      return;
    }

    const credentials: JamfCredentials = {
      url: url.trim(),
      username: username.trim(),
      password: password,
    };

    setStatus('success');
    setMessage('Credentials set for this session');
    onCredentialsChange?.(credentials);
  };

  const handleClear = () => {
    setUrl('');
    setUsername('');
    setPassword('');
    setStatus('idle');
    setMessage('');
    onCredentialsChange?.(null);
  };

  const handleTestConnection = async () => {
    if (!url || !username || !password) {
      setStatus('error');
      setMessage('All fields are required to test connection');
      return;
    }

    if (!validateUrl(url)) {
      setStatus('error');
      setMessage('Invalid URL format');
      return;
    }

    setStatus('testing');
    setMessage('Testing connection...');

    // Simulate connection test (in real implementation, this would call Jamf API)
    setTimeout(() => {
      setStatus('success');
      setMessage('Connection test successful (simulated)');
    }, 1500);
  };

  return (
    <div className="jamf-auth-container">
      <div className="jamf-auth-header">
        <h1 className="jamf-auth-title">🔐 Jamf Pro Authentication</h1>
        <p className="jamf-auth-description">
          Enter your Jamf Pro credentials for Terraform execution.
          Credentials are only stored in memory for this session and are never persisted.
        </p>
      </div>

      <div className="jamf-auth-form">
        <div className="form-group">
          <label htmlFor="jamf-url" className="form-label">
            Jamf Pro URL
          </label>
          <input
            id="jamf-url"
            type="text"
            className="form-input"
            placeholder="https://your-instance.jamfcloud.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <span className="form-hint">
            Your Jamf Pro server URL (e.g., https://company.jamfcloud.com)
          </span>
        </div>

        <div className="form-group">
          <label htmlFor="jamf-username" className="form-label">
            Username
          </label>
          <input
            id="jamf-username"
            type="text"
            className="form-input"
            placeholder="admin@company.com"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
          />
          <span className="form-hint">
            Your Jamf Pro administrator username
          </span>
        </div>

        <div className="form-group">
          <label htmlFor="jamf-password" className="form-label">
            Password
          </label>
          <div className="password-input-wrapper">
            <input
              id="jamf-password"
              type={showPassword ? 'text' : 'password'}
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
            <button
              type="button"
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? '👁️' : '👁️‍🗨️'}
            </button>
          </div>
          <span className="form-hint">
            Your Jamf Pro administrator password
          </span>
        </div>

        {message && (
          <div className={`auth-message auth-message-${status}`}>
            <span className="auth-message-icon">
              {status === 'success' && '✅'}
              {status === 'error' && '❌'}
              {status === 'testing' && '⏳'}
            </span>
            <span>{message}</span>
          </div>
        )}

        <div className="form-actions">
          <button
            className="btn btn-primary"
            onClick={handleSetCredentials}
            disabled={status === 'testing'}
          >
            ✓ Set Credentials
          </button>
          <button
            className="btn btn-secondary"
            onClick={handleTestConnection}
            disabled={status === 'testing'}
          >
            {status === 'testing' ? '⏳ Testing...' : '🔍 Test Connection'}
          </button>
          <button
            className="btn btn-danger"
            onClick={handleClear}
            disabled={status === 'testing'}
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      <div className="jamf-auth-info">
        <h3 className="info-title">ℹ️ Security Information</h3>
        <ul className="info-list">
          <li>Credentials are stored in memory only for this browser session</li>
          <li>Credentials are NOT persisted to disk or localStorage</li>
          <li>Credentials will be cleared when you close the browser tab</li>
          <li>Used only for Terraform execution - never sent to backend server</li>
        </ul>
      </div>
    </div>
  );
};

export default JamfAuth;

