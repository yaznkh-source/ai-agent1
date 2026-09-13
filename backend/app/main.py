"""
AI Agency OS - Main FastAPI Application
Combines ECC + Open WebUI concepts into unified AI Agency System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .core.config import settings
from .core.database import init_db
from .routers import chat, agents, skills, memory, tools, functions, pipelines, agency, auth, knowledge, eval, integrations, billing, verification, marketplace, realtime, storage, audit, teams, zapier, hubspot
from .core.auth import create_default_users

# Initialize DB
init_db()
try:
    create_default_users()
except Exception as e:
    print(f"Auth init: {e}")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS - Critical for Open WebUI-like preview support
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - Track A-D
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(agents.router)
app.include_router(skills.router)
app.include_router(memory.router)
app.include_router(tools.router)
app.include_router(functions.router)
app.include_router(pipelines.router)
app.include_router(agency.router)
app.include_router(knowledge.router)
app.include_router(eval.router)
app.include_router(integrations.router)
app.include_router(billing.router)
app.include_router(verification.router)
app.include_router(marketplace.router)
app.include_router(realtime.router)
app.include_router(storage.router)
app.include_router(audit.router)
app.include_router(teams.router)
app.include_router(zapier.router)
app.include_router(hubspot.router)

@app.get("/")
async def root():
    from .agents.definitions import get_all_agents
    from .skills.manager import skill_manager
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "inspired_by": ["ECC (Everything Claude Code)", "Open WebUI"],
        "features": {
            "agents": f"{len(get_all_agents())} specialized agents (ECC-inspired, target 68)",
            "skills": f"{len(skill_manager.list_skills())} reusable skills (target 292)",
            "tools": "Open WebUI-like tool calling + 9 tools",
            "functions": "Pipe, Filter, Action, Event (Open WebUI)",
            "pipelines": "OpenAI API compatible workflows + 4 pipelines",
            "memory": "Session persistence + Instincts continuous learning + RAG",
            "verification": "Build, test, lint, typecheck, security gate (real + mock)",
            "shield": "AgentShield security scanning",
            "agency": "Clients, Projects, Tasks management",
            "auth": "JWT + RBAC + multi-tenancy",
            "knowledge": "ChromaDB + embeddings + collections",
            "eval": "Eval harness + agent router",
            "integrations": "Slack, Discord, GitHub, n8n, WhatsApp",
            "billing": "Tiers + usage + Stripe mock"
        },
        "endpoints": {
            "docs": "/api/docs",
            "chats": "/api/chats",
            "agents": "/api/agents",
            "skills": "/api/skills",
            "pipelines": "/api/pipelines",
            "agency": "/api/agency/dashboard",
            "auth": "/api/auth/demo-accounts",
            "knowledge": "/api/knowledge/collections",
            "eval": "/api/eval/datasets",
            "integrations": "/api/integrations/",
            "billing": "/api/billing/tiers"
        },
        "tracks": {
            "A": "Freelancer - LLM cost tracking + RAG + Client Portal",
            "B": "SaaS - Auth + Billing + Eval Harness",
            "C": "Team Tool - Real verification + GitHub + Slack",
            "D": "Intelligence - 35 agents + 30 skills + Router + Pipeline Builder"
        }
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": settings.VERSION}

@app.get("/api/config")
async def get_config():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "default_model": settings.DEFAULT_MODEL,
        "enabled_models": settings.ENABLED_MODELS,
        "features": {
            "verification": settings.VERIFICATION_ENABLED,
            "shield": settings.AGENT_SHIELD_ENABLED,
            "hooks": settings.HOOKS_ENABLED,
            "learning": settings.CONTINUOUS_LEARNING,
            "ollama": settings.OLLAMA_ENABLED
        }
    }

# Serve frontend if built
frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't intercept API routes
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        
        # Serve index.html for SPA routing
        index_path = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend not built"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
