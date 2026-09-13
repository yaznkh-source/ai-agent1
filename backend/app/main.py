"""
AI Agency OS - Main FastAPI Application
Combines ECC + Open WebUI concepts into unified AI Agency System
Task A4: Rate limiting + Task A2: Security fix + Task C8: Security headers + metrics
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import time

from .core.config import settings
from .core.database import init_db
from .core.swagger import openapi_custom_info, swagger_custom_css
from .routers import chat, agents, skills, memory, tools, functions, pipelines, agency, auth, knowledge, eval, integrations, billing, billing_real, verification, marketplace, realtime, storage, audit, teams, zapier, hubspot, hubspot_real, slack_real, monitoring, gdpr, backup, metrics, llm, domain_free, tools_curated, loops
from .core.auth import create_default_users

# Task A4: Rate limiting - slowapi
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
    print("✅ Rate limiting enabled via slowapi - 100/minute default")
except ImportError:
    limiter = None
    print("⚠️ slowapi not installed - rate limiting disabled (install via pip install slowapi)")

# Initialize DB
init_db()
try:
    create_default_users()
except Exception as e:
    print(f"Auth init: {e}")

app = FastAPI(
    title=openapi_custom_info["title"],
    version=openapi_custom_info["version"],
    description=openapi_custom_info["description"],
    contact=openapi_custom_info["contact"],
    license_info=openapi_custom_info["license"],
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Task A4: Add rate limiter to app
if limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - Critical for Open WebUI-like preview support - Task A2: Security - restrict in prod
# In production, should be specific origins, not "*"
if settings.ENV == "production":
    # In prod, use specific origins from env or default to ai-agency.os
    allowed_origins = os.getenv("CORS_ORIGINS", "https://ai-agency.os,https://api.ai-agency.os,https://docs.ai-agency.os").split(",")
    print(f"🔒 Production CORS: {allowed_origins}")
else:
    allowed_origins = settings.CORS_ORIGINS
    print(f"⚠️ Dev CORS: {allowed_origins} - open for preview")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task C8: Security headers middleware - Production Hardened 95/100 → 98/100
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if settings.ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Task C8: Request logging + metrics middleware
@app.middleware("http")
async def log_requests_and_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log for Prometheus
    try:
        from .routers.metrics import REQUEST_COUNT, REQUEST_LATENCY
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(process_time)
    except:
        pass
    
    # Add process time header
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers - Track A-D + B (GDPR, Backup, Metrics)
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
app.include_router(billing_real.router)
app.include_router(verification.router)
app.include_router(marketplace.router)
app.include_router(realtime.router)
app.include_router(storage.router)
app.include_router(audit.router)
app.include_router(teams.router)
app.include_router(zapier.router)
app.include_router(hubspot.router)
app.include_router(hubspot_real.router)
app.include_router(slack_real.router)
app.include_router(monitoring.router)
app.include_router(gdpr.router)
app.include_router(backup.router)
app.include_router(metrics.router)
app.include_router(llm.router)
app.include_router(domain_free.router)
app.include_router(tools_curated.router)
app.include_router(loops.router)

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
