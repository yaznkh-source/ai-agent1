import { useEffect, useState } from 'react';
import { chatApi } from '../../lib/api';
import { useChatStore } from '../../stores/chat';
import { MessageSquare, Plus, Trash2, Bot, LayoutDashboard, Users, FileText, Settings, Shield, Sparkles, LogOut, Swords, Trophy, Smartphone } from 'lucide-react';

interface Props {
  activeView: string;
  setActiveView: (v: string) => void;
  isAdmin: boolean;
}

export default function ProductionSidebar({ activeView, setActiveView, isAdmin }: Props) {
  const { chats, setChats, setCurrentChat, setMessages } = useChatStore();
  const [loading, setLoading] = useState(false);

  useEffect(() => { loadChats(); }, []);

  const loadChats = async () => {
    setLoading(true);
    try {
      const data = await chatApi.list();
      setChats(data);
    } catch {}
    setLoading(false);
  };

  const createNewChat = async () => {
    try {
      const newChat = await chatApi.create({ title: 'محادثة جديدة', model: 'gpt-4o-mini' });
      setChats([newChat, ...chats]);
      setCurrentChat(newChat);
      setMessages([]);
      setActiveView('chat');
    } catch {}
  };

  const selectChat = async (chat: any) => {
    try {
      const full = await chatApi.get(chat.id);
      setCurrentChat(full);
      setMessages(full.messages || []);
      setActiveView('chat');
    } catch {}
  };

  const deleteChat = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await chatApi.delete(id);
      setChats(chats.filter((c: any) => c.id !== id));
    } catch {}
  };

  // للمستخدم العادي — فقط ما يحتاجه — مثل ChatGPT / Manus / Arena.ai — نظيف 10 views — Battle + Leaderboard — يعمل فعلياً
  const userMenu = [
    { id: 'chat', label: 'المحادثة', icon: MessageSquare },
    { id: 'battle', label: 'ساحة المعركة', icon: Swords },
    { id: 'leaderboard', label: 'لوحة الصدارة', icon: Trophy },
    { id: 'agents', label: 'الوكلاء', icon: Bot },
    { id: 'projects', label: 'المشاريع', icon: FileText },
    { id: 'agency', label: 'الوكالة', icon: Users },
    { id: 'mobile', label: 'الجوال', icon: Smartphone },
  ];

  const adminMenu = isAdmin ? [
    { id: 'admin', label: 'لوحة الإدارة', icon: Shield },
  ] : [];

  return (
    <div className="w-[260px] bg-[#f7f7f8] border-r border-zinc-200 flex flex-col h-full">
      {/* Logo — مثل Arena.ai — نظيف */}
      <div className="p-4">
        <div className="flex items-center gap-2.5 mb-4">
          <div className="w-8 h-8 rounded-lg bg-black text-white flex items-center justify-center font-bold text-sm">AI</div>
          <span className="font-semibold text-[15px]">AI Agency OS</span>
        </div>
        <button
          onClick={createNewChat}
          className="w-full flex items-center gap-2 px-3 py-2.5 bg-white border border-zinc-200 rounded-lg hover:bg-zinc-50 transition text-sm font-medium shadow-sm"
        >
          <Plus size={16} />
          محادثة جديدة
        </button>
      </div>

      {/* Chat History — مثل ChatGPT */}
      <div className="flex-1 overflow-y-auto px-2">
        <div className="px-2 py-2 text-[11px] font-medium text-zinc-500 uppercase tracking-wider">المحادثات</div>
        {loading ? (
          <div className="px-3 py-2 text-sm text-zinc-400">جاري التحميل...</div>
        ) : chats.length === 0 ? (
          <div className="px-3 py-2 text-sm text-zinc-400">لا توجد محادثات</div>
        ) : (
          <div className="space-y-0.5">
            {chats.map((chat: any) => (
              <div
                key={chat.id}
                onClick={() => selectChat(chat)}
                className="group flex items-center justify-between px-3 py-2 rounded-lg hover:bg-white hover:shadow-sm cursor-pointer transition text-sm"
              >
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <MessageSquare size={14} className="text-zinc-400 flex-shrink-0" />
                  <span className="truncate text-zinc-700">{chat.title}</span>
                </div>
                <button
                  onClick={(e) => deleteChat(chat.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-zinc-100 rounded transition"
                >
                  <Trash2 size={12} className="text-zinc-400" />
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 px-2 py-2 text-[11px] font-medium text-zinc-500 uppercase tracking-wider">القائمة</div>
        <div className="space-y-0.5">
          {userMenu.map(item => {
            const Icon = item.icon;
            const active = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id)}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition ${active ? 'bg-white shadow-sm text-black font-medium' : 'text-zinc-600 hover:bg-white hover:shadow-sm'}`}
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
          {adminMenu.map(item => {
            const Icon = item.icon;
            const active = activeView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id)}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition ${active ? 'bg-black text-white' : 'text-zinc-500 hover:bg-zinc-100 border border-dashed border-zinc-300'}`}
              >
                <Icon size={16} />
                {item.label}
                <span className="ml-auto text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded">ADMIN</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Footer — مثل Arena.ai — نظيف جداً */}
      <div className="p-3 border-t border-zinc-200">
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white cursor-pointer transition"
          onClick={() => setActiveView('settings')}>
          <div className="w-7 h-7 rounded-full bg-zinc-200 flex items-center justify-center text-xs font-medium">U</div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium truncate">مستخدم</div>
            <div className="text-[11px] text-zinc-500">Free Plan</div>
          </div>
          <Settings size={14} className="text-zinc-400" />
        </div>
      </div>
    </div>
  );
}
