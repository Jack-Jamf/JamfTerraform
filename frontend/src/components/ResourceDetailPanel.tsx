import React, { useState, useEffect } from 'react';
import { ExecutionService, type JamfResourceDetailResponse } from '../services/ExecutionService';
import type { JamfCredentials } from '../types';
import './ResourceDetailPanel.css';

interface ResourceDetailPanelProps {
  credentials: JamfCredentials;
  resourceType: string;
  resourceId: number;
  resourceName: string;
  onClose: () => void;
}

const ResourceDetailPanel: React.FC<ResourceDetailPanelProps> = ({
  credentials,
  resourceType,
  resourceId,
  resourceName,
  onClose,
}) => {
  const [loading, setLoading] = useState(true);
  const [detail, setDetail] = useState<JamfResourceDetailResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadResourceDetail = async () => {
    setLoading(true);
    setError(null);

    const response = await ExecutionService.getResourceDetail(
      credentials,
      resourceType,
      resourceId
    );

    setLoading(false);

    if (response.success) {
      setDetail(response);
    } else {
      setError(response.error || 'Failed to load resource details');
    }
  };

  useEffect(() => {
    loadResourceDetail();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resourceId]);

  const handleDownloadHCL = () => {
    if (!detail) return;

    // Use bundle_hcl if available (includes dependencies), otherwise fallback to single resource hcl
    const content = detail.bundle_hcl || detail.hcl;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const sanitizedName = resourceName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    a.download = `${sanitizedName}.tf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopyHCL = async () => {
    if (!detail) return;
    await navigator.clipboard.writeText(detail.hcl);
    // TODO: Show toast notification
  };

  const getResourceIcon = (type: string) => {
    const icons: Record<string, string> = {
      policies: '📋',
      scripts: '📜',
      packages: '📦',
      categories: '🏷️',
      buildings: '🏢',
      'config-profiles': '⚙️',
      'smart-groups': '👥',
      'jamf-app-catalog': '🍎',
    };
    return icons[type] || '📄';
  };

  return (
    <div className="resource-detail-overlay" onClick={onClose}>
      <div className="resource-detail-panel" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="detail-header">
          <div className="header-content">
            <span className="resource-icon-large">{getResourceIcon(resourceType)}</span>
            <div className="header-text">
              <h2>{resourceName}</h2>
              <span className="resource-type-badge">{resourceType}</span>
            </div>
          </div>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        {/* Content */}
        <div className="detail-content">
          {loading ? (
            <div className="detail-loading">
              <div className="spinner"></div>
              <p>Loading resource details...</p>
            </div>
          ) : error ? (
            <div className="detail-error">
              <span>❌ {error}</span>
              <button onClick={loadResourceDetail}>Retry</button>
            </div>
          ) : detail ? (
            <>
              {/* Dependencies Section */}
              {detail.dependencies && detail.dependencies.length > 0 && (
                <div className="dependencies-section">
                  <h3>📦 Dependencies</h3>
                  <div className="dependency-tree">
                    {detail.dependencies.map((dep, idx) => (
                      <div key={idx} className="dependency-item">
                        <span className="dep-icon">{getResourceIcon(dep.type)}</span>
                        <div className="dep-info">
                          <span className="dep-type">{dep.type}</span>
                          <span className="dep-name">{dep.name}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* HCL Preview */}
              <div className="hcl-section">
                <h3>📝 Generated HCL</h3>
                <div className="hcl-code">
                  <pre><code>{detail.hcl}</code></pre>
                </div>
              </div>

              {/* Actions */}
              <div className="detail-actions">
                <button className="btn-primary" onClick={handleDownloadHCL}>
                  ⬇️ Download .tf {detail.bundle_hcl ? "(Bundle)" : ""}
                </button>
                <button className="btn-secondary" onClick={handleCopyHCL}>
                  📋 Copy HCL
                </button>
              </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default ResourceDetailPanel;
