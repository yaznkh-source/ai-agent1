# خطة المسار B — من 70/100 Beta Ready إلى 80/100 Production Hardened — $0 تكلفة

## الهدف
من 70/100 BETA READY → 80/100 PRODUCTION HARDENED
تضيف: backup/restore، load testing، E2E، GDPR endpoints، Prometheus real client، Stripe test mode real SDK

## المشاكل المتبقية من 70/100

1. **لا backup/restore** — Operational 50/100
2. **لا load testing** — Scalability 20/100
3. **لا E2E test** — Functional 70/100 يحتاج E2E project→planner→agent→QA
4. **Monitoring لا يزال hardcoded** — يمكن إضافة prometheus_client حقيقي $0
5. **GDPR endpoints غير موجودة** — لا export/delete/consent
6. **Stripe لا يزال mock** — يمكن إضافة stripe SDK test mode $0

## المهام — 5 أيام — $0

### B1: Backup/Restore Script (2 ساعات)
- ملف: scripts/backup.sh + scripts/restore.sh + backend/app/routers/backup.py
- إنشاء backup script ينسخ sqlite db + storage + chroma
- restore script يسترجع
- API endpoints /api/backup/create, /api/backup/restore, /api/backup/list
- دليل: ./scripts/backup.sh → backup-2026-09-13.tar.gz

### B2: Load Testing with Locust (3 ساعات)
- ملف: tests/locustfile.py + docs/LOAD_TESTING.md
- pip install locust
- سيناريوهات: 10 users, 100 users, login, list agents, create project, chat
- دليل: locust -f tests/locustfile.py --headless -u 10 -r 2 --run-time 30s
- توثيق نتائج

### B3: E2E Test Full Flow (4 ساعات)
- ملف: backend/tests/test_e2e.py
- سيناريو: register → login → create client → create project → create task → run agent → check result → client portal
- يختبر تدفق كامل حقيقي
- دليل: pytest tests/test_e2e.py -v

### B4: GDPR Endpoints (3 ساعات)
- ملف: backend/app/routers/gdpr.py + docs/GDPR.md
- endpoints: /api/gdpr/export (تصدير بيانات المستخدم), /api/gdpr/delete (حذف حساب), /api/gdpr/consent
- توثيق GDPR checklist
- دليل: curl /api/gdpr/export → JSON with user data

### B5: Prometheus Real Client (2 ساعات)
- ملف: backend/app/core/metrics.py + backend/app/routers/monitoring.py
- pip install prometheus_client
- إضافة metrics حقيقية: request_count, request_latency, agents_executed, etc
- /metrics endpoint حقيقي
- الاحتفاظ بـ mock كـ fallback لكن مع real metrics

### B6: Stripe Test Mode Real SDK (3 ساعات)
- ملف: backend/app/routers/billing_real.py
- pip install stripe
- إذا STRIPE_SECRET_KEY يبدأ بـ sk_test_ → استخدم real SDK في test mode
- إذا لا يوجد key → استخدم mock مع reality field (كما هو)
- Checkout Session حقيقي في test mode
- Webhook verification حقيقي إذا whsec_ موجود

### B7: Security Audit Logging (2 ساعات)
- ملف: backend/app/core/audit_logger.py
- تسجيل كل محاولة login، كل access denied، كل cross-tenant attempt
- /api/audit/security endpoint

### B8: Production Deployment Guide (2 ساعات)
- ملف: docs/PRODUCTION_DEPLOYMENT.md
- دليل نشر حقيقي خطوة بخطوة: domain, SSL, docker prod, k8s, backup, monitoring, secrets

## النتيجة المتوقعة

```
Code Completeness: 80 → 85/100 (+backup, gdpr, metrics, stripe test mode)
Functional Verification: 70 → 80/100 (+E2E test)
Integration Reality: 30 → 45/100 (+Prometheus real, Stripe test mode real)
Production Readiness: 65 → 75/100 (+backup/restore tested, deployment guide)
Security Readiness: 70 → 80/100 (+audit logging, GDPR)
Scalability Evidence: 20 → 40/100 (+locust load testing 10/100 users)
Operational Readiness: 50 → 70/100 (+backup/restore, real metrics, /metrics)
Commercial Readiness: 40 → 50/100 (+Stripe test mode real checkout)

OVERALL: 70 → 80/100 PRODUCTION HARDENED
```

## التكلفة
- $0 — locust, prometheus_client, stripe SDK all free, test mode no charges
- وقت: 5 أيام (40 ساعة)

## ابدأ الآن — B1 Backup/Restore
