import type { GenerateHCLRequest, GenerateHCLResponse } from '../types';

// Always use Railway backend (local backend not running)
const API_BASE_URL = 'https://jamfaform-production.up.railway.app';

export class ExecutionService {
  /**
   * Generate HCL configuration from a prompt.
   * This is the centralized execution API call as per workspace rules.
   */
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
}
