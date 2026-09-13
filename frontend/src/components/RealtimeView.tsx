import { useEffect, useState, useRef } from 'react';
import { Radio, Send, Users, Zap } from 'lucide-react';

export default function RealtimeView() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [room, setRoom] = useState('general');
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const [rooms, setRooms] = useState<any>(null);

  useEffect(() => {
    fetch('/api/realtime/rooms').then(r=>r.json()).then(setRooms).catch(()=>{});
    connect();
    return () => wsRef.current?.close();
  }, [room]);

  const connect = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/api/realtime/ws/${room}?user_id=default-user`;
    
    // For demo, use mock if WebSocket fails
    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnected(true);
        setMessages(m => [...m, { type: 'system', text: `✅ متصل بغرفة ${room}`, timestamp: new Date().toISOString() }]);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setMessages(m => [...m, { type: data.type || 'message', data, timestamp: new Date().toISOString() }]);
        } catch {
          setMessages(m => [...m, { type: 'message', text: event.data, timestamp: new Date().toISOString() }]);
        }
      };

      ws.onclose = () => {
        setConnected(false);
        setMessages(m => [...m, { type: 'system', text: '❌ انقطع الاتصال', timestamp: new Date().toISOString() }]);
      };

      ws.onerror = () => {
        setConnected(false);
      };
    } catch {
      setConnected(false);
      // Mock mode
      setMessages(m => [...m, { type: 'system', text: '⚠️ WebSocket غير متاح - وضع Mock', timestamp: new Date().toISOString() }]);
    }
  };

  const send = () => {
    if (!input.trim()) return;
    
    if (wsRef.current && connected) {
      wsRef.current.send(JSON.stringify({ text: input, room, user_id: 'default-user' }));
    } else {
      // Mock
      setMessages(m => [...m, 
        { type: 'message', text: `أنت: ${input}`, timestamp: new Date().toISOString() },
        { type: 'agent_start', data: { agent_id: 'planner', task: input }, timestamp: new Date().toISOString() },
        { type: 'agent_token', data: { token: 'جاري التخطيط...' }, timestamp: new Date().toISOString() },
        { type: 'agent_complete', data: { result: `تم التخطيط لـ: ${input}` }, timestamp: new Date().toISOString() },
      ]);
    }
    
    setInput('');
  };

  const broadcastTest = async (type: string) => {
    try {
      if (type === 'task') {
        await fetch('/api/realtime/notify/task/test-task', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: 'in_progress', project_id: 'test-project', room })
        });
      } else if (type === 'agent') {
        await fetch('/api/realtime/notify/agent/planner', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ type: 'start', run_id: 'run-123', data: 'مهمة جديدة', room })
        });
      }
    } catch {}
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      <div className="flex-1 flex flex-col bg-white">
        <div className="p-4 border-b flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${connected?'bg-green-500 animate-pulse':'bg-red-500'}`} />
          <h2 className="font-bold flex items-center gap-2"><Radio size={18} className="text-violet-600"/>الوقت الحقيقي - WebSocket</h2>
          <span className="text-xs bg-zinc-100 px-2 py-1 rounded-full">غرفة: {room}</span>
          <span className={`text-xs px-2 py-1 rounded-full ${connected?'bg-green-100 text-green-700':'bg-red-100 text-red-700'}`}>{connected?'متصل':'غير متصل'}</span>
          <div className="ml-auto flex gap-2">
            <input value={room} onChange={e=>setRoom(e.target.value)} placeholder="اسم الغرفة" className="px-3 py-1.5 border rounded-xl text-xs" />
            <button onClick={connect} className="px-3 py-1.5 bg-violet-600 text-white rounded-xl text-xs">اتصال</button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg, i) => (
            <div key={i} className={`p-3 rounded-xl border text-sm ${
              msg.type==='system'?'bg-zinc-50 text-zinc-500 text-xs':
              msg.type==='agent_start'?'bg-violet-50 border-violet-200':
              msg.type==='agent_complete'?'bg-green-50 border-green-200':
              msg.type==='task_update'?'bg-blue-50 border-blue-200':
              'bg-white'
            }`}>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold">{msg.type}</span>
                <span className="text-xs text-zinc-400 ml-auto">{new Date(msg.timestamp).toLocaleTimeString('ar')}</span>
              </div>
              <div className="mt-1">
                {msg.text && <div>{msg.text}</div>}
                {msg.data && <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(msg.data, null, 2).slice(0,300)}</pre>}
              </div>
            </div>
          ))}
          {messages.length===0 && <div className="text-center py-16 text-zinc-400 text-sm">لا رسائل - ابدأ محادثة أو اختبر البث</div>}
        </div>

        <div className="p-4 border-t bg-zinc-50">
          <div className="flex gap-2">
            <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="اكتب رسالة للبث في الغرفة..." className="flex-1 px-4 py-2.5 border rounded-xl bg-white" />
            <button onClick={send} className="px-4 py-2.5 bg-violet-600 text-white rounded-xl"><Send size={16}/></button>
          </div>
          <div className="flex gap-2 mt-3">
            <button onClick={()=>broadcastTest('task')} className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs">بث تحديث مهمة</button>
            <button onClick={()=>broadcastTest('agent')} className="px-3 py-1.5 bg-violet-100 text-violet-700 rounded-full text-xs">بث بدء وكيل</button>
          </div>
        </div>
      </div>

      <div className="w-80 bg-white border-l p-4 overflow-y-auto">
        <h3 className="font-semibold mb-4">الغرف النشطة</h3>
        {rooms ? (
          <div className="space-y-2">
            {Object.entries(rooms.counts || {}).map(([r, count]: any) => (
              <div key={r} className="p-3 bg-zinc-50 rounded-xl flex items-center justify-between">
                <span className="text-sm font-medium">{r}</span>
                <span className="text-xs bg-violet-100 text-violet-700 px-2 py-1 rounded-full flex items-center gap-1"><Users size={10}/>{count}</span>
              </div>
            ))}
            {Object.keys(rooms.counts || {}).length===0 && <div className="text-xs text-zinc-400">لا غرف نشطة</div>}
            <div className="text-xs text-zinc-400 mt-2">إجمالي اتصالات: {rooms.total_connections}</div>
          </div>
        ) : <div className="text-xs text-zinc-400">جاري التحميل...</div>}

        <div className="mt-8">
          <h4 className="font-semibold text-sm mb-3">💡 استخدامات WebSocket</h4>
          <div className="space-y-3 text-xs text-zinc-600">
            <div className="p-3 bg-violet-50 border border-violet-200 rounded-xl">
              <div className="font-medium">بث تنفيذ الوكيل مباشر</div>
              <div className="mt-1">عندما يبدأ وكيل مهمة، كل أعضاء المشروع يرون token by token مثل ChatGPT</div>
            </div>
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl">
              <div className="font-medium">تحديثات المهام فورية</div>
              <div className="mt-1">عندما تكتمل مهمة، العميل يرى التحديث فوراً بدون refresh</div>
            </div>
            <div className="p-3 bg-green-50 border border-green-200 rounded-xl">
              <div className="font-medium">تعاون فريق</div>
              <div className="mt-1">فريق يعمل على نفس المشروع - يرى كل واحد ما يفعله الآخرون live</div>
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-zinc-900 text-zinc-100 rounded-xl text-xs">
          <div className="font-medium mb-2">كود WebSocket:</div>
          <pre className="whitespace-pre-wrap text-[10px]">
{`const ws = new WebSocket(
  'wss://host/api/realtime/ws/general?user_id=123'
);
ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  // data.type: agent_start, agent_token, agent_complete, task_update
};`}
          </pre>
        </div>
      </div>
    </div>
  );
}
