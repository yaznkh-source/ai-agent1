import { useEffect, useState } from 'react';
import { agencyApi } from '../lib/api';
import { LayoutDashboard, Users, FolderKanban, CheckSquare, Plus, BarChart3 } from 'lucide-react';

export default function AgencyView() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [clients, setClients] = useState<any[]>([]);
  const [projects, setProjects] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [showCreateClient, setShowCreateClient] = useState(false);
  const [newClient, setNewClient] = useState({ name: '', company: '', email: '' });

  useEffect(() => { loadAll(); }, []);

  const loadAll = async () => {
    try {
      const [dash, cl, pr, ta] = await Promise.all([
        agencyApi.dashboard(),
        agencyApi.clients(),
        agencyApi.projects(),
        agencyApi.tasks()
      ]);
      setDashboard(dash);
      setClients(cl);
      setProjects(pr);
      setTasks(ta);
    } catch (e) { console.error(e); }
  };

  const createClient = async () => {
    if (!newClient.name.trim()) return;
    try {
      await agencyApi.createClient(newClient);
      setNewClient({ name: '', company: '', email: '' });
      setShowCreateClient(false);
      loadAll();
    } catch (e) { console.error(e); }
  };

  if (activeTab === 'dashboard') {
    return (
      <div className="flex-1 bg-zinc-50 overflow-y-auto p-6">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
            <LayoutDashboard className="text-violet-600" />
            لوحة تحكم الوكالة
          </h1>
          <p className="text-zinc-600 mb-8">نظام إدارة العملاء والمشاريع - AI Agency OS</p>

          {dashboard && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-white rounded-2xl border p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">{dashboard.stats.clients}</div>
                      <div className="text-sm text-zinc-500">العملاء</div>
                    </div>
                    <Users className="text-blue-500" />
                  </div>
                </div>
                <div className="bg-white rounded-2xl border p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">{dashboard.stats.projects}</div>
                      <div className="text-sm text-zinc-500">المشاريع</div>
                    </div>
                    <FolderKanban className="text-violet-500" />
                  </div>
                </div>
                <div className="bg-white rounded-2xl border p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">{dashboard.stats.tasks}</div>
                      <div className="text-sm text-zinc-500">المهام</div>
                    </div>
                    <CheckSquare className="text-amber-500" />
                  </div>
                </div>
                <div className="bg-white rounded-2xl border p-6 bg-gradient-to-br from-violet-600 to-indigo-600 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">{dashboard.stats.completion_rate}%</div>
                      <div className="text-sm text-violet-100">معدل الإنجاز</div>
                    </div>
                    <BarChart3 className="text-violet-200" />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-2xl border p-6">
                  <h3 className="font-semibold mb-4">المشاريع الأخيرة</h3>
                  <div className="space-y-3">
                    {dashboard.recent_projects?.map((p: any) => (
                      <div key={p.id} className="flex items-center justify-between p-3 bg-zinc-50 rounded-xl">
                        <div>
                          <div className="font-medium text-sm">{p.name}</div>
                          <div className="text-xs text-zinc-500">{new Date(p.updated_at).toLocaleDateString('ar')}</div>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs ${p.status==='active'?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{p.status}</span>
                      </div>
                    ))}
                    {(!dashboard.recent_projects || dashboard.recent_projects.length===0) && <div className="text-sm text-zinc-400">لا توجد مشاريع بعد</div>}
                  </div>
                </div>

                <div className="bg-white rounded-2xl border p-6">
                  <h3 className="font-semibold mb-4">المهام الأخيرة</h3>
                  <div className="space-y-2">
                    {dashboard.recent_tasks?.map((t: any) => (
                      <div key={t.id} className="flex items-center gap-3 p-2.5 bg-zinc-50 rounded-xl">
                        <div className={`w-2 h-2 rounded-full ${t.status==='done'?'bg-green-500':t.status==='in_progress'?'bg-amber-500':'bg-zinc-300'}`} />
                        <div className="flex-1 min-w-0">
                          <div className="text-sm truncate">{t.title}</div>
                          <div className="text-xs text-zinc-500">{t.priority} • {t.status}</div>
                        </div>
                      </div>
                    ))}
                    {(!dashboard.recent_tasks || dashboard.recent_tasks.length===0) && <div className="text-sm text-zinc-400">لا توجد مهام</div>}
                  </div>
                </div>
              </div>
            </>
          )}

          <div className="mt-8 flex gap-3">
            <button onClick={() => setActiveTab('clients')} className="px-4 py-2 bg-violet-600 text-white rounded-xl text-sm">إدارة العملاء</button>
            <button onClick={() => setActiveTab('projects')} className="px-4 py-2 bg-white border rounded-xl text-sm">المشاريع</button>
            <button onClick={() => setActiveTab('tasks')} className="px-4 py-2 bg-white border rounded-xl text-sm">المهام</button>
          </div>
        </div>
      </div>
    );
  }

  if (activeTab === 'clients') {
    return (
      <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold flex items-center gap-2"><Users className="text-blue-600"/>العملاء ({clients.length})</h1>
            <div className="flex gap-2">
              <button onClick={() => setActiveTab('dashboard')} className="px-4 py-2 bg-white border rounded-xl text-sm">لوحة التحكم</button>
              <button onClick={() => setShowCreateClient(!showCreateClient)} className="px-4 py-2 bg-violet-600 text-white rounded-xl text-sm flex items-center gap-2"><Plus size={16}/>عميل جديد</button>
            </div>
          </div>

          {showCreateClient && (
            <div className="bg-white rounded-2xl border p-6 mb-6">
              <h3 className="font-semibold mb-4">إضافة عميل جديد</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input value={newClient.name} onChange={e=>setNewClient({...newClient,name:e.target.value})} placeholder="اسم العميل *" className="px-4 py-2.5 border rounded-xl text-sm" />
                <input value={newClient.company} onChange={e=>setNewClient({...newClient,company:e.target.value})} placeholder="الشركة" className="px-4 py-2.5 border rounded-xl text-sm" />
                <input value={newClient.email} onChange={e=>setNewClient({...newClient,email:e.target.value})} placeholder="البريد" className="px-4 py-2.5 border rounded-xl text-sm" />
              </div>
              <div className="mt-4 flex gap-2">
                <button onClick={createClient} className="px-4 py-2 bg-violet-600 text-white rounded-xl text-sm">حفظ</button>
                <button onClick={()=>setShowCreateClient(false)} className="px-4 py-2 bg-zinc-100 rounded-xl text-sm">إلغاء</button>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {clients.map((c: any) => (
              <div key={c.id} className="bg-white rounded-2xl border p-5 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-white font-bold mb-3">{c.name.charAt(0)}</div>
                <div className="font-semibold">{c.name}</div>
                <div className="text-sm text-zinc-500">{c.company || '—'}</div>
                <div className="text-xs text-zinc-400 mt-1">{c.email || ''}</div>
                <div className="mt-3 flex items-center justify-between">
                  <span className={`text-xs px-2 py-1 rounded-full ${c.status==='active'?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{c.status}</span>
                  <span className="text-xs text-zinc-400">{new Date(c.created_at).toLocaleDateString('ar')}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Projects & Tasks tabs simplified
  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">{activeTab==='projects'?'المشاريع':'المهام'}</h1>
          <button onClick={() => setActiveTab('dashboard')} className="px-4 py-2 bg-white border rounded-xl text-sm">لوحة التحكم</button>
        </div>
        <div className="bg-white rounded-2xl border p-6">
          {activeTab==='projects' ? (
            <div className="space-y-3">
              {projects.map((p: any) => (
                <div key={p.id} className="p-4 border rounded-xl flex items-center justify-between">
                  <div>
                    <div className="font-medium">{p.name}</div>
                    <div className="text-xs text-zinc-500">{p.description?.slice(0,80) || 'لا يوجد وصف'}</div>
                  </div>
                  <span className="text-xs px-2 py-1 bg-violet-100 text-violet-700 rounded-full">{p.status}</span>
                </div>
              ))}
              {projects.length===0 && <div className="text-sm text-zinc-400">لا توجد مشاريع - أنشئ مشروعاً من API أو عبر الوكلاء</div>}
            </div>
          ) : (
            <div className="space-y-2">
              {tasks.map((t: any) => (
                <div key={t.id} className="p-3 border rounded-xl flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${t.status==='done'?'bg-green-500':t.status==='in_progress'?'bg-amber-500':'bg-zinc-300'}`} />
                  <div className="flex-1">
                    <div className="text-sm font-medium">{t.title}</div>
                    <div className="text-xs text-zinc-500">{t.priority} • {t.assigned_agent || 'غير مسند'}</div>
                  </div>
                  <span className="text-xs px-2 py-1 bg-zinc-100 rounded-full">{t.status}</span>
                </div>
              ))}
              {tasks.length===0 && <div className="text-sm text-zinc-400">لا توجد مهام</div>}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
