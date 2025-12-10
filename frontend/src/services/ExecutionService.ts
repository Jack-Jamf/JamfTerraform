import type { GenerateHCLRequest, GenerateHCLResponse, JamfCredentials, JamfAuthResponse } from '../types';

// Production API URL
export const API_BASE_URL = 'https://jamfaform-production.up.railway.app';
// const API_BASE_URL = 'http://localhost:8000';  // For local testing


export interface JamfResourceListResponse {
  resources: Array<{ id: number; name: string }>;
  resource_type: string;
  success: boolean;
  error?: string;
}

export class ExecutionService {
  /**
   * Generate HCL configuration from a prompt.
   * This is the centralized execution API call as per workspace rules.
   */
  static async bulkExport(
    credentials: JamfCredentials,
    resources: Array<{ type: string; id: number }>,
    includeDependencies: boolean = true
  ): Promise<Blob> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jamf/bulk-export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentials: {
             url: credentials.url,
             username: credentials.username,
             password: credentials.password
          },
          resources,
          include_dependencies: includeDependencies
        }),
      });

      if (!response.ok) {
         const errorText = await response.text();
         console.error('Bulk export failed', errorText);
         
         // Try to parse as JSON for better error message
         try {
           const errorJson = JSON.parse(errorText);
           throw new Error(errorJson.detail || errorJson.message || `Export failed with status ${response.status}`);
         } catch {
           throw new Error(`Export failed: ${response.statusText} (${response.status})`);
         }
      }
      
      // Verify we're receiving a ZIP file, not an error response
      // Note: CORS must expose Content-Type header for this check to work
      const contentType = response.headers.get('Content-Type');
      const contentDisposition = response.headers.get('Content-Disposition');
      const contentLength = response.headers.get('Content-Length');
      
      console.log('Export response headers:', {
        contentType,
        contentDisposition,
        contentLength
      });
      
      // Only validate Content-Type if it's available (CORS might not expose it)
      if (contentType && !contentType.includes('application/zip') && !contentType.includes('application/octet-stream')) {
        console.error(`Unexpected content type: ${contentType}`);
        const errorBody = await response.text();
        console.error('Response body:', errorBody);
        throw new Error('Server returned invalid response. Expected ZIP file but received: ' + contentType);
      }
      
      return await response.blob();
    } catch (e) {
      console.error('Bulk export error:', e);
      // Re-throw error so calling code can display message to user
      throw e;
    }
  }

  static async generateHCL(request: GenerateHCLRequest): Promise<GenerateHCLResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: GenerateHCLResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Failed to generate HCL:', error);
      return {
        hcl: '',
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Check backend health status.
   */
  static async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/healthz`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Fetch cookbook modules from backend.
   */
  static async getCookbook(): Promise<import('../types').CookbookData> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/cookbook`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Failed to fetch cookbook:', error);
      // Return empty cookbook on error
      return { modules: [] };
    }
  }

  /**
   * List resources from a Jamf Pro instance.
   */
  static async listJamfResources(
    credentials: JamfCredentials,
    resourceType: string
  ): Promise<JamfResourceListResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jamf/resources`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentials: {
            url: credentials.url,
            username: credentials.username,
            password: credentials.password,
          },
          resource_type: resourceType,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to list Jamf resources:', error);
      return {
        resources: [],
        resource_type: resourceType,
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Export entire Jamf Pro instance or selected resource types.
   */
  static async exportJamfInstance(
    credentials: JamfCredentials,
    selectedTypes?: string[]
  ): Promise<JamfInstanceExportResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jamf/instance-export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentials: {
            url: credentials.url,
            username: credentials.username,
            password: credentials.password,
          },
          selected_types: selectedTypes || [],
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to export Jamf instance:', error);
      return {
        summary: [],
        hcl: '',
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Get detailed information about a specific resource.
   */
  static async getResourceDetail(
    credentials: JamfCredentials,
    resourceType: string,
    resourceId: number
  ): Promise<JamfResourceDetailResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jamf/resource-detail`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentials: {
            url: credentials.url,
            username: credentials.username,
            password: credentials.password,
          },
          resource_type: resourceType,
          resource_id: resourceId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to get resource detail:', error);
      return {
        resource: {},
        dependencies: [],
        hcl: '',
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Verify Jamf Pro credentials.
   */
  static async verifyAuth(credentials: JamfCredentials): Promise<JamfAuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/jamf/verify-auth`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credentials: {
            url: credentials.url,
            username: credentials.username,
            password: credentials.password,
          }
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to verify auth:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }
}

export interface JamfInstanceSummary {
  resource_type: string;
  count: number;
  items: Array<{ id: number; name: string }>;
}

export interface JamfInstanceExportResponse {
  summary: JamfInstanceSummary[];
  hcl: string;
  success: boolean;
  error?: string;
}

export interface ResourceDependency {
  type: string;
  id: number;
  name: string;
}

export interface JamfResourceDetailResponse {
  resource: any;
  dependencies: ResourceDependency[];
  hcl: string;
  bundle_hcl?: string;
  success: boolean;
  error?: string;
}
