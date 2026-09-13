import { useState, useEffect } from 'react';
import ProductionApp from './components/production/ProductionApp';
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
import MarketplaceView from './components/MarketplaceView';
import RealtimeView from './components/RealtimeView';
import AuditView from './components/AuditView';
import TeamsView from './components/TeamsView';
import ZapierView from './components/ZapierView';
import PrivacyPolicyView from './components/PrivacyPolicyView';
import TermsView from './components/TermsView';
import FreeDomainView from './components/FreeDomainView';
import FreeLLMView from './components/FreeLLMView';
import LoopsView from './components/LoopsView';
import CuratedToolsView from './components/CuratedToolsView';
import VoiceView from './components/VoiceView';
import BetaView from './components/BetaView';
import ProdLaunchView from './components/ProdLaunchView';
import MRR30KView from './components/MRR30KView';
import MRR100KView from './components/MRR100KView';
import EnterpriseView from './components/EnterpriseView';
import MRR1MView from './components/MRR1MView';
import BetaZeroView from './components/BetaZeroView';

// نظام متكامل يعمل بشكل حقيقي مثل Manus و ChatGPT و Arena.ai
// - الوضع الافتراضي: ProductionApp نظيف مثل Arena.ai — Chat, Agents, Projects فقط — يعمل فعلياً
// - وضع الإدارة: ?admin=1 أو localStorage isAdmin=true — يعرض كل الأدوات الداخلية MRR, Enterprise, Beta Zero — مخفي عن المستخدم العادي

function App() {
  const [mode, setMode] = useState<'production' | 'admin-old'>('production');
  const [activeView, setActiveView] = useState('dashboard');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    // إذا طلب admin-old — اعرض الواجهة القديمة بكل الأزرار — للتوافق
    if (params.get('admin-old') === '1') {
      setMode('admin-old');
    }
    // الوضع الافتراضي الآن هو production نظيف مثل Manus و Arena.ai
    // للوصول للواجهة القديمة: ?admin-old=1
    // للإدارة في الواجهة الجديدة: ?admin=1
  }, []);

  // وضع الإنتاج النظيف — مثل Manus و ChatGPT و Arena.ai — افتراضي
  if (mode === 'production') {
    return <ProductionApp />;
  }

  // وضع الإدارة القديم — 38 زر — فقط إذا طلب ?admin-old=1 — للتوافق والاختبار
  const renderView = () => {
    switch (activeView) {
      case 'dashboard': return <Dashboard />;
      case 'chat': return <ChatView />;
      case 'agents': return <AgentsView />;
      case 'skills': return <SkillsView />;
      case 'pipelines': return <PipelinesView />;
      case 'tools': return <ToolsView view="tools" />;
      case 'memory': return <ToolsView view="memory" />;
      case 'agency': return <AgencyView />;
      case 'security': return <ToolsView view="security" />;
      case 'auth': return <AuthView />;
      case 'knowledge': return <KnowledgeView />;
      case 'eval': return <EvalView />;
      case 'integrations': return <IntegrationsView />;
      case 'billing': return <BillingView />;
      case 'pipeline-builder': return <PipelineBuilderView />;
      case 'pipeline-flow': return <PipelineFlowBuilder />;
      case 'client-portal': return <ClientPortalView />;
      case 'landing': return <LandingPageView setActiveView={setActiveView} />;
      case 'analytics': return <AnalyticsView />;
      case 'marketplace': return <MarketplaceView />;
      case 'realtime': return <RealtimeView />;
      case 'audit': return <AuditView />;
      case 'teams': return <TeamsView />;
      case 'zapier': return <ZapierView />;
      case 'privacy': return <PrivacyPolicyView />;
      case 'terms': return <TermsView />;
      case 'free-domain': return <FreeDomainView />;
      case 'free-llm': return <FreeLLMView />;
      case 'loops': return <LoopsView />;
      case 'curated-tools': return <CuratedToolsView />;
      case 'voice': return <VoiceView />;
      case 'beta': return <BetaView />;
      case 'prod-launch': return <ProdLaunchView />;
      case 'mrr-30k': return <MRR30KView />;
      case 'mrr-100k': return <MRR100KView />;
      case 'enterprise': return <EnterpriseView />;
      case 'mrr-1m': return <MRR1MView />;
      case 'beta-zero': return <BetaZeroView />;
      default: return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-zinc-50 overflow-hidden" dir="rtl">
      <div className="fixed top-2 left-2 z-50 bg-amber-100 border border-amber-300 text-amber-800 text-xs px-3 py-1.5 rounded-full">
        وضع قديم — 38 زر — للواجهة النظيفة احذف ?admin-old=1 من الرابط — <button onClick={() => { window.location.href = window.location.pathname; }} className="underline font-medium">العودة للنظيف</button>
      </div>
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <div className="flex-1 flex overflow-hidden">
        {renderView()}
      </div>
    </div>
  );
}

export default App;
