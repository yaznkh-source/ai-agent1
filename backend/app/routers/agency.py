"""
Agency router - AI Agency OS specific: clients, projects, tasks
Combines ECC's orchestration + Open WebUI's workspace concept
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Client, Project, Task, SessionLocal
from ..models.schemas import ClientCreate, ProjectCreate, TaskCreate
from ..verification.loop import verification_loop
from ..core.security import shield
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/agency", tags=["agency"])

# === Clients ===
@router.get("/clients")
async def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).order_by(Client.created_at.desc()).all()
    return [{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "company": c.company,
        "description": c.description,
        "status": c.status,
        "created_at": c.created_at.isoformat(),
        "meta": c.meta
    } for c in clients]

@router.post("/clients")
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(
        id=str(uuid.uuid4()),
        name=client.name,
        email=client.email,
        company=client.company,
        description=client.description,
        meta=client.meta or {}
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"id": new_client.id, "name": new_client.name}

@router.get("/clients/{client_id}")
async def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")
    
    projects = db.query(Project).filter(Project.client_id == client_id).all()
    
    return {
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "company": client.company,
        "description": client.description,
        "status": client.status,
        "created_at": client.created_at.isoformat(),
        "projects": [{"id": p.id, "name": p.name, "status": p.status} for p in projects],
        "meta": client.meta
    }

@router.delete("/clients/{client_id}")
async def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(404, "Client not found")
    db.delete(client)
    db.commit()
    return {"deleted": True}

# === Projects ===
@router.get("/projects")
async def list_projects(client_id: str = None, db: Session = Depends(get_db)):
    q = db.query(Project)
    if client_id:
        q = q.filter(Project.client_id == client_id)
    projects = q.order_by(Project.updated_at.desc()).all()
    return [{
        "id": p.id,
        "client_id": p.client_id,
        "name": p.name,
        "description": p.description,
        "status": p.status,
        "agents": p.agents,
        "created_at": p.created_at.isoformat(),
        "updated_at": p.updated_at.isoformat(),
        "meta": p.meta
    } for p in projects]

@router.post("/projects")
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        id=str(uuid.uuid4()),
        client_id=project.client_id,
        name=project.name,
        description=project.description,
        workflow=project.workflow or {},
        agents=project.agents or [],
        meta=project.meta or {}
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"id": new_project.id, "name": new_project.name}

@router.get("/projects/{project_id}")
async def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    tasks = db.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at.desc()).all()
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
async def update_project(project_id: str, updates: dict, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    for key, value in updates.items():
        if hasattr(project, key):
            setattr(project, key, value)
    project.updated_at = datetime.utcnow()
    db.commit()
    return {"updated": True}

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    db.query(Task).filter(Task.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    return {"deleted": True}

# === Tasks ===
@router.get("/tasks")
async def list_tasks(project_id: str = None, status: str = None, db: Session = Depends(get_db)):
    q = db.query(Task)
    if project_id:
        q = q.filter(Task.project_id == project_id)
    if status:
        q = q.filter(Task.status == status)
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
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
        "meta": t.meta
    } for t in tasks]

@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        id=str(uuid.uuid4()),
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assigned_agent=task.assigned_agent,
        skill_used=task.skill_used,
        meta=task.meta or {}
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"id": new_task.id, "title": new_task.title}

@router.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    return {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "assigned_agent": task.assigned_agent,
        "skill_used": task.skill_used,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "meta": task.meta
    }

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, updates: dict, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    for key, value in updates.items():
        if hasattr(task, key):
            setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    db.commit()
    return {"updated": True}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task)
    db.commit()
    return {"deleted": True}

# === Dashboard & Verification ===
@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    clients_count = db.query(Client).count()
    projects_count = db.query(Project).count()
    tasks_count = db.query(Task).count()
    tasks_todo = db.query(Task).filter(Task.status == "todo").count()
    tasks_in_progress = db.query(Task).filter(Task.status == "in_progress").count()
    tasks_done = db.query(Task).filter(Task.status == "done").count()
    
    recent_projects = db.query(Project).order_by(Project.updated_at.desc()).limit(5).all()
    recent_tasks = db.query(Task).order_by(Task.updated_at.desc()).limit(10).all()
    
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
