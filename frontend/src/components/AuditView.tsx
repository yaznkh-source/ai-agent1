import { useEffect, useState } from 'react';
import api from '../lib/api';
import { ShieldCheck, AlertTriangle, Activity, User, Clock } from 'lucide-react';

export default function AuditView() {
  const [logs, setLogs] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [security, setSecurity] = useState<any>(null);
  const [filterAction, setFilterAction] = useState('');

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const [logsRes, statsRes, secRes] = await Promise.all([
        api.get('/audit/logs', { params: { limit: 50 } }),
        api.get('/audit/stats'),
        api.get('/audit/security')
      ]);
      setLogs(logsRes.data.logs);
      setStats(statsRes.data);
      setSecurity(secRes.data);
    } catch {}
  };

  const filteredLogs = filterAction ? logs.filter(l=>l.action===filterAction) : logs;

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><ShieldCheck className="text-violet-600"/>سجل التدقيق - Audit Logs</h1>
        <p className="text-sm text-zinc-600 mb-6">SOC2, GDPR compliance - تتبع كل الإجراءات، للامتثال والأمان</p>

        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{stats.total_logs}</div><div className="text-xs text-zinc-500">إجمالي سجلات</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold text-violet-600">{stats.last_24h}</div><div className="text-xs text-zinc-500">آخر 24 ساعة</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold text-green-600">{stats.success_rate}</div><div className="text-xs text-zinc-500">معدل نجاح</div></div>
            <div className="bg-white rounded-2xl border p-5 bg-gradient-to-br from-violet-600 to-indigo-600 text-white"><div className="text-sm font-bold">{stats.most_common_action?.[0]}</div><div className="text-xs text-violet-100">أكثر إجراء: {stats.most_common_action?.[1]} مرة</div></div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2 bg-white rounded-2xl border p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold flex items-center gap-2"><Activity size={16}/>آخر السجلات</h3>
              <select value={filterAction} onChange={e=>setFilterAction(e.target.value)} className="px-3 py-1.5 border rounded-xl text-xs">
                <option value="">كل الإجراءات</option>
                <option value="agent_run">تشغيل وكيل</option>
                <option value="skill_used">استخدام مهارة</option>
                <option value="login">تسجيل دخول</option>
                <option value="file_uploaded">رفع ملف</option>
              </select>
            </div>
            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {filteredLogs.map((log:any) => (
                <div key={log.id} className={`p-3 rounded-xl border text-xs flex items-center gap-3 ${log.status==='failed'?'bg-red-50 border-red-200':'bg-zinc-50'}`}>
                  <div className={`w-2 h-2 rounded-full ${log.status==='success'?'bg-green-500':'bg-red-500'}`} />
                  <div className="flex-1">
                    <div className="font-medium">{log.action} - {log.resource_type}:{log.resource.slice(0,8)}</div>
                    <div className="text-zinc-500 flex items-center gap-2 mt-1"><User size={10}/>{log.user_email} <Clock size={10}/>{new Date(log.timestamp).toLocaleTimeString('ar')}</div>
                  </div>
                  <div className="text-zinc-400">{log.ip}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            {security && (
              <>
                <div className="bg-white rounded-2xl border p-5">
                  <h4 className="font-semibold text-sm mb-3 flex items-center gap-2"><AlertTriangle size={14} className="text-amber-500"/>الأمان</h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between"><span>فشل تسجيل دخول 24س:</span><span className={security.failed_logins_24h>3?'text-red-600 font-bold':'text-green-600'}>{security.failed_logins_24h}</span></div>
                    <div className="flex justify-between"><span>مفاتيح API 7أيام:</span><span>{security.api_keys_created_7d}</span></div>
                  </div>
                  <div className="mt-4 space-y-2">
                    {security.recommendations?.map((rec:string,i:number) => (
                      <div key={i} className={`text-xs p-2 rounded-lg ${rec.startsWith('✅')?'bg-green-50 text-green-700':'bg-amber-50 text-amber-700'}`}>{rec}</div>
                    ))}
                  </div>
                </div>

                <div className="bg-white rounded-2xl border p-5">
                  <h4 className="font-semibold text-sm mb-3">الامتثال</h4>
                  <div className="space-y-3 text-xs">
                    <div>
                      <div className="font-medium">SOC2</div>
                      <div className="mt-1 space-y-1">
                        {Object.entries(security.compliance?.soc2||{}).map(([k,v]:any)=><div key={k} className="flex justify-between"><span>{k}</span><span>{v}</span></div>)}
                      </div>
                    </div>
                    <div>
                      <div className="font-medium">GDPR</div>
                      <div className="mt-1 space-y-1">
                        {Object.entries(security.compliance?.gdpr||{}).map(([k,v]:any)=><div key={k} className="flex justify-between"><span>{k}</span><span>{v}</span></div>)}
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {stats && (
              <div className="bg-white rounded-2xl border p-5">
                <h4 className="font-semibold text-sm mb-3">حسب الإجراء</h4>
                <div className="space-y-2">
                  {Object.entries(stats.by_action||{}).map(([action,count]:any)=>(
                    <div key={action} className="flex justify-between text-xs"><span>{action}</span><span className="bg-violet-100 text-violet-700 px-2 py-0.5 rounded-full">{count}</span></div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="bg-zinc-900 text-zinc-100 rounded-2xl p-6">
          <h4 className="font-semibold mb-3">💡 لماذا Audit Logs مهم للوكالة؟</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div><div className="font-medium text-violet-400">1. SOC2 Compliance</div><div className="text-xs text-zinc-400 mt-1">العملاء المؤسسات يطلبون سجل تدقيق كامل - بدونه لا تبيع لـ Enterprise</div></div>
            <div><div className="font-medium text-violet-400">2. تتبع التكلفة</div><div className="text-xs text-zinc-400 mt-1">كل agent_run يسجل cost - تعرف أي عميل/مهمة تكلف أكثر</div></div>
            <div><div className="font-medium text-violet-400">3. الأمان</div><div className="text-xs text-zinc-400 mt-1">كشف محاولات اختراق، تتبع من فعل ماذا ومتى</div></div>
          </div>
        </div>
      </div>
    </div>
  );
}
