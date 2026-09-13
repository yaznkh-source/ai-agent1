import { useEffect, useState } from 'react';
import { agentsApi } from '../lib/api';
import { Bot, Play, Code, Search, Shield, Zap } from 'lucide-react';

export default function AgentsView() {
  const [agents, setAgents] = useState<any[]>([]);
  const [categories, setCategories] = useState<any>({});
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedAgent, setSelectedAgent] = useState<any>(null);
  const [task, setTask] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const data = await agentsApi.list();
      setAgents(data.agents || []);
      setCategories(data.categories || {});
    } catch (e) {
      console.error(e);
    }
  };

  const runAgent = async () => {
    if (!selectedAgent || !task.trim()) return;
    setLoading(true);
    setResult('');
    try {
      const res = await agentsApi.run({
        agent_id: selectedAgent.id,
        task: task,
        context: { user_id: 'default-user' }
      });
      setResult(res.result || JSON.stringify(res, null, 2));
    } catch (e: any) {
      setResult(`Error: ${e.message}`);
    }
    setLoading(false);
  };

  const filteredAgents = selectedCategory === 'all' 
    ? agents 
    : agents.filter(a => a.category === selectedCategory);

  const categoryIcons: any = {
    planning: '🧭',
    development: '💻',
    review: '🔍',
    research: '🔬',
    operations: '⚙️',
    data: '📊',
    ai: '🤖',
    content: '✍️'
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      {/* Agents List */}
      <div className="w-96 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h2 className="font-bold text-lg flex items-center gap-2">
            <Bot className="text-violet-600" />
            الوكلاء المتخصصون
            <span className="ml-auto text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded-full">
              {agents.length} وكيل
            </span>
          </h2>
          <p className="text-xs text-zinc-500 mt-1">
            مستوحى من ECC - 68 وكيل متخصص، معزول السياق
          </p>
        </div>

        <div className="p-3 border-b">
          <div className="flex gap-2 overflow-x-auto pb-2">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors ${
                selectedCategory === 'all' ? 'bg-violet-600 text-white' : 'bg-zinc-100 hover:bg-zinc-200'
              }`}
            >
              الكل ({agents.length})
            </button>
            {Object.entries(categories).map(([key, cat]: any) => (
              <button
                key={key}
                onClick={() => setSelectedCategory(key)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors flex items-center gap-1 ${
                  selectedCategory === key ? 'bg-violet-600 text-white' : 'bg-zinc-100 hover:bg-zinc-200'
                }`}
              >
                <span>{categoryIcons[key] || '•'}</span>
                {cat.name} ({cat.count})
              </button>
            ))}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {filteredAgents.map(agent => (
            <button
              key={agent.id}
              onClick={() => setSelectedAgent(agent)}
              className={`w-full text-left p-4 rounded-xl border transition-all ${
                selectedAgent?.id === agent.id
                  ? 'bg-violet-50 border-violet-200 ring-2 ring-violet-100'
                  : 'bg-white border-zinc-200 hover:border-zinc-300 hover:shadow-sm'
              }`}
            >
              <div className="flex items-start gap-3">
                <div 
                  className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm flex-shrink-0"
                  style={{ backgroundColor: agent.color || '#8B5CF6' }}
                >
                  {agent.name.charAt(0)}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-sm truncate">{agent.name}</div>
                  <div className="text-xs text-zinc-500 truncate">{agent.role}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[10px] px-2 py-0.5 bg-zinc-100 rounded-full">
                      {agent.category}
                    </span>
                    <span className="text-[10px] text-zinc-400">
                      {agent.skills?.length || 0} مهارات
                    </span>
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Agent Detail & Runner */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {selectedAgent ? (
          <>
            <div className="p-6 bg-white border-b">
              <div className="flex items-start gap-4">
                <div 
                  className="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-bold text-xl"
                  style={{ backgroundColor: selectedAgent.color }}
                >
                  {selectedAgent.name.charAt(0)}
                </div>
                <div className="flex-1">
                  <h1 className="text-2xl font-bold">{selectedAgent.name}</h1>
                  <p className="text-zinc-600">{selectedAgent.role}</p>
                  <p className="text-sm text-zinc-500 mt-2">{selectedAgent.description}</p>
                  
                  <div className="flex flex-wrap gap-2 mt-4">
                    <span className="px-3 py-1 bg-violet-100 text-violet-700 rounded-full text-xs font-medium">
                      {selectedAgent.category}
                    </span>
                    <span className="px-3 py-1 bg-zinc-100 rounded-full text-xs">
                      Model: {selectedAgent.model}
                    </span>
                    {selectedAgent.skills?.map((skill: string) => (
                      <span key={skill} className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs flex items-center gap-1">
                        <Zap size={10} />
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              <div className="bg-white rounded-2xl border p-5">
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <Code size={16} />
                  System Prompt
                </h3>
                <pre className="text-xs bg-zinc-50 p-4 rounded-xl overflow-x-auto whitespace-pre-wrap text-zinc-700">
                  {selectedAgent.system_prompt}
                </pre>
              </div>

              <div className="bg-white rounded-2xl border p-5">
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <Play size={16} />
                  تشغيل الوكيل
                </h3>
                <textarea
                  value={task}
                  onChange={(e) => setTask(e.target.value)}
                  placeholder={`اكتب مهمة لـ ${selectedAgent.name}... مثال: صمم API لنظام إدارة العملاء`}
                  className="w-full h-32 p-4 border rounded-xl resize-none focus:ring-2 focus:ring-violet-200 focus:border-violet-300 outline-none"
                />
                <button
                  onClick={runAgent}
                  disabled={loading || !task.trim()}
                  className="mt-3 px-6 py-2.5 bg-violet-600 hover:bg-violet-700 disabled:bg-zinc-300 text-white rounded-xl font-medium flex items-center gap-2 transition-colors"
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      جاري التشغيل...
                    </>
                  ) : (
                    <>
                      <Play size={16} />
                      تشغيل
                    </>
                  )}
                </button>
              </div>

              {result && (
                <div className="bg-white rounded-2xl border p-5">
                  <h3 className="font-semibold mb-3">النتيجة</h3>
                  <div className="bg-zinc-900 text-zinc-100 p-4 rounded-xl overflow-x-auto">
                    <pre className="text-sm whitespace-pre-wrap">{result}</pre>
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-violet-100 flex items-center justify-center">
                <Bot size={32} className="text-violet-600" />
              </div>
              <h3 className="font-semibold text-lg mb-2">اختر وكيلاً للبدء</h3>
              <p className="text-sm text-zinc-500">
                كل وكيل متخصص في مجال معين ويعمل بسياق معزول لضمان جودة المراجعة والتنفيذ.
                مستوحى من فكرة ECC: نفس السياق يكتب ويراجع = نقاط عمياء.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
