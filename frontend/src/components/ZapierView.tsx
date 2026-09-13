import { useEffect, useState } from 'react';
import api from '../lib/api';
import { Zap, Webhook, Play, CheckCircle } from 'lucide-react';

export default function ZapierView() {
  const [data, setData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'triggers'|'actions'|'examples'|'webhooks'>('triggers');
  const [webhooks, setWebhooks] = useState<any[]>([]);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const res = await api.get('/integrations/zapier/');
      setData(res.data);
      const whRes = await api.get('/integrations/zapier/webhooks');
      setWebhooks(whRes.data.webhooks);
    } catch {}
  };

  const testTrigger = async (id: string) => {
    try {
      const res = await api.post(`/integrations/zapier/triggers/${id}/test`);
      alert(`Sample: ${JSON.stringify(res.data.sample, null, 2)}`);
    } catch (e:any) { alert(e.message); }
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Zap className="text-orange-500"/>Zapier + Make + HubSpot + Slack - تكاملات عميقة</h1>
        <p className="text-sm text-zinc-600 mb-6">اربط AI Agency OS بـ 5000+ تطبيق عبر Zapier, Make, HubSpot Workflows, Slack Workflows, n8n, Pabbly</p>

        {data?.stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.total_triggers}</div><div className="text-xs text-zinc-500">Triggers</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.total_actions}</div><div className="text-xs text-zinc-500">Actions</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.active_zaps}</div><div className="text-xs text-zinc-500">Active Zaps</div></div>
            <div className="bg-white rounded-2xl border p-5 bg-gradient-to-br from-orange-500 to-red-500 text-white"><div className="text-sm font-bold">{data.stats.supported_platforms.length} Platforms</div><div className="text-xs text-orange-100">{data.stats.supported_platforms.join(', ').slice(0,40)}...</div></div>
          </div>
        )}

        <div className="flex gap-2 mb-6">
          <div className="flex bg-white border rounded-xl p-1">
            {(['triggers','actions','examples','webhooks'] as const).map(tab => (
              <button key={tab} onClick={()=>setActiveTab(tab)} className={`px-4 py-2 rounded-lg text-sm font-medium capitalize ${activeTab===tab?'bg-violet-600 text-white':'text-zinc-600'}`}>{tab}</button>
            ))}
          </div>
        </div>

        {activeTab==='triggers' && data?.triggers && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.triggers.map((t:any) => (
              <div key={t.id} className="bg-white rounded-2xl border p-5">
                <div className="flex items-start justify-between">
                  <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center"><Zap size={18} className="text-orange-600"/></div>
                  <button onClick={()=>testTrigger(t.id)} className="px-3 py-1.5 bg-zinc-100 rounded-full text-xs flex items-center gap-1"><Play size={12}/>Test</button>
                </div>
                <div className="font-semibold mt-3 text-sm">{t.name}</div>
                <div className="text-xs text-zinc-500 mt-1">{t.description}</div>
                <pre className="mt-3 text-[10px] bg-zinc-900 text-zinc-100 p-3 rounded-xl overflow-x-auto">{JSON.stringify(t.sample, null, 2)}</pre>
              </div>
            ))}
          </div>
        )}

        {activeTab==='actions' && data?.actions && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.actions.map((a:any) => (
              <div key={a.id} className="bg-white rounded-2xl border p-5">
                <div className="w-10 h-10 rounded-xl bg-violet-100 flex items-center justify-center"><CheckCircle size={18} className="text-violet-600"/></div>
                <div className="font-semibold mt-3 text-sm">{a.name}</div>
                <div className="text-xs text-zinc-500 mt-1">{a.description}</div>
                <div className="mt-3 flex flex-wrap gap-1">
                  {a.input.map((inp:string) => <span key={inp} className="text-xs bg-violet-50 text-violet-700 px-2 py-1 rounded-full">{inp}</span>)}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab==='examples' && data?.examples && (
          <div className="space-y-3">
            {data.examples.map((ex:any, i:number) => (
              <div key={i} className="bg-white rounded-2xl border p-5 flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center text-white font-bold">{i+1}</div>
                <div className="flex-1">
                  <div className="font-semibold text-sm">{ex.name}</div>
                  <div className="text-xs text-zinc-500 mt-1">{ex.description}</div>
                  <div className="text-xs mt-2 flex items-center gap-2"><span className="bg-orange-100 text-orange-700 px-2 py-1 rounded-full">{ex.trigger}</span> → <span className="bg-violet-100 text-violet-700 px-2 py-1 rounded-full">{ex.action}</span></div>
                </div>
              </div>
            ))}
            
            <div className="mt-8 bg-zinc-900 text-zinc-100 rounded-2xl p-6">
              <h4 className="font-semibold mb-3">🔧 كيف يعمل Zapier مع AI Agency OS</h4>
              <div className="space-y-2 text-sm text-zinc-300">
                {data.how_it_works?.map((step:string, i:number) => <div key={i}>{step}</div>)}
              </div>
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="p-3 bg-zinc-800 rounded-xl"><div className="font-medium text-orange-400">Zapier</div><div className="text-zinc-400 mt-1">5000+ apps, no code, $19/mo</div></div>
                <div className="p-3 bg-zinc-800 rounded-xl"><div className="font-medium text-violet-400">Make</div><div className="text-zinc-400 mt-1">Visual, powerful, $9/mo</div></div>
                <div className="p-3 bg-zinc-800 rounded-xl"><div className="font-medium text-blue-400">HubSpot</div><div className="text-zinc-400 mt-1">Workflows + webhooks, CRM</div></div>
              </div>
            </div>
          </div>
        )}

        {activeTab==='webhooks' && (
          <div className="space-y-4">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2"><Webhook size={16}/>Active Webhooks - {webhooks.length}</h3>
              {webhooks.length===0 ? <div className="text-sm text-zinc-400">لا webhooks نشطة - أنشئ Zap في Zapier وستظهر هنا</div> : (
                <div className="space-y-2">
                  {webhooks.map((wh:any) => (
                    <div key={wh.id} className="p-3 bg-zinc-50 rounded-xl text-xs">
                      <div className="font-medium">{wh.trigger_id} → {wh.target_url.slice(0,50)}...</div>
                      <div className="text-zinc-500 mt-1">User: {wh.user_id} - {new Date(wh.created_at).toLocaleString('ar')}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h4 className="font-semibold text-sm mb-3">اختبار Trigger Webhook</h4>
              <div className="flex gap-2">
                <select id="triggerSelect" className="px-3 py-2 border rounded-xl text-sm">
                  <option value="new_project">new_project</option>
                  <option value="task_completed">task_completed</option>
                  <option value="agent_completed">agent_completed</option>
                </select>
                <button onClick={async()=>{
                  const triggerId = (document.getElementById('triggerSelect') as HTMLSelectElement)?.value;
                  try {
                    const res = await api.post(`/integrations/zapier/webhooks/trigger/${triggerId}`, { test: true, project_id: 'test', timestamp: new Date().toISOString() });
                    alert(`Triggered ${res.data.matched_zaps} zaps: ${JSON.stringify(res.data.results.slice(0,1), null, 2)}`);
                  } catch (e:any) { alert(e.message); }
                }} className="px-4 py-2 bg-orange-500 text-white rounded-xl text-sm">Trigger Test</button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-2xl border p-5">
                <h4 className="font-semibold text-sm">HubSpot</h4>
                <div className="text-xs text-zinc-600 mt-2">Deal Won → Create Project via webhook POST /api/agency/projects</div>
                <a href="/api/docs" className="text-xs text-violet-600 mt-2 inline-block">API Docs →</a>
              </div>
              <div className="bg-white rounded-2xl border p-5">
                <h4 className="font-semibold text-sm">Slack</h4>
                <div className="text-xs text-zinc-600 mt-2">Slash commands: /ai-agency create project, /ai-agency run agent</div>
                <div className="text-xs text-zinc-400 mt-1">Events: project created → #projects</div>
              </div>
              <div className="bg-white rounded-2xl border p-5">
                <h4 className="font-semibold text-sm">GitHub</h4>
                <div className="text-xs text-zinc-600 mt-2">PR merged → Trigger pipeline, Issue created → Create task</div>
                <div className="text-xs text-zinc-400 mt-1">Webhook: /api/integrations/github/webhook</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
