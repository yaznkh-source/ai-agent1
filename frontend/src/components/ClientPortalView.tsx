import { useEffect, useState } from 'react';
import api from '../lib/api';
import { FolderKanban, CheckSquare, MessageSquare, FileText, Clock } from 'lucide-react';

export default function ClientPortalView() {
  const [clients, setClients] = useState<any[]>([]);
  const [selectedClient, setSelectedClient] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  const [selectedProject, setSelectedProject] = useState<any>(null);

  useEffect(() => { loadClients(); }, []);

  const loadClients = async () => {
    try {
      const res = await api.get('/agency/clients');
      setClients(res.data || []);
    } catch {}
  };

  const selectClient = async (client: any) => {
    setSelectedClient(client);
    try {
      const [projRes, clientRes] = await Promise.all([
        api.get('/agency/projects', { params: { client_id: client.id } }),
        api.get(`/agency/clients/${client.id}`)
      ]);
      setProjects(projRes.data || []);
      setSelectedProject(null);
      setTasks([]);
    } catch {}
  };

  const selectProject = async (project: any) => {
    setSelectedProject(project);
    try {
      const res = await api.get('/agency/tasks', { params: { project_id: project.id } });
      setTasks(res.data || []);
    } catch {}
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      {/* Clients */}
      <div className="w-80 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h2 className="font-bold flex items-center gap-2"><FileText size={18} className="text-blue-600"/>بوابة العملاء</h2>
          <p className="text-xs text-zinc-500 mt-1">عرض مبسط للعميل - بدون وكلاء داخليين</p>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {clients.map((c:any) => (
            <button key={c.id} onClick={()=>selectClient(c)} className={`w-full text-left p-4 rounded-xl border transition-all ${selectedClient?.id===c.id?'bg-blue-50 border-blue-200':'bg-white hover:shadow-sm'}`}>
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center text-white font-bold mb-2">{c.name.charAt(0)}</div>
              <div className="font-medium text-sm">{c.name}</div>
              <div className="text-xs text-zinc-500">{c.company || '—'}</div>
              <div className="text-xs text-zinc-400 mt-1">{c.email}</div>
            </button>
          ))}
          {clients.length===0 && <div className="text-sm text-zinc-400 text-center py-8">لا عملاء - أنشئ من تبويب الوكالة</div>}
        </div>
      </div>

      {/* Projects */}
      <div className="w-80 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h3 className="font-semibold flex items-center gap-2"><FolderKanban size={16}/>مشاريع {selectedClient?.name || ''}</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {projects.map((p:any) => (
            <button key={p.id} onClick={()=>selectProject(p)} className={`w-full text-left p-3 rounded-xl border ${selectedProject?.id===p.id?'bg-violet-50 border-violet-200':'bg-white hover:bg-zinc-50'}`}>
              <div className="font-medium text-sm">{p.name}</div>
              <div className="text-xs text-zinc-500 mt-1 line-clamp-2">{p.description || 'لا وصف'}</div>
              <div className="flex items-center gap-2 mt-2">
                <span className={`text-xs px-2 py-0.5 rounded-full ${p.status==='active'?'bg-green-100 text-green-700':'bg-zinc-100'}`}>{p.status}</span>
                <span className="text-xs text-zinc-400 flex items-center gap-1"><Clock size={10}/>{new Date(p.updated_at).toLocaleDateString('ar')}</span>
              </div>
            </button>
          ))}
          {selectedClient && projects.length===0 && <div className="text-sm text-zinc-400 text-center py-8">لا مشاريع لهذا العميل</div>}
          {!selectedClient && <div className="text-sm text-zinc-400 text-center py-8">اختر عميلاً أولاً</div>}
        </div>
      </div>

      {/* Project Detail - Client View */}
      <div className="flex-1 overflow-y-auto p-6">
        {selectedProject ? (
          <div className="max-w-4xl">
            <div className="bg-white rounded-2xl border p-6 mb-6">
              <h1 className="text-2xl font-bold">{selectedProject.name}</h1>
              <p className="text-zinc-600 mt-2">{selectedProject.description}</p>
              <div className="flex gap-2 mt-4">
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs">{selectedProject.status}</span>
                <span className="px-3 py-1 bg-zinc-100 rounded-full text-xs">العميل: {selectedClient?.name}</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white rounded-2xl border p-5">
                <div className="text-2xl font-bold">{tasks.length}</div>
                <div className="text-sm text-zinc-500">إجمالي المهام</div>
              </div>
              <div className="bg-white rounded-2xl border p-5">
                <div className="text-2xl font-bold text-amber-600">{tasks.filter((t:any)=>t.status==='in_progress').length}</div>
                <div className="text-sm text-zinc-500">قيد التنفيذ</div>
              </div>
              <div className="bg-white rounded-2xl border p-5 bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
                <div className="text-2xl font-bold text-green-700">{tasks.filter((t:any)=>t.status==='done').length}</div>
                <div className="text-sm text-green-600">مكتملة</div>
              </div>
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2"><CheckSquare size={18}/>المهام - عرض العميل المبسط</h3>
              <p className="text-xs text-zinc-500 mb-4">العميل يرى التقدم بدون تفاصيل الوكلاء الداخليين - مثل Open WebUI workspace لكن للعملاء</p>
              
              <div className="space-y-3">
                {tasks.map((t:any) => (
                  <div key={t.id} className="p-4 border rounded-xl flex gap-4">
                    <div className={`w-2 h-10 rounded-full flex-shrink-0 ${t.status==='done'?'bg-green-500':t.status==='in_progress'?'bg-amber-500':t.status==='review'?'bg-blue-500':'bg-zinc-300'}`} />
                    <div className="flex-1">
                      <div className="font-medium text-sm">{t.title}</div>
                      <div className="text-xs text-zinc-500 mt-1">{t.description || 'لا وصف'}</div>
                      <div className="flex items-center gap-2 mt-2">
                        <span className={`text-xs px-2 py-1 rounded-full ${t.status==='done'?'bg-green-100 text-green-700':t.status==='in_progress'?'bg-amber-100 text-amber-700':'bg-zinc-100'}`}>{t.status}</span>
                        <span className="text-xs text-zinc-400">{t.priority} أولوية</span>
                      </div>
                    </div>
                    <div className="text-xs text-zinc-400">{new Date(t.updated_at).toLocaleDateString('ar')}</div>
                  </div>
                ))}
                {tasks.length===0 && <div className="text-sm text-zinc-400 text-center py-8">لا مهام في هذا المشروع</div>}
              </div>
            </div>

            <div className="mt-6 bg-gradient-to-br from-blue-50 to-violet-50 border border-blue-200 rounded-2xl p-5">
              <h4 className="font-semibold text-blue-900 mb-2">💡 فكرة بوابة العملاء</h4>
              <div className="text-sm text-blue-800 space-y-1">
                <div>• العميل يدخل بـ login خاص (role=client) - يشوف فقط مشاريعه</div>
                <div>• لا يرى الوكلاء الداخليين (backend-dev, reviewer...) - يرى فقط "التصميم قيد التنفيذ" أو "تم التسليم"</div>
                <div>• يستطيع رفع ملفات + تعليقات + الموافقة على التسليم</div>
                <div>• إشعارات: عند اكتمال مهمة → إيميل + Slack للعميل</div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <FolderKanban size={48} className="mx-auto text-zinc-300 mb-4" />
              <h3 className="font-semibold">اختر مشروعاً لعرض بوابة العميل</h3>
              <p className="text-sm text-zinc-500 mt-2 max-w-md">هذه هي الواجهة التي سيراها العميل - مبسطة، بدون تعقيد الوكلاء، تركز على التسليمات والتقدم</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
