import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">CG</span>
          <span>CareerGraph</span>
        </div>

        <div className="status">
          <span className="status-dot" />
          GRAPH ONLINE
        </div>
      </header>

      <Dashboard />
    </div>
  );
}

export default App;