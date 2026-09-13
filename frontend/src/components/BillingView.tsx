import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function BillingView() {
  const [tiers, setTiers] = useState<any>({});
  const [subscription, setSubscription] = useState<any>(null);
  const [usage, setUsage] = useState<any>(null);

  useEffect(() => {
    api.get('/billing/tiers').then(r=>setTiers(r.data.tiers||{})).catch(()=>{});
    api.get('/billing/subscription/default-user').then(r=>setSubscription(r.data)).catch(()=>{});
    api.get('/billing/usage/default-user').then(r=>setUsage(r.data)).catch(()=>{});
  }, []);

  const subscribe = async (tierId: string) => {
    try {
      const res = await api.post('/billing/subscribe', { tier_id: tierId, user_id: 'default-user', email: 'demo@ai-agency.os' });
      setSubscription(res.data.subscription);
      alert(res.data.message);
    } catch {}
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">💳 الفوترة والاشتراكات - SaaS Model</h1>
        <p className="text-sm text-zinc-600 mb-8">Track B2 - نموذج تسعير للوكالات: Free, Starter $49, Pro $199, Enterprise $999</p>

        {subscription && (
          <div className="bg-white rounded-2xl border p-6 mb-8">
            <h3 className="font-semibold mb-4">اشتراكك الحالي</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="p-4 bg-violet-50 border border-violet-200 rounded-xl">
                <div className="text-sm text-violet-700">الخطة</div>
                <div className="text-xl font-bold text-violet-900">{subscription.tier?.name || subscription.tier_id}</div>
                <div className="text-xs text-violet-600">${subscription.tier?.price || 0}/شهر</div>
              </div>
              <div className="p-4 bg-zinc-50 rounded-xl">
                <div className="text-sm text-zinc-500">الاستهلاك</div>
                <div className="text-lg font-bold">{subscription.usage?.tasks_this_month || 0} مهمة</div>
                <div className="text-xs text-zinc-400">{subscription.usage?.tokens_used || 0} tokens</div>
              </div>
              <div className="p-4 bg-zinc-50 rounded-xl">
                <div className="text-sm text-zinc-500">التكلفة</div>
                <div className="text-lg font-bold">${(subscription.usage?.cost || 0).toFixed(4)}</div>
                <div className="text-xs text-zinc-400">LLM فقط</div>
              </div>
              <div className="p-4 bg-green-50 border border-green-200 rounded-xl">
                <div className="text-sm text-green-700">الربحية</div>
                <div className="text-lg font-bold text-green-900">${(subscription.profitability?.gross_profit || 0).toFixed(2)}</div>
                <div className="text-xs text-green-600">{subscription.profitability?.margin || '0%'} هامش</div>
              </div>
            </div>

            {usage && (
              <div className="mt-6">
                <div className="text-sm font-medium mb-2">استخدام Tokens: {usage.percent_used?.tokens?.toFixed(1) || 0}%</div>
                <div className="w-full h-2 bg-zinc-100 rounded-full overflow-hidden">
                  <div className="h-full bg-violet-600 rounded-full" style={{ width: `${Math.min(100, usage.percent_used?.tokens || 0)}%` }} />
                </div>
                <div className="flex justify-between text-xs text-zinc-500 mt-1">
                  <span>{usage.usage?.prompt_tokens + usage.usage?.completion_tokens} مستخدم</span>
                  <span>{usage.limits?.llm_tokens} الحد</span>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.entries(tiers).map(([id, tier]: any) => (
            <div key={id} className={`bg-white rounded-2xl border p-6 ${tier.popular?'ring-2 ring-violet-500 shadow-lg':''} relative`}>
              {tier.popular && <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-violet-600 text-white text-xs px-3 py-1 rounded-full">الأكثر شيوعاً</div>}
              <h3 className="font-bold text-lg">{tier.name}</h3>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-bold">${tier.price}</span>
                <span className="text-sm text-zinc-500">/شهر</span>
              </div>
              
              <div className="mt-6 space-y-3 text-sm">
                <div className="flex justify-between"><span className="text-zinc-500">الوكلاء</span><span className="font-medium">{tier.features.agents}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">المشاريع</span><span className="font-medium">{tier.features.projects}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">مهام/شهر</span><span className="font-medium">{tier.features.tasks_per_month}</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">Tokens</span><span className="font-medium">{(tier.features.llm_tokens/1000000).toFixed(1)}M</span></div>
                <div className="flex justify-between"><span className="text-zinc-500">أعضاء</span><span className="font-medium">{tier.features.members}</span></div>
                {tier.features.dedicated_support && <div className="text-xs bg-violet-50 text-violet-700 px-2 py-1 rounded-full">دعم مخصص</div>}
                {tier.features.custom_agents && <div className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-full">وكلاء مخصصين</div>}
              </div>

              <button onClick={()=>subscribe(id)} className={`mt-6 w-full py-2.5 rounded-xl font-medium text-sm ${tier.popular?'bg-violet-600 text-white hover:bg-violet-700':'bg-zinc-900 text-white hover:bg-zinc-800'}`}>
                {id==='free'?'ابدأ مجاناً':'اشترك الآن'}
              </button>

              <div className="mt-3 text-xs text-zinc-400 text-center">Stripe: {tier.stripe_price_id}</div>
            </div>
          ))}
        </div>

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-3">📈 كيف تحسب الربحية</h3>
            <div className="text-sm text-zinc-600 space-y-2">
              <div>• <strong>الإيراد:</strong> سعر الاشتراك (مثلاً $199 Pro)</div>
              <div>• <strong>التكلفة:</strong> LLM tokens + استضافة + دعم</div>
              <div>• <strong>الربح الإجمالي:</strong> إيراد - تكلفة LLM</div>
              <div>• <strong>مثال:</strong> عميل Pro يستخدم 2M tokens بـ $10 تكلفة → ربح $189 (95% هامش)</div>
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-xl text-xs">
                الوكلاء المحلية (Ollama) مجانية 100% → هامش أعلى، لكن جودة أقل. استخدم مزيج: مهام بسيطة → Ollama، معقدة → GPT-4o
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl border p-6">
            <h3 className="font-semibold mb-3">🔄 Stripe Webhook (Mock)</h3>
            <div className="text-sm text-zinc-600 space-y-2">
              <div>في الإنتاج:</div>
              <div className="font-mono text-xs bg-zinc-900 text-zinc-100 p-3 rounded-xl">
                POST /api/billing/webhook/stripe<br/>
                Events:<br/>
                - checkout.session.completed → تفعيل<br/>
                - invoice.payment_succeeded → تمديد<br/>
                - invoice.payment_failed → past_due<br/>
                - customer.subscription.deleted → downgrade free
              </div>
              <div className="text-xs text-zinc-500">الآن mock فقط، لكن البنية جاهزة لـ Stripe حقيقي</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
