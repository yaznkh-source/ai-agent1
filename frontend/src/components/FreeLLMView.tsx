import { useState, useEffect } from 'react';

export default function FreeLLMView() {
  const [data, setData] = useState<any>(null);
  const [providers, setProviders] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/api/llm/').then(r => r.json()),
      fetch('/api/llm/providers').then(r => r.json())
    ]).then(([info, prov]) => {
      setData(info);
      setProviders(prov);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading free LLM providers...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">🤖 Free LLM Providers — $0 — From free-claude-code 54.8k Stars</h1>
      <p className="text-zinc-600 mb-6">NVIDIA NIM 40 req/min free + OpenRouter free + Ollama local free + LM Studio + DeepSeek cheap — margin 88%→100% — BaseProvider ABC + per-model mapping + optimization + rate limiting + thinking tokens</p>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-bold">Cost $0 → Margin 100%</h3>
          <p className="text-sm">OpenAI GPT-4o $5/1M input $15/1M output → margin 88% $175 profit on $199 Pro<br/>NVIDIA NIM free 40 req/min $0 → margin 100% $199 profit → $24 extra per user/mo<br/>50 users × $24 = $1200 extra profit/mo</p>
        </div>
        <div className="border rounded p-4 bg-blue-50">
          <h3 className="font-bold">Available Providers</h3>
          <p className="text-sm">{providers?.available?.join(', ') || 'None — set API keys for real'}<br/>Count: {providers?.available_count || 0}/{providers?.count || 0}</p>
        </div>
        <div className="border rounded p-4 bg-purple-50">
          <h3 className="font-bold">Per-Model Mapping</h3>
          <p className="text-sm">Route cheap tasks to free, complex to paid — mix freely<br/>planner → NIM 70B free, qa → Ollama free, architect → GPT-4o paid<br/>Avg cost per project $0.10 vs $10 — 100x cheaper</p>
        </div>
      </div>

      {data && (
        <>
          <div className="grid grid-cols-2 gap-4 mb-6">
            {Object.entries(data.providers || {}).map(([key, prov]: any) => (
              <div key={key} className="border rounded p-4">
                <h3 className="font-bold">{prov.name} — {prov.free} — {prov.cost} — {prov.margin}</h3>
                <p className="text-xs text-zinc-600 mb-2">Models: {prov.models?.join(', ')}</p>
                <p className="text-xs">Recommended for: {prov.recommended_for?.join(', ')}</p>
                <p className="text-xs mt-2 bg-zinc-100 p-1 rounded">How to get: {prov.how_to_get}</p>
                <p className="text-xs mt-1">Available: {prov.available ? '✅ Yes' : '❌ No — set API key'} — {prov.api_key || prov.base_url}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="border rounded p-4">
              <h3 className="font-bold">Request Optimization — 5 Categories — Save Quota</h3>
              <p className="text-sm">{data.request_optimization?.description}</p>
              <p className="text-xs mt-2">Categories: {data.request_optimization?.categories?.join(', ')}</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold">Smart Rate Limiting — Better than 100/min</h3>
              <p className="text-sm">{data.smart_rate_limiting?.description}</p>
              <pre className="text-xs bg-zinc-100 p-2 rounded mt-2">{JSON.stringify(data.smart_rate_limiting, null, 2)}</pre>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold">Thinking Tokens + Tool Parser</h3>
              <p className="text-xs">Thinking: {data.thinking_tokens?.description}</p>
              <p className="text-xs mt-2">Tool Parser: {data.tool_parser?.description}</p>
              <p className="text-xs">Patterns: {data.tool_parser?.patterns?.join(', ')}</p>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold">Cost Comparison</h3>
              <pre className="text-xs bg-zinc-100 p-2 rounded">{JSON.stringify(data.cost_comparison, null, 2)}</pre>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
