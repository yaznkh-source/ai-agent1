"""
Real RAG System - ChromaDB + Embeddings (Track A2)
Upgrades MemoryManager from keyword to vector search
Inspired by Open WebUI RAG + ECC memory
"""
from typing import List, Dict, Optional
import os
import hashlib
from .config import settings

class SimpleEmbedding:
    """Simple embedding without heavy dependencies - TF-IDF like + hash"""
    def __init__(self, dim=384):
        self.dim = dim
    
    def embed(self, text: str) -> List[float]:
        # Simple hash-based embedding for demo - in production use sentence-transformers
        # This is deterministic and captures some semantics via word hashing
        words = text.lower().split()
        vec = [0.0] * self.dim
        
        for word in words:
            # Hash word to index
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx = h % self.dim
            # Simple term frequency
            vec[idx] += 1.0
            
            # Also add bigrams
            if len(word) > 3:
                for i in range(len(word)-2):
                    bigram = word[i:i+3]
                    hb = int(hashlib.md5(bigram.encode()).hexdigest(), 16)
                    idx2 = hb % self.dim
                    vec[idx2] += 0.3
        
        # Normalize
        import math
        norm = math.sqrt(sum(x*x for x in vec)) or 1
        vec = [x/norm for x in vec]
        return vec
    
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        # Cosine similarity
        dot = sum(a*b for a, b in zip(vec1, vec2))
        return dot

class VectorStore:
    """In-memory vector store with optional ChromaDB persistence"""
    def __init__(self, persist_dir: str = None):
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        self.embedding = SimpleEmbedding()
        self.documents = []  # List of {id, text, embedding, metadata}
        
        # Try to load ChromaDB if available
        self.chroma_client = None
        self.chroma_collection = None
        try:
            import chromadb
            os.makedirs(self.persist_dir, exist_ok=True)
            self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
            self.chroma_collection = self.chroma_client.get_or_create_collection("ai_agency_knowledge")
            print("✅ ChromaDB connected")
        except Exception as e:
            print(f"⚠️ ChromaDB not available, using in-memory: {e}")
    
    def add_document(self, text: str, metadata: Dict = None, doc_id: str = None):
        import uuid
        doc_id = doc_id or str(uuid.uuid4())
        emb = self.embedding.embed(text)
        
        doc = {
            "id": doc_id,
            "text": text,
            "embedding": emb,
            "metadata": metadata or {}
        }
        self.documents.append(doc)
        
        # Also add to Chroma if available
        if self.chroma_collection:
            try:
                self.chroma_collection.add(
                    ids=[doc_id],
                    documents=[text],
                    metadatas=[metadata or {}]
                )
            except Exception as e:
                print(f"Chroma add failed: {e}")
        
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.chroma_collection:
            try:
                results = self.chroma_collection.query(
                    query_texts=[query],
                    n_results=top_k
                )
                # Convert chroma format to our format
                docs = []
                if results["documents"]:
                    for i, doc_text in enumerate(results["documents"][0]):
                        docs.append({
                            "id": results["ids"][0][i],
                            "text": doc_text,
                            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                            "score": 1.0 - (results["distances"][0][i] if results["distances"] else 0)
                        })
                return docs
            except Exception as e:
                print(f"Chroma search failed, fallback to memory: {e}")
        
        # Fallback to in-memory
        query_emb = self.embedding.embed(query)
        scored = []
        for doc in self.documents:
            score = self.embedding.similarity(query_emb, doc["embedding"])
            scored.append((score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": doc["id"], "text": doc["text"], "metadata": doc["metadata"], "score": score} 
                for score, doc in scored[:top_k] if score > 0.1]

class KnowledgeManager:
    """Manages knowledge collections like Open WebUI"""
    def __init__(self):
        self.vector_store = VectorStore()
        self.collections = {}  # collection_name -> list of doc_ids
        self.load_builtin_knowledge()
    
    def load_builtin_knowledge(self):
        """Load builtin knowledge for demo"""
        builtin_docs = [
            {"text": "ECC هو نظام تحسين أداء حاضنة الوكلاء مع 68 وكيل متخصص و 292 مهارة. يعمل بنظام plan->test->implement->review->verify->remember->improve", "meta": {"collection": "ecc", "type": "definition"}},
            {"text": "Open WebUI هو واجهة ذكاء اصطناعي سهلة تدعم Ollama و OpenAI API. لديها Tools لتوسيع قدرات LLM و Functions لتوسيع المنصة و Pipelines لفصل المعالجة الثقيلة", "meta": {"collection": "openwebui", "type": "definition"}},
            {"text": "TDD Workflow: RED -> GREEN -> REFACTOR. اكتب اختبار فاشل أولاً يحدد السلوك المطلوب، ثم اكتب أقل كود يجعله ينجح، ثم نظف الكود مع شبكة أمان الاختبارات. 80%+ تغطية", "meta": {"collection": "skills", "type": "tdd"}},
            {"text": "Verification Loop: تحقق حتمي خارج سياق النموذج: Build (هل يبني؟), Test (هل الاختبارات تنجح؟), Lint (أسلوب), Typecheck (أنواع), Security (ثغرات)", "meta": {"collection": "skills", "type": "verification"}},
            {"text": "AgentShield يفحص: تسريب أسرار (API keys), حقن prompts (تجاوز تعليمات), أوامر خطيرة (rm -rf), صلاحيات مفرطة", "meta": {"collection": "security", "type": "shield"}},
            {"text": "الوكالة الذكية تقدم: تطوير مواقع، تطبيقات جوال، أتمتة، محتوى، SEO. نموذج العمل: اشتراك شهري + تكلفة تنفيذ", "meta": {"collection": "agency", "type": "business"}},
        ]
        
        for doc in builtin_docs:
            self.vector_store.add_document(doc["text"], doc["meta"])
    
    def add_to_collection(self, collection: str, text: str, metadata: Dict = None):
        meta = {"collection": collection, **(metadata or {})}
        doc_id = self.vector_store.add_document(text, meta)
        if collection not in self.collections:
            self.collections[collection] = []
        self.collections[collection].append(doc_id)
        return doc_id
    
    def search_collection(self, collection: str, query: str, top_k: int = 5):
        # Search all then filter by collection
        results = self.vector_store.search(query, top_k*2)
        filtered = [r for r in results if r["metadata"].get("collection") == collection]
        return filtered[:top_k]
    
    def search_all(self, query: str, top_k: int = 5):
        return self.vector_store.search(query, top_k)
    
    def list_collections(self):
        # Count docs per collection
        from collections import Counter
        collections = Counter()
        for doc in self.vector_store.documents:
            coll = doc["metadata"].get("collection", "default")
            collections[coll] += 1
        
        # Also from chroma if available
        return dict(collections)
    
    def add_file_content(self, filename: str, content: str, collection: str = "uploads"):
        """Add file content - splits into chunks"""
        # Simple chunking
        chunk_size = 500
        words = content.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append(chunk)
        
        doc_ids = []
        for idx, chunk in enumerate(chunks):
            meta = {"collection": collection, "filename": filename, "chunk": idx, "total_chunks": len(chunks)}
            doc_id = self.add_to_collection(collection, chunk, meta)
            doc_ids.append(doc_id)
        
        return {"filename": filename, "chunks": len(chunks), "doc_ids": doc_ids}

knowledge_manager = KnowledgeManager()
