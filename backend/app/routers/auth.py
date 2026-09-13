"""
Auth Router - JWT + RBAC (Track B1)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, User
from ..core.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, get_current_user_optional, cost_tracker,
    create_default_users
)
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

# Initialize default users on import
try:
    create_default_users()
except:
    pass

@router.post("/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == req.username) | (User.email == req.username)).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    
    token = create_access_token({"sub": user.id, "role": user.role, "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/register")
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == req.username) | (User.email == req.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    import uuid
    user = User(
        id=str(uuid.uuid4()),
        username=req.username,
        email=req.email,
        hashed_password=get_password_hash(req.password),
        role=req.role if req.role in ["user", "client"] else "user",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": user.id, "role": user.role, "username": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

@router.get("/users")
async def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Only admin/owner can list
    if current_user.role not in ["super_admin", "agency_owner"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    users = db.query(User).all()
    return [{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role,
        "is_active": u.is_active,
        "created_at": u.created_at.isoformat() if u.created_at else None
    } for u in users]

@router.get("/costs")
async def get_costs(current_user: User = Depends(get_current_user_optional)):
    # Cost tracking (Track A1)
    if current_user.role in ["super_admin", "agency_owner"]:
        return cost_tracker.get_all_costs()
    else:
        return {current_user.id: cost_tracker.get_user_cost(current_user.id)}

@router.get("/costs/me")
async def get_my_costs(current_user: User = Depends(get_current_user_optional)):
    return cost_tracker.get_user_cost(current_user.id)

@router.get("/demo-accounts")
async def demo_accounts():
    return {
        "accounts": [
            {"username": "admin", "password": "admin123", "role": "super_admin", "desc": "Full access"},
            {"username": "owner", "password": "owner123", "role": "agency_owner", "desc": "Agency owner"},
            {"username": "member", "password": "member123", "role": "agency_member", "desc": "Team member"},
            {"username": "client", "password": "client123", "role": "client", "desc": "Client view"},
            {"username": "demo", "password": "demo", "role": "agency_owner", "desc": "Demo (default)"},
        ],
        "note": "Use POST /api/auth/login to get token, then use Authorization: Bearer <token>"
    }
