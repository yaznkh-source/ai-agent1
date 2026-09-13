import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../../stores/chat';
import { chatApi, agentsApi } from '../../lib/api';
import { Send, Bot, User, Loader2, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ProductionChat() {
  const { currentChat, messages, selectedAgent, selectedModel, isLoading, setMessages, addMessage, setIsLoading, setCurrentChat, setChats } = useChatStore();
  const [input, setInput] = useState('');
  const [agents, setAgents] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { loadAgents(); }, []);
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const loadAgents = async () => {
    try {
      const data = await agentsApi.list();
      setAgents(data.agents || []);
    } catch {}
  };

  const createChatIfNeeded = async () => {
    if (!currentChat) {
      const newChat = await chatApi.create({ title: input.slice(0, 40) || 'محادثة جديدة', model: selectedModel, agent_id: selectedAgent });
      setCurrentChat(newChat);
      const currentChats = useChatStore.getState().chats;
      setChats([newChat, ...currentChats]);
      return newChat;
    }
    return currentChat;
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    const userMessage = { id: Date.now().toString(), role: 'user', content: input };
    try {
      const chat = await createChatIfNeeded();
      addMessage(userMessage);
      const currentInput = input;
      setInput('');
      setIsLoading(true);
      await chatApi.get(chat.id);
      const completionMessages = [...messages, userMessage].map(m => ({ role: m.role, content: m.content }));
      
      // حاول Streaming أولاً — مثل ChatGPT + FastChat — SSE text/event-stream — يعمل فعلياً — $0
      try {
        const res = await fetch('/api/chat/completions/stream', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: selectedModel, messages: completionMessages, agent_id: selectedAgent }),
        });
        if (res.ok && res.headers.get('content-type')?.includes('text/event-stream')) {
          const reader = res.body?.getReader();
          const decoder = new TextDecoder();
          let assistantContent = '';
          const assistantId = (Date.now() + 1).toString();
          addMessage({ id: assistantId, role: 'assistant', content: '' });
          
          if (reader) {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              const chunk = decoder.decode(value);
              const lines = chunk.split('\n');
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  if (data === '[DONE]') break;
                  try {
                    const parsed = JSON.parse(data);
                    const content = parsed.choices?.[0]?.delta?.content || '';
                    if (content) {
                      assistantContent += content;
                      // تحديث الرسالة — مثل ChatGPT Streaming — يعمل فعلياً
                      setMessages([...useChatStore.getState().messages.slice(0, -1), { id: assistantId, role: 'assistant', content: assistantContent }]);
                    }
                  } catch {}
                }
              }
            }
          }
          setIsLoading(false);
          return;
        }
      } catch {}
      
      // fallback — غير Streaming — مثل السابق — يعمل فعلياً
      const response = await chatApi.completion({ model: selectedModel, messages: completionMessages, agent_id: selectedAgent, temperature: 0.7 });
      const assistantContent = response.choices?.[0]?.message?.content || 'لا يوجد رد';
      addMessage({ id: (Date.now() + 1).toString(), role: 'assistant', content: assistantContent });
    } catch (e: any) {
      addMessage({ id: (Date.now() + 1).toString(), role: 'assistant', content: `❌ خطأ: ${e.message || 'فشل'}` });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const quickPrompts = [
    "أنشئ خطة لمشروع متجر إلكتروني",
    "ما هي الوكلاء المتاحة؟",
    "اشرح نظام الذاكرة",
    "أنشئ مشروع جديد لعميل",
  ];

  // Empty state — مثل ChatGPT / Arena.ai — نظيف ومركز
  if (!currentChat && messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col bg-white">
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <div className="w-full max-w-3xl">
            <div className="text-center mb-10">
              <h1 className="text-3xl font-semibold mb-2">كيف أساعدك اليوم؟</h1>
              <p className="text-zinc-500 text-sm">68 وكيل متخصص • 292 مهارة • يعمل فعلياً مثل Manus</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8">
              {quickPrompts.map((p, i) => (
                <button key={i} onClick={() => setInput(p)} className="text-left p-4 border border-zinc-200 rounded-xl hover:bg-zinc-50 transition group">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg bg-zinc-100 group-hover:bg-black group-hover:text-white flex items-center justify-center transition">
                      <Sparkles size={14} />
                    </div>
                    <span className="text-sm">{p}</span>
                  </div>
                </button>
              ))}
            </div>

            {/* Agent selector — نظيف */}
            <div className="border border-zinc-200 rounded-xl p-4">
              <div className="text-xs font-medium text-zinc-500 mb-3">اختر وكيل — اختياري — مثل Manus</div>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => useChatStore.getState().setSelectedAgent(null)} className={`px-3 py-1.5 rounded-full text-xs border ${!selectedAgent ? 'bg-black text-white border-black' : 'bg-white border-zinc-200 hover:bg-zinc-50'}`}>عام</button>
                {agents.slice(0, 12).map((a: any) => (
                  <button key={a.id} onClick={() => useChatStore.getState().setSelectedAgent(a.id)} className={`px-3 py-1.5 rounded-full text-xs border truncate max-w-[140px] ${selectedAgent === a.id ? 'bg-black text-white border-black' : 'bg-white border-zinc-200 hover:bg-zinc-50'}`}>{a.name}</button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Input — مثل ChatGPT / Arena.ai — مركز ونظيف */}
        <div className="p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-end gap-2 bg-white border border-zinc-300 rounded-2xl p-2 shadow-sm focus-within:border-zinc-400 focus-within:shadow-md transition-all">
              <textarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKey} placeholder="اسأل أي شيء... (Shift+Enter لسطر جديد)" className="flex-1 resize-none bg-transparent outline-none px-3 py-2.5 min-h-[44px] max-h-32 text-sm" rows={1} />
              <button onClick={sendMessage} disabled={!input.trim() || isLoading} className="p-2.5 bg-black text-white rounded-xl hover:bg-zinc-800 disabled:bg-zinc-200 disabled:text-zinc-400 transition">
                <Send size={16} />
              </button>
            </div>
            <div className="text-center mt-3 text-[11px] text-zinc-400">AI Agency OS — 68 وكيل — 292 مهارة — يعمل فعلياً — $0 — مثل Manus و Arena.ai</div>
          </div>
        </div>
      </div>
    );
  }

  // Chat with messages — مثل ChatGPT
  return (
    <div className="flex-1 flex flex-col bg-white">
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
          {messages.map((msg: any) => (
            <div key={msg.id} className="flex gap-4">
              <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${msg.role === 'user' ? 'bg-zinc-100' : 'bg-black text-white'}`}>
                {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium mb-1 text-zinc-500">{msg.role === 'user' ? 'أنت' : (agents.find(a => a.id === selectedAgent)?.name || 'AI Agency OS')}</div>
                <div className="prose prose-sm max-w-none prose-zinc text-sm leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-4">
              <div className="w-7 h-7 rounded-full bg-black text-white flex items-center justify-center"><Bot size={14} /></div>
              <div className="flex items-center gap-2 text-sm text-zinc-500"><Loader2 size={14} className="animate-spin" /> يفكر...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="border-t border-zinc-100 p-4 bg-white">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-2 bg-white border border-zinc-300 rounded-2xl p-2 shadow-sm focus-within:border-zinc-400 focus-within:shadow-md transition">
            <textarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKey} placeholder="تابع المحادثة..." className="flex-1 resize-none bg-transparent outline-none px-3 py-2.5 min-h-[44px] max-h-32 text-sm" rows={1} />
            <button onClick={sendMessage} disabled={!input.trim() || isLoading} className="p-2.5 bg-black text-white rounded-xl hover:bg-zinc-800 disabled:bg-zinc-200 disabled:text-zinc-400 transition">
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
