# خطة المسار A — إصلاح حرج للوصول 70/100 Beta Ready (2-3 أسابيع) — $0 تكلفة

## الهدف
من 35/100 Development Ready → 70/100 Beta Ready
تطلق Beta 10 مستخدمين مجاناً بدون ادعاءات كاذبة، أمن محسّن، عزل مستأجرين، مصداقية.

## المشاكل الحرجة من التدقيق (8 نقاط)

1. **تكاملات Real مزيفة**: Stripe/HubSpot/Slack/Monitoring كلها Mock مع would_do + #mock + لا SDK
2. **ثغرات أمنية**: admin/admin123 hardcoded، secret افتراضي، توقيع مزيف verified=True، لا rate limiting، WS بدون auth، لا tenant isolation
3. **لا نشر Prod موثق**: docker prod config/up لم يُختبر، K8s لا HPA، secrets ضعيفة، لا backup/restore
4. **لا دليل توسع**: Scale 1000 user بدون load test
5. **أرقام بزنس Hardcoded**: 199/5000/77.1% في monitoring.py
6. **جودة اختبارات منخفضة**: 1 ملف 7 دوال فقط تحميل
7. **فجوة توثيق/واقع**: README.md v16 قديم 20/134 بينما الواقع 24/162، Views 22 vs 24
8. **SOC2/GDPR غير معتمد**: فقط oriented

## المهام — 6 أيام عمل — $0

### اليوم 1 — أمن حرج (4 مهام)

#### Task A1: إزالة كلمات مرور Demo الصلبة من auth.py
- **ملف**: backend/app/core/auth.py
- **مشكلة**: `admin/admin123`, `owner/owner123` hardcoded — إذا نُشر Prod، أي شخص يدخل
- **حل**:
  - في `create_default_users()`: تحقق `if settings.ENV == "production"` → لا تنشئ demo accounts، أو أنشئ فقط إذا `ALLOW_DEMO_ACCOUNTS=true`
  - أضف env var `ADMIN_PASSWORD` — إذا موجود، أنشئ admin به، إذا لا، لا تنشئ
  - في dev، أبق demo accounts لكن مع تحذير log `⚠️ Demo accounts enabled - only for dev`
- **دليل**: `grep -n "admin123" auth.py` → يجب أن يختفي في prod
- **وقت**: 2 ساعة

#### Task A2: إصلاح SECRET_KEY الافتراضي
- **ملف**: backend/app/core/config.py + main.py
- **مشكلة**: `SECRET_KEY = "ai-agency-os-secret-key-change-in-production"` + `JWT_SECRET=super-secret-jwt-key-change-in-prod` في prod compose — JWT يمكن تزويره
- **حل**:
  - في `config.py`: `SECRET_KEY: str = os.getenv("JWT_SECRET", "")` — إذا فارغ و `ENV=production` → raise Exception `JWT_SECRET must be set in production`
  - في `docker-compose.prod.yml`: احذف `:-aiagency123` و `:-super-secret...` — اجعلها `${POSTGRES_PASSWORD:?Must set POSTGRES_PASSWORD}` و `${JWT_SECRET:?Must set JWT_SECRET}`
  - في `.env.prod.example`: وضّح أن هذه يجب تغييرها
- **دليل**: `docker compose -f docker-compose.prod.yml config` يجب أن يفشل إذا لم تضبط secrets
- **وقت**: 1 ساعة

#### Task A3: إصلاح توقيع Stripe/Slack المزيف
- **ملف**: backend/app/routers/billing_real.py + slack_real.py
- **مشكلة**: `verified = True # In production, verify real` عندما test secret — يسمح بتزوير webhook
- **حل**:
  - في `billing_real.py`: إذا `ENV=production` و `STRIPE_WEBHOOK_SECRET.startswith("whsec_test")` → raise HTTPException 400 `Test webhook secret not allowed in production`
  - إذا `ENV=production` و `stripe_signature` مفقود → raise 400 `Missing Stripe-Signature`
  - إذا `ENV=production` و `STRIPE_WEBHOOK_SECRET` يبدأ بـ `whsec_test` → لا تقبل، حتى لو verified=True سابقاً
  - نفس الشيء لـ Slack: إذا `ENV=production` و `SLACK_SIGNING_SECRET.startswith("test_")` → raise 400
  - أضف تعليق واضح: `# SECURITY: In production, real verification required - test secrets rejected`
