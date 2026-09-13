from fastapi import APIRouter, HTTPException
from ..pipelines.engine import pipeline_engine
from ..models.schemas import PipelineCreate, PipelineExecuteRequest

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])

@router.get("/")
async def list_pipelines():
    pipelines = pipeline_engine.list_pipelines()
    return {"pipelines": pipelines, "count": len(pipelines)}

@router.get("/{pipeline_id}")
async def get_pipeline(pipeline_id: str):
    pipeline = pipeline_engine.get_pipeline(pipeline_id)
    if not pipeline:
        raise HTTPException(404, f"Pipeline {pipeline_id} not found")
    return {
        "id": pipeline.id,
        "name": pipeline.name,
        "description": pipeline.description,
        "steps": [{"id": s.id, "name": s.name, "type": s.type, "config": s.config} for s in pipeline.steps],
        "valves": pipeline.valves,
        "status": pipeline.status
    }

@router.post("/")
async def create_pipeline(p: PipelineCreate):
    pipeline = pipeline_engine.create_pipeline(
        name=p.name,
        description=p.description,
        steps=p.steps,
        valves=p.valves
    )
    return {
        "id": pipeline.id,
        "name": pipeline.name,
        "description": pipeline.description,
        "steps_count": len(pipeline.steps)
    }

@router.delete("/{pipeline_id}")
async def delete_pipeline(pipeline_id: str):
    deleted = pipeline_engine.delete_pipeline(pipeline_id)
    if not deleted:
        raise HTTPException(404, f"Pipeline {pipeline_id} not found")
    return {"deleted": True}

@router.post("/{pipeline_id}/execute")
async def execute_pipeline(pipeline_id: str, req: PipelineExecuteRequest):
    try:
        result = await pipeline_engine.execute_pipeline(pipeline_id, req.context)
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/history/list")
async def get_history(limit: int = 20):
    history = pipeline_engine.get_history(limit)
    return {"history": history, "count": len(history)}
