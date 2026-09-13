import { useEffect, useState } from 'react';
import { agentsApi } from '../../lib/api';
import { Bot, Zap, ArrowRight } from 'lucide-react';
import { useChatStore } from '../../stores/chat';

interface Props {
  setActiveView: (v: string) => void;
}

export default function ProductionAgents({ setActiveView }: Props) {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => { load(); }, []);
  const load = async () => {
    setLoading(true);
    try {
      const data = await agentsApi.list();
      setAgents(data.agents || []);
    } catch {}
    setLoading(false);
  };

  const categories = ['all', ...Array.from(new Set(agents.map((a: any) => a.category).filter(Boolean)))];
  const filtered = filter === 'all' ? agents : agents.filter((a: any) => a.category === filter);

  const useAgent = (agentId: string) => {
    useChatStore.getState().setSelectedAgent(agentId);
    setActiveView('chat');
  };

  if (loading) return <div className="flex-1 flex items-center justify-center">جاري تحميل 68 وكيل...</div>;

  return (
    <div className="flex-1 overflow-auto bg-white">
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold mb-1">الوكلاء — 68 متخصص</h1>
          <p className="text-sm text-zinc-600">مثل Manus و GPT Store — كل وكيل له مهارات وأدوات حقيقية — يعمل فعلياً</p>
        </div>

        <div className="flex gap-2 mb-6 overflow-x-auto">
          {categories.slice(0, 10).map(cat => (
            <button key={cat} onClick={() => setFilter(cat)} className={`px-3 py-1.5 rounded-full text-xs border whitespace-nowrap ${filter === cat ? 'bg-black text-white border-black' : 'bg-white border-zinc-200 hover:bg-zinc-50'}`}>
              {cat === 'all' ? `الكل ${agents.length}` : cat}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((agent: any) => (
            <div key={agent.id} className="border border-zinc-200 rounded-xl p-4 hover:shadow-md transition bg-white group">
              <div className="flex items-start justify-between mb-3">
                <div className="w-9 h-9 rounded-lg bg-black text-white flex items-center justify-center">
                  <Bot size={16} />
                </div>
                <span className="text-[10px] px-2 py-1 bg-zinc-100 rounded-full">{agent.category || 'general'}</span>
              </div>
              <div className="font-medium text-sm mb-1">{agent.name}</div>
              <div className="text-xs text-zinc-500 mb-1">{agent.role || agent.id}</div>
              <div className="text-xs text-zinc-600 line-clamp-2 leading-relaxed mb-3">{agent.description || 'وكيل متخصص يعمل فعلياً'}</div>
              <div className="flex items-center gap-2 mb-3">
                <div className="flex items-center gap-1 text-[11px] text-zinc-500"><Zap size={10} /> {agent.skills?.length || 0} مهارة</div>
                <div className="flex items-center gap-1 text-[11px] text-zinc-500">🔧 {agent.tools?.length || 0} أداة</div>
              </div>
              <button onClick={() => useAgent(agent.id)} className="w-full flex items-center justify-center gap-1.5 py-2 bg-black text-white rounded-lg text-xs font-medium hover:bg-zinc-800 group-hover:gap-2 transition-all">
                استخدم الوكيل <ArrowRight size={12} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
