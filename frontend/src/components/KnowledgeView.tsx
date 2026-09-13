import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function KnowledgeView() {
  const [collections, setCollections] = useState<any>({});
  const [searchQ, setSearchQ] = useState('ما هو ECC؟');
  const [results, setResults] = useState<any[]>([]);
  const [addText, setAddText] = useState('');
  const [addCollection, setAddCollection] = useState('custom');

  useEffect(() => { loadCollections(); search(); }, []);

  const loadCollections = async () => {
    try {
      const res = await api.get('/knowledge/collections');
      setCollections(res.data.collections || {});
    } catch {}
  };

  const search = async () => {
    try {
      const res = await api.get('/knowledge/search', { params: { q: searchQ, top_k: 5 } });
      setResults(res.data.results || []);
    } catch {}
  };

  const addDoc = async () => {
    if (!addText.trim()) return;
    try {
      await api.post('/knowledge/add', { text: addText, collection: addCollection });
      setAddText('');
      loadCollections();
      search();
    } catch {}
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">🧠 نظام المعرفة RAG - ChromaDB + Embeddings</h1>
        <p className="text-sm text-zinc-600 mb-6">مستوحى من Open WebUI Knowledge Collections + ECC Memory - بحث دلالي حقيقي وليس keywords فقط</p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">المجموعات ({Object.keys(collections).length})</h3>
            <div className="space-y-2">
              {Object.entries(collections).map(([name, count]: any) => (
                <div key={name} className="flex items-center justify-between p-3 bg-zinc-50 rounded-xl">
                  <span className="text-sm font-medium">{name}</span>
                  <span className="text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded-full">{count} وثائق</span>
                </div>
              ))}
            </div>

            <div className="mt-6">
              <h4 className="font-medium text-sm mb-3">إضافة معرفة جديدة</h4>
              <input value={addCollection} onChange={e=>setAddCollection(e.target.value)} placeholder="اسم المجموعة" className="w-full px-3 py-2 border rounded-xl text-sm mb-2" />
              <textarea value={addText} onChange={e=>setAddText(e.target.value)} placeholder="نص المعرفة... مثال: شركتنا تقدم خدمات تطوير مواقع بـ React و Node.js" className="w-full h-24 p-3 border rounded-xl text-sm resize-none" />
              <button onClick={addDoc} className="mt-2 w-full py-2 bg-violet-600 text-white rounded-xl text-sm">إضافة + تضمين</button>
            </div>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4">بحث دلالي</h3>
              <div className="flex gap-2">
                <input value={searchQ} onChange={e=>setSearchQ(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder="ابحث... مثال: كيف يعمل TDD؟" className="flex-1 px-4 py-2.5 border rounded-xl" />
                <button onClick={search} className="px-6 py-2.5 bg-violet-600 text-white rounded-xl">بحث</button>
              </div>

              <div className="mt-6 space-y-3">
                {results.map((r:any, i:number) => (
                  <div key={i} className="p-4 bg-zinc-50 border rounded-xl">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">{r.metadata?.collection || 'unknown'}</span>
                      <span className="text-xs text-zinc-500">Score: {(r.score*100).toFixed(1)}%</span>
                    </div>
                    <div className="text-sm">{r.text}</div>
                    <div className="text-xs text-zinc-400 mt-2">{JSON.stringify(r.metadata)}</div>
                  </div>
                ))}
                {results.length===0 && <div className="text-sm text-zinc-400 text-center py-8">لا نتائج - جرب بحث آخر</div>}
              </div>
            </div>

            <div className="bg-gradient-to-br from-violet-50 to-indigo-50 border border-violet-200 rounded-2xl p-5">
              <h4 className="font-semibold text-violet-900 mb-2">💡 كيف يعمل RAG الحقيقي</h4>
              <div className="text-sm text-violet-800 space-y-2">
                <div>1. <strong>Chunking:</strong> تقسيم النصوص إلى 500 كلمة مع overlap</div>
                <div>2. <strong>Embedding:</strong> تحويل كل chunk إلى vector 384-dim (hash-based الآن، sentence-transformers في الإنتاج)</div>
                <div>3. <strong>Retrieval:</strong> عند السؤال، نحول السؤال لـ vector ونبحث عن أقرب vectors بـ cosine similarity</div>
                <div>4. <strong>Augmentation:</strong> نحقن النتائج في prompt الـ LLM مع citations</div>
                <div className="mt-3 p-3 bg-white/50 rounded-xl text-xs">الآن: in-memory + ChromaDB optional. في الإنتاج: استخدم all-MiniLM-L6-v2 + Chroma persistent</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
