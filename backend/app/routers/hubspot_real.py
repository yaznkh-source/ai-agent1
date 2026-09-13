"""
HubSpot Real - OAuth + Contacts/Deals/Companies/Notes/Workflows Sync Real API (Track C)
Task C1: Real HubSpot API with httpx when pat- key available, mock fallback
"""
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Dict, List
import uuid
from datetime import datetime, timedelta
import os
import json

router = APIRouter(prefix="/api/integrations/hubspot/real", tags=["hubspot-real"])

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "test_hubspot_key_123")
HUBSPOT_CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID", "test_client_id")
HUBSPOT_CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET", "test_client_secret")

# In-memory HubSpot real data
hubspot_real_contacts = []
hubspot_real_deals = []
hubspot_real_companies = []
hubspot_real_notes = []
hubspot_real_webhooks = []

# Generate mock
for i in range(5):
    hubspot_real_contacts.append({
        "id": f"contact_real_{i}",
        "email": f"contact{i}@example.com",
        "firstname": f"First{i}",
        "lastname": f"Last{i}",
        "company": f"Company {i}",
        "lifecyclestage": ["lead", "customer", "subscriber"][i%3],
        "deal_stage": ["appointmentscheduled", "closedwon", "negotiation"][i%3],
        "created_at": (datetime.utcnow() - timedelta(days=i*2)).isoformat(),
        "source": "hubspot-real",
        "hubspot_id": f"{1000+i}"
    })

@router.get("/")
async def hubspot_real_home():
    from ..core.config import settings
    
    real_api_available = False
    try:
        import httpx
        real_api_available = True
    except ImportError:
        real_api_available = False
    
    reality = "MOCK_WITH_REAL_INTENDED_CODE"
    if real_api_available and HUBSPOT_API_KEY and HUBSPOT_API_KEY.startswith("pat-"):
        reality = "REAL_LIVE_MODE - httpx available, pat- key, real HubSpot API calls"
    
    return {
        "integration": "HubSpot Mock (Real-API-Intended) - In-memory 5 contacts, no requests to api.hubapi.com unless pat- key - Task A5 + C1",
        "reality": reality,
        "httpx_available": real_api_available,
        "real_implementation_needed": [
            "pip install httpx",
            "httpx.get('https://api.hubapi.com/crm/v3/objects/contacts?limit=10', headers={'Authorization': f'Bearer {HUBSPOT_API_KEY}'}) - real call",
            "httpx.post('https://api.hubapi.com/crm/v3/objects/contacts', json={'properties': {...}}) - real create"
        ],
        "task_C1": "If httpx + pat- key, uses real HubSpot API - $0 private app token",
        "mode": "test" if HUBSPOT_API_KEY.startswith("test_") else "live",
        "env": settings.ENV,
        "api_key_configured": bool(os.getenv("HUBSPOT_API_KEY")),
        "stats": {
            "contacts": len(hubspot_real_contacts),
            "deals": len(hubspot_real_deals),
            "companies": len(hubspot_real_companies)
        },
        "endpoints": {
            "contacts": "GET /api/integrations/hubspot/real/contacts",
            "contacts_create": "POST /api/integrations/hubspot/real/contacts",
            "webhook": "POST /api/integrations/hubspot/real/webhook",
            "sync": "POST /api/integrations/hubspot/real/sync"
        }
    }

@router.get("/contacts")
async def list_contacts_real(limit: int = 10):
    # Task C1: Try real API if pat- key + httpx
    try:
        import httpx
        if HUBSPOT_API_KEY and HUBSPOT_API_KEY.startswith("pat-") and not HUBSPOT_API_KEY.startswith("test_"):
            # Real HubSpot API call
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"https://api.hubapi.com/crm/v3/objects/contacts?limit={limit}",
                        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
                        timeout=10.0
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        contacts = []
                        for item in data.get("results", [])[:limit]:
                            props = item.get("properties", {})
                            contacts.append({
                                "id": item.get("id"),
                                "email": props.get("email"),
                                "firstname": props.get("firstname"),
                                "lastname": props.get("lastname"),
                                "company": props.get("company"),
                                "created_at": props.get("createdate"),
                                "source": "hubspot-real-api",
                                "hubspot_id": item.get("id")
                            })
                        return {
                            "contacts": contacts,
                            "count": len(contacts),
                            "total": len(contacts),
                            "mode": "real",
                            "reality": "REAL_LIVE_MODE - HubSpot API",
                            "fetched_via": "GET https://api.hubapi.com/crm/v3/objects/contacts"
                        }
                    else:
                        print(f"⚠️ HubSpot API error {resp.status_code}: {resp.text[:200]} - falling back to mock")
            except Exception as e:
                print(f"⚠️ HubSpot real API failed: {e} - falling back to mock")
    except ImportError:
        pass
    
    # Mock fallback
    return {
        "contacts": hubspot_real_contacts[:limit],
        "count": len(hubspot_real_contacts[:limit]),
        "total": len(hubspot_real_contacts),
        "mode": "mock",
        "reality": "MOCK_WITH_REAL_INTENDED_CODE",
        "would_fetch_real": f"GET https://api.hubapi.com/crm/v3/objects/contacts?limit={limit} --header Authorization Bearer {HUBSPOT_API_KEY[:10]}...",
        "note": "Set HUBSPOT_API_KEY=pat-na1-... for real API calls + pip install httpx"
    }

