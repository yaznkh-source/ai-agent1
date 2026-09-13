# خطة تنفيذ شاملة A-D - AI Agency OS

## الرؤية: من MVP إلى SaaS وكالة ذكاء اصطناعي متكاملة

### الوضع الحالي (تم إنجازه)
- ✅ 20 وكيل، 15 مهارة، 9 أدوات، 6 Functions، 4 Pipelines
- ✅ Backend FastAPI + Frontend React يعملان
- ✅ Demo Mode بدون API keys
- ✅ Preview-ready

---

## المسار A: تشغيل Freelancer (أسبوع 1) - P0

### A1: تفعيل LLM حقيقي - Multi-Provider مثل Open WebUI
- [ ] تحسين `llm.py` لدعم Anthropic حقيقي + OpenAI streaming
- [ ] إضافة Ollama auto-pull + model management UI
- [ ] إضافة Cost Tracking: حساب تكلفة كل محادثة
- [ ] إضافة Model Fallback: إذا فشل GPT-4o → ينتقل لـ llama3.1

### A2: ذاكرة حقيقية RAG
- [ ] تفعيل ChromaDB + sentence-transformers embeddings
- [ ] تحويل MemoryManager من keyword إلى vector search
- [ ] إضافة Knowledge Collections UI (مثل Open WebUI)
- [ ] رفع ملفات PDF/DOCX واستخراج نص + embedding

### A3: Client Portal MVP
- [ ] صفحة `/client/:id` للعميل: يشوف مشاريعه فقط
- [ ] إخفاء الوكلاء الداخليين، يظهر فقط النتائج
- [ ] رفع ملفات + تعليقات

**التنفيذ الآن:** نبدأ بـ A1 + A2

---

## المسار B: SaaS لوكالات أخرى (أسبوع 2) - P1

### B1: Auth + Multi-tenancy
- [ ] JWT auth + bcrypt + refresh tokens
- [ ] أدوار: super_admin, agency_owner, agency_member, client
- [ ] كل agency لها clients/projects منفصلة (tenant_id)
- [ ] Middleware يفحص tenant

### B2: Billing + Usage
- [ ] نموذج Subscription: Free, Starter ($49), Pro ($199), Enterprise
- [ ] تتبع: LLM tokens, agent runs, storage
- [ ] Stripe integration (test mode)
- [ ] لوحة تحكم الربحية: تكلفة vs سعر بيع

### B3: Eval Harness (من ECC)
- [ ] نظام تقييم أداء الوكلاء: pass@k, latency, cost, success_rate
- [ ] كل task يسجل: agent_used, time, tokens, verification_gate (passed/failed)
- [ ] Dashboard: أفضل وكيل لكل نوع مهمة
- [ ] A/B testing للـ prompts

**التنفيذ الآن:** B1 أساسي

---

## المسار C: أداة داخلية للفريق (أسبوع 2-3) - P1

### C1: Verification Loop حقيقي
- [ ] بدل mock، يشغل أوامر حقيقية: `npm run build`, `pytest`, `tsc`
- [ ] Sandbox: يشغل في Docker container معزول
- [ ] يعرض logs حقيقية + artifacts
- [ ] Gate يمنع الدمج إذا فشل

### C2: GitHub Integration (مثل ECC Tools App)
- [ ] Webhook: عند push/PR → يشغل verification + review agent
- [ ] تعليق تلقائي على PR: ملخص + مشاكل أمان
- [ ] `/agency review` command في التعليقات

### C3: تكاملات الفريق
- [ ] Slack Bot: `/agency task أنشئ API للعملاء` → يشغل workflow
- [ ] Discord Bot: نفس الفكرة
- [ ] n8n Pipeline: ربط مع 300+ خدمة

**التنفيذ الآن:** C1 + C2 webhook

---

## المسار D: تطوير الواجهة والذكاء (أسبوع 3-4) - P2

### D1: توسع الوكلاء إلى 68 (ECC)
- [ ] إضافة 48 وكيل جديد:
  - Language: typescript-reviewer, java-reviewer, kotlin-reviewer, python-reviewer, go-reviewer
  - Build: pytorch-build-resolver, java-build-resolver, kotlin-build-resolver
  - Specialized: seo-specialist, ads-manager, legal-reviewer, finance-analyst
  - Content: video-editor, podcast-producer, newsletter-writer

### D2: توسع المهارات إلى 100+ (ECC 292)
- [ ] إضافة 35 مهارة جديدة:
  - Frameworks: laravel-patterns, django-patterns, rails-patterns
  - AI: rag-patterns, prompt-engineering, eval-harness
  - Ops: kubernetes-patterns, terraform-patterns

### D3: UI/UX عربي 100% + Pipeline Builder
- [ ] تحويل كل النصوص لعربية مع إنجليزية ثانوية
- [ ] Pipeline Builder بـ drag-and-drop (React Flow)
- [ ] Dark/Light mode + ثيمات
- [ ] Mobile responsive كامل

### D4: ذكاء متقدم
- [ ] Agent Router ذكي: يحلل المهمة ويختار أفضل وكيل تلقائياً (مثل ECC agent-sort)
- [ ] Skill Recommender: يقترح مهارات بناءً على المهمة
- [ ] Auto-Evolve: Instincts تتحول لمهارات تلقائياً بدون /evolve يدوي

---

## خطة التنفيذ الفوري (هذه الجلسة)

### المرحلة 1 (الآن - 30 دقيقة):
1. ✅ إنشاء ROADMAP
2. 🔄 **Auth System**: JWT + roles + middleware
3. 🔄 **Real RAG**: ChromaDB + embeddings + knowledge collections
4. 🔄 **Cost Tracking**: تتبع تكلفة LLM
5. 🔄 **More Agents**: إضافة 15 وكيل جديد (يصبح 35)
6. 🔄 **More Skills**: إضافة 15 مهارة جديدة (يصبح 30)

### المرحلة 2 (30-60 دقيقة):
7. 🔄 **Client Portal**: صفحة عميل منفصلة
8. 🔄 **Billing Models**: نماذج اشتراك + usage tracking
9. 🔄 **Real Verification**: تشغيل أوامر حقيقية + sandbox
10. 🔄 **GitHub Webhook**: endpoint + PR review
11. 🔄 **Eval Harness**: تسجيل أداء + dashboard

### المرحلة 3 (60-90 دقيقة):
12. 🔄 **Integrations**: Slack, Discord, n8n stubs + docs
13. 🔄 **Pipeline Builder UI**: React Flow drag-and-drop
14. 🔄 **Arabic 100%**: تحسين كل الواجهات
15. 🔄 **Agent Router**: اختيار وكيل ذكي

---

## المقاييس للنجاح

- **A**: Freelancer يستطيع onboarding عميل في < 10 دقائق + proposal تلقائي
- **B**: Agency تستطيع بيع اشتراكات + تتبع ربحية + 3 tenants منفصلة
- **C**: فريق يستطيع ربط GitHub + Slack + verification حقيقي يمنع دمج كود فاشل
- **D**: 35+ وكيل، 30+ مهارة، Pipeline Builder يعمل، واجهة عربية 100%

---

## التالي: التنفيذ
نبدأ الآن بالمرحلة 1 فوراً.
