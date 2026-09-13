"""
Marketplace Router - Skills, Pipelines, Agents Marketplace (Track B)
Inspired by Open WebUI community + ECC marketplace
"""
from fastapi import APIRouter
from typing import Dict, List
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

# Mock marketplace data
marketplace_items = {
    "skills": [
        {"id": "seo-audit-pro", "name": "SEO Audit Pro", "author": "seo-expert", "price": 29, "rating": 4.8, "downloads": 1250, "category": "content", "description": "Advanced SEO audit with Core Web Vitals, schema, and content analysis", "featured": True},
        {"id": "tdd-advanced", "name": "TDD Advanced", "author": "tdd-guru", "price": 0, "rating": 4.9, "downloads": 3400, "category": "development", "description": "Advanced TDD with mutation testing and property-based testing", "featured": True},
        {"id": "rag-enterprise", "name": "RAG Enterprise", "author": "ai-team", "price": 99, "rating": 4.7, "downloads": 890, "category": "ai", "description": "Enterprise RAG with HyDE, reranking, and self-RAG", "featured": False},
        {"id": "k8s-security", "name": "K8s Security Hardening", "author": "devops-pro", "price": 49, "rating": 4.6, "downloads": 650, "category": "operations", "description": "K8s security best practices, RBAC, NetworkPolicies, PodSecurity", "featured": False},
    ],
    "pipelines": [
        {"id": "saas-onboarding", "name": "SaaS Onboarding Flow", "author": "growth-team", "price": 0, "rating": 4.9, "downloads": 2100, "description": "Complete SaaS onboarding: research → proposal → plan → setup → email", "steps": 5, "featured": True},
        {"id": "content-factory", "name": "Content Factory", "author": "content-king", "price": 19, "rating": 4.8, "downloads": 1800, "description": "One long-form → 10 short-form across X, LinkedIn, Instagram, Blog", "steps": 6, "featured": True},
        {"id": "security-audit-full", "name": "Full Security Audit", "author": "security-team", "price": 0, "rating": 4.7, "downloads": 950, "description": "OWASP Top 10 + secrets + prompt injection + fix + verify", "steps": 4, "featured": False},
    ],
    "agents": [
        {"id": "seo-specialist-pro", "name": "SEO Specialist Pro", "author": "seo-expert", "price": 49, "rating": 4.8, "downloads": 780, "category": "content", "description": "Advanced SEO with technical + content + off-page + analytics", "featured": True},
        {"id": "sales-closer-elite", "name": "Sales Closer Elite", "author": "sales-guru", "price": 99, "rating": 4.9, "downloads": 450, "category": "operations", "description": "Elite closer with objection handling, negotiation, MEDDICC", "featured": False},
    ]
}

@router.get("/")
async def marketplace_home():
    return {
        "featured": {
            "skills": [s for s in marketplace_items["skills"] if s["featured"]],
            "pipelines": [p for p in marketplace_items["pipelines"] if p["featured"]],
            "agents": [a for a in marketplace_items["agents"] if a["featured"]],
        },
        "stats": {
            "total_skills": len(marketplace_items["skills"]) + 292,  # builtin + marketplace
            "total_pipelines": len(marketplace_items["pipelines"]) + 4,
            "total_agents": len(marketplace_items["agents"]) + 68,
            "total_downloads": sum(s["downloads"] for s in marketplace_items["skills"]) + sum(p["downloads"] for p in marketplace_items["pipelines"]),
            "total_authors": 150
        },
        "categories": ["development", "content", "ai", "operations", "security", "data", "planning"]
    }

@router.get("/skills")
async def list_marketplace_skills(category: str = None, sort: str = "popular", free_only: bool = False):
    skills = marketplace_items["skills"]
    if category:
        skills = [s for s in skills if s["category"] == category]
    if free_only:
        skills = [s for s in skills if s["price"] == 0]
    
    if sort == "popular":
        skills = sorted(skills, key=lambda x: x["downloads"], reverse=True)
    elif sort == "rating":
        skills = sorted(skills, key=lambda x: x["rating"], reverse=True)
    elif sort == "price_low":
        skills = sorted(skills, key=lambda x: x["price"])
    
    return {"skills": skills, "count": len(skills)}