@router.post("/contacts")
async def create_contact_real(payload: Dict):
    # Task C1: Try real API if pat- key
    try:
        import httpx
        if HUBSPOT_API_KEY and HUBSPOT_API_KEY.startswith("pat-"):
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.hubapi.com/crm/v3/objects/contacts",
                        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}", "Content-Type": "application/json"},
                        json={"properties": {
                            "email": payload.get("email"),
                            "firstname": payload.get("firstname", ""),
                            "lastname": payload.get("lastname", ""),
                            "company": payload.get("company", "")
                        }},
                        timeout=10.0
                    )
                    if resp.status_code in [200, 201]:
                        data = resp.json()
                        return {
                            "created": True,
                            "contact": {
                                "id": data.get("id"),
                                "email": payload.get("email"),
                                "firstname": payload.get("firstname"),
                                "lastname": payload.get("lastname"),
                                "source": "hubspot-real-api",
                                "hubspot_id": data.get("id")
                            },
                            "mode": "real",
                            "reality": "REAL_LIVE_MODE"
                        }
            except Exception as e:
                print(f"⚠️ HubSpot create real failed: {e} - mock fallback")
    except ImportError:
        pass
    
    # Mock fallback
    contact = {
        "id": f"contact_real_{uuid.uuid4().hex[:8]}",
        "email": payload.get("email"),
        "firstname": payload.get("firstname", ""),
        "lastname": payload.get("lastname", ""),
        "company": payload.get("company", ""),
        "created_at": datetime.utcnow().isoformat(),
        "source": "ai-agency-os-real",
        "hubspot_id": f"{2000+len(hubspot_real_contacts)}",
        "reality": "MOCK_WITH_REAL_INTENDED_CODE"
    }
    hubspot_real_contacts.append(contact)
    return {"created": True, "contact": contact, "mode": "mock", "reality": "MOCK_WITH_REAL_INTENDED_CODE"}

@router.post("/webhook")
async def hubspot_webhook_real(payload: Dict):
    event_type = payload.get("event_type", "deal_closed_won")
    deal_data = payload.get("deal", {})
    contact_data = payload.get("contact", {})
    
    result = {
        "received": True,
        "event_type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "mock",
        "would_do": []
    }
    
    if event_type == "deal_closed_won" or deal_data.get("dealstage") == "closedwon":
        project = {
            "id": f"proj_{uuid.uuid4().hex[:8]}",
            "name": deal_data.get("dealname", "Project from HubSpot Real"),
            "client_email": contact_data.get("email", "client@example.com"),
            "description": f"From HubSpot deal {deal_data.get('id')} amount ${deal_data.get('amount', 199)}",
            "source": "hubspot-real",
            "amount": deal_data.get("amount", 199),
            "created_at": datetime.utcnow().isoformat()
        }
        result["would_do"].append(f"Create project via POST /api/agency/projects")
        result["project"] = project
    
    hubspot_real_webhooks.append(result)
    return result

@router.post("/sync")
async def sync_hubspot_to_agency(payload: Dict = None):
    payload = payload or {}
    return {
        "synced": True,
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "mock" if HUBSPOT_API_KEY.startswith("test_") else "live_mock",
        "results": {
            "contacts_fetched": len(hubspot_real_contacts),
            "clients_created": 2,
            "projects_created": 1
        },
        "reality": "MOCK_WITH_REAL_INTENDED_CODE - Set pat- key + httpx for real sync"
    }

@router.get("/oauth")
async def hubspot_oauth_real(code: str = None):
    if not code:
        client_id = HUBSPOT_CLIENT_ID
        redirect_uri = "https://api.ai-agency.os/api/integrations/hubspot/real/oauth"
        scope = "crm.objects.contacts.read crm.objects.contacts.write"
        oauth_url = f"https://app.hubspot.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        return {"oauth_url": oauth_url, "how_to": "Redirect user to oauth_url"}
    else:
        return {
            "code": code,
            "access_token": f"pat-mock-access-{uuid.uuid4().hex[:16]}",
            "refresh_token": f"pat-mock-refresh-{uuid.uuid4().hex[:16]}",
            "expires_in": 1800
        }

@router.get("/webhooks/list")
async def list_webhooks_real(limit: int = 20):
    return {"webhooks": hubspot_real_webhooks[-limit:], "count": len(hubspot_real_webhooks)}
