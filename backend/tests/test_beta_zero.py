"""Test Beta 100 مستخدم $0 — SOC2 $30K-$80K + Domain $12/سنة + k8s $100+/شهر + Integrations $0 + GTM $0 — بناء وتنسيق مرحلة Beta والتوسع حتى أول 100 مستخدم بتكلفة $0 تماماً — بعد تابع x6 — دائماً بالعربية"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_beta_zero_info():
    r = client.get("/api/beta-zero/")
    assert r.status_code == 200
    data = r.json()
    assert "Beta 100" in str(data) or "beta" in str(data).lower()
    assert "$0" in str(data)

def test_beta_zero_soc2():
    r = client.get("/api/beta-zero/soc2")
    assert r.status_code == 200
    data = r.json()
    assert "SOC2" in str(data) or "OpenControl" in str(data)
    assert "$0" in str(data) or "30K" in str(data)

def test_beta_zero_domain():
    r = client.get("/api/beta-zero/domain")
    assert r.status_code == 200
    data = r.json()
    assert "Domain" in str(data) or "Vercel" in str(data)
    assert "$0" in str(data)

def test_beta_zero_k8s():
    r = client.get("/api/beta-zero/k8s")
    assert r.status_code == 200
    data = r.json()
    assert "k8s" in str(data).lower() or "Kubernetes" in str(data) or "Kind" in str(data)
    assert "$0" in str(data)

def test_beta_zero_integrations():
    r = client.get("/api/beta-zero/integrations")
    assert r.status_code == 200
    data = r.json()
    assert "Stripe" in str(data) or "HubSpot" in str(data) or "Slack" in str(data)
    assert "$0" in str(data)

def test_beta_zero_gtm():
    r = client.get("/api/beta-zero/gtm")
    assert r.status_code == 200
    data = r.json()
    assert "Go-to-Market" in str(data) or "Product Hunt" in str(data) or "Supabase" in str(data)
    assert "$0" in str(data)

def test_beta_zero_checklist():
    r = client.get("/api/beta-zero/checklist")
    assert r.status_code == 200
    data = r.json()
    assert "checklist" in data
    assert data["total"] == 12
    assert data["done_0"] == 12

def test_beta_zero_stats():
    r = client.get("/api/beta-zero/stats")
    assert r.status_code == 200
    data = r.json()
    assert "beta_10_free" in data
    assert "prod_100" in data
    assert "mrr_30k" in data
    assert "mrr_100k" in data
    assert data["mrr_100k"]["arr"] == 1886280
    assert "soc2_zero" in data
    assert "domain_zero" in data
    assert "k8s_zero" in data
    assert "integrations_zero" in data
    assert "gtm_zero" in data
    assert "$0" in data["total_saving"] or "30K" in data["total_saving"]

def test_beta_zero_view_exists():
    import os
    for path in ["frontend/src/components/BetaZeroView.tsx", "/home/user/ai-agent1/frontend/src/components/BetaZeroView.tsx"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Beta 100" in content or "beta-zero" in content.lower()
                assert "$0" in content
                return
    assert False, "BetaZeroView.tsx not found"

def test_all_beta_zero_integration():
    r_beta = client.get("/api/beta/stats")
    r_prod = client.get("/api/prod/stats")
    r_mrr_30k = client.get("/api/mrr/stats")
    r_mrr_100k = client.get("/api/mrr/100k/stats")
    r_mrr_1m = client.get("/api/mrr/1m/stats")
    r_ent = client.get("/api/enterprise/")
    r_zero = client.get("/api/beta-zero/stats")
    assert r_beta.status_code == 200
    assert r_prod.status_code == 200
    assert r_mrr_30k.status_code == 200
    assert r_mrr_100k.status_code == 200
    assert r_mrr_1m.status_code == 200
    assert r_ent.status_code == 200
    assert r_zero.status_code == 200
    assert r_zero.json()["mrr_100k"]["arr"] == 1886280
    assert r_zero.json()["prod_100"]["mrr"] == 19900
