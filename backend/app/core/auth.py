"""
Auth System - JWT + RBAC for SaaS multi-tenancy (Track B)
Inspired by Open WebUI auth + ECC security
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db, User, SessionLocal
import uuid

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Roles hierarchy
ROLES = {
    "super_admin": 100,
    "agency_owner": 80,
    "agency_member": 50,
    "client": 20,
    "user": 10
}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user

async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)), db: Session = Depends(get_db)):
    if not credentials:
        # Return default user for demo mode
        return User(id="default-user", username="demo", email="demo@ai-agency.os", role="agency_owner", is_active=True)
    
    try:
        return await get_current_user(credentials, db)
    except:
        return User(id="default-user", username="demo", email="demo@ai-agency.os", role="agency_owner", is_active=True)

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_level = ROLES.get(current_user.role, 0)
        required_level = ROLES.get(required_role, 0)
        if user_level < required_level:
            raise HTTPException(status_code=403, detail=f"Requires role {required_role}, you have {current_user.role}")
        return current_user
    return role_checker

def create_default_users():
    """Create default users for demo - Task A1: Security fix for prod"""
    from .config import settings
    import os
    
    # Task A1: In production, don't create demo accounts unless explicitly allowed
    if settings.ENV == "production" and not settings.ALLOW_DEMO_ACCOUNTS:
        print("🔒 Production mode: Demo accounts disabled (ALLOW_DEMO_ACCOUNTS=False)")
        # Only create admin from env var if provided
        admin_pass = os.getenv("ADMIN_PASSWORD")
        if admin_pass:
            db = SessionLocal()
            try:
                if not db.query(User).filter(User.username == "admin").first():
                    user = User(
                        id=str(uuid.uuid4()),
                        username="admin",
                        email=os.getenv("ADMIN_EMAIL", "admin@ai-agency.os"),
                        hashed_password=get_password_hash(admin_pass),
                        role="super_admin",
                        is_active=True
                    )
                    db.add(user)
                    db.commit()
                    print(f"✅ Admin user created from ADMIN_PASSWORD env var")
            finally:
                db.close()
        return
    
    # In dev/test, create demo accounts with warning
    if settings.ENV == "production" and settings.ALLOW_DEMO_ACCOUNTS:
        print("⚠️ WARNING: Demo accounts enabled in production (ALLOW_DEMO_ACCOUNTS=True) - NOT RECOMMENDED for real prod")
    else:
        print("⚠️ Demo accounts enabled - only for development (ENV != production or ALLOW_DEMO_ACCOUNTS=True)")
    
    db = SessionLocal()
    try:
        # Check if exists
        if db.query(User).filter(User.username == "admin").first():
            return
        
        # Use env var for admin password if provided, else default for dev
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        if settings.ENV != "production" and admin_password == "admin123":
            print("⚠️ Using default demo passwords - only for dev")
        
        users = [
            {"username": "admin", "email": "admin@ai-agency.os", "password": admin_password, "role": "super_admin"},
            {"username": "owner", "email": "owner@agency.com", "password": os.getenv("OWNER_PASSWORD", "owner123"), "role": "agency_owner"},
            {"username": "member", "email": "member@agency.com", "password": os.getenv("MEMBER_PASSWORD", "member123"), "role": "agency_member"},
            {"username": "client", "email": "client@example.com", "password": os.getenv("CLIENT_PASSWORD", "client123"), "role": "client"},
        ]
        
        for u in users:
            user = User(
                id=str(uuid.uuid4()),
                username=u["username"],
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                role=u["role"],
                is_active=True
            )
            db.add(user)
        
        # Default demo user
        if not db.query(User).filter(User.id == "default-user").first():
            demo = User(
                id="default-user",
                username="demo",
                email="demo@ai-agency.os",
                hashed_password=get_password_hash(os.getenv("DEMO_PASSWORD", "demo")),
                role="agency_owner",
                is_active=True
            )
            db.add(demo)
        
        db.commit()
        if settings.ENV != "production":
            print("✅ Default users created: admin/admin123, owner/owner123, member/member123, client/client123 (dev only)")
        else:
            print("✅ Demo users created in production (ALLOW_DEMO_ACCOUNTS=True) - change passwords via env vars")
    finally:
        db.close()

# Cost tracking (Track A1)
class CostTracker:
    """Track LLM costs per user/agency"""
    def __init__(self):
        self.costs = {}  # user_id -> {tokens, cost}
        # Pricing per 1k tokens (approx)
        self.pricing = {
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
            "llama3.1:8b": {"input": 0, "output": 0},  # local free
        }
    
    def track(self, user_id: str, model: str, prompt_tokens: int, completion_tokens: int):
        pricing = self.pricing.get(model, self.pricing["gpt-4o-mini"])
        cost = (prompt_tokens/1000)*pricing["input"] + (completion_tokens/1000)*pricing["output"]
        
        if user_id not in self.costs:
            self.costs[user_id] = {"prompt_tokens": 0, "completion_tokens": 0, "cost": 0, "requests": 0}
        
        self.costs[user_id]["prompt_tokens"] += prompt_tokens
        self.costs[user_id]["completion_tokens"] += completion_tokens
        self.costs[user_id]["cost"] += cost
        self.costs[user_id]["requests"] += 1
        
        return cost
    
    def get_user_cost(self, user_id: str):
        return self.costs.get(user_id, {"prompt_tokens": 0, "completion_tokens": 0, "cost": 0, "requests": 0})
    
    def get_all_costs(self):
        return self.costs

cost_tracker = CostTracker()
