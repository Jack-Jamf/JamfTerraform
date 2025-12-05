import { useState, useEffect } from "react";
import type { JamfCredentials } from "./types";
import { ExecutionService } from "./services/ExecutionService";
import Chat from "./components/Chat";
import CookbookMenu from "./components/CookbookMenu";
import JamfStatus from "./components/JamfStatus";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState<"online" | "offline">(
    "offline"
  );
  const [selectedRecipe, setSelectedRecipe] = useState<string | null>(null);
  const [, setJamfCredentials] = useState<JamfCredentials | null>(null);

  useEffect(() => {
    // Check backend health on mount
    const checkHealth = async () => {
      const isHealthy = await ExecutionService.healthCheck();
      setBackendStatus(isHealthy ? "online" : "offline");
    };

    checkHealth();

    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleRecipeSelect = (prompt: string) => {
    setSelectedRecipe(prompt);
    // The Chat component will handle the selected recipe via props
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
        <div className="app-status-group">
          <CookbookMenu onRecipeSelect={handleRecipeSelect} />
          <JamfStatus onCredentialsChange={setJamfCredentials} />
          <div className="app-status">
            <div className={`status-indicator ${backendStatus}`}></div>
            <span>
              Status {backendStatus === "online" ? "Connected" : "Offline"}
            </span>
          </div>
        </div>
      </header>

      <div className="app-content">
        <div className="tab-content">
          <Chat
            selectedRecipe={selectedRecipe}
            onRecipeUsed={() => setSelectedRecipe(null)}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
