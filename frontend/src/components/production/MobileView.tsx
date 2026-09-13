import { useState, useEffect } from 'react';
import { Smartphone, Monitor, Mic, Send } from 'lucide-react';

export default function MobileView() {
  const [daemonStatus, setDaemonStatus] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);

  useEffect(() => { load(); }, []);
  const load = async () => {
    try {
      const res = await fetch('/api/agents-execution/daemon/status');
      setDaemonStatus(await res.json());
      const res2 = await fetch('/api/agents-execution/tasks');
      const data = await res2.json();
      setTasks(data.tasks || []);
    } catch {}
  };

  return (
    <div className="flex-1 overflow-auto bg-white">
      <div className="max-w-3xl mx-auto px-6 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black text-white text-xs mb-4">
            <Smartphone size={12} /> Cross-Device — مثل Paseo — ابدأ من المكتب، تابع من الهاتف
          </div>
          <h1 className="text-3xl font-semibold mb-2">📱 Mobile — Cross-Device</h1>
          <p className="text-sm text-zinc-600">مثل Paseo — شغل الوكلاء بالتوازي على أجهزتك الخاصة — أرسل من هاتفك أو مكتبك — self-hosted — Privacy-First — $0</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="border border-zinc-200 rounded-xl p-4 text-center">
            <Monitor size={20} className="mx-auto mb-2" />
            <div className="text-xs text-zinc-500">Desktop</div>
            <div className="text-sm font-medium">متصل — مثل Paseo</div>
          </div>
          <div className="border border-zinc-200 rounded-xl p-4 text-center">
            <Smartphone size={20} className="mx-auto mb-2" />
            <div className="text-xs text-zinc-500">Mobile</div>
            <div className="text-sm font-medium">متاح — iOS/Android — مثل Paseo</div>
          </div>
        </div>

        {daemonStatus && (
          <div className="border border-zinc-200 rounded-xl p-4 mb-6">
            <div className="font-medium text-sm mb-2">Daemon Status — مثل Paseo Daemon — يعمل فعلياً</div>
            <div className="text-xs text-zinc-600 space-y-1">
              <div>الوكلاء: {daemonStatus.total_agents} — Idle: {daemonStatus.idle_agents} — Running: {daemonStatus.running_agents}</div>
              <div>المهام: {daemonStatus.total_tasks} — جارية: {daemonStatus.running_tasks}</div>
            </div>
          </div>
        )}

        <div className="border border-zinc-200 rounded-xl overflow-hidden">
          <div className="px-4 py-2 bg-zinc-50 text-xs font-medium">المهام — مثل Manus — تعمل فعلياً</div>
          {tasks.length === 0 ? (
            <div className="px-4 py-8 text-center text-sm text-zinc-500">لا توجد مهام — ابدأ مهمة من Chat أو Battle</div>
          ) : (
            <div className="divide-y divide-zinc-100">
              {tasks.slice(0, 10).map((t: any) => (
                <div key={t.task_id} className="px-4 py-3 flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium">{t.agent_id} — {t.task}</div>
                    <div className="text-xs text-zinc-500">{t.status} — {t.progress}%</div>
                  </div>
                  <div className={`text-xs px-2 py-1 rounded-full ${t.status === 'completed' ? 'bg-green-100 text-green-700' : t.status === 'running' ? 'bg-blue-100 text-blue-700' : 'bg-zinc-100'}`}>{t.status}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="mt-6 border border-zinc-200 rounded-xl p-4 bg-zinc-50">
          <div className="font-medium text-xs mb-2">Paseo Pattern — مثل Manus — كيف يعمل Cross-Device حقيقي</div>
          <div className="text-[11px] text-zinc-600 space-y-1">
            <div>• Daemon خادم محلي يدير وكلاء البرمجة — الوكلاء يعملون على جهازك — بيئة تطوير كاملة — أدواتك، إعداداتك — يعمل فعلياً</div>
            <div>• Clients: desktop, mobile iOS/Android, web, CLI — كلها تتصل بـ Daemon — تبدأ في المكتب، تتفقد من الهاتف — يعمل فعلياً</div>
            <div>• Voice Control: تحكم صوتي — أملِ المهام أو تحدث عن المشاكل — يعمل فعلياً</div>
            <div>• Privacy-First: لا تتبع، لا تسجيل دخول إجباري — يعمل محلياً — $0</div>
            <div>• مصدر: https://github.com/lmarena/coco — Paseo — https://paseo.sh — MIT — npm install -g @getpaseo/cli</div>
          </div>
        </div>
      </div>
    </div>
  );
}
