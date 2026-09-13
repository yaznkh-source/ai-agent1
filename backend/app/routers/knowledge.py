"""
Knowledge Router - RAG + Collections (Track A2)
Open WebUI-like knowledge management
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..core.rag import knowledge_manager

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.get("/collections")
async def list_collections():
    cols = knowledge_manager.list_collections()
    return {"collections": cols, "total": len(cols)}

@router.get("/search")
async def search_knowledge(q: str, collection: str = None, top_k: int = 5):
    if collection:
        results = knowledge_manager.search_collection(collection, q, top_k)
    else:
        results = knowledge_manager.search_all(q, top_k)
    return {"query": q, "collection": collection, "results": results, "count": len(results)}

@router.post("/add")
async def add_knowledge(payload: dict):
    text = payload.get("text", "")
    collection = payload.get("collection", "default")
    metadata = payload.get("metadata", {})
    
    if not text:
        raise HTTPException(400, "Text required")
    
    doc_id = knowledge_manager.add_to_collection(collection, text, metadata)
    return {"doc_id": doc_id, "collection": collection, "text_length": len(text)}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), collection: str = "uploads"):
    content = await file.read()
    try:
        text = content.decode('utf-8')
    except:
        text = content.decode('latin-1', errors='ignore')
    
    result = knowledge_manager.add_file_content(file.filename, text, collection)
    return result

@router.get("/collection/{collection_name}")
async def get_collection(collection_name: str, q: str = None, top_k: int = 10):
    if q:
        results = knowledge_manager.search_collection(collection_name, q, top_k)
        return {"collection": collection_name, "query": q, "results": results}
    else:
        # List all docs in collection (from in-memory)
        docs = [d for d in knowledge_manager.vector_store.documents if d["metadata"].get("collection") == collection_name]
        return {"collection": collection_name, "documents": [{"id": d["id"], "text": d["text"][:200], "metadata": d["metadata"]} for d in docs[:20]], "total": len(docs)}
