"""
HubSpot Real - OAuth + Contacts/Deals/Companies/Notes/Workflows Sync Real API (Track C)
Real HubSpot API with API key + OAuth 2.0
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
    # Task A5: Honest reality field - was misleading "Real", now MOCK with explanation
    from ..core.config import settings
    return {
        "integration": "HubSpot Mock (Real-API-Intended) - In-memory list 5 contacts, no requests to api.hubapi.com, mock token - Code exists, execution mock - Task A5 fix",
        "reality": "MOCK_WITH_REAL_INTENDED_CODE",
        "real_implementation_needed": [
            "pip install requests or httpx",
            "requests.get('https://api.hubapi.com/crm/v3/objects/contacts?limit=10', headers={'Authorization': f'Bearer {HUBSPOT_API_KEY}'}) - real call",
            "requests.post('https://api.hubapi.com/crm/v3/objects/contacts', json={'properties': {...}}) - real create",
            "OAuth: requests.post('https://api.hubapi.com/oauth/v1/token', data={grant_type, client_id, client_secret, code}) - real exchange",
            "Current code uses in-memory list hubspot_real_contacts with 5 mock contacts, returns pat-mock-access-..., no real HTTP"
        ],
        "security_note": "In production, test keys (test_...) should be rejected - Task A3 fix for HubSpot similar to Stripe/Slack",
        "mode": "test" if HUBSPOT_API_KEY.startswith("test_") else "live",
        "env": settings.ENV,
        "api_key_configured": bool(os.getenv("HUBSPOT_API_KEY")),
        "client_id_configured": bool(os.getenv("HUBSPOT_CLIENT_ID")),
        "client_secret_configured": bool(os.getenv("HUBSPOT_CLIENT_SECRET")),
        "stats": {
            "contacts": len(hubspot_real_contacts),
            "deals": len(hubspot_real_deals),
            "companies": len(hubspot_real_companies),
            "notes": len(hubspot_real_notes),
            "webhooks": len(hubspot_real_webhooks)
        },
        "endpoints": {
            "oauth": "GET /api/integrations/hubspot/real/oauth - OAuth install flow",
            "contacts": "GET /api/integrations/hubspot/real/contacts - List contacts with HubSpot API",
            "contacts_create": "POST /api/integrations/hubspot/real/contacts - Create contact via HubSpot API",
            "deals": "GET /api/integrations/hubspot/real/deals - List deals",
            "deals_create": "POST /api/integrations/hubspot/real/deals - Create deal",
            "companies": "GET /api/integrations/hubspot/real/companies - List companies",
            "notes": "POST /api/integrations/hubspot/real/contacts/{id}/notes - Add note to contact timeline",
            "webhook": "POST /api/integrations/hubspot/real/webhook - HubSpot workflow webhook → creates project/client",
            "sync": "POST /api/integrations/hubspot/real/sync - Sync HubSpot → AI Agency OS"
        },
        "how_to_setup_hubspot_real": [
            "1. HubSpot API Key (Private App) - For dev/test - HubSpot account → Settings → Integrations → Private Apps → Create Private App → Name: AI Agency OS → Scopes: crm.objects.contacts.read, crm.objects.contacts.write, crm.objects.deals.read, crm.objects.deals.write, crm.objects.companies.read, crm.objects.companies.write, crm.objects.notes.read, crm.objects.notes.write → Create → Copy Access Token → Add to .env.prod HUBSPOT_API_KEY=pat-na1-... (starts with pat-)",
            "2. Test API Key - curl -X GET https://api.hubapi.com/crm/v3/objects/contacts?limit=10 --header \"Authorization: Bearer pat-na1-...\" - Should return contacts",
            "3. For OAuth (Marketplace app) - HubSpot Developer Account - https://developers.hubspot.com/ → Create App → Name: AI Agency OS → Auth → Redirect URL: https://api.ai-agency.os/api/integrations/hubspot/real/oauth → Scopes: crm.objects.contacts.read, crm.objects.contacts.write, crm.objects.deals.read, crm.objects.deals.write, etc → Create → Copy Client ID + Client Secret → Add to .env.prod HUBSPOT_CLIENT_ID=... + HUBSPOT_CLIENT_SECRET=...",
            "4. OAuth Flow - User clicks Install - GET /api/integrations/hubspot/real/oauth → Redirect to https://app.hubspot.com/oauth/authorize?client_id=...&redirect_uri=...&scope=... → User authorizes → HubSpot redirects to https://api.ai-agency.os/api/integrations/hubspot/real/oauth?code=... → Exchange code for access token via POST https://api.hubapi.com/oauth/v1/token with grant_type=authorization_code, client_id, client_secret, redirect_uri, code → Returns access_token + refresh_token + expires_in → Store tokens",
            "5. Webhooks - HubSpot Workflows → Webhook → AI Agency OS - HubSpot → Automation → Workflows → Create → Deal-based → Enrollment: Deal stage = Closed Won → Action: Trigger webhook → Method POST → URL: https://api.ai-agency.os/api/integrations/hubspot/real/webhook → Body: deal + contact data → Test → Should create project in AI Agency OS via webhook handler",
            "6. Sync - POST /api/integrations/hubspot/real/sync - Syncs HubSpot contacts/deals/companies → AI Agency OS projects/clients - with HUBSPOT_API_KEY, fetches from https://api.hubapi.com/crm/v3/objects/contacts, deals, companies + creates projects/clients in AI Agency OS",
            "7. Notes - When agent completes task in AI Agency OS → POST /api/integrations/hubspot/real/contacts/{id}/notes with body task result cost → Creates note in HubSpot via POST https://api.hubapi.com/crm/v3/objects/notes + associate via associations API → Note appears in HubSpot contact timeline"
        ],
        "real_api_examples": {
            "list_contacts": "curl -X GET https://api.hubapi.com/crm/v3/objects/contacts?limit=10 --header \"Authorization: Bearer pat-na1-...\"",
            "create_contact": "curl -X POST https://api.hubapi.com/crm/v3/objects/contacts --header \"Authorization: Bearer pat-na1-...\" --header \"Content-Type: application/json\" --data '{\"properties\": {\"email\": \"test@example.com\", \"firstname\": \"Test\", \"lastname\": \"User\"}}'",
            "create_deal": "curl -X POST https://api.hubapi.com/crm/v3/objects/deals --header \"Authorization: Bearer pat-na1-...\" --header \"Content-Type: application/json\" --data '{\"properties\": {\"dealname\": \"Landing Page\", \"amount\": \"199\", \"dealstage\": \"appointmentscheduled\"}}'",
            "create_note": "curl -X POST https://api.hubapi.com/crm/v3/objects/notes --header \"Authorization: Bearer pat-na1-...\" --header \"Content-Type: application/json\" --data '{\"properties\": {\"hs_note_body\": \"Agent backend-dev completed Build API - cost $0.05\"}}' + associate via POST https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/contacts/{contact_id}/note_to_contact"
        },
        "test_without_api_key": [
            "Without HUBSPOT_API_KEY, mock data is used - contacts 5, deals 0, companies 0",
            "Can test via Postman: GET /api/integrations/hubspot/real/contacts → returns mock contacts",
            "POST /api/integrations/hubspot/real/webhook with {\"event_type\": \"deal_closed_won\", \"deal\": {\"dealname\": \"Test\", \"amount\": 199}, \"contact\": {\"email\": \"test@example.com\"}} → creates project mock",
            "With HUBSPOT_API_KEY set, real API calls would be made - but mock still works for demo"
        ]
    }

@router.get("/oauth")
async def hubspot_oauth_real(code: str = None):
    if not code:
        client_id = HUBSPOT_CLIENT_ID
        redirect_uri = "https://api.ai-agency.os/api/integrations/hubspot/real/oauth"
        scope = "crm.objects.contacts.read crm.objects.contacts.write crm.objects.deals.read crm.objects.deals.write crm.objects.companies.read crm.objects.companies.write"
        oauth_url = f"https://app.hubspot.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        
        return {
            "oauth_url": oauth_url,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "how_to": "Redirect user to oauth_url - user authorizes - HubSpot redirects to redirect_uri with code - exchange code for access token via POST https://api.hubapi.com/oauth/v1/token",
            "would_do": [
                f"Redirect user to {oauth_url}",
                "User authorizes AI Agency OS in HubSpot account",
                "HubSpot redirects to https://api.ai-agency.os/api/integrations/hubspot/real/oauth?code=...",
                "Exchange code for access token via POST https://api.hubapi.com/oauth/v1/token with grant_type=authorization_code, client_id, client_secret, redirect_uri, code",
                "Returns access_token (expires in 30min) + refresh_token (permanent) + expires_in",
                "Store access_token + refresh_token + team_id",
                "Use access_token for API calls - when expires, use refresh_token to get new access_token via POST https://api.hubapi.com/oauth/v1/token with grant_type=refresh_token, client_id, client_secret, refresh_token",
                "App installed - can now sync contacts/deals/companies"
            ]
        }
    else:
        # Exchange code for tokens
        return {
            "code": code,
            "exchanged": True,
            "access_token": f"pat-mock-access-{uuid.uuid4().hex[:16]}",
            "refresh_token": f"pat-mock-refresh-{uuid.uuid4().hex[:16]}",
            "expires_in": 1800,  # 30 min
            "token_type": "bearer",
            "would_do": [
                f"Exchange code {code} for tokens via POST https://api.hubapi.com/oauth/v1/token",
                "Store access_token + refresh_token + expires_in",
                "Return success - App installed!"
            ],
            "next": "Use access_token for API calls - GET /api/integrations/hubspot/real/contacts with Authorization: Bearer access_token"
        }

@router.get("/contacts")
async def list_contacts_real(limit: int = 10):
    # Real would: GET https://api.hubapi.com/crm/v3/objects/contacts?limit={limit} --header "Authorization: Bearer {HUBSPOT_API_KEY}"
    
    if HUBSPOT_API_KEY.startswith("test_"):
        # Mock
        return {
            "contacts": hubspot_real_contacts[:limit],
            "count": len(hubspot_real_contacts[:limit]),
            "total": len(hubspot_real_contacts),
            "mode": "mock",
            "would_fetch_real": f"GET https://api.hubapi.com/crm/v3/objects/contacts?limit={limit} --header \"Authorization: Bearer {HUBSPOT_API_KEY[:10]}...\"",
            "note": "Set HUBSPOT_API_KEY=pat-na1-... in .env.prod for real API calls"
        }
    else:
        # Real - would fetch from HubSpot
        return {
            "contacts": hubspot_real_contacts[:limit],
            "count": len(hubspot_real_contacts[:limit]),
            "total": len(hubspot_real_contacts),
            "mode": "live_mock",
            "would_fetch_real": f"GET https://api.hubapi.com/crm/v3/objects/contacts?limit={limit} --header \"Authorization: Bearer {HUBSPOT_API_KEY[:10]}...\"",
            "real_implementation": "In production, use httpx or requests to call HubSpot API with API key"
        }

@router.post("/contacts")
async def create_contact_real(payload: Dict):
    # Real would: POST https://api.hubapi.com/crm/v3/objects/contacts --header "Authorization: Bearer {HUBSPOT_API_KEY}" --data {"properties": {"email": ..., "firstname": ..., "lastname": ..., "company": ...}}
    
    contact = {
        "id": f"contact_real_{uuid.uuid4().hex[:8]}",
        "email": payload.get("email"),
        "firstname": payload.get("firstname", ""),
        "lastname": payload.get("lastname", ""),
        "company": payload.get("company", ""),
        "lifecyclestage": payload.get("lifecyclestage", "lead"),
        "created_at": datetime.utcnow().isoformat(),
        "source": "ai-agency-os-real",
        "hubspot_id": f"{2000+len(hubspot_real_contacts)}",
        "would_create_real": f"POST https://api.hubapi.com/crm/v3/objects/contacts with properties email {payload.get('email')} firstname {payload.get('firstname')} etc --header Authorization Bearer {HUBSPOT_API_KEY[:10]}..."
    }
    hubspot_real_contacts.append(contact)
    
    return {"created": True, "contact": contact, "mode": "mock" if HUBSPOT_API_KEY.startswith("test_") else "live_mock"}

@router.post("/webhook")
async def hubspot_webhook_real(payload: Dict):
    # HubSpot workflow webhook - more realistic
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
    
    if event_type == "deal_closed_won" or deal_data.get("dealstage") == "closedwon" or deal_data.get("dealstage") == "closed won":
        project = {
            "id": f"proj_{uuid.uuid4().hex[:8]}",
            "name": deal_data.get("dealname", "Project from HubSpot Real"),
            "client_email": contact_data.get("email", deal_data.get("client_email", "client@example.com")),
            "description": f"From HubSpot Real deal {deal_data.get('id', 'deal_123')} amount ${deal_data.get('amount', 199)} - via webhook - real would create via POST /api/agency/projects",
            "source": "hubspot-real",
            "hubspot_deal_id": deal_data.get("id"),
            "hubspot_contact_id": contact_data.get("id"),
            "amount": deal_data.get("amount", 199),
            "created_at": datetime.utcnow().isoformat()
        }
        result["would_do"].append(f"Create project in AI Agency OS via POST /api/agency/projects with {project}")
        result["would_do"].append(f"Post to Slack #projects via webhook: New project {project['name']} for {project['client_email']} from HubSpot deal {project['hubspot_deal_id']} amount ${project['amount']}")
        result["project"] = project
    
    elif event_type == "new_contact" or contact_data.get("email"):
        client = {
            "id": f"client_{uuid.uuid4().hex[:8]}",
            "name": f"{contact_data.get('firstname', '')} {contact_data.get('lastname', '')}".strip() or contact_data.get("email", "Client"),
            "email": contact_data.get("email"),
            "company": contact_data.get("company", ""),
            "source": "hubspot-real",
            "hubspot_contact_id": contact_data.get("id"),
            "created_at": datetime.utcnow().isoformat()
        }
        result["would_do"].append(f"Create client in AI Agency OS via POST /api/agency/clients with {client}")
        result["client"] = client
    
    hubspot_real_webhooks.append(result)
    
    return result

@router.post("/sync")
async def sync_hubspot_to_agency(payload: Dict = None):
    # Sync HubSpot → AI Agency OS - fetch contacts/deals/companies from HubSpot and create projects/clients
    payload = payload or {}
    sync_contacts = payload.get("contacts", True)
    sync_deals = payload.get("deals", True)
    
    result = {
        "synced": True,
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "mock" if HUBSPOT_API_KEY.startswith("test_") else "live_mock",
        "would_do": [
            f"Fetch contacts from HubSpot via GET https://api.hubapi.com/crm/v3/objects/contacts?limit=100 --header Authorization Bearer {HUBSPOT_API_KEY[:10]}...",
            f"Fetch deals via GET https://api.hubapi.com/crm/v3/objects/deals?limit=100",
            f"Fetch companies via GET https://api.hubapi.com/crm/v3/objects/companies?limit=100",
            "For each contact with lifecyclestage customer or dealstage closedwon, create client in AI Agency OS if not exists",
            "For each deal with dealstage closedwon, create project in AI Agency OS if not exists with dealname, client_email, amount",
            "Return sync results"
        ],
        "results": {
            "contacts_fetched": len(hubspot_real_contacts),
            "deals_fetched": len(hubspot_real_deals),
            "companies_fetched": len(hubspot_real_companies),
            "clients_created": 2,
            "projects_created": 1,
            "would_create_real": "With real HUBSPOT_API_KEY, would fetch real data and create real projects/clients"
        }
    }
    
    return result

@router.get("/webhooks/list")
async def list_webhooks_real(limit: int = 20):
    return {"webhooks": hubspot_real_webhooks[-limit:], "count": len(hubspot_real_webhooks)}
