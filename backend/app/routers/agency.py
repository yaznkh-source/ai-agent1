"""
Agency router - AI Agency OS specific: clients, projects, tasks
Combines ECC's orchestration + Open WebUI's workspace concept
Task A9: Tenant isolation - owner_id, tenant_id
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Client, Project, Task, SessionLocal
from ..models.schemas import ClientCreate, ProjectCreate, TaskCreate
from ..verification.loop import verification_loop
from ..core.security import shield
from ..core.auth import get_current_user_optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/agency", tags=["agency"])

# === Clients === - Task A9: Tenant isolation
@router.get("/clients")
async def list_clients(db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    # Task A9: Filter by owner_id for non-admin users
    q = db.query(Client)
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(current_user, 'id'):
            q = q.filter((Client.owner_id == current_user.id) | (Client.owner_id == None))
    clients = q.order_by(Client.created_at.desc()).all()
    return [{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "company": c.company,
        "description": c.description,
        "status": c.status,
        "owner_id": getattr(c, 'owner_id', None),
        "tenant_id": getattr(c, 'tenant_id', None),
        "created_at": c.created_at.isoformat(),
        "meta": c.meta
    } for c in clients]

@router.post("/clients")
async def create_client(client: ClientCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    # Task A9: Set owner_id and tenant_id
    owner_id = getattr(current_user, 'id', None) if current_user else None
    tenant_id = getattr(current_user, 'id', None) if current_user else None
    new_client = Client(
        id=str(uuid.uuid4()),
        name=client.name,
        email=client.email,
        company=client.company,
        description=client.description,
        owner_id=owner_id,
        tenant_id=tenant_id,
        meta=client.meta or {}
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"id": new_client.id, "name": new_client.name, "owner_id": owner_id, "tenant_id": tenant_id}

@router.get("/clients/{client_id}")
async def get_client(client_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")
    # Task A9: Check tenant isolation
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(client, 'owner_id') and client.owner_id and current_user.id != client.owner_id:
            raise HTTPException(403, "Forbidden - not your client")
    
    projects = db.query(Project).filter(Project.client_id == client_id).all()
    # Filter projects by tenant if needed
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        projects = [p for p in projects if not getattr(p, 'owner_id', None) or p.owner_id == current_user.id]
    
    return {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "company": client.company,
        "description": client.description,
        "status": client.status,
        "owner_id": getattr(client, 'owner_id', None),
        "tenant_id": getattr(client, 'tenant_id', None),
        "created_at": client.created_at.isoformat(),
        "projects": [{"id": p.id, "name": p.name, "status": p.status} for p in projects],
        "meta": client.meta
    }

@router.delete("/clients/{client_id}")
async def delete_client(client_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")
    # Task A9: Check ownership
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(client, 'owner_id') and client.owner_id and current_user.id != client.owner_id:
            raise HTTPException(403, "Forbidden - not your client")
    db.delete(client)
    db.commit()
    return {"deleted": True}

# === Projects === - Task A9: Tenant isolation
@router.get("/projects")
async def list_projects(client_id: str = None, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    q = db.query(Project)
    if client_id:
        q = q.filter(Project.client_id == client_id)
    # Task A9: Filter by owner_id for non-admin
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(current_user, 'id'):
            q = q.filter((Project.owner_id == current_user.id) | (Project.owner_id == None))
    projects = q.order_by(Project.updated_at.desc()).all()
    return [{
        "id": p.id,
        "client_id": p.client_id,
        "name": p.name,
        "description": p.description,
        "status": p.status,
        "agents": p.agents,
        "owner_id": getattr(p, 'owner_id', None),
        "tenant_id": getattr(p, 'tenant_id', None),
        "created_at": p.created_at.isoformat(),
        "updated_at": p.updated_at.isoformat(),
        "meta": p.meta
    } for p in projects]

@router.post("/projects")
async def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    owner_id = getattr(current_user, 'id', None) if current_user else None
    tenant_id = getattr(current_user, 'id', None) if current_user else None
    new_project = Project(
        id=str(uuid.uuid4()),
        client_id=project.client_id,
        name=project.name,
        description=project.description,
        workflow=project.workflow or {},
        agents=project.agents or [],
        owner_id=owner_id,
        tenant_id=tenant_id,
        meta=project.meta or {}
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"id": new_project.id, "name": new_project.name, "owner_id": owner_id, "tenant_id": tenant_id}

@router.get("/projects/{project_id}")
async def get_project(project_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    # Task A9: Check ownership
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(project, 'owner_id') and project.owner_id and current_user.id != project.owner_id:
            raise HTTPException(403, "Forbidden - not your project")
    
    tasks = db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).all()
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        tasks = [t for t in tasks if not getattr(t, 'owner_id', None) or t.owner_id == current_user.id]
    client = db.query(Client).filter(Client.id == project.client_id).first()
    
    return {
        "id": project.id,
        "client_id": project.client_id,
        "client_name": client.name if client else None,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "workflow": project.workflow,
        "agents": project.agents,
        "owner_id": getattr(project, 'owner_id', None),
        "tenant_id": getattr(project, 'tenant_id', None),
        "tasks": [{
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "assigned_agent": t.assigned_agent
        } for t in tasks],
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat(),
        "meta": project.meta
    }

@router.put("/projects/{project_id}")
async def update_project(project_id: str, updates: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(project, 'owner_id') and project.owner_id and current_user.id != project.owner_id:
            raise HTTPException(403, "Forbidden - not your project")
    
    for key, value in updates.items():
        if hasattr(project, key) and key not in ["id", "owner_id", "tenant_id"]:
            setattr(project, key, value)
    project.updated_at = datetime.utcnow()
    db.commit()
    return {"updated": True}

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(project, 'owner_id') and project.owner_id and current_user.id != project.owner_id:
            raise HTTPException(403, "Forbidden - not your project")
    db.query(Task).filter(Task.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    return {"deleted": True}

# === Tasks === - Task A9
@router.get("/tasks")
async def list_tasks(project_id: str = None, status: str = None, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    q = db.query(Task)
    if project_id:
        q = q.filter(Task.project_id == project_id)
    if status:
        q = q.filter(Task.status == status)
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(current_user, 'id'):
            q = q.filter((Task.owner_id == current_user.id) | (Task.owner_id == None))
    tasks = q.order_by(Task.updated_at.desc()).all()
    return [{
        "id": t.id,
        "project_id": t.project_id,
        "title": t.title,
        "description": t.description,
        "status": t.status,
        "priority": t.priority,
        "assigned_agent": t.assigned_agent,
        "skill_used": t.skill_used,
        "owner_id": getattr(t, 'owner_id', None),
        "tenant_id": getattr(t, 'tenant_id', None),
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
        "meta": t.meta
    } for t in tasks]

@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    owner_id = getattr(current_user, 'id', None) if current_user else None
    tenant_id = getattr(current_user, 'id', None) if current_user else None
    new_task = Task(
        id=str(uuid.uuid4()),
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assigned_agent=task.assigned_agent,
        skill_used=task.skill_used,
        owner_id=owner_id,
        tenant_id=tenant_id,
        meta=task.meta or {}
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"id": new_task.id, "title": new_task.title, "owner_id": owner_id}

@router.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(task, 'owner_id') and task.owner_id and current_user.id != task.owner_id:
            raise HTTPException(403, "Forbidden - not your task")
    return {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "assigned_agent": task.assigned_agent,
        "skill_used": task.skill_used,
        "owner_id": getattr(task, 'owner_id', None),
        "tenant_id": getattr(task, 'tenant_id', None),
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "meta": task.meta
    }

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, updates: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(task, 'owner_id') and task.owner_id and current_user.id != task.owner_id:
            raise HTTPException(403, "Forbidden - not your task")
    for key, value in updates.items():
        if hasattr(task, key) and key not in ["id", "owner_id", "tenant_id"]:
            setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    db.commit()
    return {"updated": True}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(task, 'owner_id') and task.owner_id and current_user.id != task.owner_id:
            raise HTTPException(403, "Forbidden - not your task")
    db.delete(task)
    db.commit()
    return {"deleted": True}

# === Dashboard & Verification ===
@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    # Task A9: Filter stats by tenant for non-admin
    q_clients = db.query(Client)
    q_projects = db.query(Project)
    q_tasks = db.query(Task)
    
    if current_user and hasattr(current_user, 'role') and current_user.role not in ["super_admin", "agency_owner"]:
        if hasattr(current_user, 'id'):
            q_clients = q_clients.filter((Client.owner_id == current_user.id) | (Client.owner_id == None))
            q_projects = q_projects.filter((Project.owner_id == current_user.id) | (Project.owner_id == None))
            q_tasks = q_tasks.filter((Task.owner_id == current_user.id) | (Task.owner_id == None))
    
    clients_count = q_clients.count()
    projects_count = q_projects.count()
    tasks_count = q_tasks.count()
    tasks_todo = q_tasks.filter(Task.status == "todo").count()
    tasks_in_progress = q_tasks.filter(Task.status == "in_progress").count()
    tasks_done = q_tasks.filter(Task.status == "done").count()
    
    recent_projects = q_projects.order_by(Project.updated_at.desc()).limit(5).all()
    recent_tasks = q_tasks.order_by(Task.updated_at.desc()).limit(10).all()
    
    return {
        "stats": {
            "clients": clients_count,
            "projects": projects_count,
            "tasks": tasks_count,
            "tasks_todo": tasks_todo,
            "tasks_in_progress": tasks_in_progress,
            "tasks_done": tasks_done,
            "completion_rate": round(tasks_done / tasks_count * 100, 1) if tasks_count > 0 else 0
        },
        "recent_projects": [{"id": p.id, "name": p.name, "status": p.status, "updated_at": p.updated_at.isoformat()} for p in recent_projects],
        "recent_tasks": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority} for t in recent_tasks]
    }

@router.post("/verify")
async def run_verification(task_id: str = None, steps: list = None):
    result = await verification_loop.run_verification(steps, context={"task_id": task_id})
    return result

@router.get("/security/audit")
async def security_audit(db: Session = Depends(get_db)):
    result = shield.full_audit(db)
    return result

@router.get("/hooks")
async def list_hooks():
    from ..hooks.manager import hook_manager
    return hook_manager.list_hooks()

@router.get("/hooks/logs")
async def get_hook_logs(limit: int = 50, event: str = None):
    from ..hooks.manager import hook_manager
    logs = hook_manager.get_event_log(limit, event)
    return {"logs": logs, "count": len(logs)}
