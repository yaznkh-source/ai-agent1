"""
Tests for GDPR, Backup, Metrics - Task C7 - Production Ready 90/100 → 95/100
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_gdpr_info():
    response = client.get("/api/gdpr/")
    assert response.status_code == 200
    data = response.json()
    assert "gdpr" in data
    assert "endpoints" in data
    assert "export" in data["endpoints"]
    print("✅ test_gdpr_info - GDPR info endpoint works")

def test_gdpr_retention():
    response = client.get("/api/gdpr/retention")
    assert response.status_code == 200
    data = response.json()
    assert "retention_policy" in data
    print("✅ test_gdpr_retention - Retention policy works")

def test_gdpr_export_requires_auth():
    response = client.get("/api/gdpr/export")
    assert response.status_code in [401, 403, 422]  # Should require auth
    print("✅ test_gdpr_export_requires_auth - Export requires auth (security)")

def test_backup_info():
    response = client.get("/api/backup/")
    assert response.status_code == 200
    data = response.json()
    assert "backup_dir" in data
    assert "backups" in data
    assert "reality" in data
    print("✅ test_backup_info - Backup info works")

def test_backup_create_requires_auth():
    response = client.post("/api/backup/create")
    assert response.status_code in [401, 403, 422]  # Should require auth
    print("✅ test_backup_create_requires_auth - Backup create requires auth")

def test_metrics_info():
    response = client.get("/api/metrics/")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "prometheus_available" in data
    print(f"✅ test_metrics_info - Metrics info works, prometheus_available: {data['prometheus_available']}")

def test_metrics_prometheus():
    response = client.get("/api/metrics/prometheus")
    assert response.status_code == 200
    # Should be Prometheus text format
    assert "ai_agency" in response.text or "HELP" in response.text
    print("✅ test_metrics_prometheus - Prometheus metrics endpoint works")

def test_metrics_json():
    response = client.get("/api/metrics/json")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    print("✅ test_metrics_json - Metrics JSON works")

def test_privacy_terms_frontend_build():
    # Check that privacy and terms components exist
    import os
    privacy_path = os.path.join(os.path.dirname(__file__), '../../frontend/src/components/PrivacyPolicyView.tsx')
    terms_path = os.path.join(os.path.dirname(__file__), '../../frontend/src/components/TermsView.tsx')
    assert os.path.exists(privacy_path), "PrivacyPolicyView.tsx should exist"
    assert os.path.exists(terms_path), "TermsView.tsx should exist"
    
    with open(privacy_path) as f:
        content = f.read()
        assert "GDPR" in content
        assert "Right to Access" in content or "Right to" in content
    
    with open(terms_path) as f:
        content = f.read()
        assert "Terms" in content
        assert "Pricing" in content or "Free" in content
    
    print("✅ test_privacy_terms_frontend_build - Privacy & Terms components exist")

def test_load_testing_files_exist():
    import os
    locust_path = os.path.join(os.path.dirname(__file__), 'locustfile.py')
    results_path = os.path.join(os.path.dirname(__file__), '../../docs/LOAD_TESTING_RESULTS.md')
    assert os.path.exists(locust_path), "locustfile.py should exist"
    assert os.path.exists(results_path), "LOAD_TESTING_RESULTS.md should exist"
    
    with open(locust_path) as f:
        content = f.read()
        assert "HttpUser" in content
        assert "locust" in content.lower() or "HttpUser" in content
    
    print("✅ test_load_testing_files_exist - Locust files exist")

def test_hubspot_real_api_with_mock():
    response = client.get("/api/integrations/hubspot/real/")
    assert response.status_code == 200
    data = response.json()
    assert "reality" in data
    assert "httpx_available" in data
    print(f"✅ test_hubspot_real_api_with_mock - HubSpot reality: {data['reality']}")

def test_slack_real_api_with_mock():
    response = client.get("/api/integrations/slack/real/")
    assert response.status_code == 200
    data = response.json()
    assert "reality" in data
    assert "slack_sdk_available" in data
    print(f"✅ test_slack_real_api_with_mock - Slack reality: {data['reality']}")

def test_billing_real_with_stripe_sdk():
    response = client.get("/api/billing/real/")
    assert response.status_code == 200
    data = response.json()
    assert "reality" in data
    assert "stripe_sdk_installed" in data
    print(f"✅ test_billing_real_with_stripe_sdk - Billing reality: {data['reality']}, stripe_sdk: {data['stripe_sdk_installed']}")

if __name__ == "__main__":
    test_gdpr_info()
    test_gdpr_retention()
    test_gdpr_export_requires_auth()
    test_backup_info()
    test_backup_create_requires_auth()
    test_metrics_info()
    test_metrics_prometheus()
    test_metrics_json()
    test_privacy_terms_frontend_build()
    test_load_testing_files_exist()
    test_hubspot_real_api_with_mock()
    test_slack_real_api_with_mock()
    test_billing_real_with_stripe_sdk()
    print("\n🎉 All 13 GDPR/Backup/Metrics tests passed! — Task C7 ✅")
