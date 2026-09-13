import { useState, useEffect } from 'react';

export default function VoiceView() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/voice/')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8">Loading voice Whisper...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">🎤 Voice — Whisper Local Free — From free-claude-code 54.8k Stars — $0 — 100% Margin</h1>
      <p className="text-zinc-600 mb-6">Whisper local free speech-to-text $0 100% margin — faster-whisper 4x faster — tiny 39M base 74M small 244M medium 769M large 1550M — 99 languages auto-detect — voice notes for agents — Otter.ai $16/mo alternative $0</p>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-bold">Cost $0 vs Otter.ai $16/mo</h3>
          <p className="text-sm">Whisper local free $0 100% margin vs Otter.ai $16/mo — needs local CPU/GPU RAM 1GB-10GB — tiny 39M base 74M good balance — 50 clients × $16 = $800/mo saving $0 vs $800</p>
        </div>
        <div className="border rounded p-4 bg-blue-50">
          <h3 className="font-bold">Use Cases — $0</h3>
          <p className="text-sm">content-creator agent transcribe client voice briefs $0 — support-agent transcribe support calls $0 — researcher transcribe interviews $0 — agency client voice → text → tasks $0</p>
        </div>
        <div className="border rounded p-4 bg-purple-50">
          <h3 className="font-bold">Providers — $0</h3>
          <p className="text-sm">Whisper local openai-whisper + faster-whisper 4x faster CTranslate2 $0 — NVIDIA NIM Whisper 40 req/min free nvapi-... $0 — 99 languages auto-detect</p>
        </div>
      </div>

      {data && (
        <>
          <div className="grid grid-cols-2 gap-4 mb-6">
            {Object.entries(data.providers || {}).map(([key, prov]: any) => (
              <div key={key} className="border rounded p-4">
                <h3 className="font-bold">{prov.name} — {prov.cost} — {prov.margin || ''}</h3>
                <p className="text-xs">Models: {prov.models?.join(', ') || ''} — Languages: {prov.languages || ''}</p>
                <p className="text-xs mt-2 bg-zinc-100 p-1 rounded">Install: {prov.how_to_install}</p>
                {prov.api && <p className="text-xs mt-1">API: {prov.api}</p>}
                {prov.recommended && <p className="text-xs font-bold text-green-600">Recommended</p>}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="border rounded p-4">
              <h3 className="font-bold">Integration</h3>
              <pre className="text-xs bg-zinc-100 p-2 rounded">{JSON.stringify(data.integration, null, 2)}</pre>
            </div>
            <div className="border rounded p-4">
              <h3 className="font-bold">Cost Comparison</h3>
              <pre className="text-xs bg-zinc-100 p-2 rounded">{JSON.stringify(data.cost_comparison, null, 2)}</pre>
            </div>
          </div>

          <div className="mt-6 border rounded p-4 bg-yellow-50">
            <h3 className="font-bold">Test Transcription — $0 — Mock Always Works — Real When Whisper Installed</h3>
            <p className="text-sm">POST /api/voice/transcribe — upload audio mp3/wav/m4a/ogg — returns transcription — real Whisper when openai-whisper or faster-whisper installed mock when not — $0 local free 100% margin — from free-claude-code voice Whisper local/NVIDIA NIM</p>
            <p className="text-xs mt-2">Example: curl -X POST http://localhost:8000/api/voice/transcribe -F file=@audio.mp3 -F model=base -F language=auto | jq .transcription</p>
          </div>
        </>
      )}
    </div>
  );
}
