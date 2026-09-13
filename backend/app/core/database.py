"""
Database layer - SQLite with SQLAlchemy
Inspired by Open WebUI's persistence + ECC's memory hooks
"""
from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime, Boolean, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from .config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === Models ===

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # admin, user, client
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    title = Column(String, default="New Chat")
    model = Column(String, default="gpt-4o-mini")
    agent_id = Column(String, nullable=True)  # ECC agent
    project_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta = Column(JSON, default={})

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String, index=True)
    role = Column(String)  # user, assistant, system, tool
    content = Column(Text)
    tool_calls = Column(JSON, nullable=True)
    model = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})

class Memory(Base):
    __tablename__ = "memories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    chat_id = Column(String, nullable=True)
    type = Column(String)  # session_summary, fact, instinct, skill_usage
    content = Column(Text)
    embedding = Column(JSON, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})

class Instinct(Base):
    __tablename__ = "instincts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pattern = Column(String)  # pattern name
    description = Column(Text)
    trigger = Column(String)
    action = Column(Text)
    confidence = Column(Float, default=0.5)
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    description = Column(Text)
    content = Column(Text)  # SKILL.md content
    enabled = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentModel(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True)
    name = Column(String)
    role = Column(String)
    description = Column(Text)
    system_prompt = Column(Text)
    skills = Column(JSON, default=[])  # list of skill ids
    tools = Column(JSON, default=[])  # list of tool ids
    model = Column(String, default="gpt-4o-mini")
    enabled = Column(Boolean, default=True)
    category = Column(String)  # planning, development, review, research, etc
    created_at = Column(DateTime, default=datetime.utcnow)

class ToolModel(Base):
    __tablename__ = "tools"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    schema = Column(JSON)  # OpenAI function calling schema
    code = Column(Text, nullable=True)  # Python code for tool
    enabled = Column(Boolean, default=True)
    category = Column(String)

class FunctionModel(Base):
    __tablename__ = "functions"
    id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)  # pipe, filter, action, event
    description = Column(Text)
    code = Column(Text)
    valves = Column(JSON, default={})  # config like Open WebUI Valves
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PipelineModel(Base):
    __tablename__ = "pipelines"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    steps = Column(JSON, default=[])  # list of steps
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")
    # Task A9: Tenant isolation - owner_id and tenant_id
    owner_id = Column(String, index=True, nullable=True)  # User who owns this client
    tenant_id = Column(String, index=True, nullable=True)  # Tenant isolation
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, index=True)
    name = Column(String)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")  # active, completed, paused
    workflow = Column(JSON, default={})  # workflow definition
    agents = Column(JSON, default=[])  # assigned agents
    # Task A9: Tenant isolation
    owner_id = Column(String, index=True, nullable=True)  # User who owns this project
    tenant_id = Column(String, index=True, nullable=True)  # Tenant isolation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta = Column(JSON, default={})

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo")  # todo, in_progress, review, done
    priority = Column(String, default="medium")
    assigned_agent = Column(String, nullable=True)
    skill_used = Column(String, nullable=True)
    # Task A9: Tenant isolation
    owner_id = Column(String, index=True, nullable=True)
    tenant_id = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta = Column(JSON, default={})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
