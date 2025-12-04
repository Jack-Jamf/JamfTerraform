import { useState, useEffect } from 'react';
import type { TabType } from './types';
import { ExecutionService } from './services/ExecutionService';
import TabBar from './components/TabBar';
import Chat from './components/Chat';
import Cookbook from './components/Cookbook';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('chat');
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline'>('offline');
  const [selectedRecipe, setSelectedRecipe] = useState<string | null>(null);

  useEffect(() => {
    // Check backend health on mount
    const checkHealth = async () => {
      const isHealthy = await ExecutionService.healthCheck();
      setBackendStatus(isHealthy ? 'online' : 'offline');
    };

    checkHealth();

    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleRecipeSelect = (prompt: string) => {
    setSelectedRecipe(prompt);
    setActiveTab('chat');
    // The Chat component will handle the selected recipe via props
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'chat':
        return <Chat selectedRecipe={selectedRecipe} onRecipeUsed={() => setSelectedRecipe(null)} />;
      case 'cookbook':
        return <Cookbook onRecipeSelect={handleRecipeSelect} />;
      default:
        return <Chat selectedRecipe={selectedRecipe} onRecipeUsed={() => setSelectedRecipe(null)} />;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-title-section">
          <div className="app-logo">🚀</div>
          <div>
            <h1 className="app-title">JamfTerraform</h1>
            <p className="app-subtitle">AI-Powered Terraform Generator</p>
          </div>
        </div>
        <div className="app-status">
          <div className={`status-indicator ${backendStatus}`}></div>
          <span>Backend {backendStatus === 'online' ? 'Connected' : 'Offline'}</span>
        </div>
      </header>

      <div className="app-content">
        <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
        <div className="tab-content">{renderTabContent()}</div>
      </div>
    </div>
  );
}

export default App;
