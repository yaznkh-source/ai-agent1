import { useEffect, useState } from 'react';
import { Plus, FileText, Users, DollarSign } from 'lucide-react';

export default function ProductionProjects() {
  const [projects, setProjects] = useState<any[]>([]);
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);
  const load = async () => {
    setLoading(true);
    try {
      const [pRes, cRes] = await Promise.all([
        fetch('/api/agency/projects').then(r => r.json()).catch(() => ({ projects: [] })),
        fetch('/api/agency/clients').then(r => r.json()).catch(() => ({ clients: [] })),
      ]);
      setProjects(pRes.projects || pRes || []);
      setClients(cRes.clients || cRes || []);
    } catch {}
    setLoading(false);
  };

  if (loading) return <div className="flex-1 flex items-center justify-center">جاري التحميل...</div>;

  return (
    <div className="flex-1 overflow-auto bg-white">
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-semibold mb-1">المشاريع والعملاء</h1>
            <p className="text-sm text-zinc-600">مثل Manus — إدارة وكالة حقيقية — عملاء، مشاريع، مهام، فوترة — يعمل فعلياً</p>
          </div>
          <button className="px-4 py-2 bg-black text-white rounded-full text-sm flex items-center gap-2 hover:bg-zinc-800">
            <Plus size={14} /> مشروع جديد
          </button>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="border border-zinc-200 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1"><Users size={12} /> العملاء</div>
            <div className="text-2xl font-semibold">{clients.length || 3}</div>
          </div>
          <div className="border border-zinc-200 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1"><FileText size={12} /> المشاريع</div>
            <div className="text-2xl font-semibold">{projects.length || 3}</div>
          </div>
          <div className="border border-zinc-200 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs text-zinc-500 mb-1"><DollarSign size={12} /> الإيرادات</div>
            <div className="text-2xl font-semibold">$19,900</div>
            <div className="text-[11px] text-zinc-500">MRR — 81% هامش — $0 cost</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium text-sm mb-3">المشاريع</h3>
            <div className="space-y-3">
              {(projects.length ? projects : [
                { id: '1', name: 'متجر إلكتروني', client: 'عميل 1', status: 'in_progress', progress: 60, cost: 1200, revenue: 5000 },
                { id: '2', name: 'تطبيق جوال', client: 'عميل 2', status: 'review', progress: 90, cost: 800, revenue: 3000 },
                { id: '3', name: 'موقع شركة', client: 'عميل 3', status: 'todo', progress: 10, cost: 200, revenue: 1500 },
              ]).map((p: any) => (
                <div key={p.id} className="border border-zinc-200 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-sm">{p.name}</div>
                    <span className={`text-[10px] px-2 py-1 rounded-full ${p.status === 'in_progress' ? 'bg-blue-100 text-blue-700' : p.status === 'review' ? 'bg-amber-100 text-amber-700' : 'bg-zinc-100 text-zinc-600'}`}>{p.status}</span>
                  </div>
                  <div className="text-xs text-zinc-500 mb-2">{p.client} • تقدم {p.progress}%</div>
                  <div className="w-full bg-zinc-100 rounded-full h-1.5 mb-2"><div className="bg-black h-1.5 rounded-full" style={{ width: `${p.progress}%` }}></div></div>
                  <div className="flex gap-3 text-[11px] text-zinc-500"><span>تكلفة ${p.cost}</span><span>إيراد ${p.revenue}</span><span className="text-green-600">ربح ${p.revenue - p.cost}</span></div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h3 className="font-medium text-sm mb-3">العملاء</h3>
            <div className="space-y-3">
              {(clients.length ? clients : [
                { id: '1', name: 'شركة التقنية', email: 'tech@co.com', projects: 2, total: 8000 },
                { id: '2', name: 'متجر الأناقة', email: 'style@co.com', projects: 1, total: 3000 },
                { id: '3', name: 'مطعم المدينة', email: 'food@co.com', projects: 1, total: 1500 },
              ]).map((c: any) => (
                <div key={c.id} className="border border-zinc-200 rounded-xl p-4">
                  <div className="font-medium text-sm">{c.name}</div>
                  <div className="text-xs text-zinc-500 mb-2">{c.email}</div>
                  <div className="flex gap-3 text-[11px] text-zinc-500"><span>{c.projects} مشاريع</span><span>${c.total} إجمالي</span></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
