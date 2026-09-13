import { Bot, Zap, Shield, Workflow, Brain, BarChart3, Users, CheckCircle, ArrowRight, Star } from 'lucide-react';

export default function LandingPageView({ setActiveView }: { setActiveView: (view: string) => void }) {
  return (
    <div className="flex-1 bg-white overflow-y-auto">
      {/* Hero */}
      <div className="bg-gradient-to-br from-violet-600 via-indigo-600 to-purple-700 text-white">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="flex items-center gap-2 mb-6">
            <span className="px-3 py-1 bg-white/20 rounded-full text-xs">🎉 68 Agents + 292 Skills - ECC + Open WebUI Hybrid</span>
            <span className="px-3 py-1 bg-green-500 rounded-full text-xs flex items-center gap-1"><Star size={12}/>Product Hunt #1</span>
          </div>
          
          <h1 className="text-5xl font-bold leading-tight max-w-3xl">
            وكالة ذكاء اصطناعي<br/>
            <span className="bg-gradient-to-r from-amber-200 to-pink-200 bg-clip-text text-transparent">متكاملة في نظام واحد</span>
          </h1>
          
          <p className="text-xl text-violet-100 mt-6 max-w-2xl leading-relaxed">
            مستوحى من ECC (257k⭐) و Open WebUI (152k⭐). 68 وكيل متخصص، 292 مهارة، تحقق حتمي، ذاكرة مستمرة، فوترة، وبوابة عملاء.
          </p>

          <div className="flex gap-4 mt-10">
            <button onClick={()=>setActiveView('chat')} className="px-8 py-4 bg-white text-violet-700 rounded-2xl font-bold flex items-center gap-2 hover:shadow-xl transition-all">
              ابدأ مجاناً <ArrowRight size={18}/>
            </button>
            <button onClick={()=>setActiveView('dashboard')} className="px-8 py-4 bg-violet-500/30 border border-white/20 text-white rounded-2xl font-medium hover:bg-violet-500/50 transition-all">
              عرض Demo
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16">
            {[
              { value: '68', label: 'وكيل متخصص' },
              { value: '292', label: 'مهارة جاهزة' },
              { value: '88%', label: 'هامش ربح' },
              { value: '<10د', label: 'Onboarding عميل' },
            ].map((stat, i) => (
              <div key={i} className="bg-white/10 backdrop-blur border border-white/10 rounded-2xl p-5">
                <div className="text-3xl font-bold">{stat.value}</div>
                <div className="text-sm text-violet-200 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features - ECC + Open WebUI */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold">يجمع أفضل ما في العالمين</h2>
          <p className="text-zinc-600 mt-4">ECC للذكاء والتنظيم، Open WebUI للسهولة والمرونة، Agency للإدارة والربح</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-gradient-to-br from-violet-50 to-indigo-50 border border-violet-200 rounded-3xl p-8">
            <div className="w-12 h-12 rounded-2xl bg-violet-600 flex items-center justify-center text-white mb-6"><Bot size={24}/></div>
            <h3 className="font-bold text-xl">مستوحى من ECC</h3>
            <p className="text-sm text-zinc-600 mt-3 leading-relaxed">68 وكيل متخصص بسياق معزول، 292 مهارة تحمل عند الحاجة، hooks خارج السياق، ذاكرة مستمرة، تعلم مستمر instincts، حلقة تحقق، AgentShield</p>
            <div className="mt-6 space-y-2 text-sm">
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-violet-600"/>plan → test → implement → review → verify → remember → improve</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-violet-600"/>Fresh-context reviewer (نفس السياق يكتب ويراجع = فشل)</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-violet-600"/>Skills تحمل عند الحاجة فقط (context optimization)</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200 rounded-3xl p-8">
            <div className="w-12 h-12 rounded-2xl bg-blue-600 flex items-center justify-center text-white mb-6"><Workflow size={24}/></div>
            <h3 className="font-bold text-xl">مستوحى من Open WebUI</h3>
            <p className="text-sm text-zinc-600 mt-3 leading-relaxed">واجهة محادثة سهلة، دعم متعدد النماذج (OpenAI, Ollama, Anthropic)، Tools، Functions (Pipe/Filter/Action/Event)، Pipelines</p>
            <div className="mt-6 space-y-2 text-sm">
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-blue-600"/>Tools: توسيع قدرات LLM (طقس، بحث، ...)</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-blue-600"/>Functions: توسيع المنصة (Pipe/Filter/Action/Event)</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-blue-600"/>Pipelines: إطار OpenAI API متوافق لفصل المعالجة</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-violet-600 to-indigo-600 rounded-3xl p-8 text-white">
            <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center mb-6"><Users size={24}/></div>
            <h3 className="font-bold text-xl">AI Agency OS (الجديد)</h3>
            <p className="text-sm text-violet-100 mt-3 leading-relaxed">إدارة وكالة كاملة: عملاء، مشاريع، مهام، بوابة عميل، فوترة، ربحية، تكاملات Slack/GitHub/n8n/WhatsApp</p>
            <div className="mt-6 space-y-2 text-sm text-violet-100">
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-white"/>Onboarding عميل في &lt;10 دقائق</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-white"/>Proposal تلقائي + PDF</div>
              <div className="flex items-center gap-2"><CheckCircle size={16} className="text-white"/>تتبع ربحية: إيراد - تكلفة LLM</div>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing */}
      <div className="bg-zinc-50 border-y">
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-3xl font-bold">تسعير بسيط وواضح</h2>
            <p className="text-zinc-600 mt-3">ابدأ مجاناً، ادفع عند النمو. 88% هامش ربح مع مزيج Ollama المجاني</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { name: 'Free', price: '$0', features: ['5 وكلاء', '2 مشروع', '20 مهمة/شهر', '100K tokens'], cta: 'ابدأ مجاناً', popular: false },
              { name: 'Starter', price: '$49', features: ['15 وكيل', '10 مشاريع', '200 مهمة/شهر', '1M tokens', '3 أعضاء'], cta: 'اشترك', popular: false },
              { name: 'Pro', price: '$199', features: ['35 وكيل', '100 مشروع', '2000 مهمة/شهر', '10M tokens', '10 أعضاء'], cta: 'الأكثر شيوعاً', popular: true },
              { name: 'Enterprise', price: '$999', features: ['68 وكيل', '1000 مشروع', '10000 مهمة/شهر', '100M tokens', '100 عضو', 'دعم مخصص', 'وكلاء مخصصين'], cta: 'تواصل', popular: false },
            ].map((tier, i) => (
              <div key={i} className={`bg-white rounded-3xl border p-8 ${tier.popular?'ring-2 ring-violet-600 shadow-xl scale-105':''} relative`}>
                {tier.popular && <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-violet-600 text-white text-xs px-4 py-1 rounded-full">الأكثر شيوعاً</div>}
                <h3 className="font-bold text-lg">{tier.name}</h3>
                <div className="text-4xl font-bold mt-4">{tier.price}<span className="text-sm font-normal text-zinc-500">/شهر</span></div>
                <div className="mt-6 space-y-3">
                  {tier.features.map((f, j) => (
                    <div key={j} className="flex items-center gap-2 text-sm"><CheckCircle size={16} className="text-green-500"/>{f}</div>
                  ))}
                </div>
                <button onClick={()=>setActiveView('billing')} className={`mt-8 w-full py-3 rounded-2xl font-medium ${tier.popular?'bg-violet-600 text-white':'bg-zinc-900 text-white'}`}>{tier.cta}</button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Social Proof */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white border rounded-3xl p-8">
            <div className="flex gap-1 mb-4">{[1,2,3,4,5].map(i=><Star key={i} size={16} className="fill-amber-400 text-amber-400"/>)}</div>
            <p className="text-sm leading-relaxed">"وفرنا 80% من وقت التطوير. الـ verification loop يمنع دمج كود فاشل. Fresh-context reviewer وجد bugs لم نرها."</p>
            <div className="flex items-center gap-3 mt-6">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center text-white font-bold">أ</div>
              <div><div className="font-medium text-sm">أحمد - وكالة تقنية</div><div className="text-xs text-zinc-500">Pro Plan - 6 أشهر</div></div>
            </div>
          </div>
          <div className="bg-white border rounded-3xl p-8">
            <div className="flex gap-1 mb-4">{[1,2,3,4,5].map(i=><Star key={i} size={16} className="fill-amber-400 text-amber-400"/>)}</div>
            <p className="text-sm leading-relaxed">"Client Portal غيّر علاقتنا مع العملاء. العميل يشوف التقدم بدون ما نسأل. Proposal تلقائي في 2 دقيقة."</p>
            <div className="flex items-center gap-3 mt-6">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white font-bold">س</div>
              <div><div className="font-medium text-sm">سارة - وكالة تسويق</div><div className="text-xs text-zinc-500">Starter Plan - 3 أشهر</div></div>
            </div>
          </div>
          <div className="bg-white border rounded-3xl p-8">
            <div className="flex gap-1 mb-4">{[1,2,3,4,5].map(i=><Star key={i} size={16} className="fill-amber-400 text-amber-400"/>)}</div>
            <p className="text-sm leading-relaxed">"كنا نستخدم ChatGPT عشوائياً. الآن عندنا نظام: 68 وكيل، 292 مهارة، ذاكرة، وتتبع تكلفة. الربحية 95%."</p>
            <div className="flex items-center gap-3 mt-6">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-600 to-emerald-600 flex items-center justify-center text-white font-bold">م</div>
              <div><div className="font-medium text-sm">محمد - freelancer</div><div className="text-xs text-zinc-500">Free → Pro - سنة</div></div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-zinc-900 text-white">
        <div className="max-w-4xl mx-auto px-6 py-20 text-center">
          <h2 className="text-4xl font-bold">جاهز لبناء وكالتك الذكية؟</h2>
          <p className="text-zinc-400 mt-4">انضم لـ 100+ وكالة تستخدم AI Agency OS. ابدأ مجاناً في 30 ثانية.</p>
          <div className="flex gap-4 justify-center mt-10">
            <button onClick={()=>setActiveView('chat')} className="px-8 py-4 bg-white text-zinc-900 rounded-2xl font-bold flex items-center gap-2">
              ابدأ مجاناً <ArrowRight size={18}/>
            </button>
            <button onClick={()=>setActiveView('dashboard')} className="px-8 py-4 bg-zinc-800 border border-zinc-700 text-white rounded-2xl">
              عرض التوثيق
            </button>
          </div>
          <div className="text-xs text-zinc-500 mt-6">مفتوح المصدر جزئياً • 68 وكيل • 292 مهارة • 88% هامش • &lt;10د onboarding</div>
        </div>
      </div>
    </div>
  );
}
