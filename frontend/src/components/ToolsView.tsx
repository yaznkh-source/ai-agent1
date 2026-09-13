import { useEffect, useState } from 'react';
import { toolsApi, functionsApi, memoryApi, agencyApi } from '../lib/api';
import { Wrench, Brain, Shield, Filter, Zap } from 'lucide-react';

export default function ToolsView({ view }: { view: string }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, [view]);

  const load = async () => {
    setLoading(true);
    try {
      if (view === 'tools') {
        const res = await toolsApi.list();
        setData(res);
      } else if (view === 'memory') {
        const [mem, instincts] = await Promise.all([memoryApi.list(), memoryApi.instincts()]);
        setData({ memories: mem.memories, instincts: instincts.instincts });
      } else if (view === 'security') {
        const res = await agencyApi.securityAudit();
        setData(res);
      } else if (view === 'functions') {
        const res = await functionsApi.list();
        setData(res);
      }
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  if (loading) return <div className="flex-1 flex items-center justify-center">جاري التحميل...</div>;

  if (view === 'tools') {
    return (
      <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Wrench className="text-orange-600"/>الأدوات - Open WebUI Tools</h1>
          <p className="text-zinc-600 mb-6 text-sm">Tools توسع قدرات LLM - جمع بيانات حية، طقس، أسعار، تنفيذ كود</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data?.tools?.map((tool: any) => (
              <div key={tool.id} className="bg-white rounded-2xl border p-5">
                <div className="w-10 h-10 rounded-xl bg-orange-100 flex items-center justify-center mb-3"><Wrench size={18} className="text-orange-600"/></div>
                <div className="font-semibold text-sm">{tool.name}</div>
                <div className="text-xs text-zinc-500 mt-1">{tool.description}</div>
                <div className="flex gap-2 mt-3">
                  <span className="text-[10px] px-2 py-1 bg-zinc-100 rounded-full">{tool.category}</span>
                  <span className={`text-[10px] px-2 py-1 rounded-full ${tool.enabled?'bg-green-100 text-green-700':'bg-red-100 text-red-700'}`}>{tool.enabled?'مفعل':'معطل'}</span>
                </div>
                <details className="mt-3">
                  <summary className="text-xs text-violet-600 cursor-pointer">عرض Schema</summary>
                  <pre className="mt-2 text-[10px] bg-zinc-900 text-zinc-100 p-3 rounded-xl overflow-x-auto">{JSON.stringify(tool.schema, null, 2)}</pre>
                </details>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (view === 'memory') {
    return (
      <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Brain className="text-pink-600"/>الذاكرة والـ Instincts</h1>
          <p className="text-zinc-600 mb-6 text-sm">ECC: SessionStart/End hooks تحفظ وتعيد تحميل السياق، مع سقف أحرف حتى لا ينفجر الـ context window</p>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4">الذاكرة ({data?.memories?.length || 0})</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {data?.memories?.map((m: any) => (
                  <div key={m.id} className="p-3 bg-zinc-50 rounded-xl border text-sm">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] px-2 py-0.5 bg-violet-100 text-violet-700 rounded-full">{m.type}</span>
                      <span className="text-[10px] text-zinc-400">{new Date(m.created_at).toLocaleString('ar')}</span>
                      <span className="ml-auto text-[10px]">ثقة: {Math.round(m.confidence*100)}%</span>
                    </div>
                    <div className="text-xs text-zinc-700">{m.content.slice(0,200)}</div>
                  </div>
                ))}
                {(!data?.memories || data.memories.length===0) && <div className="text-sm text-zinc-400">لا توجد ذاكرة بعد - ابدأ محادثة ليتم الحفظ تلقائياً</div>}
              </div>
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2"><Zap size={16} className="text-amber-500"/>Instincts - التعلم المستمر</h3>
              <p className="text-xs text-zinc-500 mb-4">يستخرج الأنماط من جلساتك إلى instincts قابلة لإعادة الاستخدام مع confidence scoring، ثم يجمعها إلى مهارات عبر /evolve</p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {data?.instincts?.map((inst: any) => (
                  <div key={inst.id} className="p-3 bg-amber-50/50 border border-amber-100 rounded-xl text-sm">
                    <div className="font-medium text-xs">{inst.pattern}</div>
                    <div className="text-xs text-zinc-600 mt-1">{inst.description.slice(0,120)}</div>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-[10px] px-2 py-0.5 bg-amber-100 text-amber-700 rounded-full">ثقة {Math.round(inst.confidence*100)}%</span>
                      <span className="text-[10px] text-zinc-500">استخدم {inst.usage_count}x</span>
                      <span className="text-[10px] text-zinc-500">نجاح {Math.round(inst.success_rate*100)}%</span>
                    </div>
                  </div>
                ))}
                {(!data?.instincts || data.instincts.length===0) && <div className="text-sm text-zinc-400">لا توجد instincts بعد - سيتعلم النظام تلقائياً من استخدام الأدوات</div>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (view === 'security') {
    return (
      <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Shield className="text-red-600"/>AgentShield - فحص الأمان</h1>
          <p className="text-zinc-600 mb-6 text-sm">يفحص prompts, hooks, MCP config, permissions, secrets, agent files - مثل ECC</p>
          
          {data && (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-white rounded-2xl border p-5">
                  <div className="text-2xl font-bold text-red-600">{data.critical || 0}</div>
                  <div className="text-xs text-zinc-500">حرج</div>
                </div>
                <div className="bg-white rounded-2xl border p-5">
                  <div className="text-2xl font-bold text-orange-600">{data.high || 0}</div>
                  <div className="text-xs text-zinc-500">عالي</div>
                </div>
                <div className="bg-white rounded-2xl border p-5">
                  <div className="text-2xl font-bold text-amber-600">{data.medium || 0}</div>
                  <div className="text-xs text-zinc-500">متوسط</div>
                </div>
                <div className="bg-white rounded-2xl border p-5">
                  <div className="text-2xl font-bold">{data.total_issues || 0}</div>
                  <div className="text-xs text-zinc-500">الإجمالي</div>
                </div>
              </div>

              <div className="bg-white rounded-2xl border p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold">حالة النظام: <span className={`px-3 py-1 rounded-full text-xs ${data.status==='secure'?'bg-green-100 text-green-700':data.status==='warning'?'bg-amber-100 text-amber-700':'bg-red-100 text-red-700'}`}>{data.status}</span></h3>
                  <div className="text-xs text-zinc-500">فحص {data.scanned?.agents || 0} وكيل، {data.scanned?.skills || 0} مهارة</div>
                </div>
                
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {data.issues?.map((issue: any, i: number) => (
                    <div key={i} className={`p-3 rounded-xl border text-sm ${issue.severity==='critical'?'bg-red-50 border-red-200':issue.severity==='high'?'bg-orange-50 border-orange-200':'bg-zinc-50'}`}>
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${issue.severity==='critical'?'bg-red-600 text-white':issue.severity==='high'?'bg-orange-500 text-white':'bg-zinc-200'}`}>{issue.severity}</span>
                        <span className="text-xs font-medium">{issue.type}</span>
                        <span className="text-xs text-zinc-500 ml-auto">{issue.file}</span>
                      </div>
                      <div className="text-xs mt-1">{issue.message}</div>
                    </div>
                  ))}
                  {(!data.issues || data.issues.length===0) && <div className="text-center py-8"><Shield size={32} className="mx-auto text-green-500 mb-2"/><div className="text-sm font-medium text-green-700">النظام آمن - لا توجد مشاكل</div></div>}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    );
  }

  // Functions view
  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Filter className="text-indigo-600"/>Functions - Pipe, Filter, Action, Event</h1>
        <p className="text-zinc-600 mb-6 text-sm">Functions توسع قدرات Open WebUI نفسه - إضافة نماذج، أزرار، فلاتر، أحداث</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data?.functions?.map((fn: any) => (
            <div key={fn.id} className="bg-white rounded-2xl border p-5">
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-semibold text-sm flex items-center gap-2">
                    {fn.name}
                    <span className={`text-[10px] px-2 py-0.5 rounded-full ${fn.type==='pipe'?'bg-blue-100 text-blue-700':fn.type==='filter'?'bg-amber-100 text-amber-700':fn.type==='action'?'bg-green-100 text-green-700':'bg-purple-100 text-purple-700'}`}>{fn.type}</span>
                  </div>
                  <div className="text-xs text-zinc-500 mt-1">{fn.description}</div>
                </div>
                <span className={`text-[10px] px-2 py-1 rounded-full ${fn.enabled?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{fn.enabled?'مفعل':'معطل'}</span>
              </div>
              <details className="mt-3">
                <summary className="text-xs text-violet-600 cursor-pointer">عرض الكود</summary>
                <pre className="mt-2 text-[10px] bg-zinc-900 text-zinc-100 p-3 rounded-xl overflow-x-auto">{fn.code.slice(0,800)}...</pre>
              </details>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
