import LocalExecution from './LocalExecution';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 JamfTerraform Agent</h1>
        <p>Local Terraform Execution</p>
      </header>
      <LocalExecution />
    </div>
  );
}

export default App;
