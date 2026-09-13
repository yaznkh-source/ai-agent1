"""
Agents router - ECC's 68 agents management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, AgentModel, SessionLocal
from ..agents.definitions import get_all_agents, get_agent_by_id, get_agents_by_category, AGENT_CATEGORIES
from ..agents.orchestrator import orchestrator
from ..models.schemas import AgentRunRequest, WorkflowRunRequest

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("/")
async def list_agents(category: str = None):
    if category:
        agents = get_agents_by_category(category)
    else:
        agents = get_all_agents()
    return {
        "agents": agents,
        "total": len(agents),
        "categories": AGENT_CATEGORIES
    }

@router.get("/categories")
async def list_categories():
    return AGENT_CATEGORIES

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(404, f"Agent {agent_id} not found")
    return agent

@router.post("/run")
async def run_agent(req: AgentRunRequest):
    # Task C3: Prometheus metrics wiring - increment agents_executed
    try:
        from .metrics import increment_agent_executed
        increment_agent_executed(req.agent_id)
    except:
        pass
    
    result = await orchestrator.run_single_agent(
        agent_id=req.agent_id,
        task=req.task,
        context=req.context,
        chat_history=req.chat_history
    )
    return result

@router.post("/workflow/run")
async def run_workflow(req: WorkflowRunRequest):
    if req.workflow_id:
        workflows = orchestrator.get_predefined_workflows()
        workflow = workflows.get(req.workflow_id)
        if not workflow:
            raise HTTPException(404, f"Workflow {req.workflow_id} not found")
    elif req.workflow:
        workflow = req.workflow
    else:
        raise HTTPException(400, "Either workflow_id or workflow must be provided")
    
    result = await orchestrator.run_workflow(
        workflow=workflow,
        initial_task=req.task,
        context=req.context
    )
    return result

@router.get("/workflows/list")
async def list_workflows():
    workflows = orchestrator.get_predefined_workflows()
    return {
        "workflows": [
            {"id": wid, "name": wid.replace("-", " ").title(), "steps": w, "steps_count": len(w)}
            for wid, w in workflows.items()
        ]
    }

@router.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    workflows = orchestrator.get_predefined_workflows()
    workflow = workflows.get(workflow_id)
    if not workflow:
        raise HTTPException(404, f"Workflow {workflow_id} not found")
    return {"id": workflow_id, "steps": workflow}
