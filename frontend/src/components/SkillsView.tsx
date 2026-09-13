import { useEffect, useState } from 'react';
import { skillsApi } from '../lib/api';
import { Zap, Search, BookOpen } from 'lucide-react';

export default function SkillsView() {
  const [skills, setSkills] = useState<any[]>([]);
  const [categories, setCategories] = useState<any>({});
  const [selected, setSelected] = useState<any>(null);
  const [search, setSearch] = useState('');
  const [filterCat, setFilterCat] = useState('all');

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    try {
      const data = await skillsApi.list();
      setSkills(data.skills || []);
      setCategories(data.categories || {});
    } catch (e) { console.error(e); }
  };

  const handleSearch = async () => {
    if (!search.trim()) { load(); return; }
    try {
      const data = await skillsApi.search(search);
      setSkills(data.results || []);
    } catch (e) { console.error(e); }
  };

  const filtered = filterCat === 'all' ? skills : skills.filter(s => s.category === filterCat);

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      <div className="w-96 bg-white border-r flex flex-col">
        <div className="p-4 border-b">
          <h2 className="font-bold text-lg flex items-center gap-2">
            <Zap className="text-amber-500" />
            مكتبة المهارات
            <span className="ml-auto text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full">{skills.length}</span>
          </h2>
          <p className="text-xs text-zinc-500 mt-1">292 مهارة قابلة لإعادة الاستخدام - تحمل عند الحاجة</p>
          
          <div className="mt-4 flex gap-2">
            <div className="flex-1 relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSearch()}
                placeholder="ابحث في المهارات..."
                className="w-full pl-9 pr-3 py-2 border rounded-xl text-sm focus:ring-2 focus:ring-violet-200 outline-none"
              />
            </div>
            <button onClick={handleSearch} className="px-3 py-2 bg-violet-600 text-white rounded-xl text-sm">بحث</button>
          </div>

          <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
            <button onClick={() => setFilterCat('all')} className={`px-3 py-1 rounded-full text-xs whitespace-nowrap ${filterCat==='all'?'bg-violet-600 text-white':'bg-zinc-100'}`}>الكل</button>
            {Object.keys(categories).map(cat => (
              <button key={cat} onClick={() => setFilterCat(cat)} className={`px-3 py-1 rounded-full text-xs whitespace-nowrap ${filterCat===cat?'bg-violet-600 text-white':'bg-zinc-100'}`}>
                {cat} ({categories[cat]})
              </button>
            ))}
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {filtered.map(skill => (
            <button key={skill.id} onClick={() => setSelected(skill)} className={`w-full text-left p-3 rounded-xl border text-sm transition-all ${selected?.id===skill.id?'bg-violet-50 border-violet-200':'bg-white hover:shadow-sm'}`}>
              <div className="font-medium">{skill.name}</div>
              <div className="text-xs text-zinc-500 mt-1 line-clamp-2">{skill.description}</div>
              <div className="flex gap-2 mt-2">
                <span className="text-[10px] px-2 py-0.5 bg-zinc-100 rounded-full">{skill.category}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        {selected ? (
          <div className="max-w-4xl">
            <div className="bg-white rounded-2xl border p-6 mb-6">
              <div className="flex items-start justify-between">
                <div>
                  <h1 className="text-2xl font-bold flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center"><Zap size={20} className="text-amber-600" /></div>
                    {selected.name}
                  </h1>
                  <p className="text-zinc-600 mt-2">{selected.description}</p>
                  <div className="flex gap-2 mt-3">
                    <span className="px-3 py-1 bg-violet-100 text-violet-700 rounded-full text-xs">{selected.category}</span>
                    <span className="px-3 py-1 bg-zinc-100 rounded-full text-xs">ID: {selected.id}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2"><BookOpen size={16} />محتوى المهارة</h3>
              <div className="prose prose-sm max-w-none">
                <pre className="bg-zinc-900 text-zinc-100 p-6 rounded-xl overflow-x-auto whitespace-pre-wrap text-sm leading-relaxed">
                  {selected.content}
                </pre>
              </div>
            </div>

            <div className="mt-6 bg-gradient-to-br from-violet-50 to-indigo-50 border border-violet-200 rounded-2xl p-5">
              <h4 className="font-semibold text-violet-900 mb-2">💡 كيف تعمل المهارات (ECC)</h4>
              <p className="text-sm text-violet-800 leading-relaxed">
                المهارات تحافظ على تركيز السياق - تحمل فقط عند الحاجة، وليس دائماً.
                هذا يختلف عن القواعد (Rules) التي تحمل دائماً. عندما يحتاج الوكيل لمهارة، يتم حقنها في system prompt.
                <br/><br/>
                <strong>مثال:</strong> عند طلب "اكتب كود بـ TDD"، يتم تحميل مهارة tdd-workflow تلقائياً.
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <Zap size={48} className="mx-auto text-zinc-300 mb-4" />
              <h3 className="font-semibold">اختر مهارة لعرض تفاصيلها</h3>
              <p className="text-sm text-zinc-500 mt-2 max-w-md">المهارات هي workflows قابلة لإعادة الاستخدام مثل TDD، المراجعة الأمنية، البحث العميق، وغيرها</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
