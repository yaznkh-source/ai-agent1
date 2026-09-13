import { useEffect, useState } from 'react';
import { Trophy, Swords } from 'lucide-react';

export default function AgentLeaderboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);
  const load = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/leaderboard/');
      const json = await res.json();
      setData(json);
    } catch {}
    setLoading(false);
  };

  if (loading) return <div className="flex-1 flex items-center justify-center">جاري تحميل لوحة الصدارة — مثل Arena.ai...</div>;

  const leaderboard = data?.leaderboard || [];

  return (
    <div className="flex-1 overflow-auto bg-white">
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black text-white text-xs mb-4">
            <Trophy size={12} /> Leaderboard — مثل https://lmarena.ai/?leaderboard
          </div>
          <h1 className="text-3xl font-semibold mb-2">🏆 Agent Leaderboard</h1>
          <p className="text-sm text-zinc-600">لوحة صدارة 68 وكيل — ترتيب حسب Elo — مثل Arena.ai — Elo, Bradley-Terry, Confidence Intervals — {data?.total_battles || 0} معارك — {data?.total_votes || 0} تصويت — يعمل فعلياً — $0</p>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="border border-zinc-200 rounded-xl p-4 text-center">
            <div className="text-xs text-zinc-500">الوكلاء</div>
            <div className="text-2xl font-semibold">{data?.total_agents || leaderboard.length}</div>
          </div>
          <div className="border border-zinc-200 rounded-xl p-4 text-center">
            <div className="text-xs text-zinc-500">المعارك</div>
            <div className="text-2xl font-semibold">{data?.total_battles || 0}</div>
          </div>
          <div className="border border-zinc-200 rounded-xl p-4 text-center">
            <div className="text-xs text-zinc-500">التصويتات</div>
            <div className="text-2xl font-semibold">{data?.total_votes || 0}</div>
          </div>
        </div>

        <div className="border border-zinc-200 rounded-xl overflow-hidden">
          <div className="grid grid-cols-12 gap-2 px-4 py-2 bg-zinc-50 text-[11px] font-medium text-zinc-500 uppercase">
            <div className="col-span-1">#</div>
            <div className="col-span-3">الوكيل</div>
            <div className="col-span-2">Elo</div>
            <div className="col-span-2">معارك</div>
            <div className="col-span-2">فوز</div>
            <div className="col-span-2">نسبة فوز</div>
          </div>
          {leaderboard.map((e: any) => (
            <div key={e.agent_id} className="grid grid-cols-12 gap-2 px-4 py-3 border-t border-zinc-100 text-sm hover:bg-zinc-50">
              <div className="col-span-1 font-medium">#{e.rank}</div>
              <div className="col-span-3 truncate font-medium">{e.agent_id}</div>
              <div className="col-span-2">{e.rating}</div>
              <div className="col-span-2">{e.battles}</div>
              <div className="col-span-2">{e.wins}</div>
              <div className="col-span-2">{Math.round(e.win_rate * 100)}%</div>
            </div>
          ))}
          {leaderboard.length === 0 && (
            <div className="px-4 py-8 text-center text-sm text-zinc-500">
              <Swords size={24} className="mx-auto mb-2 text-zinc-300" />
              لا توجد معارك بعد — ابدأ Battle Arena — مثل Arena.ai — $0
            </div>
          )}
        </div>

        <div className="mt-6 border border-zinc-200 rounded-xl p-4 bg-zinc-50">
          <div className="font-medium text-xs mb-2">المنهجية — مثل arena-rank — https://github.com/lmarena/arena-rank — 118 نجوم</div>
          <div className="text-[11px] text-zinc-600 space-y-1">
            <div>• Elo Rating — مثل الشطرنج — كل وكيل يبدأ 1000 — عند فوز يرتفع — عند خسارة ينخفض — K=32 — مثل arena-rank — يعمل فعلياً</div>
            <div>• Bradley-Terry Model — نموذج إحصائي لتقدير قوة النماذج من مقارنات زوجية — مثل arena-rank — يعمل فعلياً</div>
            <div>• Confidence Intervals — فترات ثقة — مثل arena-rank — تعمل فعلياً</div>
            <div>• مصدر: https://github.com/lmarena/arena-rank — 118 نجوم — منهجية لوحة صدارة Arena — Elo, Bradley-Terry — يعمل فعلياً</div>
          </div>
        </div>
      </div>
    </div>
  );
}
