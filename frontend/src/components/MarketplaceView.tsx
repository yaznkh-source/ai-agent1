import { useEffect, useState } from 'react';
import api from '../lib/api';
import { ShoppingBag, Star, Download, DollarSign, Search } from 'lucide-react';

export default function MarketplaceView() {
  const [data, setData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'skills'|'pipelines'|'agents'>('skills');
  const [searchQ, setSearchQ] = useState('');

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const res = await api.get('/marketplace/');
      setData(res.data);
    } catch {}
  };

  const search = async () => {
    if (!searchQ.trim()) { load(); return; }
    try {
      const res = await api.get('/marketplace/search', { params: { q: searchQ, type: activeTab } });
      setData({ ...data, searchResults: res.data.results });
    } catch {}
  };

  const install = async (id: string, type: string) => {
    try {
      const res = await api.post(`/marketplace/${type.slice(0,-1)}/${id}/install`, { user_id: 'default-user' });
      alert(res.data.message);
    } catch (e: any) { alert(e.message); }
  };

  const items = activeTab === 'skills' ? data?.featured?.skills || [] : activeTab === 'pipelines' ? data?.featured?.pipelines || [] : data?.featured?.agents || [];
  const displayItems = data?.searchResults || items;

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><ShoppingBag className="text-violet-600"/>Marketplace - متجر المهارات والوكلاء</h1>
        <p className="text-sm text-zinc-600 mb-6">مستوحى من Open WebUI community + ECC marketplace - بيع وشراء skills, pipelines, agents مع عمولة 30%</p>

        {data?.stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.total_skills}</div><div className="text-xs text-zinc-500">إجمالي مهارات</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.total_pipelines}</div><div className="text-xs text-zinc-500">Pipelines</div></div>
            <div className="bg-white rounded-2xl border p-5"><div className="text-2xl font-bold">{data.stats.total_agents}</div><div className="text-xs text-zinc-500">وكلاء</div></div>
            <div className="bg-white rounded-2xl border p-5 bg-gradient-to-br from-violet-600 to-indigo-600 text-white"><div className="text-2xl font-bold">{data.stats.total_downloads}</div><div className="text-xs text-violet-100">تحميلات</div></div>
          </div>
        )}

        <div className="flex gap-2 mb-6">
          <div className="flex bg-white border rounded-xl p-1">
            {(['skills','pipelines','agents'] as const).map(tab => (
              <button key={tab} onClick={()=>setActiveTab(tab)} className={`px-4 py-2 rounded-lg text-sm font-medium capitalize ${activeTab===tab?'bg-violet-600 text-white':'text-zinc-600'}`}>{tab}</button>
            ))}
          </div>
          <div className="flex-1 flex gap-2">
            <div className="flex-1 relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"/>
              <input value={searchQ} onChange={e=>setSearchQ(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder={`ابحث في ${activeTab}...`} className="w-full pl-9 pr-3 py-2.5 border rounded-xl text-sm bg-white" />
            </div>
            <button onClick={search} className="px-4 py-2.5 bg-violet-600 text-white rounded-xl text-sm">بحث</button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayItems.map((item:any) => (
            <div key={item.id} className="bg-white rounded-2xl border p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-indigo-500 flex items-center justify-center text-white font-bold text-sm">{item.name.charAt(0)}</div>
                <span className={`text-xs px-2 py-1 rounded-full ${item.price===0?'bg-green-100 text-green-700':'bg-amber-100 text-amber-700'}`}>{item.price===0?'مجاني':`$${item.price}`}</span>
              </div>
              <div className="font-semibold mt-3 text-sm">{item.name}</div>
              <div className="text-xs text-zinc-500 mt-1 line-clamp-2">{item.description}</div>
              
              <div className="flex items-center gap-3 mt-3 text-xs text-zinc-400">
                <span className="flex items-center gap-1"><Star size={12} className="fill-amber-400 text-amber-400"/>{item.rating}</span>
                <span className="flex items-center gap-1"><Download size={12}/>{item.downloads}</span>
                <span>{item.author}</span>
              </div>

              <div className="flex gap-2 mt-4">
                <button onClick={()=>install(item.id, activeTab)} className="flex-1 py-2 bg-violet-600 text-white rounded-xl text-xs font-medium">تثبيت</button>
                <button className="px-3 py-2 bg-zinc-100 rounded-xl text-xs">تفاصيل</button>
              </div>

              {activeTab==='pipelines' && <div className="mt-2 text-xs text-zinc-400">{item.steps} خطوات</div>}
            </div>
          ))}
        </div>

        <div className="mt-8 bg-white rounded-2xl border p-6">
          <h3 className="font-semibold mb-3">💼 كيف تربح من Marketplace</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="p-4 bg-violet-50 border border-violet-200 rounded-xl">
              <div className="font-semibold">1. أنشئ مهارة مميزة</div>
              <div className="text-xs text-zinc-600 mt-2">مثلاً: مهارة SEO متقدمة توفر 10 ساعات عمل</div>
            </div>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl">
              <div className="font-semibold">2. انشر بسعر $29</div>
              <div className="text-xs text-zinc-600 mt-2">100 تحميل × $29 = $2900 - عمولة 30% = $2030 لك</div>
            </div>
            <div className="p-4 bg-green-50 border border-green-200 rounded-xl">
              <div className="font-semibold">3. تزيد شهرتك + عملاء</div>
              <div className="text-xs text-zinc-600 mt-2">المهارات المشهورة تجلب عملاء للوكالة - تسويق مجاني</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
