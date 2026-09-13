import { useState, useEffect } from 'react';

export default function CuratedToolsView() {
  const [tools, setTools] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/tools/curated/list')
      .then(r => r.json())
      .then(d => { setTools(d.tools || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading curated AI tools...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">🛠️ Curated AI Tools — From ai-agent-tools 477 Stars — Marketplace Expansion</h1>
      <p className="text-zinc-600 mb-6">10+ tools — ViralWave Studio Sora 2 video $0.34/10s, Postiz 20+ platforms, DALL-E 2, ElevenLabs, Whisper local $0, Copy.ai, Otter.ai, Perplexity, Copilot — marketplace expansion + monetization Authflow pattern 30% fee</p>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-bold">Marketplace 30% Fee — Like Apple App Store</h3>
          <p className="text-sm">Tool $49/mo → charge client $49/mo → keep $14.7 30% — 10 clients × $14.7 = $147/mo extra</p>
        </div>
        <div className="border rounded p-4 bg-blue-50">
          <h3 className="font-bold">White-Label Pro $199/mo — 81% Margin</h3>
          <p className="text-sm">Cost $29 Postiz + $3.4 videos + $5 ElevenLabs = $37.4, revenue $199, profit $161.6 81% margin</p>
        </div>
        <div className="border rounded p-4 bg-purple-50">
          <h3 className="font-bold">Bulk Content $299/mo — 84% Margin</h3>
          <p className="text-sm">Generate weeks/months content from single topic — cost $37.4 tools + $10 LLM = $47.4, profit $251.6 84% margin</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {tools.map((tool: any) => (
          <div key={tool.id} className={`border rounded p-4 ${tool.featured ? 'bg-yellow-50 border-yellow-300' : ''}`}>
            <h3 className="font-bold">{tool.name} {tool.featured ? '⭐ Featured' : ''} — {tool.category} — {tool.pricing}</h3>
            <p className="text-sm text-zinc-600 mb-2">{tool.description}</p>
            <p className="text-xs">Website: <a href={tool.website} target="_blank" className="text-blue-600 underline">{tool.website}</a></p>
            <p className="text-xs">Integration: {tool.integration}</p>
            {tool.profit_30pct && <p className="text-xs font-bold text-green-600">Profit 30%: {tool.profit_30pct}</p>}
            {tool.features && <ul className="list-disc pl-5 text-xs mt-2">{tool.features.slice(0,3).map((f: string, i: number) => <li key={i}>{f.slice(0,100)}</li>)}</ul>}
          </div>
        ))}
      </div>
    </div>
  );
}
