# AI Agency OS - نظام وكالة ذكاء اصطناعي متكامل

> مستوحى من **ECC (Everything Claude Code)** و **Open WebUI** - يجمع أفضل ما في العالمين لبناء وكالة ذكاء اصطناعي احترافية

![Version](https://img.shields.io/badge/version-1.0.0-violet)
![Agents](https://img.shields.io/badge/agents-20-blue)
![Skills](https://img.shields.io/badge/skills-15-amber)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 الفكرة الأساسية

### من ECC:
- **68 وكيل متخصص** → نفذنا 20 وكيل أساسي قابل للتوسع إلى 68
- **292 مهارة** → 15 مهارة أساسية قابلة للتوسع، تحمل عند الحاجة فقط (context optimization)
- **Hooks**: SessionStart, SessionEnd, PreToolUse, PostToolUse - تعمل خارج سياق النموذج لفرض تحقق حتمي
- **الذاكرة المستمرة**: ملخصات الجلسات + ذاكرة طويلة المدى
- **التعلم المستمر (Instincts)**: يستخرج الأنماط من الجلسات إلى instincts قابلة لإعادة الاستخدام مع confidence scoring، ثم يجمعها إلى مهارات عبر `/evolve`
- **حلقة التحقق**: build, test, lint, typecheck, security - بوابة حتمية
- **AgentShield**: فحص أمان لـ prompts, hooks, MCP, secrets, permissions
- **سير العمل**: `plan → test → implement → review → verify → remember → improve`

### من Open WebUI:
- **واجهة محادثة سهلة** مثل ChatGPT مع دعم Ollama و OpenAI
- **دعم متعدد النماذج**: OpenAI, Anthropic, Ollama, واجهات متوافقة مع OpenAI
- **Tools**: توسيع قدرات LLM (طقس، بحث، تنفيذ كود، بيانات حية)
- **Functions**:
  - **Pipe**: إضافة نموذج أو وكيل مخصص (يظهر كموديل قابل للاختيار)
  - **Filter**: اعتراض وتعديل الرسائل (middleware)
  - **Action**: إضافة أزرار تفاعلية للرسائل
  - **Event**: تشغيل منطق مخصص استجابة لأحداث النظام (170+ حدث)
- **Pipelines**: إطار عمل OpenAI API متوافق لفصل المعالجة الثقيلة عن الواجهة الرئيسية
- **مجموعات المعرفة / RAG**: بحث في المعرفة الداخلية
- **مساحة العمل**: Prompts, Models, Knowledge

### الجديد - AI Agency OS:
- **إدارة وكالة كاملة**: عملاء، مشاريع، مهام
- **أتمتة Onboarding العملاء** عبر Pipelines
- **لوحة تحكم** مع إحصائيات ومعدل إنجاز
- **تنسيق متعدد الوكلاء** مع سياق معزول للمراجع (fresh-context reviewer - فكرة ECC الرئيسية)
- **نظام مهام** مع إسناد وكلاء ومهارات

---

## 🏗️ البنية المعمارية

```
ai-agency-os/
├── backend/                 # FastAPI - مستوحى من Open WebUI backend
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py    # إعدادات مثل Open WebUI + ECC selective install
│   │   │   ├── database.py  # SQLite + SQLAlchemy - persistence مثل Open WebUI
│   │   │   ├── llm.py       # تجريد مزودي LLM (OpenAI, Ollama, Anthropic)
│   │   │   └── security.py  # AgentShield - فحص أمان مثل ECC
│   │   ├── agents/
│   │   │   ├── definitions.py # 20 وكيل متخصص (قابل للتوسع إلى 68 مثل ECC)
│   │   │   └── orchestrator.py # تنسيق plan→test→implement→review→verify
│   │   ├── skills/
│   │   │   ├── manager.py   # إدارة 15 مهارة (ECC: 292 مهارة)
│   │   │   └── definitions/ # ملفات SKILL.md مثل ECC .agents/skills/
│   │   ├── memory/
│   │   │   ├── manager.py   # ذاكرة مستمرة + سقف أحرف
│   │   │   └── instincts.py # تعلم مستمر v2 - confidence scoring
│   │   ├── hooks/
│   │   │   └── manager.py   # SessionStart/End, PreToolUse, PostToolUse
│   │   ├── tools/
│   │   │   └── registry.py  # 9 أدوات مع OpenAI function calling
│   │   ├── functions/
│   │   │   └── manager.py   # Pipe, Filter, Action, Event (Open WebUI)
│   │   ├── pipelines/
│   │   │   └── engine.py    # محرك Pipelines متوافق مع OpenAI API
│   │   ├── verification/
│   │   │   └── loop.py      # حلقة تحقق: build, test, lint, typecheck, security
│   │   ├── routers/         # 8 routers للـ API
│   │   │   ├── chat.py      # محادثات متوافقة مع OpenAI + وكلاء
│   │   │   ├── agents.py    # إدارة الوكلاء + workflows
│   │   │   ├── skills.py    # مكتبة المهارات
│   │   │   ├── memory.py    # ذاكرة + instincts
│   │   │   ├── tools.py     # أدوات
│   │   │   ├── functions.py # Functions
│   │   │   ├── pipelines.py # Pipelines
│   │   │   └── agency.py    # عملاء، مشاريع، مهام، dashboard، أمان
│   │   └── main.py          # FastAPI app مع CORS * للـ preview
│   └── requirements.txt
├── frontend/                # React + Vite - مستوحى من Open WebUI frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx      # شريط جانبي مع محادثات وتنقل
│   │   │   ├── ChatView.tsx     # واجهة محادثة + اختيار وكيل
│   │   │   ├── AgentsView.tsx   # 20 وكيل مع تشغيل مباشر
│   │   │   ├── SkillsView.tsx   # مكتبة مهارات مع بحث
│   │   │   ├── PipelinesView.tsx # تنفيذ pipelines
│   │   │   ├── ToolsView.tsx    # Tools, Memory, Security, Functions
│   │   │   ├── AgencyView.tsx   # إدارة وكالة
│   │   │   └── Dashboard.tsx    # نظرة عامة معمارية
│   │   ├── stores/chat.ts       # Zustand state
│   │   ├── lib/api.ts           # Axios + API helpers
│   │   └── App.tsx
│   ├── vite.config.ts           # host 0.0.0.0 + proxy + HMR للـ preview
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## 🚀 التشغيل السريع

### 1. المتطلبات
- Python 3.11+
- Node 20+
- (اختياري) Ollama للنماذج المحلية

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env
# عدّل .env وأضف OPENAI_API_KEY أو اتركه فارغاً للـ demo mode

# تشغيل
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# أو
python -m app.main
```

Backend سيعمل على: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/api/health
- Config: http://localhost:8000/api/config

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend سيعمل على: http://localhost:5173
- مع proxy للـ backend على /api

### 4. Docker (موصى به للإنتاج)

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Ollama: http://localhost:11434
- Chroma: http://localhost:8001

---

## 🎯 الميزات الرئيسية

### 🤖 الوكلاء (20 وكيل، قابل للتوسع إلى 68 مثل ECC)

| الفئة | الوكلاء | الوصف |
|-------|---------|--------|
| **Planning** | planner, architect, api-designer | تخطيط استراتيجي، تصميم معماري، تصميم APIs |
| **Development** | backend-dev, frontend-dev, fullstack-dev, mobile-dev | تطوير خلفي، أمامي، متكامل، جوال |
| **Review** | reviewer, security-reviewer, performance-reviewer, tdd-guardian, qa-engineer | مراجعة بسياق جديد، أمان، أداء، TDD، جودة |
| **Research** | researcher | بحث عميق متعدد المصادر مع إسناد |
| **Operations** | devops, support-agent, sales-agent | DevOps, دعم، مبيعات |
| **Data** | data-engineer | هندسة بيانات |
| **AI** | ml-engineer | هندسة تعلم آلة |
| **Content** | content-creator, docs-writer | محتوى، توثيق |

**فكرة ECC الرئيسية**: المراجع يعمل بسياق جديد (fresh-context) - نفس السياق يكتب ويراجع = نقاط عمياء

### ⚡ المهارات (15 مهارة، قابلة للتوسع إلى 292)

- `tdd-workflow`: RED → GREEN → REFACTOR مع 80%+ تغطية
- `verification-loop`: build, test, lint, typecheck, security
- `deep-research`: بحث متعدد المصادر مع تركيب وإسناد
- `backend-patterns`: API، قاعدة بيانات، cache، أمان
- `frontend-patterns`: React/Next.js، أداء، وصول
- `security-review`: OWASP، حقن، أسرار
- `api-design`: REST تصميم، إصدارات، توثيق
- `e2e-testing`: Playwright E2E
- `product-capability`: تحويل أهداف منتج إلى خريطة قدرات
- `documentation-lookup`: بحث توثيق محدث عبر Context7
- `strategic-compact`: إدارة السياق
- `brand-voice`: ملفات صوت العلامة من محتوى حقيقي
- `content-engine`: محتوى اجتماعي أصلي للمنصة
- `market-research`: بحث سوق مع إسناد
- `mcp-server-patterns`: بناء خوادم MCP

**فكرة ECC**: المهارات تحافظ على تركيز السياق - تحمل عند الحاجة فقط، ليس دائماً

### 🔧 الأدوات (9 أدوات)

- `web_search`: بحث ويب
- `code_write/read`: كتابة/قراءة كود
- `test_runner`: تشغيل اختبارات
- `security_scan`: فحص أمان عبر AgentShield
- `diagram_generator`: توليد مخططات mermaid
- `exa_search`: بحث عصبي (ECC)
- `knowledge_search`: بحث قاعدة معرفة (RAG)
- `proposal_generator`: توليد مقترحات عملاء

### 🔌 Functions (Pipe, Filter, Action, Event) - من Open WebUI

- **Pipe**: نموذج أو وكيل مخصص يظهر كموديل قابل للاختيار
  - `rag-pipe`: RAG مخصص
  - `agent-pipe`: الوكلاء كموديلات
- **Filter**: اعتراض وتعديل الرسائل (middleware)
  - `translation-filter`: ترجمة تلقائية
  - `rate-limit-filter`: تحديد معدل
- **Action**: أزرار تفاعلية
  - `summarize-action`: تلخيص رسائل
- **Event**: منطق استجابة لأحداث (170+ حدث)
  - `analytics-event`: تسجيل تحليلات

### 🔄 Pipelines (4 مسارات جاهزة)

- `research-to-code`: بحث → خطة → كود → مراجعة (سير عمل ECC كـ pipeline)
- `content-pipeline`: صوت علامة → محتوى → SEO
- `security-pipeline`: فحص → إصلاح → تحقق
- `agency-onboarding`: بحث عميل → مقترح → خطة → إعداد

**فكرة Open WebUI**: Pipelines كإطار عمل OpenAI API متوافق لفصل المعالجة الثقيلة

### 🧠 الذاكرة والـ Instincts

- **ذاكرة الجلسة**: ملخصات مقطرة من النصوص، ليس نص كامل
- **ذاكرة طويلة**: حقائق، تفضيلات، سياق مشروع
- **Instincts**: أنماط مستخرجة مع confidence scoring، تتجمع إلى مهارات عبر `/evolve`
- **Hooks**: SessionStart يحمل الذاكرة، SessionEnd يحفظ ملخص

### 🛡️ AgentShield - فحص الأمان

يفحص:
- تسريب أسرار (API keys، tokens، private keys)
- حقن prompts (تجاوز تعليمات، تجاوز نظام)
- أوامر خطيرة (rm -rf، fork bomb، curl|sh)
- صلاحيات مفرطة

### 🏢 إدارة الوكالة

- **عملاء**: إضافة، عرض، حذف
- **مشاريع**: مرتبطة بعملاء، مع workflows ووكلاء
- **مهام**: todo, in_progress, review, done مع أولوية وإسناد
- **لوحة تحكم**: إحصائيات، معدل إنجاز، أخير مشاريع/مهام
- **تحقق**: تشغيل حلقة تحقق لمهمة
- **أمان**: فحص شامل للنظام

---

## 📚 API Endpoints

### Chats (OpenAI-compatible)
- `GET /api/chats/` - قائمة محادثات
- `POST /api/chats/` - إنشاء محادثة
- `GET /api/chats/{id}` - تفاصيل محادثة
- `POST /api/chats/completions` - إكمال محادثة (متوافق مع OpenAI)
- `GET /api/chats/models/list` - قائمة نماذج

### Agents
- `GET /api/agents/` - قائمة وكلاء (مع ?category=)
- `GET /api/agents/{id}` - تفاصيل وكيل
- `POST /api/agents/run` - تشغيل وكيل واحد
- `POST /api/agents/workflow/run` - تشغيل سير عمل متعدد وكلاء
- `GET /api/agents/workflows/list` - قائمة workflows جاهزة

### Skills
- `GET /api/skills/` - قائمة مهارات
- `GET /api/skills/{id}` - تفاصيل مهارة
- `GET /api/skills/search/{query}` - بحث مهارات

### Memory
- `GET /api/memory/` - قائمة ذاكرة
- `POST /api/memory/` - حفظ ذاكرة
- `GET /api/memory/search?q=` - بحث ذاكرة
- `GET /api/memory/instincts/` - قائمة instincts
- `POST /api/memory/instincts/evolve` - تطوير instincts إلى مهارة

### Tools
- `GET /api/tools/` - قائمة أدوات
- `POST /api/tools/execute` - تنفيذ أداة

### Functions
- `GET /api/functions/` - قائمة functions
- `POST /api/functions/` - إنشاء function

### Pipelines
- `GET /api/pipelines/` - قائمة pipelines
- `POST /api/pipelines/` - إنشاء pipeline
- `POST /api/pipelines/{id}/execute` - تنفيذ pipeline
- `GET /api/pipelines/history/list` - سجل تنفيذ

### Agency
- `GET /api/agency/dashboard` - لوحة تحكم
- `GET /api/agency/clients` - عملاء
- `POST /api/agency/clients` - إنشاء عميل
- `GET /api/agency/projects` - مشاريع
- `POST /api/agency/projects` - إنشاء مشروع
- `GET /api/agency/tasks` - مهام
- `POST /api/agency/tasks` - إنشاء مهمة
- `GET /api/agency/security/audit` - فحص أمان شامل
- `POST /api/agency/verify` - تشغيل حلقة تحقق
- `GET /api/agency/hooks` - قائمة hooks
- `GET /api/agency/hooks/logs` - سجل أحداث hooks

---

## 🔧 الإعداد

### .env

```bash
OPENAI_API_KEY=sk-... # أو اتركه فارغاً للـ demo mode
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=gpt-4o-mini
```

**Demo Mode**: إذا لم يتم إعداد API key، النظام يعمل في وضع demo مع ردود وهمية توضح ما سيفعله مع LLM حقيقي

---

## 🌍 دعم Preview (مهم لـ Arena)

النظام مصمم ليعمل في بيئة preview:

**Backend**:
- `host: 0.0.0.0` وليس 127.0.0.1
- `CORS_ORIGINS: ["*"]` للسماح بكل origins
- يعمل على منفذ 8000

**Frontend**:
- `vite --host 0.0.0.0 --port 5173`
- Proxy لـ /api إلى backend
- HMR مع clientPort 443 للـ preview

---

## 📖 أمثلة استخدام

### 1. تشغيل وكيل واحد

```bash
curl -X POST http://localhost:8000/api/agents/run \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "planner",
    "task": "خطط لمشروع متجر إلكتروني بسيط",
    "context": {"user_id": "default-user"}
  }'
```

### 2. تشغيل سير عمل كامل (ECC)

```bash
curl -X POST http://localhost:8000/api/agents/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "full_feature",
    "task": "أنشئ نظام إدارة مهام بسيط مع API و UI",
    "context": {"user_id": "default-user"}
  }'
```

### 3. محادثة متوافقة مع OpenAI

```bash
curl -X POST http://localhost:8000/api/chats/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "اشرح لي ECC"}],
    "agent_id": "researcher"
  }'
```

### 4. تنفيذ Pipeline

```bash
curl -X POST http://localhost:8000/api/pipelines/research-to-code/execute \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "task": "نظام حجز مواعيد",
      "client_name": "عيادة الأسنان"
    }
  }'
```

### 5. إنشاء عميل ومشروع (وكالة)

```bash
# عميل
curl -X POST http://localhost:8000/api/agency/clients \
  -H "Content-Type: application/json" \
  -d '{"name": "شركة التقنية", "company": "Tech Co", "email": "info@tech.co"}'

# مشروع
curl -X POST http://localhost:8000/api/agency/projects \
  -H "Content-Type: application/json" \
  -d '{"client_id": "<id>", "name": "متجر إلكتروني", "description": "متجر بسيط"}'

# مهمة
curl -X POST http://localhost:8000/api/agency/tasks \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<id>", "title": "تصميم قاعدة البيانات", "assigned_agent": "architect"}'
```

---

## 🤝 المساهمة

النظام قابل للتوسع:

1. **إضافة وكيل**: عدّل `backend/app/agents/definitions.py`
2. **إضافة مهارة**: أنشئ ملف `.md` في `backend/app/skills/definitions/`
3. **إضافة أداة**: عدّل `backend/app/tools/registry.py`
4. **إضافة pipeline**: عبر API أو `backend/app/pipelines/engine.py`

---

## 📄 الترخيص

MIT

---

## 🙏 شكر

- [ECC](https://github.com/affaan-m/ECC) - نظام تحسين أداء حاضنة الوكلاء (257k ⭐)
- [Open WebUI](https://github.com/open-webui/open-webui) - واجهة ذكاء اصطناعي سهلة الاستخدام (152k ⭐)

بُني بـ ❤️ كـ AI Agency OS متكامل

---

## 📞 الدعم

- Issues: GitHub Issues
- Docs: `/api/docs` (Swagger)
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
