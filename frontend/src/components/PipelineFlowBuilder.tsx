import { useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Bot, Wrench, Code, Filter, Play, Save } from 'lucide-react';
import api from '../lib/api';

const initialNodes: Node[] = [
  { id: '1', type: 'input', position: { x: 250, y: 0 }, data: { label: 'Start: {task}' } },
  { id: '2', position: { x: 250, y: 100 }, data: { label: 'Agent: researcher' } },
  { id: '3', position: { x: 250, y: 200 }, data: { label: 'Agent: planner' } },
  { id: '4', type: 'output', position: { x: 250, y: 300 }, data: { label: 'End' } },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2' },
  { id: 'e2-3', source: '2', target: '3' },
  { id: 'e3-4', source: '3', target: '4' },
];

export default function PipelineFlowBuilder() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [pipelineName, setPipelineName] = useState('مسار Flow جديد');
  const [result, setResult] = useState<any>(null);
  const [executing, setExecuting] = useState(false);

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const addNode = (type: string) => {
    const newNode: Node = {
      id: (nodes.length + 1).toString(),
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label: `${type}: جديد` },
      type: type === 'input' ? 'input' : type === 'output' ? 'output' : 'default',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const savePipeline = async () => {
    // Convert flow to pipeline steps based on edges order
    const steps = nodes
      .filter(n => n.type !== 'input' && n.type !== 'output')
      .map((node, idx) => ({
        id: node.id,
        name: node.data.label,
        type: node.data.label.includes('Agent') ? 'agent' : node.data.label.includes('Tool') ? 'tool' : 'llm',
        config: {
          agent_id: 'fullstack-dev',
          task: node.data.label,
        }
      }));

    try {
      const res = await api.post('/pipelines/', {
        name: pipelineName,
        description: `Flow builder pipeline with ${nodes.length} nodes`,
        steps,
      });
      alert(`تم حفظ المسار: ${res.data.id} مع ${steps.length} خطوات`);
    } catch (e: any) {
      alert('خطأ: ' + e.message);
    }
  };

  const executeFlow = async () => {
    setExecuting(true);
    setResult(null);
    try {
      // Simple execution: run nodes in edge order
      const orderedNodes = [];
      let current = nodes.find(n => n.type === 'input');
      const visited = new Set();
      
      while (current && !visited.has(current.id)) {
        visited.add(current.id);
        const nextEdge = edges.find(e => e.source === current!.id);
        if (nextEdge) {
          const nextNode = nodes.find(n => n.id === nextEdge.target);
          if (nextNode && nextNode.type !== 'output') {
            orderedNodes.push(nextNode);
          }
          current = nextNode;
        } else {
          break;
        }
      }

      let context: any = { task: 'أنشئ نظام إدارة عملاء', previous_result: '' };
      const stepResults = [];

      for (const node of orderedNodes) {
        try {
          const res = await api.post('/agents/run', {
            agent_id: 'fullstack-dev',
            task: `${node.data.label}\n\nContext: ${context.previous_result || context.task}`,
            context: { user_id: 'default-user' }
          });
          context.previous_result = res.data.result;
          stepResults.push({ node: node.data.label, result: res.data.result.slice(0,150) });
        } catch (e) {
          stepResults.push({ node: node.data.label, result: 'Mock: ' + node.data.label });
          context.previous_result = 'Mock result for ' + node.data.label;
        }
      }

      setResult({ steps: stepResults, final: context.previous_result });
    } catch (e: any) {
      setResult({ error: e.message });
    }
    setExecuting(false);
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      <div className="flex-1 flex flex-col">
        <div className="p-4 bg-white border-b flex items-center gap-3">
          <input value={pipelineName} onChange={e=>setPipelineName(e.target.value)} className="text-lg font-bold bg-transparent border-0 outline-0 flex-1" />
          <div className="flex gap-2">
            <button onClick={()=>addNode('default')} className="px-3 py-1.5 bg-violet-100 text-violet-700 rounded-full text-xs flex items-center gap-1"><Bot size={12}/>+ وكيل</button>
            <button onClick={()=>addNode('input')} className="px-3 py-1.5 bg-green-100 text-green-700 rounded-full text-xs">+ بداية</button>
            <button onClick={()=>addNode('output')} className="px-3 py-1.5 bg-red-100 text-red-700 rounded-full text-xs">+ نهاية</button>
            <button onClick={savePipeline} className="px-4 py-2 bg-zinc-900 text-white rounded-xl text-sm flex items-center gap-2"><Save size={14}/>حفظ</button>
            <button onClick={executeFlow} disabled={executing} className="px-4 py-2 bg-violet-600 text-white rounded-xl text-sm flex items-center gap-2"><Play size={14}/>{executing?'جاري...':'تنفيذ Flow'}</button>
          </div>
        </div>

        <div className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >
            <Controls />
            <MiniMap />
            <Background />
          </ReactFlow>
        </div>
      </div>

      <div className="w-96 bg-white border-l flex flex-col">
        <div className="p-4 border-b">
          <h3 className="font-semibold">نتيجة Flow</h3>
          <p className="text-xs text-zinc-500 mt-1">تنفيذ حسب ترتيب الاتصالات</p>
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          {result ? (
            <div className="space-y-3">
              {result.steps?.map((s:any, i:number) => (
                <div key={i} className="p-3 bg-zinc-50 rounded-xl border text-xs">
                  <div className="font-medium">{i+1}. {s.node}</div>
                  <div className="text-zinc-600 mt-1">{s.result}</div>
                </div>
              ))}
              {result.final && <div className="p-4 bg-violet-50 border border-violet-200 rounded-xl text-sm">{result.final.slice(0,500)}</div>}
              {result.error && <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{result.error}</div>}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-12 h-12 mx-auto bg-violet-100 rounded-xl flex items-center justify-center mb-3"><Play size={20} className="text-violet-600"/></div>
              <div className="text-sm text-zinc-500">اسحب العقد واربطها ثم اضغط تنفيذ</div>
              <div className="text-xs text-zinc-400 mt-2">Flow Builder مستوحى من n8n + Open WebUI Pipelines</div>
            </div>
          )}
        </div>
        <div className="p-4 border-t bg-zinc-50 text-xs">
          <div className="font-semibold mb-2">💡 كيف يعمل</div>
          <div className="text-zinc-600 leading-relaxed">
            اسحب العقد، اربطها بالأسهم، كل عقدة تنفذ وتتمرر نتيجتها للتالية كـ previous_result.
            مثل n8n لكن للوكلاء AI.
          </div>
        </div>
      </div>
    </div>
  );
}
