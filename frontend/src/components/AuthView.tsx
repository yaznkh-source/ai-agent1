import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function AuthView() {
  const [accounts, setAccounts] = useState<any[]>([]);
  const [loginForm, setLoginForm] = useState({ username: 'admin', password: 'admin123' });
  const [token, setToken] = useState<string>('');
  const [user, setUser] = useState<any>(null);
  const [costs, setCosts] = useState<any>(null);

  useEffect(() => {
    fetch('/api/auth/demo-accounts').then(r=>r.json()).then(d=>setAccounts(d.accounts||[]));
    const saved = localStorage.getItem('token');
    if (saved) setToken(saved);
  }, []);

  const login = async () => {
    try {
      const res = await api.post('/auth/login', loginForm);
      setToken(res.data.access_token);
      setUser(res.data.user);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
    } catch (e: any) {
      alert('Login failed: ' + e.message);
    }
  };

  const getMe = async () => {
    try {
      const res = await api.get('/auth/me', { headers: { Authorization: `Bearer ${token}` } });
      setUser(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const getCosts = async () => {
    try {
      const res = await api.get('/auth/costs', { headers: { Authorization: `Bearer ${token}` } });
      setCosts(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">🔐 نظام المصادقة - JWT + RBAC</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">تسجيل دخول</h3>
            <div className="space-y-3">
              <input value={loginForm.username} onChange={e=>setLoginForm({...loginForm, username:e.target.value})} placeholder="Username" className="w-full px-4 py-2.5 border rounded-xl" />
              <input type="password" value={loginForm.password} onChange={e=>setLoginForm({...loginForm, password:e.target.value})} placeholder="Password" className="w-full px-4 py-2.5 border rounded-xl" />
              <button onClick={login} className="w-full py-2.5 bg-violet-600 text-white rounded-xl">دخول</button>
              {token && <div className="text-xs bg-zinc-900 text-zinc-100 p-3 rounded-xl break-all">Token: {token.slice(0,50)}...</div>}
              {user && <div className="text-sm bg-green-50 border border-green-200 p-3 rounded-xl">مرحبا {user.username} - دور: {user.role}</div>}
            </div>
            <div className="mt-4 flex gap-2">
              <button onClick={getMe} className="px-4 py-2 bg-zinc-100 rounded-xl text-sm">/me</button>
              <button onClick={getCosts} className="px-4 py-2 bg-zinc-100 rounded-xl text-sm">التكاليف</button>
            </div>
            {costs && <pre className="mt-3 text-xs bg-zinc-900 text-zinc-100 p-3 rounded-xl overflow-auto">{JSON.stringify(costs, null, 2)}</pre>}
          </div>

          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">حسابات تجريبية</h3>
            <div className="space-y-2">
              {accounts.map((acc:any) => (
                <div key={acc.username} className="p-3 bg-zinc-50 rounded-xl border flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm">{acc.username} / {acc.password}</div>
                    <div className="text-xs text-zinc-500">{acc.role} - {acc.desc}</div>
                  </div>
                  <button onClick={()=>setLoginForm({username:acc.username, password:acc.password})} className="px-3 py-1 bg-violet-100 text-violet-700 rounded-full text-xs">استخدام</button>
                </div>
              ))}
            </div>
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl text-sm">
              <div className="font-semibold text-blue-900">🔑 RBAC هرمية الأدوار:</div>
              <div className="text-xs text-blue-800 mt-2 space-y-1">
                <div>super_admin (100) - كل شيء</div>
                <div>agency_owner (80) - إدارة الوكالة + الفوترة</div>
                <div>agency_member (50) - مشاريع ومهام</div>
                <div>client (20) - عرض مشاريعه فقط</div>
                <div>user (10) - محادثات فقط</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 bg-white rounded-2xl border p-6">
          <h3 className="font-semibold mb-3">📊 تتبع التكلفة (Track A1)</h3>
          <p className="text-sm text-zinc-600 mb-4">كل استدعاء LLM يحسب تكلفته: prompt_tokens + completion_tokens × سعر الموديل. مفيد للربحية.</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div className="p-3 bg-zinc-50 rounded-xl"><div className="font-bold">gpt-4o-mini</div><div>Input: $0.15/1M</div><div>Output: $0.6/1M</div></div>
            <div className="p-3 bg-zinc-50 rounded-xl"><div className="font-bold">gpt-4o</div><div>Input: $5/1M</div><div>Output: $15/1M</div></div>
            <div className="p-3 bg-zinc-50 rounded-xl"><div className="font-bold">claude-3.5</div><div>Input: $3/1M</div><div>Output: $15/1M</div></div>
            <div className="p-3 bg-green-50 border border-green-200 rounded-xl"><div className="font-bold">llama3.1:8b</div><div>مجاني محلي</div><div>via Ollama</div></div>
          </div>
        </div>
      </div>
    </div>
  );
}
