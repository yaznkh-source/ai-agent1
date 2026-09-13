import { useEffect, useState } from 'react';
import { chatApi } from '../lib/api';
import { useChatStore } from '../stores/chat';
import { MessageSquare, Plus, Trash2, Bot, Zap, Brain, Wrench, Workflow, Shield, LayoutDashboard, Lock, BookOpen, BarChart3, Plug, CreditCard, Users, GitBranch, FileText, Globe, LineChart, ShoppingBag, Radio, ClipboardList, Users2, Zap as ZapIcon } from 'lucide-react';

interface SidebarProps {
  activeView: string;
  setActiveView: (view: string) => void;
}

export default function Sidebar({ activeView, setActiveView }: SidebarProps) {
  const { chats, setChats, setCurrentChat, setMessages } = useChatStore();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadChats();
  }, []);

  const loadChats = async () => {
    setLoading(true);
    try {
      const data = await chatApi.list();
      setChats(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const createNewChat = async () => {
    try {
      const newChat = await chatApi.create({ title: 'New Chat', model: 'gpt-4o-mini' });
      setChats([newChat, ...chats]);
      setCurrentChat(newChat);
      setMessages([]);
      setActiveView('chat');
    } catch (e) {
      console.error(e);
    }
  };

  const selectChat = async (chat: any) => {
    try {
      const fullChat = await chatApi.get(chat.id);
      setCurrentChat(fullChat);
      setMessages(fullChat.messages || []);
      setActiveView('chat');
    } catch (e) {
      console.error(e);
    }
  };

  const deleteChat = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await chatApi.delete(id);
      setChats(chats.filter(c => c.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  const menuItems = [
    { id: 'landing', label: 'الموقع التسويقي', labelEn: 'Landing', icon: Globe, track: 'B' },
    { id: 'dashboard', label: 'لوحة التحكم', labelEn: 'Dashboard', icon: LayoutDashboard, track: 'ABCD' },
    { id: 'analytics', label: 'التحليلات', labelEn: 'Analytics', icon: LineChart, track: 'B' },
    { id: 'marketplace', label: 'المتجر', labelEn: 'Marketplace', icon: ShoppingBag, track: 'B' },
    { id: 'realtime', label: 'الوقت الحقيقي', labelEn: 'Realtime', icon: Radio, track: 'C' },
    { id: 'audit', label: 'التدقيق', labelEn: 'Audit', icon: ClipboardList, track: 'C' },
    { id: 'teams', label: 'الفريق', labelEn: 'Teams', icon: Users2, track: 'B' },
    { id: 'zapier', label: 'Zapier/Make', labelEn: 'Zapier', icon: ZapIcon, track: 'C' },
    { id: 'chat', label: 'المحادثات', labelEn: 'Chat', icon: MessageSquare, track: 'A' },
    { id: 'agents', label: 'الوكلاء', labelEn: 'Agents', icon: Bot, track: 'D' },
    { id: 'skills', label: 'المهارات', labelEn: 'Skills', icon: Zap, track: 'D' },
    { id: 'pipelines', label: 'مسارات العمل', labelEn: 'Pipelines', icon: Workflow, track: 'C' },
    { id: 'pipeline-builder', label: 'منشئ المسارات', labelEn: 'Builder', icon: GitBranch, track: 'D' },
    { id: 'pipeline-flow', label: 'منشئ Flow', labelEn: 'Flow Builder', icon: GitBranch, track: 'D' },
    { id: 'tools', label: 'الأدوات', labelEn: 'Tools', icon: Wrench, track: 'A' },
    { id: 'memory', label: 'الذاكرة', labelEn: 'Memory', icon: Brain, track: 'A' },
    { id: 'knowledge', label: 'المعرفة RAG', labelEn: 'Knowledge', icon: BookOpen, track: 'A' },
    { id: 'agency', label: 'الوكالة', labelEn: 'Agency', icon: Users, track: 'A' },
    { id: 'client-portal', label: 'بوابة العميل', labelEn: 'Client Portal', icon: FileText, track: 'A' },
    { id: 'security', label: 'الأمان', labelEn: 'Security', icon: Shield, track: 'C' },
    { id: 'auth', label: 'المصادقة', labelEn: 'Auth', icon: Lock, track: 'B' },
    { id: 'billing', label: 'الفوترة', labelEn: 'Billing', icon: CreditCard, track: 'B' },
    { id: 'eval', label: 'التقييم', labelEn: 'Eval', icon: BarChart3, track: 'B' },
    { id: 'integrations', label: 'التكاملات', labelEn: 'Integrations', icon: Plug, track: 'C' },
    { id: 'privacy', label: 'الخصوصية', labelEn: 'Privacy', icon: Shield, track: 'B' },
    { id: 'terms', label: 'الشروط', labelEn: 'Terms', icon: FileText, track: 'B' },
    { id: 'free-domain', label: 'نطاق مجاني', labelEn: 'Free Domain', icon: Globe, track: 'D' },
    { id: 'free-llm', label: 'نماذج مجانية', labelEn: 'Free LLM', icon: Brain, track: 'D' },
    { id: 'loops', label: 'حلقات طويلة', labelEn: 'Loops', icon: Workflow, track: 'D' },
    { id: 'curated-tools', label: 'أدوات منتقاة', labelEn: 'Curated Tools', icon: Wrench, track: 'D' },
    { id: 'voice', label: 'الصوت Whisper', labelEn: 'Voice Whisper', icon: Radio, track: 'D' },
  ];

  return (
    <div className="w-72 bg-zinc-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-zinc-800">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center font-bold text-lg glow">
            AI
          </div>
          <div>
            <h1 className="font-bold text-lg">AI Agency OS</h1>
            <p className="text-xs text-zinc-400">ECC + Open WebUI</p>
          </div>
        </div>
        
        <button
          onClick={createNewChat}
          className="w-full flex items-center gap-2 px-4 py-2.5 bg-violet-600 hover:bg-violet-700 rounded-xl transition-colors font-medium"
        >
          <Plus size={18} />
          محادثة جديدة
        </button>
      </div>

      {/* Navigation */}
      <div className="p-3 border-b border-zinc-800">
        <div className="grid grid-cols-2 gap-2">
          {menuItems.map(item => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id)}
                className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm transition-all ${
                  isActive 
                    ? 'bg-zinc-800 text-white shadow-lg' 
                    : 'text-zinc-400 hover:text-white hover:bg-zinc-800/50'
                }`}
              >
                <Icon size={16} />
                <span className="truncate">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-3">
        <h3 className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-3 px-2">
          المحادثات الأخيرة
        </h3>
        
        {loading ? (
          <div className="text-zinc-500 text-sm px-2">جاري التحميل...</div>
        ) : chats.length === 0 ? (
          <div className="text-zinc-500 text-sm px-2">لا توجد محادثات</div>
        ) : (
          <div className="space-y-1">
            {chats.map((chat: any) => (
              <div
                key={chat.id}
                onClick={() => selectChat(chat)}
                className="group flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-zinc-800 cursor-pointer transition-colors"
              >
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <MessageSquare size={14} className="text-zinc-500 flex-shrink-0" />
                  <span className="text-sm truncate">{chat.title}</span>
                </div>
                <button
                  onClick={(e) => deleteChat(chat.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-zinc-700 rounded-lg transition-all"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-zinc-800">
        <div className="bg-zinc-800/50 rounded-xl p-3">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium">النظام نشط v2 - ABCD</span>
          </div>
          <div className="text-xs text-zinc-400 space-y-1">
            <div>🤖 35 وكيل متخصص (هدف 68)</div>
            <div>⚡ 30 مهارة جاهزة (هدف 292)</div>
            <div>🔧 9 أدوات + 6 Functions</div>
            <div>🧠 RAG + ChromaDB</div>
            <div>🔐 Auth + Billing + Eval</div>
            <div>🔌 Slack/GitHub/n8n</div>
            <div>🛡️ AgentShield نشط</div>
          </div>
          <div className="mt-3 grid grid-cols-4 gap-1 text-[9px]">
            <div className="bg-violet-600 text-white px-1 py-0.5 rounded text-center">A Freelance</div>
            <div className="bg-blue-600 text-white px-1 py-0.5 rounded text-center">B SaaS</div>
            <div className="bg-green-600 text-white px-1 py-0.5 rounded text-center">C Team</div>
            <div className="bg-amber-600 text-white px-1 py-0.5 rounded text-center">D Intel</div>
          </div>
        </div>
      </div>
    </div>
  );
}
