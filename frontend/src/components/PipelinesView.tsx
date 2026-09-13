import { useEffect, useState } from 'react';
import { pipelinesApi } from '../lib/api';
import { Workflow, Play, Clock, CheckCircle, XCircle } from 'lucide-react';

export default function PipelinesView() {
  const [pipelines, setPipelines] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [context, setContext] = useState('{"task": "أنشئ نظام إدارة عملاء بسيط", "client_name": "شركة التقنية"}');
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => { load(); loadHistory(); }, []);

  const load = async () => {
    try {
      const data = await pipelinesApi.list();
      setPipelines(data.pipelines || []);
    } catch (e) { console.error(e); }
  };

  const loadHistory = async () => {
    try {
      const data = await pipelinesApi.history();
      setHistory(data.history || []);
    } catch {}
  };

  const selectPipeline = async (p: any) => {
    try {
      const full = await pipelinesApi.get(p.id);
      setSelected(full);
      setResult(null);
    } catch (e) { console.error(e); }
  };

  const execute = async () => {
    if (!selected) return;
    setExecuting(true);
    try {
      const ctx = JSON.parse(context);
      const res = await pipelinesApi.execute(selected.id, ctx);
      setResult(res);
      loadHistory();
    } catch (e: any) {
      setResult({ error: e.message, status: 'failed' });
    }
    setExecuting(false);
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      <div className="w-96 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h2 className="font-bold text-lg flex items-center gap-2">
            <Workflow className="text-blue-600" />
            Pipelines
            <span className="ml-auto text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">{pipelines.length}</span>
          </h2>
          <p className="text-xs text-zinc-500 mt-1">إطار عمل OpenAI API متوافق - لفصل المعالجة الثقيلة</p>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {pipelines.map(p => (
            <button key={p.id} onClick={() => selectPipeline(p)} className={`w-full text-left p-4 rounded-xl border transition-all ${selected?.id===p.id?'bg-blue-50 border-blue-200':'bg-white hover:shadow-sm'}`}>
              <div className="font-medium text-sm">{p.name}</div>
              <div className="text-xs text-zinc-500 mt-1 line-clamp-2">{p.description}</div>
              <div className="flex items-center gap-2 mt-3 text-[11px] text-zinc-400">
                <Clock size={12} />
                {p.steps_count} خطوات
                <span className={`ml-auto px-2 py-0.5 rounded-full ${p.status==='completed'?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{p.status}</span>
              </div>
            </button>
          ))}
        </div>

        <div className="p-3 border-t">
          <h4 className="text-xs font-semibold text-zinc-500 uppercase mb-2">السجل الأخير</h4>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {history.slice(0,5).map((h: any, i: number) => (
              <div key={i} className="text-xs p-2 bg-zinc-50 rounded-lg flex items-center gap-2">
                {h.status==='completed'?<CheckCircle size={12} className="text-green-500"/>:<XCircle size={12} className="text-red-400"/>}
                <span className="truncate">{h.pipeline_name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        {selected ? (
          <div className="max-w-4xl">
            <div className="bg-white rounded-2xl border p-6 mb-6">
              <h1 className="text-2xl font-bold">{selected.name}</h1>
              <p className="text-zinc-600 mt-2">{selected.description}</p>
              
              <div className="mt-6">
                <h3 className="font-semibold mb-3">خطوات المسار ({selected.steps?.length})</h3>
                <div className="space-y-3">
                  {selected.steps?.map((step: any, idx: number) => (
                    <div key={step.id} className="flex gap-4 p-4 bg-zinc-50 rounded-xl border">
                      <div className="w-8 h-8 rounded-full bg-white border flex items-center justify-center text-xs font-bold flex-shrink-0">{idx+1}</div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-sm flex items-center gap-2">
                          {step.name}
                          <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-[10px]">{step.type}</span>
                        </div>
                        <div className="text-xs text-zinc-500 mt-1 truncate">{JSON.stringify(step.config).slice(0,120)}...</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl border p-6 mb-6">
              <h3 className="font-semibold mb-3">تنفيذ المسار</h3>
              <p className="text-xs text-zinc-500 mb-3">Context JSON - المتغيرات التي ستُستخدم في القوالب مثل {"{task}"} </p>
              <textarea
                value={context}
                onChange={e => setContext(e.target.value)}
                className="w-full h-32 p-4 border rounded-xl font-mono text-sm focus:ring-2 focus:ring-blue-200 outline-none"
              />
              <button onClick={execute} disabled={executing} className="mt-4 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-300 text-white rounded-xl font-medium flex items-center gap-2">
                {executing ? <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"/>جاري التنفيذ...</> : <><Play size={16}/>تنفيذ</>}
              </button>
            </div>

            {result && (
              <div className="bg-white rounded-2xl border p-6">
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  {result.status==='completed'?<CheckCircle className="text-green-500" size={18}/>:<XCircle className="text-red-500" size={18}/>}
                  نتيجة التنفيذ - {result.status}
                </h3>
                <div className="space-y-3">
                  {result.steps?.map((s: any, i: number) => (
                    <div key={i} className={`p-3 rounded-xl border text-sm ${s.status==='completed'?'bg-green-50 border-green-200':'bg-red-50 border-red-200'}`}>
                      <div className="font-medium">{s.step_name} - {s.status}</div>
                      <div className="text-xs mt-1 opacity-75 truncate">{JSON.stringify(s.result)?.slice(0,200)}</div>
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-4 bg-zinc-900 text-zinc-100 rounded-xl">
                  <div className="text-xs text-zinc-400 mb-2">النتيجة النهائية:</div>
                  <pre className="text-sm whitespace-pre-wrap">{result.final_result || JSON.stringify(result, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <Workflow size={48} className="mx-auto text-zinc-300 mb-4" />
              <h3 className="font-semibold">اختر Pipeline للتنفيذ</h3>
              <p className="text-sm text-zinc-500 mt-2 max-w-md">Pipelines هي إطار عمل Open WebUI لتحويل الميزات إلى صيغة متوافقة مع OpenAI API، لفصل المعالجة الثقيلة عن الواجهة الرئيسية</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
