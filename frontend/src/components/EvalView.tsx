import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function EvalView() {
  const [datasets, setDatasets] = useState<any>({});
  const [runs, setRuns] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const [routerTask, setRouterTask] = useState('صمم API لنظام إدارة العملاء مع مصادقة');
  const [routerResult, setRouterResult] = useState<any>(null);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const [ds, r, m] = await Promise.all([
        api.get('/eval/datasets'),
        api.get('/eval/runs'),
        api.get('/eval/metrics')
      ]);
      setDatasets(ds.data.datasets || {});
      setRuns(r.data.runs || []);
      setMetrics(m.data);
    } catch {}
  };

  const runEval = async (dataset: string) => {
    try {
      await api.post('/eval/run', { dataset });
      load();
    } catch {}
  };

  const testRouter = async () => {
    try {
      const res = await api.post('/eval/agent-router', { task: routerTask });
      setRouterResult(res.data);
    } catch {}
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">📊 Eval Harness - تقييم أداء الوكلاء</h1>
        <p className="text-sm text-zinc-600 mb-6">مستوحى من ECC eval-harness - Evals كـ tests للذكاء الاصطناعي، مع golden dataset</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">مجموعات التقييم</h3>
            <div className="space-y-3">
              {Object.entries(datasets).map(([name, ds]: any) => (
                <div key={name} className="p-4 border rounded-xl">
                  <div className="flex items-center justify-between">
                    <div className="font-medium text-sm">{name} ({ds.count})</div>
                    <button onClick={()=>runEval(name)} className="px-3 py-1 bg-violet-600 text-white rounded-full text-xs">تشغيل</button>
                  </div>
                  <div className="text-xs text-zinc-500 mt-2">{JSON.stringify(ds.samples?.[0] || {}).slice(0,100)}...</div>
                </div>
              ))}
            </div>

            <div className="mt-6">
              <h4 className="font-medium text-sm mb-3">آخر التشغيلات</h4>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {runs.slice(-5).reverse().map((run:any) => (
                  <div key={run.run_id} className="p-3 bg-zinc-50 rounded-xl text-xs flex items-center justify-between">
                    <div>
                      <div className="font-medium">{run.dataset} - {(run.accuracy*100).toFixed(1)}%</div>
                      <div className="text-zinc-500">{run.correct}/{run.total} صحيح - {run.duration.toFixed(2)}s</div>
                    </div>
                    <div className={`w-2 h-2 rounded-full ${run.accuracy>0.8?'bg-green-500':run.accuracy>0.6?'bg-amber-500':'bg-red-500'}`} />
                  </div>
                ))}
              </div>
            </div>

            {metrics && (
              <div className="mt-6 p-4 bg-violet-50 border border-violet-200 rounded-xl">
                <div className="text-sm font-medium">المقاييس:</div>
                <div className="text-xs mt-2 space-y-1">
                  <div>آخر دقة: {(metrics.latest_accuracy*100 || 0).toFixed(1)}%</div>
                  <div>متوسط: {(metrics.avg_accuracy*100 || 0).toFixed(1)}%</div>
                  <div>إجمالي: {metrics.total_runs} تشغيل</div>
                </div>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4">🧭 Agent Router ذكي (Track D4)</h3>
              <p className="text-xs text-zinc-500 mb-4">يحلل المهمة ويختار أفضل وكيل تلقائياً - مثل ECC agent-sort skill</p>
              <textarea value={routerTask} onChange={e=>setRouterTask(e.target.value)} className="w-full h-20 p-3 border rounded-xl text-sm" placeholder="اكتب مهمة..." />
              <button onClick={testRouter} className="mt-3 w-full py-2.5 bg-violet-600 text-white rounded-xl text-sm">اختبر التوجيه</button>
              
              {routerResult && (
                <div className="mt-4 p-4 bg-zinc-900 text-zinc-100 rounded-xl text-sm">
                  <div className="font-medium">المهمة: {routerResult.task}</div>
                  <div className="mt-3 p-3 bg-violet-600 rounded-xl">
                    <div className="font-bold">✅ الوكيل المختار: {routerResult.selected_agent.name} ({routerResult.selected_agent.id})</div>
                    <div className="text-xs text-violet-100 mt-1">السبب: {routerResult.selected_agent.reason}</div>
                    <div className="text-xs text-violet-200 mt-1">ثقة: {(routerResult.confidence*100).toFixed(0)}%</div>
                  </div>
                  <div className="mt-3">
                    <div className="text-xs text-zinc-400">بدائل:</div>
                    {routerResult.alternatives?.map((alt:any) => (
                      <div key={alt.id} className="text-xs mt-1">• {alt.name} ({alt.id})</div>
                    ))}
                  </div>
                  <div className="text-xs text-zinc-500 mt-3">{routerResult.routing_logic}</div>
                </div>
              )}
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-3">🎯 كيف نستخدم Eval في الوكالة</h3>
              <div className="text-sm text-zinc-600 space-y-2">
                <div>• <strong>قبل التوظيف:</strong> اختبر وكيل جديد على golden dataset</div>
                <div>• <strong>CI:</strong> شغل evals على كل PR - امنع الدمج إذا الدقة نزلت &gt;2%</div>
                <div>• <strong>تحسين:</strong> A/B test للـ prompts - قارن accuracy/cost/latency</div>
                <div>• <strong>تسعير:</strong> اعرف أي وكيل أرخص لنفس الجودة</div>
              </div>
              <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs">
                في الإنتاج: اربط مع Langfuse للـ tracing + اجمع feedback حقيقي من العملاء
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
