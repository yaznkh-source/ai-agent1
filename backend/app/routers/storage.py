"""
Storage Router - File uploads, S3, local
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from ..core.storage import storage_service
from ..core.email import email_service
from typing import Dict

router = APIRouter(prefix="/api/storage", tags=["storage"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), metadata: str = None):
    import json
    content = await file.read()
    
    meta = {}
    if metadata:
        try:
            meta = json.loads(metadata)
        except:
            pass
    
    result = await storage_service.upload_file(
        file_content=content,
        filename=file.filename,
        content_type=file.content_type,
        metadata=meta
    )
    
    return result

@router.get("/files")
async def list_files(prefix: str = None, limit: int = 50):
    files = await storage_service.list_files(prefix, limit)
    return {"files": files, "count": len(files)}

@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    file_info = await storage_service.get_file(file_id)
    if not file_info:
        raise HTTPException(404, "File not found")
    return file_info

@router.get("/files/{file_id}/download")
async def download_file(file_id: str):
    file_info = await storage_service.get_file(file_id)
    if not file_info:
        raise HTTPException(404, "File not found")
    
    content = await storage_service.get_file_content(file_id)
    if not content:
        raise HTTPException(404, "File content not found")
    
    return Response(
        content=content,
        media_type=file_info["content_type"],
        headers={"Content-Disposition": f"attachment; filename={file_info['filename']}"}
    )

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    deleted = await storage_service.delete_file(file_id)
    if not deleted:
        raise HTTPException(404, "File not found")
    return {"deleted": True, "file_id": file_id}

# Email endpoints
@router.post("/email/send")
async def send_email(payload: Dict):
    to = payload.get("to")
    subject = payload.get("subject")
    html = payload.get("html", "")
    
    if not to or not subject:
        raise HTTPException(400, "to and subject required")
    
    result = await email_service.send_email(to, subject, html)
    return result

@router.post("/email/onboarding")
async def send_onboarding_email(payload: Dict):
    client_email = payload.get("client_email")
    client_name = payload.get("client_name", "Client")
    project_name = payload.get("project_name", "Project")
    
    result = await email_service.send_client_onboarding(client_email, client_name, project_name)
    return result

@router.post("/email/task-completed")
async def send_task_completed_email(payload: Dict):
    client_email = payload.get("client_email")
    task_title = payload.get("task_title")
    project_name = payload.get("project_name")
    
    result = await email_service.send_task_completed(client_email, task_title, project_name)
    return result

@router.get("/email/sent")
async def list_sent_emails(limit: int = 20):
    emails = email_service.get_sent_emails(limit)
    return {"emails": emails, "count": len(emails)}