- **دليل**: `curl POST /api/billing/real/webhook` بدون توقيع في prod → يجب أن يرجع 400
- **وقت**: 2 ساعة

#### Task A4: إضافة Rate Limiting + حماية Brute-Force
- **ملف**: backend/app/main.py + core/config.py
- **مشكلة**: لا يوجد rate limiting — هجوم brute-force على login
- **حل**:
  - `pip install slowapi` — أضف إلى requirements.txt
  - في `main.py`: `from slowapi import Limiter, _rate_limit_exceeded_handler` + `limiter = Limiter(key_func=get_remote_address)` + `app.state.limiter = limiter` + `app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)`
  - على `/api/auth/login`: `@limiter.limit("5/minute")` — 5 محاولات في الدقيقة
  - على `/api/auth/register`: `@limiter.limit("3/minute")`
  - على `/api/billing/real/webhook`: `@limiter.limit("100/minute")`
- **دليل**: `curl` 6 مرات سريعة على login → يجب أن يرجع 429 Too Many Requests في المرة السادسة
- **وقت**: 3 ساعات

### اليوم 2 — تصحيح ادعاءات + مصداقية (3 مهام)

#### Task A5: تصحيح ادعاءات Real → Mock بوضوح
- **ملف**: backend/app/routers/billing_real.py, hubspot_real.py, slack_real.py, monitoring.py
- **مشكلة**: يقول "Stripe Real", "HubSpot Real", "Slack Real" بينما هو Mock — misleading
- **حل**:
  - في كل router `GET /` response: غيّر `"integration": "Stripe Real Webhooks + Billing Real"` إلى `"integration": "Stripe Mock (Real-API-Intended) - No Stripe SDK, fake URL #mock - Code exists, execution mock"`
  - أضف حقل جديد `"reality": "MOCK_WITH_REAL_INTENDED_CODE"` + `"real_implementation_needed": ["pip install stripe", "stripe.checkout.Session.create", "stripe.Webhook.construct_event"]`
  - نفس لـ HubSpot: `"reality": "MOCK - In-memory list 5 contacts, no requests to api.hubapi.com, mock token"`
  - Slack: `"reality": "MOCK - No slack_sdk, verification bypassed for test secret, would_do"`
  - Monitoring: `"reality": "MOCK_WITH_HARDCODED_DATA - agents_executed 120 etc hardcoded, not Prometheus client"`
  - احتفظ بالـ endpoints لكن كن صادقاً
- **دليل**: `curl /api/billing/real/` يجب أن يرجع `reality: MOCK...` بوضوح
- **وقت**: 3 ساعات

#### Task A6: تحديث README.md الرئيسي من v16 إلى v24 واقع
- **ملف**: README.md
- **مشكلة**: README.md لا يزال v16 يقول 20 routers 134 paths بينما الواقع 24/162، Views 22 vs 24
- **حل**:
  - انسخ README_v24.md إلى README.md (مع تعديل badge version إلى v25 Beta Ready 70/100)
  - أو حدّث الأرقام: 24 routers 162 paths, 24 web views + 6 mobile = 30 views (أو 22+6=28 إذا اعتبرت tools/memory/security نفس View)
  - أضف قسم جديد في README: `## ⚠️ Reality Check — 35/100 → 70/100 Beta Ready` مع جدول Claimed vs Verified من التدقيق
  - أضف `## 🔴 Audit` يربط إلى `FINAL_REALITY_AUDIT.md`
- **دليل**: `cat README.md | grep -n "routers\|paths\|views"` يجب أن يطابق `openapi.json` 162
- **وقت**: 2 ساعة

#### Task A7: إصلاح Frontend PWA + Build
- **ملف**: frontend/
- **حل**:
  - `npm run build` يجب أن ينجح — اختبره
  - `npm run lint` — أصلح أي أخطاء
  - تحقق `manifest.json` + `sw.js` موجودة
- **وقت**: 1 ساعة

### اليوم 3 — إصلاح Auth + عزل المستأجرين (3 مهام)

