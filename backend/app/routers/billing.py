"""
Billing Router - Track B2
Subscription tiers + usage tracking + Stripe mock
"""
from fastapi import APIRouter
from typing import Dict
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/api/billing", tags=["billing"])

# Subscription tiers
TIERS = {
    "free": {
        "name": "Free",
        "price": 0,
        "currency": "USD",
        "interval": "month",
        "features": {
            "agents": 5,
            "projects": 2,
            "tasks_per_month": 20,
            "llm_tokens": 100000,
            "knowledge_docs": 10,
            "members": 1
        },
        "stripe_price_id": "price_free"
    },
    "starter": {
        "name": "Starter",
        "price": 49,
        "currency": "USD",
        "interval": "month",
        "features": {
            "agents": 15,
            "projects": 10,
            "tasks_per_month": 200,
            "llm_tokens": 1000000,
            "knowledge_docs": 100,
            "members": 3
        },
        "stripe_price_id": "price_starter_49"
    },
    "pro": {
        "name": "Pro",
        "price": 199,
        "currency": "USD",
        "interval": "month",
        "features": {
            "agents": 35,
            "projects": 100,
            "tasks_per_month": 2000,
            "llm_tokens": 10000000,
            "knowledge_docs": 1000,
            "members": 10
        },
        "stripe_price_id": "price_pro_199",
        "popular": True
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 999,
        "currency": "USD",
        "interval": "month",
        "features": {
            "agents": 68,
            "projects": 1000,
            "tasks_per_month": 10000,
            "llm_tokens": 100000000,
            "knowledge_docs": 10000,
            "members": 100,
            "dedicated_support": True,
            "custom_agents": True,
            "sso": True
        },
        "stripe_price_id": "price_enterprise_999"
    }
}

# In-memory subscriptions
subscriptions = {}

@router.get("/tiers")
async def list_tiers():
    return {"tiers": TIERS}

@router.get("/tiers/{tier_id}")
async def get_tier(tier_id: str):
    tier = TIERS.get(tier_id)
    if not tier:
        from fastapi import HTTPException
        raise HTTPException(404, "Tier not found")
    return tier

@router.post("/subscribe")
async def subscribe(payload: dict):
    tier_id = payload.get("tier_id", "free")
    user_id = payload.get("user_id", "default-user")
    email = payload.get("email", "demo@ai-agency.os")
    
    tier = TIERS.get(tier_id)
    if not tier:
        from fastapi import HTTPException
        raise HTTPException(404, "Tier not found")
    
    sub_id = str(uuid.uuid4())
    subscription = {
        "id": sub_id,
        "user_id": user_id,
        "tier_id": tier_id,
        "tier": tier,
        "status": "active" if tier_id == "free" else "pending_payment",
        "current_period_start": datetime.utcnow().isoformat(),
        "current_period_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "email": email,
        "stripe_subscription_id": f"sub_{sub_id[:8]}" if tier_id != "free" else None
    }
    
    subscriptions[user_id] = subscription
    
    return {
        "subscription": subscription,
        "checkout_url": f"https://checkout.stripe.com/pay/{sub_id}" if tier_id != "free" else None,
        "message": "Free tier activated!" if tier_id == "free" else f"Redirect to Stripe for {tier['name']} - ${tier['price']}/month"
    }

@router.get("/subscription/{user_id}")
async def get_subscription(user_id: str):
    sub = subscriptions.get(user_id)
    if not sub:
        # Default to free
        return {
            "user_id": user_id,
            "tier_id": "free",
            "tier": TIERS["free"],
            "status": "active",
            "usage": {
                "projects": 0,
                "tasks_this_month": 0,
                "tokens_used": 0,
                "docs": 0
            }
        }
    
    # Mock usage
    from ..core.auth import cost_tracker
    cost_data = cost_tracker.get_user_cost(user_id)
    
    return {
        **sub,
        "usage": {
            "projects": 2,
            "tasks_this_month": cost_data["requests"],
            "tokens_used": cost_data["prompt_tokens"] + cost_data["completion_tokens"],
            "tokens_limit": sub["tier"]["features"]["llm_tokens"],
            "cost": cost_data["cost"],
            "cost_limit": sub["tier"]["price"] * 2  # Rough
        },
        "profitability": {
            "revenue": sub["tier"]["price"],
            "llm_cost": cost_data["cost"],
            "gross_profit": sub["tier"]["price"] - cost_data["cost"],
            "margin": f"{((sub['tier']['price'] - cost_data['cost']) / sub['tier']['price'] * 100) if sub['tier']['price'] > 0 else 0:.1f}%"
        }
    }

@router.get("/usage/{user_id}")
async def get_usage(user_id: str):
    from ..core.auth import cost_tracker
    cost_data = cost_tracker.get_user_cost(user_id)
    sub = subscriptions.get(user_id, {"tier_id": "free", "tier": TIERS["free"]})
    
    return {
        "user_id": user_id,
        "tier": sub["tier_id"],
        "usage": cost_data,
        "limits": sub["tier"]["features"],
        "percent_used": {
            "tokens": (cost_data["prompt_tokens"] + cost_data["completion_tokens"]) / sub["tier"]["features"]["llm_tokens"] * 100 if sub["tier"]["features"]["llm_tokens"] > 0 else 0
        }
    }

@router.post("/webhook/stripe")
async def stripe_webhook(payload: dict):
    """Mock Stripe webhook"""
    event_type = payload.get("type", "unknown")
    
    return {
        "received": True,
        "event": event_type,
        "would_do": {
            "checkout.session.completed": "Activate subscription",
            "invoice.payment_succeeded": "Extend period",
            "invoice.payment_failed": "Mark past_due, notify",
            "customer.subscription.deleted": "Downgrade to free"
        }.get(event_type, "Log event")
    }
