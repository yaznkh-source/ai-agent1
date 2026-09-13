import { useState, useEffect } from 'react';

export default function FreeDomainView() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/domain/free/')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading free domain guide...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">🌍 Free Domain — $0 — DigitalPlat FreeDomain 199k Stars</h1>
      <p className="text-zinc-600 mb-6">Free domain .US.KG .DPDNS.ORG .QZZ.IO .XX.KG .QD.JE — 500k+ domains — PSL Cloudflare accepted — $0 vs $12/year</p>

      {data && (
        <>
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="border rounded p-4">
              <h3 className="font-bold mb-2">Available Extensions — Free $0</h3>
              <ul className="list-disc pl-5 text-sm">
                {Object.entries(data.extensions || {}).map(([ext, desc]: any) => (
                  <li key={ext}><b>{ext}</b>: {desc}</li>
                ))}
              </ul>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold mb-2">Cost Comparison</h3>
              <ul className="list-disc pl-5 text-sm">
                {Object.entries(data.cost_comparison || {}).map(([k, v]: any) => (
                  <li key={k}><b>{k}</b>: {v}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="border rounded p-4 mb-6">
            <h3 className="font-bold mb-2">Quick Start — 5 Minutes — $0</h3>
            <ol className="list-decimal pl-5 text-sm space-y-2">
              {Object.entries(data.quick_start || {}).map(([step, desc]: any) => (
                <li key={step}><b>{step}</b>: {desc}</li>
              ))}
            </ol>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="border rounded p-4">
              <h3 className="font-bold mb-2">Examples</h3>
              <pre className="text-xs bg-zinc-100 p-2 rounded">{JSON.stringify(data.examples, null, 2)}</pre>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold mb-2">Recommendation</h3>
              <pre className="text-xs bg-zinc-100 p-2 rounded">{JSON.stringify(data.recommendation, null, 2)}</pre>
            </div>
          </div>

          <div className="mt-6 border rounded p-4 bg-green-50">
            <h3 className="font-bold">Script — $0</h3>
            <code className="text-sm">{data.script}</code> — automates guide<br/>
            <code className="text-sm">./scripts/setup-free-domain.sh ai-agency-os us.kg</code>
            <div className="mt-2 text-sm">
              <a href={data.dashboard} target="_blank" className="text-blue-600 underline">Dashboard: {data.dashboard}</a><br/>
              <a href={data.tutorial} target="_blank" className="text-blue-600 underline">Tutorial</a> | <a href={data.learn} target="_blank" className="text-blue-600 underline">LEARN.md</a>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