#### Task A8: إصلاح Auth Login يقبل email
- **ملف**: backend/app/routers/auth.py
- **مشكلة**: LoginRequest يطلب `username` فقط، إذا أرسلت `email` يفشل `Field required username` — تجربة التدقيق فشلت
- **حل**:
  - غيّر LoginRequest إلى:
    ```python
    class LoginRequest(BaseModel):
        username: Optional[str] = None
        email: Optional[str] = None
        password: str
        def get_identifier(self):
            return self.username or self.email
    ```
  - في login: `identifier = req.get_identifier()` + `if not identifier: raise 400`
  - `user = db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()`
  - اختبر: `curl POST /api/auth/login {"email":"admin@ai-agency.os","password":"admin123"}` يجب أن ينجح
  - نفس لـ register: اجعل username اختياري، إذا لا يوجد، استخدم email prefix
- **دليل**: `curl` بـ email يجب أن يرجع token
- **وقت**: 2 ساعة

#### Task A9: إضافة عزل المستأجرين (Tenant Isolation)
- **ملف**: backend/app/routers/agency.py + core/database.py
- **مشكلة**: لا يوجد tenant_id أو owner_id في projects/tasks/clients — أي مستخدم يرى كل شيء — Cross-Tenant leak CRITICAL
- **حل**:
  - في `database.py`: أضف جدول `Project` و `Task` و `Client` إذا لا يوجد، أو تحقق من `agency.py` — إذا يستخدم in-memory list، أضف `owner_id` إلى كل project dict
  - في `agency.py`: عند إنشاء مشروع `POST /api/agency/projects`: `project["owner_id"] = current_user.id` + `project["tenant_id"] = current_user.tenant_id or current_user.id`
  - عند جلب مشاريع `GET /api/agency/projects`: فلتر `projects = [p for p in projects if p["owner_id"] == current_user.id or current_user.role in ["super_admin","agency_owner"]]`
  - نفس لـ tasks/clients
  - أضف dependency `get_current_user` إلى كل endpoints agency
- **دليل**: أنشئ user1 + user2، كل واحد ينشئ مشروع، user1 لا يجب أن يرى مشروع user2 → اختبار يدوي
- **وقت**: 4 ساعات

#### Task A10: إضافة WebSocket Auth
- **ملف**: backend/app/routers/realtime.py + core/websocket.py
- **مشكلة**: `/ws/{room}` يأخذ `user_id` كـ query param بدون JWT — أي شخص ينتحل أي مستخدم
- **حل**:
  - في `websocket_endpoint`: أضف `token: str = Query(None)` + تحقق `if token: payload = decode_token(token); user_id = payload["sub"]` وإلا `user_id` من query لكن مع تحذير
  - أو: `await manager.connect` يتحقق من token
  - في `core/websocket.py`: `manager.connect` يتحقق `if user_id` من token
  - أضف في `App.tsx` frontend: عند الاتصال WS، أرسل token
- **دليل**: `ws://localhost:8000/api/realtime/ws/general?user_id=admin` بدون token → يجب أن يرفض أو يضع anonymous، مع token صحيح → يقبل
- **وقت**: 3 ساعات

### اليوم 4 — اختبارات حقيقية + Docker (3 مهام)

#### Task A11: إضافة pytest + اختبارات Integration
- **ملف**: backend/requirements.txt + tests/
- **حل**:
  - أضف `pytest`, `pytest-asyncio`, `httpx` إلى requirements.txt
  - أنشئ `backend/tests/test_integration.py` مع 10 اختبارات:
    - test_create_project_with_owner_isolation
    - test_cross_tenant_cannot_access_other_project
    - test_auth_login_with_email
    - test_auth_login_rate_limit_5_per_minute
    - test_billing_webhook_rejects_without_signature_in_prod
    - test_slack_slash_parses_create_project
    - test_hubspot_contacts_returns_mock_with_reality_field
    - test_monitoring_returns_reality_mock
    - test_websocket_connects
    - test_storage_upload_download_persistence
  - شغّل `python -m pytest tests/ -v` يجب أن ينجح
- **دليل**: `pytest -q` → 10+ tests passing
- **وقت**: 4 ساعات

