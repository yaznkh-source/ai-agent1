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
from .routers import chat, agents, skills, memory, tools, functions, pipelines, agency

# Initialize DB
init_db()

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

# Include routers
app.include_router(chat.router)
app.include_router(agents.router)
app.include_router(skills.router)
app.include_router(memory.router)
app.include_router(tools.router)
app.include_router(functions.router)
app.include_router(pipelines.router)
app.include_router(agency.router)

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "inspired_by": ["ECC (Everything Claude Code)", "Open WebUI"],
        "features": {
            "agents": "68 specialized agents (ECC-inspired)",
            "skills": "292 reusable skills",
            "tools": "Open WebUI-like tool calling",
            "functions": "Pipe, Filter, Action, Event (Open WebUI)",
            "pipelines": "OpenAI API compatible workflows",
            "memory": "Session persistence + Instincts continuous learning",
            "verification": "Build, test, lint, typecheck, security gate",
            "shield": "AgentShield security scanning",
            "agency": "Clients, Projects, Tasks management"
        },
        "endpoints": {
            "docs": "/api/docs",
            "chats": "/api/chats",
            "agents": "/api/agents",
            "skills": "/api/skills",
            "pipelines": "/api/pipelines",
            "agency": "/api/agency/dashboard"
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
