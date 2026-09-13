import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatView from './components/ChatView';
import AgentsView from './components/AgentsView';
import SkillsView from './components/SkillsView';
import PipelinesView from './components/PipelinesView';
import ToolsView from './components/ToolsView';
import AgencyView from './components/AgencyView';
import Dashboard from './components/Dashboard';
import AuthView from './components/AuthView';
import KnowledgeView from './components/KnowledgeView';
import EvalView from './components/EvalView';
import IntegrationsView from './components/IntegrationsView';
import BillingView from './components/BillingView';
import PipelineBuilderView from './components/PipelineBuilderView';
import PipelineFlowBuilder from './components/PipelineFlowBuilder';
import ClientPortalView from './components/ClientPortalView';
import LandingPageView from './components/LandingPageView';
import AnalyticsView from './components/AnalyticsView';

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
      case 'auth':
        return <AuthView />;
      case 'knowledge':
        return <KnowledgeView />;
      case 'eval':
        return <EvalView />;
      case 'integrations':
        return <IntegrationsView />;
      case 'billing':
        return <BillingView />;
      case 'pipeline-builder':
        return <PipelineBuilderView />;
      case 'pipeline-flow':
        return <PipelineFlowBuilder />;
      case 'client-portal':
        return <ClientPortalView />;
      case 'landing':
        return <LandingPageView setActiveView={setActiveView} />;
      case 'analytics':
        return <AnalyticsView />;
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
