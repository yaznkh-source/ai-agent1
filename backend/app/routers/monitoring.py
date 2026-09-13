"""
Monitoring + Alerts + PagerDuty Router (Track C - Production)
Prometheus rules + Grafana alerts + PagerDuty integration
"""
from fastapi import APIRouter
from typing import Dict, List
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])

# Mock monitoring data
alerts = []
metrics = {
    "agents_executed": 120,
    "skills_used": 340,
    "llm_cost": 45.50,
    "revenue": 199.00,
    "tasks": {"todo": 10, "in_progress": 5, "review": 3, "done": 27},
    "projects": {"active": 8, "completed": 4},
    "margin": 77.1,
    "latency_p50": 150,
    "latency_p95": 450,
    "latency_p99": 1200,
    "websocket_connections": 12,
    "audit_success_rate": 90.0,
    "mrr": 5000
}

# Generate some mock alerts
for i in range(10):
    alerts.append({
        "id": str(uuid.uuid4()),
        "name": ["High LLM Cost", "Backend Down", "Low Margin", "High Latency", "Failed Tasks"][i%5],
        "severity": ["critical", "warning", "info"][i%3],
        "status": "firing" if i%3==0 else "resolved",
        "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
        "description": f"Alert {i} description",
        "would_notify": ["Slack #alerts", "Email owner@example.com", "PagerDuty"] if i%3==0 else []
    })

@router.get("/")
async def monitoring_home():
    return {
        "monitoring": "Prometheus + Grafana + Alerts + PagerDuty - 10 Panels",
        "prometheus": "http://localhost:9090 - Metrics scraping",
        "grafana": "http://localhost:3000 - Dashboards - admin/admin123",
        "dashboard": "monitoring/grafana/dashboards/ai-agency-os.json - 10 panels agents/skills/cost/tasks/projects/margin/latency/WS/audit/MRR",
        "metrics": metrics,
        "alerts": {"total": len(alerts), "firing": len([a for a in alerts if a["status"]=="firing"]), "resolved": len([a for a in alerts if a["status"]=="resolved"])},
        "how_to_setup": [
            "1. Start monitoring - docker-compose -f docker-compose.prod.yml --profile monitoring up -d - starts prometheus 9090 + grafana 3000",
            "2. Prometheus config - monitoring/prometheus.yml - scrape backend /metrics, postgres, redis, etc",
            "3. Grafana - http://localhost:3000 - admin/admin123 - Add Prometheus datasource - http://prometheus:9090 - Import dashboard monitoring/grafana/dashboards/ai-agency-os.json",
            "4. Alerts - Prometheus rules - monitoring/prometheus.yml rules: alert if backend down, LLM cost >$100/day, margin <80%, tasks failed >10%, latency p95 >1s, etc",
            "5. Grafana alerts - Dashboard → Alert → Create alert - email/Slack/PagerDuty when margin <80%, etc",
            "6. PagerDuty - https://www.pagerduty.com/ - $29/mo - on-call - if backend down at 3am, PagerDuty calls you - integrate via Grafana alert notification channel PagerDuty"
        ],
        "prometheus_rules": [
            {"name": "BackendDown", "expr": "up{job=\"backend\"} == 0", "severity": "critical", "for": "1m", "description": "Backend down - no /health response for 1m - would notify Slack #alerts + PagerDuty"},
            {"name": "HighLLMCost", "expr": "sum(increase(llm_cost_dollars[1d])) > 100", "severity": "warning", "for": "5m", "description": "LLM cost >$100/day - check which agent costs most via /api/audit/stats by_action + /api/billing/real/usage by_agent - optimize with Ollama or cache"},
            {"name": "LowMargin", "expr": "(sum(billing_revenue_dollars) - sum(llm_cost_dollars)) / sum(billing_revenue_dollars) * 100 < 80", "severity": "warning", "for": "5m", "description": "Margin <80% - target 88% - check cost breakdown + switch to Ollama for simple tasks"},
            {"name": "HighLatency", "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1", "severity": "warning", "for": "5m", "description": "API p95 latency >1s - check slow endpoints - optimize or scale K8s replicas"},
            {"name": "FailedTasksHigh", "expr": "sum(rate(tasks_failed_total[5m])) > 0.1", "severity": "warning", "for": "5m", "description": "Failed tasks >0.1/sec - check logs - maybe LLM API down or agent bug"},
            {"name": "AuditSuccessLow", "expr": "sum(rate(audit_logs_success_total[5m])) / sum(rate(audit_logs_total[5m])) * 100 < 90", "severity": "warning", "for": "5m", "description": "Audit success rate <90% - check failed actions - maybe auth or billing issues"},
        ],
        "grafana_panels": [
            {"id": 1, "title": "Agents Executed - 68 Total", "type": "stat", "expr": "sum(rate(agent_executions_total[5m]))"},
            {"id": 2, "title": "Skills Used - 292 Total", "type": "stat", "expr": "sum(rate(skill_usages_total[5m]))"},
            {"id": 3, "title": "LLM Cost - $", "type": "graph", "expr": "sum(rate(llm_cost_dollars[5m])) + sum(rate(billing_revenue_dollars[5m]))"},
            {"id": 4, "title": "Tasks - To Do / In Progress / Review / Done", "type": "piechart", "expr": "sum by (status) (tasks_total)"},
            {"id": 5, "title": "Projects - Active / Completed", "type": "stat", "expr": "count(projects_status)"},
            {"id": 6, "title": "Profitability - 88% Margin Target", "type": "gauge", "expr": "(revenue-cost)/revenue*100"},
            {"id": 7, "title": "API Latency - p50 / p95 / p99", "type": "graph", "expr": "histogram_quantile(0.5/0.95/0.99, rate(http_request_duration_seconds_bucket[5m]))"},
            {"id": 8, "title": "WebSocket Connections - Realtime", "type": "stat", "expr": "sum(websocket_connections)"},
            {"id": 9, "title": "Audit Logs - Success Rate", "type": "stat", "expr": "sum(rate(audit_logs_success_total[5m])) / sum(rate(audit_logs_total[5m])) * 100"},
            {"id": 10, "title": "Billing - MRR $5K → $50K → $150K", "type": "graph", "expr": "sum(billing_mrr_dollars) + sum(billing_mrr_dollars) - sum(llm_cost_dollars)"},
        ],
        "pagerduty": {
            "how_to": "PagerDuty $29/mo - on-call alerts - if backend down at 3am, PagerDuty calls you - Grafana → Alerting → Notification channels → Add PagerDuty → Integration key from PagerDuty → Service → Integration → Add Grafana",
            "integration_key": "From PagerDuty dashboard → Services → Service Directory → Your service → Integrations → Add → Grafana → Copy Integration Key → Add to Grafana notification channel"
        }
    }

