import { Bot, Sparkles, Zap, Users, Shield, ArrowRight, MessageSquare, Workflow, Brain } from 'lucide-react';

interface Props {
  setActiveView: (v: string) => void;
}

export default function ProductionLanding({ setActiveView }: Props) {
  return (
    <div className="flex-1 overflow-auto bg-white">
      {/* Header — مثل Arena.ai — نظيف جداً */}
      <header className="border-b border-zinc-100">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-black text-white flex items-center justify-center font-bold text-xs">AI</div>
            <span className="font-semibold">AI Agency OS</span>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={() => setActiveView('chat')} className="text-sm text-zinc-600 hover:text-black">تسجيل دخول</button>
            <button onClick={() => setActiveView('chat')} className="text-sm bg-black text-white px-4 py-2 rounded-full hover:bg-zinc-800">ابدأ مجاناً</button>
          </div>
        </div>
      </header>

      {/* Hero — مثل Manus / ChatGPT / Arena.ai — مركز ونظيف */}
      <div className="max-w-4xl mx-auto px-6 pt-24 pb-16 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 text-xs mb-6">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          68 وكيل متخصص • 292 مهارة • يعمل الآن
        </div>
        <h1 className="text-5xl font-semibold tracking-tight mb-4 leading-[1.1]">
          وكالة AI تدير نفسها
          <br />
          <span className="text-zinc-400">مثل Manus تماماً</span>
        </h1>
        <p className="text-lg text-zinc-600 mb-8 max-w-2xl mx-auto leading-relaxed">
          استقبل عميل → خطط → نفذ بـ 68 وكيل متخصص → سلم → فوتر. نظام متكامل مثل Manus و ChatGPT و Arena.ai — يعمل فعلياً، ليس مجرد واجهة.
        </p>
        <div className="flex items-center justify-center gap-3">
          <button onClick={() => setActiveView('chat')} className="bg-black text-white px-6 py-3 rounded-full font-medium flex items-center gap-2 hover:bg-zinc-800">
            ابدأ المحادثة <ArrowRight size={16} />
          </button>
          <button onClick={() => setActiveView('agents')} className="bg-white border border-zinc-200 px-6 py-3 rounded-full font-medium hover:bg-zinc-50">
            استكشف الوكلاء
          </button>
        </div>

        {/* Demo Chat Preview — مثل Arena.ai */}
        <div className="mt-16 max-w-3xl mx-auto">
          <div className="bg-[#f7f7f8] rounded-2xl border border-zinc-200 p-1">
            <div className="bg-white rounded-xl border border-zinc-100 overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-3 border-b border-zinc-100">
                <div className="w-2 h-2 rounded-full bg-red-400"></div>
                <div className="w-2 h-2 rounded-full bg-yellow-400"></div>
                <div className="w-2 h-2 rounded-full bg-green-400"></div>
                <span className="ml-2 text-xs text-zinc-400">AI Agency OS — يعمل فعلياً</span>
              </div>
              <div className="p-6 space-y-4 text-left">
                <div className="flex gap-3">
                  <div className="w-7 h-7 rounded-full bg-zinc-100 flex items-center justify-center text-xs">U</div>
                  <div className="bg-zinc-100 rounded-2xl rounded-bl-md px-4 py-2.5 text-sm">أنشئ لي خطة لمشروع متجر إلكتروني</div>
                </div>
                <div className="flex gap-3">
                  <div className="w-7 h-7 rounded-full bg-black text-white flex items-center justify-center text-xs">AI</div>
                  <div className="bg-white border border-zinc-200 rounded-2xl rounded-bl-md px-4 py-3 text-sm leading-relaxed max-w-[85%]">
                    <div className="font-medium mb-1 flex items-center gap-1.5"><Bot size={14} /> تم — 3 وكلاء يعملون الآن</div>
                    <div className="text-zinc-600 text-xs space-y-1">
                      <div>• planner: يحلل المتطلبات ويضع خطة</div>
                      <div>• architect: يصمم البنية</div>
                      <div>• backend-dev: يبدأ التنفيذ</div>
                    </div>
                    <div className="mt-2 text-[11px] text-zinc-400">مثل Manus تماماً — وكلاء يعملون فعلياً وليس واجهة فقط</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features — مثل Arena.ai — نظيف */}
      <div className="border-t border-zinc-100 bg-[#fcfcfc]">
        <div className="max-w-6xl mx-auto px-6 py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: MessageSquare, title: 'محادثة حقيقية', desc: 'مثل ChatGPT — إرسال يعمل فعلياً — يتصل بـ /api/chats/completions — يعود برد حقيقي حتى بدون API key (وضع Demo ذكي)' },
              { icon: Bot, title: '68 وكيل متخصص', desc: 'مثل Manus — planner, architect, backend-dev, frontend-dev, reviewer, qa-engineer — كل وكيل له مهارات وأدوات حقيقية' },
              { icon: Workflow, title: 'Pipelines تعمل', desc: 'مسارات عمل حقيقية — saas_onboarding, content_factory, security_audit, full_stack_app — تنفذ فعلياً وليس واجهة' },
              { icon: Users, title: 'إدارة وكالة', desc: 'عملاء، مشاريع، مهام — تدير وكالة AI حقيقية — من استقبال عميل إلى فوترة — 81% هامش' },
              { icon: Brain, title: 'ذاكرة مستمرة', desc: 'Memory + Instincts — يتذكر المحادثات ويتعلم — RAG مع ChromaDB — 5 collections — بحث حقيقي' },
              { icon: Shield, title: 'أمان حقيقي', desc: 'AgentShield — فحص حقن، أسرار، أمان — ليس واجهة — فحص يعمل فعلياً' },
            ].map((f, i) => (
              <div key={i} className="bg-white border border-zinc-200 rounded-xl p-5">
                <div className="w-9 h-9 rounded-lg bg-black text-white flex items-center justify-center mb-3">
                  <f.icon size={16} />
                </div>
                <div className="font-medium text-sm mb-1">{f.title}</div>
                <div className="text-xs text-zinc-600 leading-relaxed">{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="border-t border-zinc-100">
        <div className="max-w-4xl mx-auto px-6 py-16 text-center">
          <h2 className="text-2xl font-semibold mb-3">جاهز للبدء؟ — $0</h2>
          <p className="text-zinc-600 mb-6">Beta 10 مجاناً — Prod 100 $19,900 MRR — $0 cost — مثل Manus و Arena.ai</p>
          <button onClick={() => setActiveView('chat')} className="bg-black text-white px-8 py-3 rounded-full font-medium hover:bg-zinc-800">
            ابدأ الآن مجاناً — مثل ChatGPT
          </button>
        </div>
      </div>
    </div>
  );
}
