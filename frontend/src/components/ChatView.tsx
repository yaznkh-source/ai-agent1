import { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../stores/chat';
import { chatApi, agentsApi } from '../lib/api';
import { Send, Bot, User, Sparkles, Zap, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatView() {
  const { currentChat, messages, selectedAgent, selectedModel, isLoading, setMessages, addMessage, setIsLoading, setCurrentChat, setChats } = useChatStore();
  const [input, setInput] = useState('');
  const [agents, setAgents] = useState<any[]>([]);
  const [showAgentSelector, setShowAgentSelector] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadAgents();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadAgents = async () => {
    try {
      const data = await agentsApi.list();
      setAgents(data.agents || []);
    } catch (e) {
      console.error(e);
    }
  };

  const createChatIfNeeded = async () => {
    if (!currentChat) {
      const newChat = await chatApi.create({
        title: input.slice(0, 50) || 'New Chat',
        model: selectedModel,
        agent_id: selectedAgent
      });
      setCurrentChat(newChat);
      // Get current chats from store and prepend new chat
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
      
      // Add user message to UI immediately
      addMessage(userMessage);
      setInput('');
      setIsLoading(true);

      // Save user message to backend
      await chatApi.get(chat.id); // Ensure chat exists
      // In real app, we'd POST to /chats/{id}/messages, but for simplicity use completions endpoint

      // Build messages for completion
      const completionMessages = [...messages, userMessage].map(m => ({
        role: m.role,
        content: m.content
      }));

      // Call completions endpoint (OpenAI-compatible)
      const response = await chatApi.completion({
        model: selectedModel,
        messages: completionMessages,
        agent_id: selectedAgent,
        temperature: 0.7
      });

      const assistantContent = response.choices?.[0]?.message?.content || 'No response';
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: assistantContent
      };

      addMessage(assistantMessage);

      // Save assistant message
      // await api.post(`/chats/${chat.id}/messages`, assistantMessage);

    } catch (e: any) {
      console.error(e);
      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ خطأ: ${e.message || 'فشل في الإرسال'}`
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const quickPrompts = [
    "اشرح لي نظام ECC وكيف يستفيد من الوكلاء المتخصصين",
    "ما الفرق بين Tools و Functions و Pipelines في Open WebUI؟",
    "أنشئ خطة لمشروع وكالة ذكاء اصطناعي",
    "كيف يعمل نظام الذاكرة والـ Instincts؟",
  ];

  if (!currentChat && messages.length === 0) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 bg-gradient-to-br from-zinc-50 to-violet-50/30">
        <div className="max-w-3xl w-full">
          <div className="text-center mb-12">
            <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center text-3xl font-bold text-white shadow-xl glow">
              AI
            </div>
            <h1 className="text-4xl font-bold mb-3 bg-gradient-to-br from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              AI Agency OS
            </h1>
            <p className="text-zinc-600 text-lg mb-2">
              نظام وكالة ذكاء اصطناعي متكامل - مستوحى من ECC و Open WebUI
            </p>
            <p className="text-sm text-zinc-500">
              20 وكيل متخصص • 15 مهارة • 9 أدوات • Pipelines • ذاكرة مستمرة • AgentShield
            </p>
          </div>

          {/* Agent selector */}
          <div className="bg-white rounded-2xl shadow-sm border p-6 mb-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Bot size={18} />
              اختر الوكيل المناسب
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-h-48 overflow-y-auto">
              <button
                onClick={() => useChatStore.getState().setSelectedAgent(null)}
                className={`p-3 rounded-xl border text-left transition-all ${!selectedAgent ? 'bg-violet-50 border-violet-200 ring-2 ring-violet-200' : 'hover:bg-zinc-50'}`}
              >
                <div className="font-medium text-sm">عام</div>
                <div className="text-xs text-zinc-500">بدون تخصص</div>
              </button>
              {agents.slice(0, 8).map((agent: any) => (
                <button
                  key={agent.id}
                  onClick={() => useChatStore.getState().setSelectedAgent(agent.id)}
                  className={`p-3 rounded-xl border text-left transition-all ${selectedAgent === agent.id ? 'bg-violet-50 border-violet-200 ring-2 ring-violet-200' : 'hover:bg-zinc-50'}`}
                >
                  <div className="font-medium text-sm truncate">{agent.name}</div>
                  <div className="text-xs text-zinc-500 truncate">{agent.role}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Quick prompts */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {quickPrompts.map((prompt, i) => (
              <button
                key={i}
                onClick={() => setInput(prompt)}
                className="p-4 bg-white rounded-xl border hover:border-violet-200 hover:shadow-md transition-all text-left group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-violet-100 group-hover:bg-violet-200 flex items-center justify-center flex-shrink-0 transition-colors">
                    <Sparkles size={16} className="text-violet-600" />
                  </div>
                  <span className="text-sm text-zinc-700">{prompt}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="border-b p-4 flex items-center justify-between bg-zinc-50/50">
        <div className="flex items-center gap-3">
          <h2 className="font-semibold truncate">{currentChat?.title || 'محادثة جديدة'}</h2>
          {selectedAgent && (
            <span className="px-2.5 py-1 bg-violet-100 text-violet-700 rounded-full text-xs font-medium flex items-center gap-1">
              <Bot size={12} />
              {agents.find(a => a.id === selectedAgent)?.name || selectedAgent}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-zinc-500 px-2.5 py-1 bg-white border rounded-full">
            {selectedModel}
          </span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center flex-shrink-0">
                <Bot size={16} className="text-white" />
              </div>
            )}
            <div className={`max-w-[75%] rounded-2xl px-4 py-3 ${
              msg.role === 'user' 
                ? 'bg-violet-600 text-white rounded-br-md' 
                : 'bg-zinc-100 text-zinc-900 rounded-bl-md'
            }`}>
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-zinc-200 flex items-center justify-center flex-shrink-0">
                <User size={16} />
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center">
              <Bot size={16} className="text-white" />
            </div>
            <div className="bg-zinc-100 rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-2">
              <Loader2 size={16} className="animate-spin" />
              <span className="text-sm text-zinc-600">الوكيل يفكر...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4 bg-zinc-50/50">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3 items-end bg-white border rounded-2xl p-2 shadow-sm focus-within:ring-2 focus-within:ring-violet-200 focus-within:border-violet-300 transition-all">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="اكتب رسالتك هنا... (Shift+Enter لسطر جديد)"
              className="flex-1 resize-none bg-transparent border-0 outline-0 px-3 py-2.5 max-h-32 min-h-[44px]"
              rows={1}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="p-2.5 bg-violet-600 hover:bg-violet-700 disabled:bg-zinc-300 text-white rounded-xl transition-colors flex-shrink-0"
            >
              <Send size={18} />
            </button>
          </div>
          
          <div className="flex items-center justify-between mt-3 px-1">
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <Zap size={12} />
              <span>مدعوم بـ ECC Agents + Open WebUI Tools</span>
            </div>
            <div className="text-xs text-zinc-400">
              {selectedAgent ? `الوكيل: ${selectedAgent}` : 'وضع عام'} • {selectedModel}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
