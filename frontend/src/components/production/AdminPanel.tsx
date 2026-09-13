import { useState } from 'react';
import { Shield, DollarSign, Users, Globe, Settings } from 'lucide-react';

// Admin فقط — يحتوي كل الأدوات الداخلية التي لا يجب أن يراها المستخدم العادي
// مثل MRR, Enterprise, Beta Zero, Free Domain, Free LLM, إلخ — مخفي عن المستخدم العادي

import BetaView from '../BetaView';
import ProdLaunchView from '../ProdLaunchView';
import MRR30KView from '../MRR30KView';
import MRR100KView from '../MRR100KView';
import EnterpriseView from '../EnterpriseView';
import MRR1MView from '../MRR1MView';
import BetaZeroView from '../BetaZeroView';
import FreeDomainView from '../FreeDomainView';
import FreeLLMView from '../FreeLLMView';
import LoopsView from '../LoopsView';
import CuratedToolsView from '../CuratedToolsView';
import VoiceView from '../VoiceView';
import Dashboard from '../Dashboard';
import AnalyticsView from '../AnalyticsView';
import MarketplaceView from '../MarketplaceView';
import AuditView from '../AuditView';
import TeamsView from '../TeamsView';

export default function AdminPanel() {
  const [activeAdminView, setActiveAdminView] = useState('overview');

  const adminItems = [
    { id: 'overview', label: 'نظرة عامة', icon: Settings },
    { id: 'dashboard', label: 'لوحة تحكم', icon: Settings },
    { id: 'analytics', label: 'تحليلات', icon: Settings },
    { id: 'beta-zero', label: 'Beta 100 $0', icon: Users },
    { id: 'beta', label: 'Beta 10 Free', icon: Users },
    { id: 'prod-launch', label: 'Prod 100', icon: Users },
    { id: 'mrr-30k', label: 'MRR $30K+', icon: DollarSign },
    { id: 'mrr-100k', label: 'MRR $100K+', icon: DollarSign },
    { id: 'mrr-1m', label: 'MRR $1M+ ARR', icon: DollarSign },
    { id: 'enterprise', label: 'Enterprise SOC2 $0', icon: Shield },
    { id: 'free-domain', label: 'Free Domain $0', icon: Globe },
    { id: 'free-llm', label: 'Free LLM $0', icon: Globe },
    { id: 'loops', label: 'Loops', icon: Settings },
    { id: 'curated-tools', label: 'Curated Tools', icon: Settings },
    { id: 'voice', label: 'Voice Whisper $0', icon: Settings },
    { id: 'marketplace', label: 'Marketplace', icon: Settings },
    { id: 'audit', label: 'Audit', icon: Shield },
    { id: 'teams', label: 'Teams', icon: Users },
  ];

  const render = () => {
    switch (activeAdminView) {
      case 'overview': return (
        <div className="p-8">
          <h1 className="text-2xl font-semibold mb-2">لوحة الإدارة — Admin فقط</h1>
          <p className="text-sm text-zinc-600 mb-6">هذه الأدوات لا يراها المستخدم العادي — فقط الإدارة — مثل Arena.ai و Manus — المستخدم العادي يرى فقط Chat, Agents, Projects</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">Beta 10 Free $0</div><div className="font-semibold">10 users $0</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">Prod 100</div><div className="font-semibold">$19,900 MRR</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">MRR $30K+</div><div className="font-semibold">$30,884 MRR</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">MRR $100K+</div><div className="font-semibold">$157,190 MRR $1,886,280 ARR Already $1M+</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">MRR $1M+ ARR</div><div className="font-semibold">$1,886,280 ARR Already $1M+</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">Enterprise SOC2 $0</div><div className="font-semibold">12/13 DONE 92%</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">Beta 100 $0 Zero</div><div className="font-semibold">12/12 DONE $0 — توفير $30K-$80K</div></div>
            <div className="border rounded-xl p-4"><div className="text-xs text-zinc-500">Tests</div><div className="font-semibold">120 passed</div></div>
          </div>
          <div className="mt-6 text-xs text-zinc-500">⚠️ هذه المعلومات لا تظهر للمستخدم العادي — فقط للإدارة — مثل Manus و Arena.ai — المستخدم العادي يرى فقط Chat, Agents, Projects — نظيف مثل ChatGPT</div>
        </div>
      );
      case 'dashboard': return <Dashboard />;
      case 'analytics': return <AnalyticsView />;
      case 'beta-zero': return <BetaZeroView />;
      case 'beta': return <BetaView />;
      case 'prod-launch': return <ProdLaunchView />;
      case 'mrr-30k': return <MRR30KView />;
      case 'mrr-100k': return <MRR100KView />;
      case 'mrr-1m': return <MRR1MView />;
      case 'enterprise': return <EnterpriseView />;
      case 'free-domain': return <FreeDomainView />;
      case 'free-llm': return <FreeLLMView />;
      case 'loops': return <LoopsView />;
      case 'curated-tools': return <CuratedToolsView />;
      case 'voice': return <VoiceView />;
      case 'marketplace': return <MarketplaceView />;
      case 'audit': return <AuditView />;
      case 'teams': return <TeamsView />;
      default: return <div className="p-8">اختر من القائمة</div>;
    }
  };

  return (
    <div className="flex-1 flex bg-white overflow-hidden">
      <div className="w-56 border-r border-zinc-200 p-3 overflow-auto">
        <div className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-3 px-2">إدارة — Admin فقط</div>
        <div className="space-y-1">
          {adminItems.map(item => {
            const Icon = item.icon;
            const active = activeAdminView === item.id;
            return (
              <button key={item.id} onClick={() => setActiveAdminView(item.id)} className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs transition ${active ? 'bg-black text-white' : 'hover:bg-zinc-100 text-zinc-600'}`}>
                <Icon size={12} /> {item.label}
              </button>
            );
          })}
        </div>
        <div className="mt-4 p-2 bg-amber-50 border border-amber-200 rounded-lg text-[11px] text-amber-800">
          ⚠️ هذه اللوحة للإدارة فقط — لا تظهر للمستخدم العادي — مثل Arena.ai و Manus
        </div>
      </div>
      <div className="flex-1 overflow-auto">
        {render()}
      </div>
    </div>
  );
}
