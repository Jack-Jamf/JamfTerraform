import React, { useState } from 'react';
import { ExecutionService, type JamfResourceListResponse, type JamfInstanceExportResponse, type JamfInstanceSummary } from '../services/ExecutionService';
import type { JamfCredentials } from '../types';
import ResourceDetailPanel from './ResourceDetailPanel';
import './ProporterMenu.css';

interface ProporterMenuProps {
  isEnabled: boolean;
  credentials: JamfCredentials | null;
}

interface ResourceType {
  id: string;
  name: string;
  icon: string;
  description: string;
}

const RESOURCE_TYPES: ResourceType[] = [
  { id: 'policies', name: 'Policies', icon: '📋', description: 'Import Jamf Pro policies' },
  { id: 'smart-groups', name: 'Smart Groups', icon: '👥', description: 'Import computer/mobile smart groups' },
  { id: 'config-profiles', name: 'Configuration Profiles', icon: '⚙️', description: 'Import macOS/iOS configuration profiles' },
  { id: 'scripts', name: 'Scripts', icon: '📜', description: 'Import scripts from Jamf Pro' },
  { id: 'packages', name: 'Packages', icon: '📦', description: 'Import package definitions' },
];

interface JamfResource {
  id: number;
  name: string;
}

type ViewMode = 'main' | 'resource-type' | 'instance-export';

