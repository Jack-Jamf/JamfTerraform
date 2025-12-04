export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface GenerateHCLRequest {
  prompt: string;
  context?: string;
}

export interface GenerateHCLResponse {
  hcl: string;
  success: boolean;
  error?: string;
}

export type TabType = 'chat' | 'cookbook';

export interface CookbookModule {
  id: string;
  title: string;
  description: string;
  category: string;
  icon: string;
  tags: string[];
  prompt: string;
}

export interface CookbookData {
  modules: CookbookModule[];
}