@router.get("/metrics")
async def get_metrics():
    return {"metrics": metrics, "timestamp": datetime.utcnow().isoformat()}

@router.get("/alerts")
async def list_alerts(severity: str = None, status: str = None, limit: int = 20):
    filtered = alerts
    if severity:
        filtered = [a for a in filtered if a["severity"] == severity]
    if status:
        filtered = [a for a in filtered if a["status"] == status]
    
    filtered = sorted(filtered, key=lambda x: x["timestamp"], reverse=True)
    return {"alerts": filtered[:limit], "count": len(filtered), "total": len(alerts), "firing": len([a for a in alerts if a["status"]=="firing"])}

@router.get("/alerts/firing")
async def get_firing_alerts():
    firing = [a for a in alerts if a["status"] == "firing"]
    return {"alerts": firing, "count": len(firing), "would_notify": ["Slack #alerts", "Email owner@example.com", "PagerDuty"] if firing else []}

@router.post("/alerts/test")
async def test_alert(payload: Dict):
    alert_type = payload.get("type", "HighLLMCost")
    
    alert = {
        "id": str(uuid.uuid4()),
        "name": alert_type,
        "severity": payload.get("severity", "warning"),
        "status": "firing",
        "timestamp": datetime.utcnow().isoformat(),
        "description": f"Test alert {alert_type}",
        "would_notify": ["Slack #alerts", "Email owner@example.com", "PagerDuty"],
        "test": True
    }
    alerts.append(alert)
    
    return {
        "alert": alert,
        "would_do": [
            f"Trigger alert {alert_type} severity {alert['severity']}",
            "Prometheus rule evaluation - expr matches",
            "Grafana alert - notification channel Slack #alerts + Email + PagerDuty",
            "Slack #alerts: :warning: Alert {alert_type} firing - {alert['description']}",
            "Email owner@example.com: Alert {alert_type}",
            "PagerDuty: Incident created - on-call notified via phone/SMS if critical"
        ]
    }

@router.get("/prometheus/rules")
async def get_prometheus_rules():
    return {
        "groups": [
            {
                "name": "ai-agency-os",
                "interval": "30s",
                "rules": [
                    {"alert": "BackendDown", "expr": "up{job=\"backend\"} == 0", "for": "1m", "labels": {"severity": "critical"}, "annotations": {"summary": "Backend down", "description": "Backend down - no /health response for 1m"}},
                    {"alert": "HighLLMCost", "expr": "sum(increase(llm_cost_dollars[1d])) > 100", "for": "5m", "labels": {"severity": "warning"}, "annotations": {"summary": "High LLM cost", "description": "LLM cost >$100/day"}},
                    {"alert": "LowMargin", "expr": "(sum(billing_revenue_dollars) - sum(llm_cost_dollars)) / sum(billing_revenue_dollars) * 100 < 80", "for": "5m", "labels": {"severity": "warning"}, "annotations": {"summary": "Low margin", "description": "Margin <80% - target 88%"}},
                    {"alert": "HighLatency", "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1", "for": "5m", "labels": {"severity": "warning"}, "annotations": {"summary": "High latency", "description": "API p95 latency >1s"}},
                    {"alert": "FailedTasksHigh", "expr": "sum(rate(tasks_failed_total[5m])) > 0.1", "for": "5m", "labels": {"severity": "warning"}, "annotations": {"summary": "Failed tasks high", "description": "Failed tasks >0.1/sec"}},
                ]
            }
        ],
        "would_write_to": "monitoring/prometheus.yml or monitoring/prometheus/rules.yml"
    }

@router.get("/grafana/dashboard")
async def get_grafana_dashboard():
    # Return dashboard JSON
    try:
        with open("monitoring/grafana/dashboards/ai-agency-os.json", "r") as f:
            import json
            dashboard = json.load(f)
            return dashboard
    except:
        return {
            "dashboard": {
                "title": "AI Agency OS - 68 Agents, 292 Skills - Monitoring",
                "panels": 10,
                "would_import": "Grafana → Dashboards → Import → Upload JSON file monitoring/grafana/dashboards/ai-agency-os.json"
            }
        }
