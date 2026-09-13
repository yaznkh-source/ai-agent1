import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatView from './components/ChatView';
import AgentsView from './components/AgentsView';
import SkillsView from './components/SkillsView';
import PipelinesView from './components/PipelinesView';
import ToolsView from './components/ToolsView';
import AgencyView from './components/AgencyView';
import Dashboard from './components/Dashboard';

function App() {
  const [activeView, setActiveView] = useState('dashboard');

  const renderView = () => {
    switch (activeView) {
      case 'dashboard':
        return <Dashboard />;
      case 'chat':
        return <ChatView />;
      case 'agents':
        return <AgentsView />;
      case 'skills':
        return <SkillsView />;
      case 'pipelines':
        return <PipelinesView />;
      case 'tools':
        return <ToolsView view="tools" />;
      case 'memory':
        return <ToolsView view="memory" />;
      case 'agency':
        return <AgencyView />;
      case 'security':
        return <ToolsView view="security" />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-zinc-50 overflow-hidden" dir="rtl">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <div className="flex-1 flex overflow-hidden">
        {renderView()}
      </div>
    </div>
  );
}

export default App;
