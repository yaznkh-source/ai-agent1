import { useState, useEffect } from 'react';

export default function LoopsView() {
  const [goals, setGoals] = useState<any[]>([]);
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [newGoalTitle, setNewGoalTitle] = useState('');

  const fetchData = () => {
    Promise.all([
      fetch('/api/loops/goals').then(r => r.json()),
      fetch('/api/loops/status').then(r => r.json())
    ]).then(([g, s]) => {
      setGoals(g.goals || []);
      setStatus(s);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => { fetchData(); }, []);

  const createGoal = async () => {
    if (!newGoalTitle.trim()) return;
    await fetch('/api/loops/goals', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({title: newGoalTitle, description: 'From UI', owner: 'user'})
    });
    setNewGoalTitle('');
    fetchData();
  };

  if (loading) return <div className="p-8">Loading long-horizon loops...</div>;

  return (
    <div className="flex-1 overflow-auto p-8 bg-white">
      <h1 className="text-3xl font-bold mb-2">🔄 Long-Horizon Loops — From loopx 5.8k Stars 6050 Commits — $0</h1>
      <p className="text-zinc-600 mb-6">Durable goals, todos, gates, evidence, quota, recovery — Personal Workspace — agent-native Kanban — cards carry identity, authority, evidence, continuation</p>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="border rounded p-4 bg-blue-50">
          <h3 className="font-bold">Total Goals: {status?.total || 0}</h3>
          <p className="text-sm">Active: {status?.active || 0} | Completed: {status?.completed || 0} | Failed: {status?.failed || 0}</p>
        </div>
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-bold">Evidence: {status?.evidence_count || 0}</h3>
          <p className="text-sm">Typed evidence for every transition — plan, tool_call, observation, validation, writeback, gate_check, recovery</p>
        </div>
        <div className="border rounded p-4 bg-purple-50">
          <h3 className="font-bold">Quota-Aware Scheduling</h3>
          <p className="text-sm">Decides deliver/ask/wait/self-repair/quiet — semantic — better than 100/min simple</p>
        </div>
        <div className="border rounded p-4 bg-orange-50">
          <h3 className="font-bold">Gates + Recovery</h3>
          <p className="text-sm">Owner, safety, publication, private-data gates explicit — Recovery automatic 3 failures → ask human</p>
        </div>
      </div>

      <div className="border rounded p-4 mb-6">
        <h3 className="font-bold mb-2">Create Goal — Durable across days, restarts, harnesses — From LoopX</h3>
        <div className="flex gap-2">
          <input value={newGoalTitle} onChange={e => setNewGoalTitle(e.target.value)} placeholder="Goal title e.g., Build AI Agency feature" className="border rounded px-3 py-2 flex-1" />
          <button onClick={createGoal} className="bg-black text-white px-4 py-2 rounded">Create Goal</button>
          <button onClick={fetchData} className="border px-4 py-2 rounded">Refresh</button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {goals.map((goal: any) => (
          <div key={goal.id} className="border rounded p-4">
            <h3 className="font-bold">{goal.title} — {goal.status} — {goal.progress}%</h3>
            <p className="text-xs text-zinc-600">{goal.description} — Owner: {goal.owner} — Authority: {goal.authority}</p>
            <p className="text-xs">ID: {goal.id} | Created: {goal.created_at}</p>
            <p className="text-xs">Quota: {goal.quota?.used}/{goal.quota?.limit} remaining {goal.quota?.remaining}</p>
            <div className="mt-2">
              <b className="text-xs">Todos: {goal.todos?.length || 0}</b>
              <ul className="list-disc pl-5 text-xs">
                {(goal.todos || []).map((t: any) => <li key={t.id}>{t.title} — {t.status} — {t.assignee || 'unassigned'}</li>)}
              </ul>
            </div>
            <div className="mt-2">
              <b className="text-xs">Gates: {goal.gates?.length || 0}</b>
              <ul className="list-disc pl-5 text-xs">
                {(goal.gates || []).map((g: any) => <li key={g.id}>{g.type} — {g.status} — {g.description}</li>)}
              </ul>
            </div>
            <div className="mt-2">
              <b className="text-xs">Evidence: {goal.evidence?.length || 0}</b>
              <p className="text-xs truncate">{(goal.evidence || []).map((e: any) => e.content).join(' | ').slice(0, 100)}</p>
            </div>
          </div>
        ))}
      </div>

      {goals.length === 0 && <p className="text-zinc-500 mt-4">No goals yet — create one above — durable goals from LoopX pattern</p>}
    </div>
  );
}