@router.get("/pipelines")
async def list_marketplace_pipelines(sort: str = "popular", free_only: bool = False):
    pipelines = marketplace_items["pipelines"]
    if free_only:
        pipelines = [p for p in pipelines if p["price"] == 0]
    
    if sort == "popular":
        pipelines = sorted(pipelines, key=lambda x: x["downloads"], reverse=True)
    
    return {"pipelines": pipelines, "count": len(pipelines)}

@router.get("/agents")
async def list_marketplace_agents(category: str = None, sort: str = "popular"):
    agents = marketplace_items["agents"]
    if category:
        agents = [a for a in agents if a["category"] == category]
    
    if sort == "popular":
        agents = sorted(agents, key=lambda x: x["downloads"], reverse=True)
    
    return {"agents": agents, "count": len(agents)}

@router.get("/skill/{skill_id}")
async def get_marketplace_skill(skill_id: str):
    skill = next((s for s in marketplace_items["skills"] if s["id"] == skill_id), None)
    if not skill:
        from fastapi import HTTPException
        raise HTTPException(404, "Skill not found in marketplace")
    
    return {
        **skill,
        "content": f"# {skill['name']}\n\n{skill['description']}\n\nDetailed implementation...",
        "reviews": [
            {"user": "dev1", "rating": 5, "comment": "Excellent skill, saved hours!"},
            {"user": "agency_owner", "rating": 4, "comment": "Very useful for our workflow"},
        ],
        "versions": ["1.0.0", "1.1.0", "1.2.0"],
        "changelog": "v1.2.0: Added more examples\nv1.1.0: Fixed bug\nv1.0.0: Initial release"
    }

@router.post("/skill/{skill_id}/install")
async def install_marketplace_skill(skill_id: str, user_id: str = "default-user"):
    skill = next((s for s in marketplace_items["skills"] if s["id"] == skill_id), None)
    if not skill:
        from fastapi import HTTPException
        raise HTTPException(404, "Skill not found")
    
    # In production: copy skill to user's skills, handle payment if price > 0
    return {
        "installed": True,
        "skill_id": skill_id,
        "skill_name": skill["name"],
        "price": skill["price"],
        "message": f"Skill {skill['name']} installed! {'Payment processed' if skill['price']>0 else 'Free'}",
        "would_do": [
            "Copy skill content to backend/app/skills/definitions/",
            "If price > 0, process payment via Stripe",
            "Take 30% commission",
            "Increment download count",
            "Add to user's library"
        ]
    }

@router.get("/search")
async def search_marketplace(q: str, type: str = "all"):
    q_lower = q.lower()
    results = []
    
    if type in ["all", "skills"]:
        for skill in marketplace_items["skills"]:
            if q_lower in skill["name"].lower() or q_lower in skill["description"].lower():
                results.append({"type": "skill", **skill})
    
    if type in ["all", "pipelines"]:
        for pipe in marketplace_items["pipelines"]:
            if q_lower in pipe["name"].lower() or q_lower in pipe["description"].lower():
                results.append({"type": "pipeline", **pipe})
    
    if type in ["all", "agents"]:
        for agent in marketplace_items["agents"]:
            if q_lower in agent["name"].lower() or q_lower in agent["description"].lower():
                results.append({"type": "agent", **agent})
    
    return {"query": q, "type": type, "results": results, "count": len(results)}

@router.get("/author/{author_id}")
async def get_author(author_id: str):
    # Mock author
    return {
        "id": author_id,
        "name": author_id.replace("-", " ").title(),
        "bio": "Expert in AI agency workflows",
        "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={author_id}",
        "skills": [s for s in marketplace_items["skills"] if s["author"] == author_id],
        "pipelines": [p for p in marketplace_items["pipelines"] if p["author"] == author_id],
        "total_downloads": 5000,
        "rating": 4.8,
        "joined": "2024-01-15"
    }