const ProporterMenu: React.FC<ProporterMenuProps> = ({ isEnabled, credentials }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [viewMode, setViewMode] = useState<ViewMode>('main');
  const [selectedResourceType, setSelectedResourceType] = useState<ResourceType | null>(null);
  const [selectedResource, setSelectedResource] = useState<JamfResource | null>(null);
  const [resources, setResources] = useState<JamfResource[]>([]);
  const [instanceSummary, setInstanceSummary] = useState<JamfInstanceSummary[]>([]);
  const [instanceHCL, setInstanceHCL] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleButtonClick = () => {
    if (isEnabled) {
      setIsExpanded(!isExpanded);
      if (isExpanded) {
        setViewMode('main');
        setSelectedResourceType(null);
        setSelectedResource(null);
        setResources([]);
        setInstanceSummary([]);
        setError(null);
      }
    }
  };

  const handleExportAll = async () => {
    if (!credentials) return;
    
    setLoading(true);
    setError(null);
    setViewMode('instance-export');
    
    const response: JamfInstanceExportResponse = await ExecutionService.exportJamfInstance(credentials);
    
    setLoading(false);
    
    if (response.success) {
      setInstanceSummary(response.summary);
      setInstanceHCL(response.hcl);
    } else {
      setError(response.error || 'Failed to export instance');
    }
  };

  const handleResourceTypeClick = async (resourceType: ResourceType) => {
    if (!credentials) return;
    
    setSelectedResourceType(resourceType);
    setViewMode('resource-type');
    setLoading(true);
    setError(null);
    
    const response: JamfResourceListResponse = await ExecutionService.listJamfResources(
      credentials,
      resourceType.id
    );
    
    setLoading(false);
    
    if (response.success) {
      setResources(response.resources);
    } else {
      setError(response.error || 'Failed to fetch resources');
    }
  };

  const handleBack = () => {
    setViewMode('main');
    setSelectedResourceType(null);
    setSelectedResource(null);
    setResources([]);
    setInstanceSummary([]);
    setError(null);
  };

  const handleResourceClick = (resource: JamfResource) => {
    setSelectedResource(resource);
  };

  const handleDownloadHCL = () => {
    const blob = new Blob([instanceHCL], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'jamf_instance.tf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="proporter-menu-wrapper">
      <button
        className={`proporter-menu-button ${!isEnabled ? 'disabled' : ''}`}
        onClick={handleButtonClick}
        disabled={!isEnabled}
        title={!isEnabled ? 'Connect to Jamf Pro first' : 'Import existing Jamf configuration'}
      >
        📦 Proporter
      </button>

      {isExpanded && isEnabled && (
        <div className="proporter-menu-dropdown">
          <div className="dropdown-header">
            <h3>
              {viewMode !== 'main' && (
                <button className="back-btn" onClick={handleBack}>←</button>
              )}
              {viewMode === 'main' && '📦 Proporter - Import Config'}
              {viewMode === 'resource-type' && selectedResourceType && `${selectedResourceType.icon} ${selectedResourceType.name}`}
              {viewMode === 'instance-export' && '📦 Instance Export'}
            </h3>
            <button
              className="close-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(false);
                setViewMode('main');
                setSelectedResourceType(null);
                setResources([]);
              }}
            >
              ✕
            </button>
          </div>

          <div className="proporter-menu-content">
            {viewMode === 'main' && (
              <>
                <div className="proporter-info">
                  <p>Select a resource type or export your entire Jamf instance.</p>
                </div>
                <button className="export-all-btn" onClick={handleExportAll}>
                  🌍 Export Entire Instance
                </button>
                <div className="resource-list">
                  {RESOURCE_TYPES.map((resourceType) => (
                    <div
                      key={resourceType.id}
                      className="resource-item"
                      onClick={() => handleResourceTypeClick(resourceType)}
                    >
                      <span className="resource-icon">{resourceType.icon}</span>
                      <div className="resource-info">
                        <div className="resource-name">{resourceType.name}</div>
                        <div className="resource-description">{resourceType.description}</div>
                      </div>
                      <span className="resource-arrow">→</span>
                    </div>
                  ))}
                </div>
              </>
            )}

            {viewMode === 'resource-type' && (
              <>
                {loading ? (
                  <div className="proporter-loading">
                    <span>⏳ Loading {selectedResourceType?.name.toLowerCase()}...</span>
                  </div>
                ) : error ? (
                  <div className="proporter-error">
                    <span>❌ {error}</span>
                    <button onClick={() => selectedResourceType && handleResourceTypeClick(selectedResourceType)}>
                      Retry
                    </button>
                  </div>
                ) : resources.length === 0 ? (
                  <div className="proporter-empty">
                    <span>No {selectedResourceType?.name.toLowerCase()} found</span>
                  </div>
                ) : (
                  <div className="resource-list">
                    {resources.map((resource) => (
                      <div
                        key={resource.id}
                        className="resource-item"
                        onClick={() => handleResourceClick(resource)}
                      >
                        <span className="resource-icon">{selectedResourceType?.icon}</span>
                        <div className="resource-info">
                          <div className="resource-name">{resource.name}</div>
                          <div className="resource-description">ID: {resource.id}</div>
                        </div>
                        <span className="resource-arrow">→</span>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}

            {viewMode === 'instance-export' && (
              <>
                {loading ? (
                  <div className="proporter-loading">
                    <span>🔍 Scanning Jamf instance...</span>
                  </div>
                ) : error ? (
                  <div className="proporter-error">
                    <span>❌ {error}</span>
                    <button onClick={handleExportAll}>Retry</button>
                  </div>
                ) : (
                  <>
                    <div className="instance-summary">
                      <h4>📊 Instance Summary</h4>
                      {instanceSummary.map((summary) => (
                        <div key={summary.resource_type} className="summary-item">
                          <span className="summary-type">{summary.resource_type}</span>
                          <span className="summary-count">{summary.count} resources</span>
                        </div>
                      ))}
                    </div>
                    <div className="hcl-preview">
                      <h4>📝 Generated HCL</h4>
                      <pre>{instanceHCL}</pre>
                    </div>
                    <button className="download-btn" onClick={handleDownloadHCL}>
                      ⬇️ Download jamf_instance.tf
                    </button>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      )}

      {/* Resource Detail Panel */}
      {selectedResource && selectedResourceType && credentials && (
        <ResourceDetailPanel
          credentials={credentials}
          resourceType={selectedResourceType.id}
          resourceId={selectedResource.id}
          resourceName={selectedResource.name}
          onClose={() => setSelectedResource(null)}
        />
      )}
    </div>
  );
};

export default ProporterMenu;
