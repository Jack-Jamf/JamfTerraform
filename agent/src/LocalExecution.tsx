import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './LocalExecution.css';

interface TerraformOutput {
  line: string;
  stream: 'stdout' | 'stderr';
}

export default function LocalExecution() {
  const [hclCode, setHclCode] = useState('');
  const [jamfUrl, setJamfUrl] = useState('');
  const [jamfUsername, setJamfUsername] = useState('');
  const [jamfPassword, setJamfPassword] = useState('');
  const [output, setOutput] = useState<TerraformOutput[]>([]);
  const [isExecuting, setIsExecuting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Listen for terraform output events
    const setupListener = async () => {
      const unlisten = await listen<TerraformOutput>('terraform-output', (event) => {
        setOutput((prev) => [...prev, event.payload]);
      });

      return unlisten;
    };

    let unlistenFn: (() => void) | null = null;
    setupListener().then((fn) => {
      unlistenFn = fn;
    });

    return () => {
      if (unlistenFn) {
        unlistenFn();
      }
    };
  }, []);

  const handleExecute = async () => {
    if (!hclCode.trim() || !jamfUrl.trim() || !jamfUsername.trim() || !jamfPassword.trim()) {
      setError('Please provide HCL code and all Jamf credentials (URL, username, password)');
      return;
    }

    setIsExecuting(true);
    setError(null);
    setOutput([]);

    try {
      const result = await invoke<string>('run_terraform', {
        hclCode,
        jamfUrl,
        jamfUsername,
        jamfPassword,
      });
      
      setOutput((prev) => [
        ...prev,
        { line: `✅ ${result}`, stream: 'stdout' },
      ]);
    } catch (err) {
      setError(err as string);
      setOutput((prev) => [
        ...prev,
        { line: `❌ Error: ${err}`, stream: 'stderr' },
      ]);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleClear = () => {
    setOutput([]);
    setError(null);
  };

  return (
    <div className="local-execution">
      <div className="input-section">
        <div className="form-group">
          <label>HCL Code</label>
          <div className="hcl-preview">
            <SyntaxHighlighter
              language="hcl"
              style={vscDarkPlus}
              customStyle={{
                margin: 0,
                borderRadius: '8px',
                fontSize: '0.875rem',
                minHeight: '200px',
              }}
            >
              {hclCode || '// Paste your HCL code here'}
            </SyntaxHighlighter>
          </div>
          <textarea
            value={hclCode}
            onChange={(e) => setHclCode(e.target.value)}
            placeholder="Paste generated HCL code here..."
            rows={10}
            className="hcl-input"
          />
        </div>

        <div className="form-group">
          <label>Jamf Pro URL</label>
          <input
            type="url"
            value={jamfUrl}
            onChange={(e) => setJamfUrl(e.target.value)}
            placeholder="https://your-instance.jamfcloud.com"
            className="jamf-input"
          />
        </div>

        <div className="form-group">
          <label>Jamf Username</label>
          <input
            type="text"
            value={jamfUsername}
            onChange={(e) => setJamfUsername(e.target.value)}
            placeholder="admin"
            className="jamf-input"
            autoComplete="off"
          />
        </div>

        <div className="form-group">
          <label>Jamf Password</label>
          <input
            type="password"
            value={jamfPassword}
            onChange={(e) => setJamfPassword(e.target.value)}
            placeholder="Enter your Jamf password"
            className="jamf-input"
            autoComplete="off"
          />
        </div>

        <div className="button-group">
          <button
            onClick={handleExecute}
            disabled={isExecuting || !hclCode.trim() || !jamfUrl.trim() || !jamfUsername.trim() || !jamfPassword.trim()}
            className="execute-button"
          >
            {isExecuting ? '⏳ Executing...' : '▶️ Execute Terraform'}
          </button>
          <button
            onClick={handleClear}
            disabled={isExecuting || output.length === 0}
            className="clear-button"
          >
            🗑️ Clear Output
          </button>
        </div>

        {error && <div className="error-message">⚠️ {error}</div>}
      </div>

      <div className="output-section">
        <h3>Terraform Output</h3>
        <div className="terminal">
          {output.length === 0 ? (
            <div className="empty-output">
              📋 No output yet. Click "Execute Terraform" to start.
            </div>
          ) : (
            output.map((line, idx) => (
              <div
                key={idx}
                className={`output-line ${line.stream}`}
              >
                <span className="stream-label">[{line.stream}]</span>
                {line.line}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
