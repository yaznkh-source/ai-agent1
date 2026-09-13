import { useState } from 'react';
import { Swords, Trophy, Vote } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function AgentBattleArena() {
  const [question, setQuestion] = useState('');
  const [battle, setBattle] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [voted, setVoted] = useState(false);

  const createBattle = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setVoted(false);
    try {
      const res = await fetch('/api/arena/battle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setBattle(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const vote = async (choice: string) => {
    if (!battle || voted) return;
    try {
      const res = await fetch(`/api/arena/battle/${battle.battle_id}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vote: choice }),
      });
      const data = await res.json();
      setBattle({ ...battle, ...data, voted: true });
      setVoted(true);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex-1 overflow-auto bg-white">
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-900 text-white text-xs mb-4">
            <Swords size={12} /> Battle Arena — مثل Arena.ai — معارك مجهولة وعشوائية
          </div>
          <h1 className="text-3xl font-semibold mb-2">⚔️ Agent Battle Arena</h1>
          <p className="text-sm text-zinc-600">سؤال واحد → وكيلان (من 68) يجيبان مجهول جنباً إلى جنب → صوت للأفضل → تحديث Elo — مثل https://lmarena.ai — يعمل فعلياً — $0</p>
        </div>

        <div className="max-w-3xl mx-auto mb-8">
          <div className="flex gap-2">
            <input
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && createBattle()}
              placeholder="اكتب سؤال — مثلاً: أنشئ خطة لمشروع متجر إلكتروني"
              className="flex-1 border border-zinc-300 rounded-xl px-4 py-3 text-sm focus:border-black focus:outline-none"
            />
            <button onClick={createBattle} disabled={loading || !question.trim()} className="px-6 py-3 bg-black text-white rounded-xl text-sm font-medium hover:bg-zinc-800 disabled:bg-zinc-200">
              {loading ? 'جاري...' : 'ابدأ المعركة'}
            </button>
          </div>
        </div>

        {battle && (
          <div>
            <div className="text-center mb-4">
              <div className="text-sm font-medium">السؤال: {battle.question}</div>
              {voted && battle.agent_a_id && (
                <div className="text-xs text-zinc-500 mt-1">كشف: {battle.agent_a_name} ({battle.agent_a_id}) vs {battle.agent_b_name} ({battle.agent_b_id}) — مثل Arena.ai بعد التصويت يكشف</div>
              )}
              {!voted && <div className="text-xs text-zinc-500 mt-1">مجهول — لا تعرف أي وكيل — مثل Arena.ai — صوت أولاً</div>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border-2 border-zinc-200 rounded-xl p-4 hover:border-black transition">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-medium px-2 py-1 bg-zinc-100 rounded-full">إجابة A — مجهولة</span>
                  {voted && <span className="text-xs">{battle.agent_a_name}</span>}
                </div>
                <div className="prose prose-sm max-w-none text-sm leading-relaxed mb-4 max-h-96 overflow-auto">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{battle.answer_a}</ReactMarkdown>
                </div>
                <button onClick={() => vote('a')} disabled={voted} className={`w-full py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2 ${voted ? 'bg-zinc-100 text-zinc-400' : 'bg-black text-white hover:bg-zinc-800'}`}>
                  <Vote size={14} /> {voted && battle.vote === 'a' ? '✅ صوتت لـ A' : 'صوت لـ A أفضل'}
                </button>
              </div>

              <div className="border-2 border-zinc-200 rounded-xl p-4 hover:border-black transition">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-medium px-2 py-1 bg-zinc-100 rounded-full">إجابة B — مجهولة</span>
                  {voted && <span className="text-xs">{battle.agent_b_name}</span>}
                </div>
                <div className="prose prose-sm max-w-none text-sm leading-relaxed mb-4 max-h-96 overflow-auto">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{battle.answer_b}</ReactMarkdown>
                </div>
                <button onClick={() => vote('b')} disabled={voted} className={`w-full py-2.5 rounded-xl text-sm font-medium flex items-center justify-center gap-2 ${voted ? 'bg-zinc-100 text-zinc-400' : 'bg-black text-white hover:bg-zinc-800'}`}>
                  <Vote size={14} /> {voted && battle.vote === 'b' ? '✅ صوتت لـ B' : 'صوت لـ B أفضل'}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-center gap-3 mt-4">
              <button onClick={() => vote('tie')} disabled={voted} className={`px-4 py-2 rounded-full text-xs border ${voted ? 'bg-zinc-100 text-zinc-400' : 'bg-white border-zinc-300 hover:bg-zinc-50'}`}>تعادل — كلاهما جيد</button>
              <button onClick={() => vote('both_bad')} disabled={voted} className={`px-4 py-2 rounded-full text-xs border ${voted ? 'bg-zinc-100 text-zinc-400' : 'bg-white border-zinc-300 hover:bg-zinc-50'}`}>كلاهما سيء</button>
            </div>

            {voted && battle.leaderboard && (
              <div className="mt-8 border border-zinc-200 rounded-xl p-4">
                <div className="flex items-center gap-2 font-medium text-sm mb-3"><Trophy size={14} /> لوحة الصدارة بعد التصويت — مثل Arena.ai</div>
                <div className="space-y-1">
                  {battle.leaderboard.slice(0, 5).map((e: any) => (
                    <div key={e.agent_id} className="flex items-center justify-between text-xs py-1">
                      <span>#{e.rank} {e.agent_id}</span>
                      <span>Elo {e.rating} — {e.battles} معارك — فوز {e.wins} — {Math.round(e.win_rate * 100)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {!battle && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">⚔️</div>
            <div className="text-sm text-zinc-500">ابدأ معركة — سؤال واحد → وكيلان يجيبان مجهول → صوت → Elo — مثل Arena.ai — يعمل فعلياً — $0</div>
          </div>
        )}
      </div>
    </div>
  );
}
