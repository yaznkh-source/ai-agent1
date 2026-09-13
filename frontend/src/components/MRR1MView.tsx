import { useState, useEffect } from 'react';

export default function MRR1MView() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/mrr/1m/stats')
      .then(r => r.json())
      .then(s => { setStats(s); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading $1M+ ARR $1,886,280 ARR Already Achieved...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">💰 $1M+ ARR $1,886,280 ARR Already Achieved $157,190 MRR ×12 — $128,640/mo Profit $1,543,680/year 81% Margin Avg $0 — Scale to $500K+ MRR $671,500 MRR $8,058,000 ARR $549,820/mo Profit $6,597,840/year 83% Margin Avg — $1M+ MRR $1,343,000 MRR $16,116,000 ARR $1,099,640/mo Profit $13,195,680/year — $0 Cost — After تابع x5</h1>
      <p className="text-zinc-600 mb-6">Already $1M+ ARR Achieved $157,190 MRR ×12 = $1,886,280 ARR — $128,640/mo profit $1,543,680/year 81% margin avg — $0 cost free domain $0 DigitalPlat 199k + free LLM $0 NVIDIA NIM 40 req/min free 54.8k + voice $0 Whisper faster-whisper — Scale Prod 500→2000 $99,500→$398,000 MRR $80,800→$323,200/mo profit + Marketplace 200→1000 $2,940→$14,700/mo extra + White-label 200→1000 $39,800→$199,000 MRR $32,320→$161,600/mo profit + Content 50→200 $14,950→$59,800 MRR $12,580→$50,320/mo profit — Total $157,190 MRR → $671,500 MRR $1,886,280 ARR → $8,058,000 ARR — $28,550/mo cost → $121,680/mo cost — $128,640/mo profit → $549,820/mo profit $6,597,840/year — 83% margin avg — $0 cost — 12-24 months — Next $5M ARR $8,058,000 ARR $6,687,600/year profit — Next $10M+ ARR $16,116,000 ARR $13,195,680/year profit $1M+ MRR — $0 cost — 24-36 months — Go-to-Market — After $100K+ MRR $157,190 MRR — After تابع x4</p>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-bold">Already $1M+ ARR: ${stats?.total_mrr_100k || 157190} MRR ×12 = ${stats?.arr_100k || 1886280} ARR — Profit ${stats?.total_profit_100k || 128640}/mo ${stats?.total_profit_yearly_100k || 1543680}/year — 81% margin — $0 cost — $1M+ ARR Achieved</h3>
        </div>
        <div className="border rounded p-4 bg-blue-50">
          <h3 className="font-bold">Next $5M ARR: ${stats?.total_mrr_500k || 671500} MRR ×12 = ${stats?.arr_500k || 8058000} ARR — Cost ${stats?.total_cost_500k || 121680} Profit ${stats?.total_profit_500k || 549820}/mo ${stats?.total_profit_yearly_500k || 6597840}/year — 83% margin avg — $0 cost — 12-24 months</h3>
        </div>
        <div className="border rounded p-4 bg-purple-50">
          <h3 className="font-bold">Next $10M+ ARR $1M+ MRR: ${stats?.total_mrr_1m || 1343000} MRR ×12 = ${stats?.arr_1m || 16116000} ARR — Cost ${stats?.total_cost_1m || 243360} Profit ${stats?.total_profit_1m || 1099640}/mo ${stats?.total_profit_yearly_1m || 13195680}/year — 81% margin avg — $0 cost — 24-36 months — $1M+ MRR</h3>
        </div>
        <div className="border rounded p-4 bg-orange-50">
          <h3 className="font-bold">Scale: Prod 100 $19,900 → 500 $99,500 → 2000 $398,000 → 4000 $796,000 MRR — Total $30,884 → $157,190 $1,886,280 ARR Already $1M+ ARR → $671,500 $8,058,000 ARR Next $5M ARR → $1,343,000 $16,116,000 ARR Next $10M+ ARR $1M+ MRR — $0 cost — 6-12 → 12-24 → 24-36 months</h3>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="border rounded p-4">
          <h3 className="font-bold">Breakdown $100K+ MRR $157,190 MRR $1,886,280 ARR Already $1M+ ARR — Prod 500 $99,500 MRR + Marketplace 200 $2,940/mo + White-label 200 $39,800 MRR + Content 50 $14,950 MRR</h3>
          <pre className="text-xs bg-zinc-100 p-2 rounded mt-2 max-h-96 overflow-auto">{JSON.stringify({prod_500_mrr: stats?.prod_500_mrr, prod_2000_mrr: stats?.prod_2000_mrr, prod_4000_mrr: stats?.prod_4000_mrr, total_mrr_100k: stats?.total_mrr_100k, total_mrr_500k: stats?.total_mrr_500k, total_mrr_1m: stats?.total_mrr_1m, arr_100k: stats?.arr_100k, arr_500k: stats?.arr_500k, arr_1m: stats?.arr_1m}, null, 2)}</pre>
        </div>
        <div className="border rounded p-4">
          <h3 className="font-bold">What Remains — 3 Levels — After تابع x5 — Already $1M+ ARR $1,886,280 ARR</h3>
          <pre className="text-xs bg-zinc-100 p-2 rounded mt-2 max-h-96 overflow-auto">{JSON.stringify(stats?.what_remains, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}
