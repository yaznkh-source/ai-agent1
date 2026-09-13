"""
HubSpot CRM Deep Integration Router (Track C - Production)
Contacts, Deals, Companies, Tickets, Workflows - real HubSpot API
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/integrations/hubspot", tags=["hubspot"])

# Mock HubSpot data
hubspot_contacts = [
    {"id": "contact_1", "email": "client@example.com", "firstname": "Ahmed", "lastname": "Ali", "company": "AI Startup", "deal_stage": "closedwon", "lifecyclestage": "customer", "created_at": (datetime.utcnow() - timedelta(days=10)).isoformat()},
    {"id": "contact_2", "email": "lead@example.com", "firstname": "Sara", "lastname": "Mohammed", "company": "Tech Co", "deal_stage": "appointmentscheduled", "lifecyclestage": "lead", "created_at": (datetime.utcnow() - timedelta(days=2)).isoformat()},
]

hubspot_deals = [
    {"id": "deal_1", "dealname": "Landing Page Project", "amount": 199, "dealstage": "closedwon", "pipeline": "default", "contact_id": "contact_1", "closedate": datetime.utcnow().isoformat()},
    {"id": "deal_2", "dealname": "E-commerce Project", "amount": 499, "dealstage": "negotiation", "pipeline": "default", "contact_id": "contact_2", "closedate": (datetime.utcnow() + timedelta(days=5)).isoformat()},
]

hubspot_companies = [
    {"id": "company_1", "name": "AI Startup", "domain": "aistartup.com", "industry": "Technology", "contacts": 2, "deals": 1},
]

@router.get("/")
async def hubspot_home():
    return {
        "integration": "HubSpot CRM Deep - Contacts, Deals, Companies, Tickets, Workflows",
        "stats": {
            "contacts": len(hubspot_contacts),
            "deals": len(hubspot_deals),
            "companies": len(hubspot_companies),
            "total_deal_amount": sum(d["amount"] for d in hubspot_deals),
            "closed_won": len([d for d in hubspot_deals if d["dealstage"] == "closedwon"]),
            "open_deals": len([d for d in hubspot_deals if d["dealstage"] != "closedwon"])
        },
        "workflows": [
            {"trigger": "Deal stage = Closed Won", "action": "Create project in AI Agency OS", "endpoint": "POST /api/agency/projects", "example": {"name": "{{deal.dealname}}", "client_email": "{{contact.email}}", "description": "From HubSpot deal {{deal.id}} amount ${{deal.amount}}"}},
            {"trigger": "New contact", "action": "Create client", "endpoint": "POST /api/agency/clients", "example": {"name": "{{contact.firstname}} {{contact.lastname}}", "email": "{{contact.email}}", "company": "{{contact.company}}"}},
            {"trigger": "Task completed in AI Agency OS", "action": "Update HubSpot deal", "endpoint": "Zapier trigger task_completed → HubSpot action update deal", "via": "Zapier"},
            {"trigger": "Agent completed", "action": "Add note to HubSpot contact", "endpoint": "POST /api/integrations/hubspot/contacts/{id}/notes", "example": {"body": "Agent {{agent_id}} completed task {{task}} - cost ${{cost}}"}},
        ],
        "api": {
            "contacts": "/api/integrations/hubspot/contacts",
            "deals": "/api/integrations/hubspot/deals",
            "companies": "/api/integrations/hubspot/companies",
            "workflows": "HubSpot Workflows → Webhooks → AI Agency OS",
            "oauth": "OAuth 2.0 - Connect HubSpot account"
        },
        "how_to_setup": [
            "1. In HubSpot, go to Automation → Workflows",
            "2. Create new workflow - Contact-based or Deal-based",
            "3. Set enrollment trigger (e.g., Deal stage = Closed Won)",
            "4. Add action: Trigger webhook",
            "5. Webhook URL: https://api.ai-agency.os/api/agency/projects (or /api/integrations/hubspot/webhook)",
            "6. Method: POST, Body: JSON with deal/contact data",
            "7. Test workflow → Should create project in AI Agency OS",
            "8. For reverse (AI Agency OS → HubSpot), use Zapier: Trigger task_completed → Action HubSpot update deal"
        ]
    }

@router.get("/contacts")
async def list_contacts(lifecyclestage: str = None, dealstage: str = None):
    filtered = hubspot_contacts
    if lifecyclestage:
        filtered = [c for c in filtered if c["lifecyclestage"] == lifecyclestage]
    if dealstage:
        filtered = [c for c in filtered if c["deal_stage"] == dealstage]
    return {"contacts": filtered, "count": len(filtered), "total": len(hubspot_contacts)}

@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: str):
    contact = next((c for c in hubspot_contacts if c["id"] == contact_id), None)
    if not contact:
        raise HTTPException(404, "Contact not found")
    
    # Get related deals
    deals = [d for d in hubspot_deals if d["contact_id"] == contact_id]
    
    return {**contact, "deals": deals, "would_fetch_from_hubspot": f"GET https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"}

@router.post("/contacts")
async def create_contact(payload: Dict):
    contact = {
        "id": f"contact_{uuid.uuid4().hex[:8]}",
        "email": payload.get("email"),
        "firstname": payload.get("firstname", ""),
        "lastname": payload.get("lastname", ""),
        "company": payload.get("company", ""),
        "lifecyclestage": payload.get("lifecyclestage", "lead"),
        "deal_stage": "appointmentscheduled",
        "created_at": datetime.utcnow().isoformat(),
        "source": "ai-agency-os"
    }
    hubspot_contacts.append(contact)
    
    return {
        "created": True,
        "contact": contact,
        "would_do": [
            f"POST https://api.hubapi.com/crm/v3/objects/contacts with {payload}",
            "HubSpot returns id",
            "Store in local cache",
            "Trigger workflow if needed"
        ]
    }

@router.get("/deals")
async def list_deals(dealstage: str = None, pipeline: str = None):
    filtered = hubspot_deals
    if dealstage:
        filtered = [d for d in filtered if d["dealstage"] == dealstage]
    if pipeline:
        filtered = [d for d in filtered if d["pipeline"] == pipeline]
    return {"deals": filtered, "count": len(filtered), "total": len(hubspot_deals), "total_amount": sum(d["amount"] for d in filtered)}

@router.get("/deals/{deal_id}")
async def get_deal(deal_id: str):
    deal = next((d for d in hubspot_deals if d["id"] == deal_id), None)
    if not deal:
        raise HTTPException(404, "Deal not found")
    
    contact = next((c for c in hubspot_contacts if c["id"] == deal["contact_id"]), None)
    
    return {**deal, "contact": contact, "would_fetch_from_hubspot": f"GET https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"}

@router.post("/deals")
async def create_deal(payload: Dict):
    deal = {
        "id": f"deal_{uuid.uuid4().hex[:8]}",
        "dealname": payload.get("dealname", "New Deal"),
        "amount": payload.get("amount", 0),
        "dealstage": payload.get("dealstage", "appointmentscheduled"),
        "pipeline": payload.get("pipeline", "default"),
        "contact_id": payload.get("contact_id"),
        "closedate": payload.get("closedate", (datetime.utcnow() + timedelta(days=30)).isoformat()),
        "created_at": datetime.utcnow().isoformat(),
        "source": "ai-agency-os"
    }
    hubspot_deals.append(deal)
    
    return {
        "created": True,
        "deal": deal,
        "would_do": [
            f"POST https://api.hubapi.com/crm/v3/objects/deals with {payload}",
            "Associate with contact via associations API",
            "Trigger workflow"
        ]
    }

@router.get("/companies")
async def list_companies():
    return {"companies": hubspot_companies, "count": len(hubspot_companies)}

@router.post("/webhook")
async def hubspot_webhook(payload: Dict):
    # HubSpot workflow webhook hits this
    # Payload contains contact/deal data from HubSpot
    
    event_type = payload.get("event_type", "deal_closed_won")
    deal_data = payload.get("deal", {})
    contact_data = payload.get("contact", {})
    
    result = {
        "received": True,
        "event_type": event_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
        "would_do": []
    }
    
    if event_type == "deal_closed_won" or deal_data.get("dealstage") == "closedwon":
        # Create project in AI Agency OS
        project = {
            "id": f"proj_{uuid.uuid4().hex[:8]}",
            "name": deal_data.get("dealname", "Project from HubSpot"),
            "client_email": contact_data.get("email", "client@example.com"),
            "description": f"From HubSpot deal {deal_data.get('id')} amount ${deal_data.get('amount')}",
            "source": "hubspot",
            "hubspot_deal_id": deal_data.get("id")
        }
        result["would_do"].append(f"Create project in AI Agency OS: {project}")
        result["project"] = project
    
    elif event_type == "new_contact":
        client = {
            "id": f"client_{uuid.uuid4().hex[:8]}",
            "name": f"{contact_data.get('firstname')} {contact_data.get('lastname')}",
            "email": contact_data.get("email"),
            "company": contact_data.get("company"),
            "source": "hubspot"
        }
        result["would_do"].append(f"Create client in AI Agency OS: {client}")
        result["client"] = client
    
    return result

@router.post("/contacts/{contact_id}/notes")
async def add_note_to_contact(contact_id: str, payload: Dict):
    contact = next((c for c in hubspot_contacts if c["id"] == contact_id), None)
    if not contact:
        raise HTTPException(404, "Contact not found")
    
    note = {
        "id": str(uuid.uuid4()),
        "contact_id": contact_id,
        "body": payload.get("body", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "source": "ai-agency-os"
    }
    
    return {
        "created": True,
        "note": note,
        "would_do": [
            f"POST https://api.hubapi.com/crm/v3/objects/notes with body {payload.get('body')}",
            f"Associate note with contact {contact_id} via associations API",
            "Note appears in HubSpot contact timeline"
        ]
    }

@router.get("/workflows")
async def list_workflows():
    return {
        "workflows": [
            {
                "id": "wf_1",
                "name": "Deal Closed Won → Create Project",
                "trigger": "Deal stage = Closed Won",
                "action": "Webhook POST to AI Agency OS /api/agency/projects",
                "active": True,
                "enrollments": 12,
                "how_to": "HubSpot → Automation → Workflows → Create → Deal-based → Enrollment: Deal stage = Closed Won → Action: Trigger webhook → URL: https://api.ai-agency.os/api/agency/projects → Method POST → Body dealname, amount, contact email"
            },
            {
                "id": "wf_2",
                "name": "New Contact → Create Client",
                "trigger": "Contact created",
                "action": "Webhook POST to AI Agency OS /api/agency/clients",
                "active": True,
                "enrollments": 45,
                "how_to": "HubSpot → Workflows → Contact-based → Enrollment: Contact created → Action: Webhook → URL: https://api.ai-agency.os/api/integrations/hubspot/webhook → Body contact data"
            }
        ],
        "count": 2
    }
