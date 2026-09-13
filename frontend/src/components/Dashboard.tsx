import { useEffect, useState } from 'react';
import { agencyApi } from '../lib/api';
import { Bot, Zap, Wrench, Shield, Workflow, Brain, Code, BarChart3 } from 'lucide-react';

export default function Dashboard() {
  const [config, setConfig] = useState<any>(null);
  const [dashboard, setDashboard] = useState<any>(null);

  useEffect(() => {
    fetch('/api/config').then(r=>r.json()).then(setConfig).catch(()=>{});
    agencyApi.dashboard().then(setDashboard).catch(()=>{});
  }, []);

  return (
    <div className="flex-1 bg-gradient-to-br from-zinc-50 to-violet-50/20 overflow-y-auto p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-10">
          <div className="w-20 h-20 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center text-white font-bold text-2xl shadow-xl">AI</div>
          <h1 className="text-4xl font-bold bg-gradient-to-br from-violet-600 to-indigo-600 bg-clip-text text-transparent">AI Agency OS</h1>
          <p className="text-zinc-600 mt-3 max-w-2xl mx-auto">
            نظام وكالة ذكاء اصطناعي متكامل يجمع أفضل ما في <strong>ECC</strong> (نظام تحسين أداء حاضنة الوكلاء) و <strong>Open WebUI</strong> (واجهة سهلة الاستخدام مع دعم Ollama و OpenAI)
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-2xl border p-6 shadow-sm">
            <div className="w-12 h-12 rounded-xl bg-violet-100 flex items-center justify-center mb-4"><Bot className="text-violet-600" /></div>
            <h3 className="font-bold text-lg">مستوحى من ECC</h3>
            <p className="text-sm text-zinc-600 mt-2 leading-relaxed">
              68 وكيل متخصص، 292 مهارة، hooks، ذاكرة، تعلم مستمر (instincts)، وحلقة تحقق، وفحص أمان AgentShield
            </p>
            <div className="mt-4 space-y-2 text-xs">
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-violet-600 rounded-full"/>plan → test → implement → review → verify → remember → improve</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-violet-600 rounded-full"/>سياق معزول للمراجع (fresh-context reviewer)</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-violet-600 rounded-full"/>المهارات تحمل عند الحاجة فقط (context optimization)</div>
            </div>
          </div>

          <div className="bg-white rounded-2xl border p-6 shadow-sm">
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center mb-4"><Wrench className="text-blue-600" /></div>
            <h3 className="font-bold text-lg">مستوحى من Open WebUI</h3>
            <p className="text-sm text-zinc-600 mt-2 leading-relaxed">
              واجهة محادثة سهلة، دعم متعدد النماذج، Tools، Functions (Pipe/Filter/Action/Event)، Pipelines، RAG
            </p>
            <div className="mt-4 space-y-2 text-xs">
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-blue-600 rounded-full"/>Tools: توسيع قدرات LLM (طقس، بحث، ...)</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-blue-600 rounded-full"/>Functions: توسيع المنصة نفسها</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-blue-600 rounded-full"/>Pipelines: إطار عمل OpenAI API متوافق</div>
            </div>
          </div>

          <div className="bg-white rounded-2xl border p-6 shadow-sm bg-gradient-to-br from-violet-600 to-indigo-600 text-white">
            <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center mb-4"><BarChart3 className="text-white" /></div>
            <h3 className="font-bold text-lg">AI Agency OS</h3>
            <p className="text-sm text-violet-100 mt-2 leading-relaxed">
              نظام وكالة متكامل: عملاء، مشاريع، مهام، وكلاء، مهارات، pipelines، ذاكرة، وأمان في مكان واحد
            </p>
            <div className="mt-4 space-y-2 text-xs text-violet-100">
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-white rounded-full"/>إدارة وكالة كاملة</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-white rounded-full"/>أتمتة Onboarding العملاء</div>
              <div className="flex items-center gap-2"><div className="w-1.5 h-1.5 bg-white rounded-full"/>تتبع المهام والتحقق</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-8">
          {[
            { icon: Bot, label: 'الوكلاء', value: '20', color: 'violet' },
            { icon: Zap, label: 'المهارات', value: '15', color: 'amber' },
            { icon: Wrench, label: 'الأدوات', value: '9', color: 'orange' },
            { icon: Workflow, label: 'Pipelines', value: '4', color: 'blue' },
            { icon: Brain, label: 'الذاكرة', value: '∞', color: 'pink' },
            { icon: Shield, label: 'AgentShield', value: '✓', color: 'green' },
            { icon: Code, label: 'Verification', value: '5', color: 'indigo' },
          ].map((item, i) => {
            const Icon = item.icon;
            return (
              <div key={i} className="bg-white rounded-2xl border p-4 text-center">
                <div className={`w-10 h-10 mx-auto rounded-xl bg-${item.color}-100 flex items-center justify-center mb-2`}>
                  <Icon size={18} className={`text-${item.color}-600`} />
                </div>
                <div className="font-bold text-lg">{item.value}</div>
                <div className="text-xs text-zinc-500">{item.label}</div>
              </div>
            );
          })}
        </div>

        {dashboard && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-2xl border p-5">
              <div className="text-2xl font-bold">{dashboard.stats?.clients || 0}</div>
              <div className="text-sm text-zinc-500">العملاء</div>
            </div>
            <div className="bg-white rounded-2xl border p-5">
              <div className="text-2xl font-bold">{dashboard.stats?.projects || 0}</div>
              <div className="text-sm text-zinc-500">المشاريع</div>
            </div>
            <div className="bg-white rounded-2xl border p-5">
              <div className="text-2xl font-bold">{dashboard.stats?.tasks || 0}</div>
              <div className="text-sm text-zinc-500">المهام</div>
            </div>
            <div className="bg-white rounded-2xl border p-5 bg-gradient-to-br from-violet-50 to-indigo-50 border-violet-200">
              <div className="text-2xl font-bold text-violet-700">{dashboard.stats?.completion_rate || 0}%</div>
              <div className="text-sm text-violet-600">الإنجاز</div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-2xl border p-6">
          <h3 className="font-bold mb-4">البنية المعمارية</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <h4 className="font-semibold text-violet-700 mb-2">Backend (FastAPI)</h4>
              <ul className="space-y-1 text-zinc-600 text-xs font-mono">
                <li>• app/core/ - config, llm (multi-provider), security (AgentShield)</li>
                <li>• app/agents/ - 20 وكيل متخصص + orchestrator (plan→test→implement→review)</li>
                <li>• app/skills/ - 15 مهارة قابلة للتحميل عند الحاجة</li>
                <li>• app/memory/ - ذاكرة مستمرة + instincts تعلم مستمر</li>
                <li>• app/hooks/ - SessionStart/End, PreToolUse, PostToolUse</li>
                <li>• app/tools/ - 9 أدوات مع OpenAI function calling</li>
                <li>• app/functions/ - Pipe, Filter, Action, Event (Open WebUI)</li>
                <li>• app/pipelines/ - محرك Pipelines متوافق مع OpenAI API</li>
                <li>• app/verification/ - حلقة تحقق: build, test, lint, typecheck, security</li>
                <li>• app/routers/ - 8 routers للـ API</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">Frontend (React + Vite)</h4>
              <ul className="space-y-1 text-zinc-600 text-xs font-mono">
                <li>• ChatView - واجهة محادثة مثل Open WebUI + اختيار وكيل</li>
                <li>• AgentsView - إدارة 20 وكيل مع تشغيل مباشر</li>
                <li>• SkillsView - مكتبة 15 مهارة مع بحث</li>
                <li>• PipelinesView - تنفيذ pipelines مع context</li>
                <li>• ToolsView - عرض Tools, Memory, Security, Functions</li>
                <li>• AgencyView - إدارة عملاء، مشاريع، مهام، لوحة تحكم</li>
                <li>• Dashboard - نظرة عامة معمارية</li>
                <li>• Tailwind + Zustand + React Router</li>
                <li>• دعم كامل للـ preview (0.0.0.0 + CORS *)</li>
              </ul>
            </div>
          </div>

          {config && (
            <div className="mt-6 p-4 bg-zinc-900 text-zinc-100 rounded-xl font-mono text-xs">
              <div className="text-zinc-400 mb-2">// System Config</div>
              <div>App: {config.app_name} v{config.version}</div>
              <div>Default Model: {config.default_model}</div>
              <div>Models: {config.enabled_models?.join(', ')}</div>
              <div>Features: {JSON.stringify(config.features)}</div>
            </div>
          )}
        </div>

        <div className="mt-8 text-center text-xs text-zinc-400">
          <p>بُني بـ ❤️ مستوحى من <a href="https://github.com/affaan-m/ECC" className="text-violet-600 hover:underline">ECC</a> و <a href="https://github.com/open-webui/open-webui" className="text-blue-600 hover:underline">Open WebUI</a></p>
          <p className="mt-1">AI Agency OS - نظام وكالة ذكاء اصطناعي متكامل • 2026</p>
        </div>
      </div>
    </div>
  );
}
