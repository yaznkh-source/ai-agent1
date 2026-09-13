import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function IntegrationsView() {
  const [integrations, setIntegrations] = useState<any>(null);
  const [testResult, setTestResult] = useState<any>(null);

  useEffect(() => {
    api.get('/integrations/').then(r=>setIntegrations(r.data)).catch(()=>{});
  }, []);

  const testGithub = async () => {
    try {
      const res = await api.post('/integrations/github/webhook', { action: 'opened', number: 42, pull_request: { number: 42 } }, { headers: { 'X-GitHub-Event': 'pull_request' } });
      setTestResult(res.data);
    } catch (e:any) { setTestResult({ error: e.message }); }
  };

  const testSlack = async () => {
    try {
      const form = new FormData();
      form.append('text', 'أنشئ API للعملاء');
      form.append('user_name', 'yazn');
      form.append('channel_name', 'dev');
      const res = await api.post('/integrations/slack/command', form, { headers: { 'Content-Type': 'multipart/form-data' } });
      setTestResult(res.data);
    } catch (e:any) { setTestResult({ error: e.message }); }
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">🔌 التكاملات - Slack, Discord, GitHub, n8n, WhatsApp</h1>
        <p className="text-sm text-zinc-600 mb-6">Track C3 - تكاملات الفريق مثل ECC Tools GitHub App + Open WebUI n8n pipeline</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {[
            { id: 'slack', name: 'Slack', icon: '💬', desc: 'Slash command /agency', color: 'bg-purple-100' },
            { id: 'discord', name: 'Discord', icon: '🎮', desc: 'Bot webhook', color: 'bg-indigo-100' },
            { id: 'github', name: 'GitHub', icon: '🐙', desc: 'PR review + verification', color: 'bg-zinc-100' },
            { id: 'n8n', name: 'n8n', icon: '⚡', desc: '300+ integrations', color: 'bg-red-100' },
            { id: 'whatsapp', name: 'WhatsApp', icon: '📱', desc: 'Business API', color: 'bg-green-100' },
            { id: 'telegram', name: 'Telegram', icon: '✈️', desc: 'Bot API', color: 'bg-blue-100' },
          ].map(intg => (
            <div key={intg.id} className="bg-white rounded-2xl border p-5">
              <div className={`w-12 h-12 rounded-xl ${intg.color} flex items-center justify-center text-xl mb-3`}>{intg.icon}</div>
              <div className="font-semibold">{intg.name}</div>
              <div className="text-xs text-zinc-500 mt-1">{intg.desc}</div>
              <div className="mt-3 flex items-center gap-2">
                <span className={`text-xs px-2 py-1 rounded-full ${integrations?.integrations?.[intg.id]?.enabled?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{integrations?.integrations?.[intg.id]?.enabled?'مفعل':'غير مفعل'}</span>
                <span className="text-xs text-zinc-400">{intg.id}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">🧪 اختبار التكاملات</h3>
            <div className="space-y-3">
              <button onClick={testGithub} className="w-full py-2.5 bg-zinc-900 text-white rounded-xl text-sm">اختبر GitHub PR webhook</button>
              <button onClick={testSlack} className="w-full py-2.5 bg-purple-600 text-white rounded-xl text-sm">اختبر Slack /agency command</button>
              <button onClick={async()=>{ const r=await api.post('/integrations/n8n/webhook', { task: 'ابحث عن عملاء SaaS', pipeline_id: 'research-to-code' }); setTestResult(r.data); }} className="w-full py-2.5 bg-red-600 text-white rounded-xl text-sm">اختبر n8n webhook</button>
            </div>

            {testResult && (
              <div className="mt-6 p-4 bg-zinc-900 text-zinc-100 rounded-xl text-xs overflow-auto max-h-96">
                <pre className="whitespace-pre-wrap">{JSON.stringify(testResult, null, 2)}</pre>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-3">🐙 GitHub App - مثل ECC Tools</h3>
              <div className="text-sm text-zinc-600 space-y-2">
                <div>1. أضف webhook في repo: <code className="bg-zinc-100 px-2 py-1 rounded">POST /api/integrations/github/webhook</code></div>
                <div>2. Events: pull_request, push, issue_comment</div>
                <div>3. في تعليق PR اكتب: <code className="bg-zinc-100 px-2 py-1 rounded">/agency review</code> أو <code className="bg-zinc-100 px-2 py-1 rounded">/ecc-tools analyze</code></div>
                <div>4. البوت يرد بمراجعة + فحص أمان + verification</div>
              </div>
              <div className="mt-4 p-3 bg-zinc-50 rounded-xl text-xs font-mono">
                Example review:<br/>
                🔍 AI Agency OS Review PR #42:<br/>
                - 2 medium security issues<br/>
                - Build: passed<br/>
                - Tests: 42 passed<br/>
                - Recommendation: Approve with minor fixes
              </div>
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-3">⚡ n8n - Open WebUI Inspiration</h3>
              <div className="text-sm text-zinc-600 space-y-2">
                <div>في n8n أنشئ HTTP Request node:</div>
                <div className="p-3 bg-zinc-900 text-zinc-100 rounded-xl text-xs font-mono">
                  Method: POST<br/>
                  URL: /api/integrations/n8n/webhook<br/>
                  Body: {"{"}"task": "ابحث عن...", "pipeline_id": "research-to-code"{"}"}
                </div>
                <div>النتيجة ترجع لـ n8n وتكمل workflow مع 300+ خدمة</div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-violet-50 to-indigo-50 border border-violet-200 rounded-2xl p-5">
              <h4 className="font-semibold text-violet-900 mb-2">💡 فكرة للوكالة</h4>
              <div className="text-sm text-violet-800">
                العميل يرسل رسالة واتساب: "أريد متجر إلكتروني"<br/>
                → WhatsApp webhook → agent-sort يختار planner → يولد proposal → يرسل PDF للعميل أوتوماتيك<br/>
                → كل هذا عبر n8n بدون كود!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
