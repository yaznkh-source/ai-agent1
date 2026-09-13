# SOC2 Compliance - AI Agency OS v12

## Overview

AI Agency OS is built with SOC2 Type II compliance in mind - required for selling to Enterprise clients ($999 plan).

SOC2 = Service Organization Control 2 - 5 Trust Service Criteria (TSC).

## 1. Security (CC)

### CC1 - Control Environment
- ✅ RBAC: owner/admin/member/client/viewer with permissions matrix
- ✅ Audit logs: all actions logged with IP, user, timestamp, status
- ✅ Auth: JWT + bcrypt 4.0.1 + API keys + 2FA (future)
- ✅ Teams: owner is only who can delete, admin can invite

### CC2 - Communication & Information
- ✅ Docs: ARCHITECTURE.md, API.md, WHITELABEL.md, BUSINESS_PLAN.md
- ✅ Audit stats: by action/resource/status/user, success_rate, most active
- ✅ Security audit: failed logins 24h, api keys 7d, suspicious IPs, recommendations

### CC3 - Risk Assessment
- ✅ AgentShield: prompt injection detection, secret scanning, tool validation
- ✅ Security scanning: OWASP Top 10, secrets, prompt injection via /api/security/audit
- ✅ Verification loop: real test execution, not mock

### CC4 - Monitoring Activities
- ✅ Audit logs: 50 logs with filtering, stats, security
- ✅ Prometheus + Grafana: monitoring profile in docker-compose.prod.yml
- ✅ Healthchecks: backend /health, postgres pg_isready, redis ping, minio health

### CC5 - Control Activities
- ✅ Input validation: Pydantic models for all endpoints
- ✅ Rate limiting: via filter functions (Open WebUI-inspired)
- ✅ Encryption: at rest (Postgres, Redis, Chroma) + in transit (HTTPS, WSS)

### CC6 - Logical & Physical Access
- ✅ Auth: JWT, RBAC, API keys
- ✅ Teams: invite with role, remove member, owner protection
- ✅ White-label: domain + SSL via Let's Encrypt certbot profile

### CC7 - System Operations
- ✅ K8s: 3 backend replicas + 2 frontend + PVC 10Gi + Secret + liveness/readiness probes
- ✅ CI/CD: GitHub Actions 4 jobs backend-test frontend-test eval-harness docker-build
- ✅ Prod Docker Compose: postgres, redis, chroma, minio, ollama, prometheus, grafana, certbot

### CC8 - Change Management
- ✅ Git: all changes via commits, PRs, CI checks
- ✅ Tests: backend/tests/test_agents.py 7 functions - agents 68, skills 292, tools 9, pipelines 4, security, RAG, auth
- ✅ Versioning: v1..v12 with changelog in README

## 2. Availability (A)

### A1 - Availability
- ✅ K8s 3 replicas: if 1 dies, 2 still serve
- ✅ Healthchecks: auto-restart if /health fails
- ✅ Redis: cache + sessions + queue for resilience
- ✅ PWA: offline cache + service worker + push notifications

## 3. Processing Integrity (PI)

### PI1 - Processing Integrity
- ✅ Verification loop: build, test, lint, typecheck, security - deterministic gate
- ✅ Eval harness: accuracy trend via /api/eval/metrics
- ✅ Pipeline execution: step by step with status, result, cost tracking

## 4. Confidentiality (C)

### C1 - Confidentiality
- ✅ Secrets: K8s secrets, .env.prod.example, not in Git
- ✅ Encryption: at rest + in transit
- ✅ RBAC: client can only see own projects via client portal
- ✅ Storage: S3/MinIO with private buckets, signed URLs

## 5. Privacy (P)

### P1 - Privacy
- ✅ GDPR: data retention, right to delete, audit trail in audit security compliance
- ✅ Client portal: client sees only own data
- ✅ Teams: member can only see assigned projects (future)
- ✅ Email: onboarding, task completed - only to relevant client

## Audit Logs - SOC2 Evidence

All SOC2 requires audit logs - we have:

```bash
GET /api/audit/logs?limit=50&action=agent_run&status=success
GET /api/audit/stats # total_logs, last_24h, by_action, by_resource, by_status, success_rate
GET /api/audit/security # failed_logins_24h, api_keys_created_7d, suspicious_ips, recommendations, compliance SOC2/GDPR
POST /api/audit/log # Create custom log
```

Logs include:
- id, timestamp, user_id, user_email, action, resource, resource_type, ip, user_agent, status, details (duration_ms, cost)

Example log:
```json
{
  "id": "uuid",
  "timestamp": "2026-09-13T14:00:00Z",
  "user_id": "user_0",
  "user_email": "owner@example.com",
  "action": "agent_run",
  "resource": "resource_1",
  "resource_type": "agent",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0",
  "status": "success",
  "details": {"duration_ms": 1500, "cost": 0.05}
}
```

## How to Get SOC2 Certified

1. **Use AI Agency OS as is** - it already has audit logs, RBAC, security, K8s, etc
2. **Hire auditor**: Vanta, Drata, or manual auditor ($10K-$30K)
3. **Connect auditor to logs**: Give auditor access to /api/audit/logs + Grafana + Prometheus
4. **Fill questionnaire**: Auditor asks about CC1..CC8, A1, PI1, C1, P1 - we have answers above
5. **Get certified**: 3-6 months, then you can sell to Enterprise with SOC2 badge

## Cost to Get SOC2

- Vanta/Drata: $10K-$20K/year
- Auditor: $10K-$30K one-time
- Total: $20K-$50K first year, then $10K-$20K/year

But with SOC2, you can charge Enterprise $999/month and close deals with big companies who require SOC2.

## GDPR Compliance

- Data retention: audit logs kept 1 year, then auto-delete (implement via cron)
- Right to delete: DELETE /api/agency/clients/{id} + /api/audit/logs?user_id=... + delete from Postgres
- Audit trail: all deletes logged
- Privacy: client portal only own data, RBAC

## Checklist for Enterprise Sale

- [ ] SOC2 Type II certified (or in progress with Vanta)
- [ ] GDPR compliant (docs + right to delete)
- [ ] Audit logs 50+ with filtering
- [ ] RBAC owner/admin/member/client/viewer
- [ ] K8s 3 replicas + healthchecks
- [ ] Encryption at rest + in transit
- [ ] Security audit via /api/security/audit
- [ ] White-label with custom domain + SSL
- [ ] On-premise installer scripts/install.sh
- [ ] Docs ARCHITECTURE + API + SOC2_COMPLIANCE
- [ ] Support SLA for Enterprise

With all above, you can sell Enterprise $999/month to big companies.

## References

- SOC2: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/soc2report
- Vanta: https://www.vanta.com/
- Drata: https://drata.com/
- Our audit API: /api/audit/*
- Our security API: /api/security/*
