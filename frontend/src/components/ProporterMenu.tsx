import React, { useState } from 'react';
import { ExecutionService, type JamfResourceListResponse } from '../services/ExecutionService';
import type { JamfCredentials } from '../types';
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

const ProporterMenu: React.FC<ProporterMenuProps> = ({ isEnabled, credentials }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedResourceType, setSelectedResourceType] = useState<ResourceType | null>(null);
  const [resources, setResources] = useState<JamfResource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleButtonClick = () => {
    if (isEnabled) {
      setIsExpanded(!isExpanded);
      // Reset state when closing
      if (isExpanded) {
        setSelectedResourceType(null);
        setResources([]);
        setError(null);
      }
    }
  };

  const handleResourceTypeClick = async (resourceType: ResourceType) => {
    if (!credentials) return;
    
    setSelectedResourceType(resourceType);
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
    setSelectedResourceType(null);
    setResources([]);
    setError(null);
  };

  const handleResourceClick = (resource: JamfResource) => {
    // TODO: Phase 3 - Generate HCL for selected resource
    console.log('Generate HCL for:', selectedResourceType?.id, resource.id);
    alert(`Coming soon: Generate HCL for ${resource.name}`);
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
              {selectedResourceType ? (
                <>
                  <button className="back-btn" onClick={handleBack}>←</button>
                  {selectedResourceType.icon} {selectedResourceType.name}
                </>
              ) : (
                '📦 Proporter - Import Config'
              )}
            </h3>
            <button
              className="close-btn"
              onClick={(e) => {
                e.stopPropagation();
                setIsExpanded(false);
                setSelectedResourceType(null);
                setResources([]);
              }}
            >
              ✕
            </button>
          </div>

          <div className="proporter-menu-content">
            {!selectedResourceType ? (
              // Resource type selection
              <>
                <div className="proporter-info">
                  <p>Select a resource type to import from your connected Jamf Pro instance.</p>
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
            ) : (
              // Resource list
              <>
                {loading ? (
                  <div className="proporter-loading">
                    <span>⏳ Loading {selectedResourceType.name.toLowerCase()}...</span>
                  </div>
                ) : error ? (
                  <div className="proporter-error">
                    <span>❌ {error}</span>
                    <button onClick={() => handleResourceTypeClick(selectedResourceType)}>
                      Retry
                    </button>
                  </div>
                ) : resources.length === 0 ? (
                  <div className="proporter-empty">
                    <span>No {selectedResourceType.name.toLowerCase()} found</span>
                  </div>
                ) : (
                  <div className="resource-list">
                    {resources.map((resource) => (
                      <div
                        key={resource.id}
                        className="resource-item"
                        onClick={() => handleResourceClick(resource)}
                      >
                        <span className="resource-icon">{selectedResourceType.icon}</span>
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
          </div>
        </div>
      )}
    </div>
  );
};

export default ProporterMenu;

