"""
AI Agency OS - Core Configuration
Inspired by Open WebUI's config system + ECC's selective install
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = "AI Agency OS"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI Agency System - ECC + Open WebUI Hybrid"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Security - Task A2: Fix default secrets
    SECRET_KEY: str = ""  # Must be set via JWT_SECRET env var in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ENV: str = "development"  # development, production, test
    ALLOW_DEMO_ACCOUNTS: bool = True  # Set to False in production
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_agency.db"
    
    # LLM Providers - Like Open WebUI supports multiple providers
    # UnoRouter - Real provider $0 - https://api.unorouter.com/v1 - Working free model gemini-flash-lite:free
    OPENAI_API_KEY: Optional[str] = "sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR"
    OPENAI_BASE_URL: str = "https://api.unorouter.com/v1"
    
    UNOROUTER_API_KEY: Optional[str] = "sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR"
    UNOROUTER_BASE_URL: str = "https://api.unorouter.com/v1"
    
    ANTHROPIC_API_KEY: Optional[str] = None
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_ENABLED: bool = True
    
    # Default models - UnoRouter - Working free model gemini-flash-lite:free - Tested working 2026-09-13
    DEFAULT_MODEL: str = "gemini-flash-lite:free"
    ENABLED_MODELS: List[str] = ["gemini-flash-lite:free", "gemini-3.6-flash:free", "glm-4.7-flash:free", "claude-sonnet-4-5", "gpt-4o-mini"]
    
    # Memory & Vector DB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    MEMORY_MAX_CHARS: int = 10000
    INSTINCTS_ENABLED: bool = True
    
    # ECC-inspired features
    VERIFICATION_ENABLED: bool = True
    AGENT_SHIELD_ENABLED: bool = True
    HOOKS_ENABLED: bool = True
    CONTINUOUS_LEARNING: bool = True
    
    # Agency features
    MAX_CLIENTS: int = 100
    MAX_PROJECTS_PER_CLIENT: int = 50
    MAX_AGENTS_PER_PROJECT: int = 20
    
    # CORS - for Open WebUI-like preview support
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Task A2: Security - Fail fast if JWT_SECRET not set in production
import os
if settings.ENV == "production":
    jwt_secret = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY") or settings.SECRET_KEY
    if not jwt_secret or jwt_secret in ["ai-agency-os-secret-key-change-in-production", "super-secret-jwt-key-change-in-production", "change-me-in-production", ""]:
        raise ValueError("🔴 SECURITY CRITICAL: JWT_SECRET must be set in production via env var. Set JWT_SECRET to a strong random value (e.g. openssl rand -hex 32). Current value is default/empty.")
    settings.SECRET_KEY = jwt_secret
else:
    # In dev, allow default but warn
    if not settings.SECRET_KEY:
        settings.SECRET_KEY = "dev-secret-key-only-for-development-not-production"
        print("⚠️ Using dev SECRET_KEY - not for production")

# Ensure SECRET_KEY is set
if not settings.SECRET_KEY:
    settings.SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key-only-for-development-not-production")
    if settings.ENV == "production":
        raise ValueError("JWT_SECRET must be set in production")
