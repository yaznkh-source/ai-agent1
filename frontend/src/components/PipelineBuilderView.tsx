import { useState } from 'react';
import { Workflow, Plus, Trash2, Play, Save, Bot, Wrench, Code, Filter } from 'lucide-react';
import api from '../lib/api';

interface Step {
  id: string;
  name: string;
  type: 'agent' | 'tool' | 'llm' | 'filter';
  config: any;
}

export default function PipelineBuilderView() {
  const [pipelineName, setPipelineName] = useState('مسار جديد');
  const [pipelineDesc, setPipelineDesc] = useState('وصف المسار');
  const [steps, setSteps] = useState<Step[]>([
    { id: '1', name: 'بحث', type: 'agent', config: { agent_id: 'researcher', task: 'ابحث عن {task}' } },
    { id: '2', name: 'خطة', type: 'agent', config: { agent_id: 'planner', task: 'خطط بناء على:\n{previous_result}' } },
  ]);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<any>(null);

  const addStep = (type: Step['type']) => {
    const newStep: Step = {
      id: Date.now().toString(),
      name: `خطوة ${steps.length + 1}`,
      type,
      config: type === 'agent' ? { agent_id: 'fullstack-dev', task: '{previous_result}' } :
              type === 'tool' ? { tool_name: 'web_search', args: { query: '{task}' } } :
              type === 'llm' ? { prompt: 'لخص:\n{previous_result}', model: 'gpt-4o-mini' } :
              { input: 'previous_result', output: 'previous_result', transform: 'summarize' }
    };
    setSteps([...steps, newStep]);
  };

  const updateStep = (id: string, updates: Partial<Step>) => {
    setSteps(steps.map(s => s.id === id ? { ...s, ...updates } : s));
  };

  const removeStep = (id: string) => {
    setSteps(steps.filter(s => s.id !== id));
  };

  const savePipeline = async () => {
    try {
      const res = await api.post('/pipelines/', {
        name: pipelineName,
        description: pipelineDesc,
        steps: steps.map(s => ({ id: s.id, name: s.name, type: s.type, config: s.config }))
      });
      alert(`تم حفظ المسار: ${res.data.id}`);
    } catch (e: any) {
      alert('خطأ: ' + e.message);
    }
  };

  const executePipeline = async () => {
    setExecuting(true);
    setResult(null);
    try {
      // First save as temp then execute via orchestrator mock
      // For demo, execute steps sequentially via API
      let context: any = { task: 'أنشئ نظام إدارة عملاء', client_name: 'شركة التقنية' };
      const stepResults = [];
      
      for (const step of steps) {
        if (step.type === 'agent') {
          const res = await api.post('/agents/run', {
            agent_id: step.config.agent_id,
            task: step.config.task.replace('{previous_result}', context.previous_result || '').replace('{task}', context.task),
            context: { user_id: 'default-user' }
          });
          context.previous_result = res.data.result;
          context[`step_${step.id}`] = res.data.result;
          stepResults.push({ step: step.name, result: res.data.result.slice(0,200) });
        } else if (step.type === 'tool') {
          const res = await api.post('/tools/execute', {
            tool_name: step.config.tool_name,
            arguments: step.config.args
          });
          context.previous_result = JSON.stringify(res.data);
          stepResults.push({ step: step.name, result: JSON.stringify(res.data).slice(0,200) });
        } else {
          // LLM or filter mock
          context.previous_result = `Mock result for ${step.name}: ${context.previous_result?.slice(0,100) || context.task}`;
          stepResults.push({ step: step.name, result: context.previous_result });
        }
      }
      
      setResult({ final: context.previous_result, steps: stepResults });
    } catch (e: any) {
      setResult({ error: e.message });
    }
    setExecuting(false);
  };

  const typeIcons = {
    agent: <Bot size={14} />,
    tool: <Wrench size={14} />,
    llm: <Code size={14} />,
    filter: <Filter size={14} />
  };

  const typeColors = {
    agent: 'bg-violet-100 text-violet-700 border-violet-200',
    tool: 'bg-orange-100 text-orange-700 border-orange-200',
    llm: 'bg-blue-100 text-blue-700 border-blue-200',
    filter: 'bg-green-100 text-green-700 border-green-200'
  };

  return (
    <div className="flex-1 flex bg-zinc-50 overflow-hidden">
      {/* Builder */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="p-4 bg-white border-b">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 flex items-center justify-center text-white">
              <Workflow size={20} />
            </div>
            <div className="flex-1">
              <input value={pipelineName} onChange={e=>setPipelineName(e.target.value)} className="text-xl font-bold bg-transparent border-0 outline-0 w-full" />
              <input value={pipelineDesc} onChange={e=>setPipelineDesc(e.target.value)} className="text-sm text-zinc-500 bg-transparent border-0 outline-0 w-full" />
            </div>
            <div className="flex gap-2">
              <button onClick={savePipeline} className="px-4 py-2 bg-zinc-900 text-white rounded-xl text-sm flex items-center gap-2"><Save size={16}/>حفظ</button>
              <button onClick={executePipeline} disabled={executing} className="px-4 py-2 bg-violet-600 text-white rounded-xl text-sm flex items-center gap-2"><Play size={16}/>{executing?'جاري...':'تنفيذ'}</button>
            </div>
          </div>

          <div className="flex gap-2">
            <button onClick={()=>addStep('agent')} className="px-3 py-1.5 bg-violet-100 text-violet-700 rounded-full text-xs flex items-center gap-1"><Bot size={12}/>+ وكيل</button>
            <button onClick={()=>addStep('tool')} className="px-3 py-1.5 bg-orange-100 text-orange-700 rounded-full text-xs flex items-center gap-1"><Wrench size={12}/>+ أداة</button>
            <button onClick={()=>addStep('llm')} className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs flex items-center gap-1"><Code size={12}/>+ LLM</button>
            <button onClick={()=>addStep('filter')} className="px-3 py-1.5 bg-green-100 text-green-700 rounded-full text-xs flex items-center gap-1"><Filter size={12}/>+ فلتر</button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-3xl mx-auto">
            <div className="relative">
              {/* Vertical line */}
              <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-zinc-200 -translate-x-1/2 hidden md:block" />

              <div className="space-y-6">
                {steps.map((step, idx) => (
                  <div key={step.id} className="relative flex flex-col md:flex-row items-center gap-4">
                    {/* Number */}
                    <div className="hidden md:flex absolute left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-white border-2 border-zinc-300 items-center justify-center text-xs font-bold z-10">
                      {idx+1}
                    </div>

                    <div className={`flex-1 w-full bg-white rounded-2xl border p-5 shadow-sm ${idx%2===0?'md:mr-12':'md:ml-12 md:order-2'}`}>
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 rounded-full text-xs border flex items-center gap-1 ${typeColors[step.type]}`}>
                            {typeIcons[step.type]} {step.type}
                          </span>
                          <input value={step.name} onChange={e=>updateStep(step.id, { name: e.target.value })} className="font-medium bg-transparent border-0 outline-0" />
                        </div>
                        <button onClick={()=>removeStep(step.id)} className="p-1 hover:bg-red-50 text-zinc-400 hover:text-red-600 rounded-lg"><Trash2 size={14}/></button>
                      </div>

                      <div className="space-y-3">
                        {step.type === 'agent' && (
                          <>
                            <div>
                              <label className="text-xs text-zinc-500">Agent ID</label>
                              <select value={step.config.agent_id} onChange={e=>updateStep(step.id, { config: { ...step.config, agent_id: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm">
                                <option value="researcher">researcher</option>
                                <option value="planner">planner</option>
                                <option value="backend-dev">backend-dev</option>
                                <option value="frontend-dev">frontend-dev</option>
                                <option value="fullstack-dev">fullstack-dev</option>
                                <option value="reviewer">reviewer</option>
                                <option value="seo-specialist">seo-specialist</option>
                                <option value="content-creator">content-creator</option>
                              </select>
                            </div>
                            <div>
                              <label className="text-xs text-zinc-500">Task Template (use {"{task}"}, {"{previous_result}"})</label>
                              <textarea value={step.config.task} onChange={e=>updateStep(step.id, { config: { ...step.config, task: e.target.value } })} className="w-full mt-1 p-3 border rounded-xl text-sm h-20 resize-none" />
                            </div>
                          </>
                        )}

                        {step.type === 'tool' && (
                          <>
                            <div>
                              <label className="text-xs text-zinc-500">Tool Name</label>
                              <select value={step.config.tool_name} onChange={e=>updateStep(step.id, { config: { ...step.config, tool_name: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm">
                                <option value="web_search">web_search</option>
                                <option value="security_scan">security_scan</option>
                                <option value="diagram_generator">diagram_generator</option>
                                <option value="knowledge_search">knowledge_search</option>
                              </select>
                            </div>
                            <div>
                              <label className="text-xs text-zinc-500">Args JSON</label>
                              <input value={JSON.stringify(step.config.args)} onChange={e=>{ try { const args=JSON.parse(e.target.value); updateStep(step.id, { config: { ...step.config, args } }); } catch {} }} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm font-mono" />
                            </div>
                          </>
                        )}

                        {step.type === 'llm' && (
                          <>
                            <div>
                              <label className="text-xs text-zinc-500">Prompt Template</label>
                              <textarea value={step.config.prompt} onChange={e=>updateStep(step.id, { config: { ...step.config, prompt: e.target.value } })} className="w-full mt-1 p-3 border rounded-xl text-sm h-20 resize-none" />
                            </div>
                            <div>
                              <label className="text-xs text-zinc-500">Model</label>
                              <select value={step.config.model} onChange={e=>updateStep(step.id, { config: { ...step.config, model: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm">
                                <option value="gpt-4o-mini">gpt-4o-mini</option>
                                <option value="gpt-4o">gpt-4o</option>
                                <option value="llama3.1:8b">llama3.1:8b</option>
                              </select>
                            </div>
                          </>
                        )}

                        {step.type === 'filter' && (
                          <>
                            <div className="grid grid-cols-2 gap-3">
                              <div>
                                <label className="text-xs text-zinc-500">Input Key</label>
                                <input value={step.config.input} onChange={e=>updateStep(step.id, { config: { ...step.config, input: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm" />
                              </div>
                              <div>
                                <label className="text-xs text-zinc-500">Output Key</label>
                                <input value={step.config.output} onChange={e=>updateStep(step.id, { config: { ...step.config, output: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm" />
                              </div>
                            </div>
                            <div>
                              <label className="text-xs text-zinc-500">Transform</label>
                              <select value={step.config.transform} onChange={e=>updateStep(step.id, { config: { ...step.config, transform: e.target.value } })} className="w-full mt-1 px-3 py-2 border rounded-xl text-sm">
                                <option value="identity">identity</option>
                                <option value="summarize">summarize</option>
                                <option value="extract_json">extract_json</option>
                              </select>
                            </div>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Spacer for alternating layout */}
                    <div className={`hidden md:block flex-1 ${idx%2===0?'md:order-2':'md:mr-12'}`} />
                  </div>
                ))}

                {steps.length === 0 && (
                  <div className="text-center py-16 bg-white rounded-2xl border-2 border-dashed">
                    <Workflow size={32} className="mx-auto text-zinc-300 mb-3" />
                    <div className="text-sm text-zinc-500">لا توجد خطوات - أضف وكيل أو أداة للبدء</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Result Panel */}
      <div className="w-96 bg-white border-l flex flex-col">
        <div className="p-4 border-b">
          <h3 className="font-semibold">نتيجة التنفيذ</h3>
          <p className="text-xs text-zinc-500 mt-1">Context: task, client_name, previous_result</p>
        </div>
        <div className="flex-1 overflow-y-auto p-4">
          {result ? (
            <div className="space-y-4">
              {result.steps?.map((s:any, i:number) => (
                <div key={i} className="p-3 bg-zinc-50 rounded-xl border">
                  <div className="font-medium text-xs">{i+1}. {s.step}</div>
                  <div className="text-xs text-zinc-600 mt-1 whitespace-pre-wrap">{s.result}</div>
                </div>
              ))}
              {result.final && (
                <div className="p-4 bg-violet-50 border border-violet-200 rounded-xl">
                  <div className="text-xs font-semibold text-violet-900 mb-2">النتيجة النهائية:</div>
                  <div className="text-sm whitespace-pre-wrap">{result.final.slice(0,500)}</div>
                </div>
              )}
              {result.error && <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">{result.error}</div>}
            </div>
          ) : (
            <div className="text-center py-12">
              <Play size={24} className="mx-auto text-zinc-300 mb-2" />
              <div className="text-sm text-zinc-500">اضغط تنفيذ لترى النتيجة</div>
              <div className="text-xs text-zinc-400 mt-2">سيتم تشغيل الخطوات بالتتابع مع تمرير previous_result</div>
            </div>
          )}
        </div>

        <div className="p-4 border-t bg-zinc-50">
          <div className="text-xs font-semibold mb-2">💡 فكرة Pipeline Builder</div>
          <div className="text-xs text-zinc-600 leading-relaxed">
            مستوحى من Open WebUI Pipelines + n8n: كل خطوة تستقبل context وتنتج previous_result للخطوة التالية.
            يمكنك استخدام {"{task}"}، {"{client_name}"}، {"{previous_result}"}، {"{step_<id>}"} في القوالب.
          </div>
        </div>
      </div>
    </div>
  );
}