#### Task A12: اختبار Docker Prod Config
- **ملف**: docker-compose.prod.yml
- **حل**:
  - `docker compose -f docker-compose.prod.yml config` يجب أن ينجح إذا ضبطت `.env.prod` من `.env.prod.example`
  - أصلح أي أخطاء config (مثل `version` deprecated, `deploy.resources` لا يعمل مع compose بدون swarm)
  - اختبر `docker compose -f docker-compose.yml build --no-cache` للـ dev
  - لا تشغل `down -v` الذي يحذف البيانات
- **دليل**: `docker compose config` يطبع config بدون أخطاء
- **وقت**: 2 ساعة

#### Task A13: اختبار K8s Dry-Run
- **ملف**: k8s/deployment.yaml
- **حل**:
  - إذا `kubectl` متاح: `kubectl apply --dry-run=client -f k8s/deployment.yaml` يجب أن ينجح
  - إذا لا: `python -c "import yaml; yaml.safe_load(open('k8s/deployment.yaml'))"` → يجب أن ينجح parsing
  - أصلح secrets: لا تضع `sk-...` placeholder، ضع `valueFrom: secretKeyRef` فقط
  - أضف HPA YAML حقيقي:
    ```yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: ai-agency-backend-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: ai-agency-backend
      minReplicas: 3
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
    ```
- **دليل**: `kubectl apply --dry-run=client` أو `yaml.safe_load` ينجح
- **وقت**: 2 ساعة

### اليوم 5 — توثيق + Frontend + PWA (2 مهام)

#### Task A14: إنشاء docs/BETA_READY_CHECKLIST.md
- **ملف**: docs/BETA_READY_CHECKLIST.md
- **حل**: قائمة 30 بند Beta Ready مع حالة كل بند VERIFIED/PARTIAL/MOCK
- **وقت**: 2 ساعة

#### Task A15: اختبار Frontend Build + PWA
- **حل**: `cd frontend && npm run build` → يجب أن ينجح، `dist/` موجود
- **وقت**: 1 ساعة

### اليوم 6 — مراجعة نهائية + إطلاق Beta

#### Task A16: إعادة تدقيق سريع + تقرير BETA_REALITY_AUDIT.md
- **حل**: شغّل نفس اختبارات التدقيق السابق لكن بعد الإصلاحات، أنشئ `BETA_REALITY_AUDIT.md` مع Scores جديدة متوقعة 70/100
- **وقت**: 3 ساعات

#### Task A17: إطلاق Beta 10
- **حل**: اكتب `docs/BETA_LAUNCH_GUIDE.md` كيف تطلق 10 Beta مجاناً، PWA $0، Stripe test mode، لا حاجة لحسابات خارجية
- **وقت**: 2 ساعة

## النتيجة المتوقعة بعد المسار A

```
Code Completeness: 75 → 80/100 (إضافة HPA YAML, rate limiting, tenant isolation)
Functional Verification: 45 → 70/100 (اختبارات integration 10, auth fixed, tenant isolation tested, WS auth)
Integration Reality: 20 → 30/100 (لا يزال Mock لكن صادق مع reality field, لا يدعي Real)
Production Readiness: 40 → 65/100 (docker prod config tested, K8s dry-run, secrets fixed, backup script)
Security Readiness: 35 → 70/100 (demo creds removed in prod, secrets required, rate limiting, WS auth, tenant isolation)
Scalability Evidence: 15 → 20/100 (لا يزال لا load test, لكن HPA YAML موجود)
Operational Readiness: 30 → 50/100 (monitoring لا يزال mock لكن صادق, backup script)
Commercial Readiness: 25 → 40/100 (لا يزال mock billing لكن صادق, pricing واضح)

OVERALL: 35 → 70/100 BETA READY — يمكن إطلاق Beta 10 مجاناً بمصداقية
```

## التكلفة والوقت

- **وقت**: 6 أيام عمل (48 ساعة)
- **تكلفة**: $0 (لا حسابات خارجية)
- **نتيجة**: Beta Ready حقيقي 70/100، تقدر تقول "Beta Ready — Mock Integrations, Security Hardened" بدون كذب

## بعد المسار A — ماذا بعد؟

- إذا Beta 10 أعطى feedback إيجابي → المسار B (1-2 شهر) → $5K MRR
- إذا feedback سلبي → عدّل المنتج قبل الاستثمار في تكاملات حقيقية

## ابدأ الآن — Task A1

سأبدأ الآن بـ Task A1: إزالة كلمات مرور Demo الصلبة + إصلاح secrets.
