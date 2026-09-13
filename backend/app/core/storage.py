"""
File Storage Service - S3 / Local (Track A)
For client files, knowledge docs, pipeline artifacts
"""
from typing import Dict, List, Optional
import os
import uuid
from datetime import datetime
import hashlib

class StorageService:
    def __init__(self):
        self.provider = os.getenv("STORAGE_PROVIDER", "local")  # local, s3, gcs
        self.local_dir = os.getenv("STORAGE_LOCAL_DIR", "./storage")
        self.s3_bucket = os.getenv("S3_BUCKET")
        self.s3_region = os.getenv("S3_REGION", "us-east-1")
        
        os.makedirs(self.local_dir, exist_ok=True)
        
        # In-memory file index
        self.files = {}
        
        # Try S3
        self.s3_client = None
        if self.provider == "s3":
            try:
                import boto3
                self.s3_client = boto3.client('s3', region_name=self.s3_region)
                print("✅ S3 connected")
            except Exception as e:
                print(f"⚠️ S3 not available: {e}, using local")
                self.provider = "local"
    
    def _get_file_path(self, file_id: str) -> str:
        return os.path.join(self.local_dir, file_id)
    
    async def upload_file(self, file_content: bytes, filename: str, content_type: str = None, metadata: Dict = None) -> Dict:
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(filename)[1]
        stored_name = f"{file_id}{ext}"
        
        file_info = {
            "id": file_id,
            "filename": filename,
            "stored_name": stored_name,
            "content_type": content_type or "application/octet-stream",
            "size": len(file_content),
            "hash": hashlib.md5(file_content).hexdigest(),
            "provider": self.provider,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "url": f"/api/storage/files/{file_id}" if self.provider == "local" else f"https://{self.s3_bucket}.s3.{self.s3_region}.amazonaws.com/{stored_name}"
        }
        
        if self.provider == "s3" and self.s3_client:
            try:
                self.s3_client.put_object(
                    Bucket=self.s3_bucket,
                    Key=stored_name,
                    Body=file_content,
                    ContentType=content_type
                )
                file_info["s3_key"] = stored_name
            except Exception as e:
                file_info["status"] = "failed"
                file_info["error"] = str(e)
        else:
            # Local storage
            try:
                with open(self._get_file_path(stored_name), "wb") as f:
                    f.write(file_content)
                file_info["local_path"] = self._get_file_path(stored_name)
            except Exception as e:
                file_info["status"] = "failed"
                file_info["error"] = str(e)
        
        self.files[file_id] = file_info
        return file_info
    
    async def get_file(self, file_id: str) -> Optional[Dict]:
        return self.files.get(file_id)
    
    async def get_file_content(self, file_id: str) -> Optional[bytes]:
        file_info = self.files.get(file_id)
        if not file_info:
            return None
        
        if self.provider == "s3" and self.s3_client:
            try:
                response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=file_info["stored_name"])
                return response['Body'].read()
            except:
                return None
        else:
            try:
                with open(self._get_file_path(file_info["stored_name"]), "rb") as f:
                    return f.read()
            except:
                return None
    
    async def list_files(self, prefix: str = None, limit: int = 50) -> List[Dict]:
        files = list(self.files.values())
        if prefix:
            files = [f for f in files if f["filename"].startswith(prefix)]
        return files[-limit:]
    
    async def delete_file(self, file_id: str) -> bool:
        file_info = self.files.get(file_id)
        if not file_info:
            return False
        
        if self.provider == "s3" and self.s3_client:
            try:
                self.s3_client.delete_object(Bucket=self.s3_bucket, Key=file_info["stored_name"])
            except:
                pass
        else:
            try:
                os.remove(self._get_file_path(file_info["stored_name"]))
            except:
                pass
        
        del self.files[file_id]
        return True

storage_service = StorageService()
