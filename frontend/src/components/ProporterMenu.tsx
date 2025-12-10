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
  { id: 'static-groups', name: 'Static Groups', icon: '📌', description: 'Import computer/mobile static groups' },
  { id: 'config-profiles', name: 'Configuration Profiles', icon: '⚙️', description: 'Import macOS/iOS configuration profiles' },
  { id: 'scripts', name: 'Scripts', icon: '📜', description: 'Import scripts from Jamf Pro' },
  { id: 'packages', name: 'Packages', icon: '📦', description: 'Import package metadata (files must be added manually)' },
  { id: 'jamf-app-catalog', name: 'Jamf App Catalog', icon: '🍎', description: 'Import Jamf App Catalog installers' },
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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Selection / Bulk Export State
  const [isSelecting, setIsSelecting] = useState(false);
  const [selection, setSelection] = useState<Set<string>>(new Set());
  const [includeDependencies, setIncludeDependencies] = useState(true);
  
  // Export progress state
  const [exportPhase, setExportPhase] = useState<'idle' | 'scanning' | 'downloading'>('idle');

  const handleToggleSelect = (type: string, id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    const key = `${type}:${id}`;
    const newSel = new Set(selection);
    if (newSel.has(key)) newSel.delete(key);
    else newSel.add(key);
    setSelection(newSel);
  };

  // Check if any packages are in the current selection
  const hasPackagesSelected = Array.from(selection).some(key => key.startsWith('packages:'));

  const handleBulkDownload = async () => {
    if (!credentials || selection.size === 0) return;
    
    setLoading(true);
    setError(null);
    const resources = Array.from(selection).map(key => {
        const [type, idStr] = key.split(':');
        return { type, id: parseInt(idStr) };
    });

    try {
      const blob = await ExecutionService.bulkExport(credentials, resources, includeDependencies);
      setLoading(false);

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'jamf_bulk_export.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      // Clear selection after download? Maybe optional.
      // setSelection(new Set()); 
      // setIsSelecting(false);
    } catch (err) {
      setLoading(false);
      setError(err instanceof Error ? err.message : 'Bulk export failed');
    }
  };

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
        setIsSelecting(false);
        setSelection(new Set());
        setIncludeDependencies(true);
      }
    }
  };

  const handleExportAll = async () => {
    if (!credentials) return;
    
    setLoading(true);
    setExportPhase('scanning');
    setError(null);
    setViewMode('instance-export');
    
    const response: JamfInstanceExportResponse = await ExecutionService.exportJamfInstance(credentials);
    
    setLoading(false);
    setExportPhase('idle');
    
    if (response.success) {
      setInstanceSummary(response.summary);
    } else {
      setError(response.error || 'Failed to export instance');
    }
  };

  // Download all resources from instance summary as ZIP with support files
  const handleDownloadInstanceZip = async () => {
    if (!credentials || instanceSummary.length === 0) return;
    
    setLoading(true);
    setExportPhase('downloading');
    setError(null);
    
    // Collect all resource IDs from the summary
    const allResources: Array<{ type: string; id: number }> = [];
    for (const summary of instanceSummary) {
      for (const item of summary.items) {
        allResources.push({ type: summary.resource_type, id: item.id });
      }
    }
    
    try {
      const blob = await ExecutionService.bulkExport(credentials, allResources, true);
      setLoading(false);
      setExportPhase('idle');
      
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'jamf_instance_export.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setLoading(false);
      setExportPhase('idle');
      setError(err instanceof Error ? err.message : 'Failed to download instance export');
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
              {viewMode === 'resource-type' && selectedResourceType && (
                <div className="header-title-row">
                  <span>{selectedResourceType.icon} {selectedResourceType.name}</span>
                  <button 
                    className={`select-mode-btn ${isSelecting ? 'active' : ''}`}
                    onClick={(e) => { e.stopPropagation(); setIsSelecting(!isSelecting); }}
                  >
                    {isSelecting ? 'Done' : 'Select'}
                  </button>
                </div>
              )}
              {viewMode === 'instance-export' && '📊 Instance Summary'}
            </h3>
            <button
              className="close-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(false);
                setViewMode('main');
                setSelectedResourceType(null);
                setResources([]);
                setIsSelecting(false);
                setSelection(new Set());
              }}
            >
              ✕
            </button>
          </div>
          
          {isSelecting && selection.size > 0 && (
            <div className="bulk-actions-bar">
               {hasPackagesSelected && (
                 <div className="package-warning-banner">
                    <span>📦 Package files (.pkg/.dmg) are NOT downloaded due to size. Use <a href="https://github.com/rtrouton/rtrouton_scripts/tree/main/rtrouton_scripts/Casper_Scripts/Jamf_Pro_JCDS_Installer_Package_Download" target="_blank" rel="noopener noreferrer">this script</a> to download them separately.</span>
                  </div>
               )}
               <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span className="selection-count">{selection.size} item{selection.size !== 1 ? 's' : ''}</span>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-secondary)' }}>
                      <input 
                         type="checkbox" 
                         checked={includeDependencies} 
                         onChange={(e) => setIncludeDependencies(e.target.checked)}
                         style={{ accentColor: 'var(--color-jamf-blue)', cursor: 'pointer' }}
                      />
                      <span>Include Dependencies</span>
                  </label>
               </div>
              <button className="bulk-download-btn" onClick={handleBulkDownload}>
                ⬇️ Download ZIP
              </button>
            </div>
          )}

          <div className="proporter-menu-content">
            {viewMode === 'main' && (
              <>
                <div className="proporter-info">
                  <p>Browse resources by type or scan your entire instance.</p>
                </div>
                <button className="export-all-btn" onClick={handleExportAll}>
                  📊 Instance Summary
                </button>
                <div className="section-divider">
                  <span>Browse by Type</span>
                </div>
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
                        className={`resource-item ${selectedResourceType && selection.has(`${selectedResourceType.id}:${resource.id}`) ? 'selected' : ''}`}
                        onClick={(e) => isSelecting && selectedResourceType ? handleToggleSelect(selectedResourceType.id, resource.id, e) : handleResourceClick(resource)}
                      >
                        {isSelecting && selectedResourceType && (
                            <input 
                                type="checkbox"
                                className="resource-checkbox"
                                checked={selection.has(`${selectedResourceType.id}:${resource.id}`)}
                                readOnly
                                style={{ marginRight: '10px' }}
                            />
                        )}
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
                {loading && exportPhase === 'scanning' ? (
                  <div className="proporter-loading">
                    <div className="export-progress">
                      <div className="progress-spinner"></div>
                      <div className="progress-text">
                        <span className="progress-title">🔍 Scanning Jamf Instance</span>
                        <span className="progress-detail">Discovering resources and dependencies...</span>
                      </div>
                    </div>
                  </div>
                ) : loading && exportPhase === 'downloading' ? (
                  <div className="proporter-loading">
                    <div className="export-progress">
                      <div className="progress-spinner"></div>
                      <div className="progress-text">
                        <span className="progress-title">📦 Generating Export</span>
                        <span className="progress-detail">
                          Processing {instanceSummary.reduce((sum, s) => sum + s.count, 0)} resources...
                        </span>
                        <span className="progress-hint">Downloading scripts and configuration profiles</span>
                      </div>
                    </div>
                  </div>
                ) : error ? (
                  <div className="proporter-error">
                    <span>❌ {error}</span>
                    <button onClick={handleExportAll}>Retry</button>
                  </div>
                ) : (
                  <>
                    <div className="instance-summary">
                      <h4>🏢 Your Jamf Pro Instance</h4>
                      <div className="summary-total">
                        {instanceSummary.reduce((sum, s) => sum + s.count, 0)} total resources
                      </div>
                      {instanceSummary.map((summary) => (
                        <div key={summary.resource_type} className="summary-item">
                          <span className="summary-type">{summary.resource_type}</span>
                          <span className="summary-count">{summary.count} resources</span>
                        </div>
                      ))}
                    </div>
                    <div className="package-warning-banner" style={{ marginBottom: '12px' }}>
                      <span>📦 Package files (.pkg/.dmg) are NOT downloaded due to size. Use <a href="https://github.com/rtrouton/rtrouton_scripts/tree/main/rtrouton_scripts/Casper_Scripts/Jamf_Pro_JCDS_Installer_Package_Download" target="_blank" rel="noopener noreferrer">this script</a> to download them separately.</span>
                    </div>
                    <button className="download-btn" onClick={handleDownloadInstanceZip} disabled={loading}>
                      <span className="btn-icon">⬇️</span>
                      <span className="btn-text">Download as Terraform (ZIP)</span>
                    </button>
                    <div className="export-hint">
                      <small>Generates production-ready .tf files with dependencies</small>
                    </div>
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
