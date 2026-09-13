"""
AI Agency OS Python SDK
pip install ai-agency-sdk (mock - in production publish to PyPI)
"""
import requests
from typing import Dict, List, Optional

class AIAgencyClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    # Agents
    def list_agents(self, category: str = None) -> List[Dict]:
        params = {"category": category} if category else {}
        res = self.session.get(f"{self.base_url}/api/agents/", params=params)
        res.raise_for_status()
        return res.json()["agents"]
    
    def get_agent(self, agent_id: str) -> Dict:
        res = self.session.get(f"{self.base_url}/api/agents/{agent_id}")
        res.raise_for_status()
        return res.json()
    
    def run_agent(self, agent_id: str, task: str, context: Dict = None) -> Dict:
        payload = {"agent_id": agent_id, "task": task, "context": context or {}}
        res = self.session.post(f"{self.base_url}/api/agents/run", json=payload)
        res.raise_for_status()
        return res.json()
    
    # Skills
    def list_skills(self, category: str = None) -> List[Dict]:
        params = {"category": category} if category else {}
        res = self.session.get(f"{self.base_url}/api/skills/", params=params)
        res.raise_for_status()
        return res.json()["skills"]
    
    def get_skill(self, skill_id: str) -> Dict:
        res = self.session.get(f"{self.base_url}/api/skills/{skill_id}")
        res.raise_for_status()
        return res.json()
    
    # Chat
    def chat(self, message: str, conversation_id: str = None, agent_id: str = None) -> Dict:
        payload = {"message": message, "conversation_id": conversation_id, "agent_id": agent_id}
        res = self.session.post(f"{self.base_url}/api/chat/", json=payload)
        res.raise_for_status()
        return res.json()
    
    # Pipelines
    def list_pipelines(self) -> List[Dict]:
        res = self.session.get(f"{self.base_url}/api/pipelines/")
        res.raise_for_status()
        return res.json()["pipelines"]
    
    def run_pipeline(self, pipeline_id: str, input_data: Dict) -> Dict:
        payload = {"pipeline_id": pipeline_id, "input": input_data}
        res = self.session.post(f"{self.base_url}/api/pipelines/run", json=payload)
        res.raise_for_status()
        return res.json()
    
    # Agency
    def list_projects(self) -> List[Dict]:
        res = self.session.get(f"{self.base_url}/api/agency/projects")
        res.raise_for_status()
        return res.json()["projects"]
    
    def create_project(self, name: str, client_email: str, description: str = "") -> Dict:
        payload = {"name": name, "client_email": client_email, "description": description}
        res = self.session.post(f"{self.base_url}/api/agency/projects", json=payload)
        res.raise_for_status()
        return res.json()
    
    # Knowledge / RAG
    def search_knowledge(self, query: str, collection: str = None) -> Dict:
        params = {"query": query, "collection": collection} if collection else {"query": query}
        res = self.session.get(f"{self.base_url}/api/knowledge/search", params=params)
        res.raise_for_status()
        return res.json()
    
    def add_document(self, collection: str, content: str, metadata: Dict = None) -> Dict:
        payload = {"collection": collection, "content": content, "metadata": metadata or {}}
        res = self.session.post(f"{self.base_url}/api/knowledge/documents", json=payload)
        res.raise_for_status()
        return res.json()
    
    # Marketplace
    def search_marketplace(self, query: str, type: str = "all") -> Dict:
        res = self.session.get(f"{self.base_url}/api/marketplace/search", params={"q": query, "type": type})
        res.raise_for_status()
        return res.json()
    
    def install_skill(self, skill_id: str) -> Dict:
        res = self.session.post(f"{self.base_url}/api/marketplace/skill/{skill_id}/install", json={"user_id": "sdk-user"})
        res.raise_for_status()
        return res.json()

# Example usage
if __name__ == "__main__":
    client = AIAgencyClient(base_url="http://localhost:8000")
    
    print("🤖 AI Agency OS Python SDK Demo")
    print("="*50)
    
    # List agents
    agents = client.list_agents()
    print(f"✅ Found {len(agents)} agents")
    print(f"   Example: {agents[0]['name']} ({agents[0]['id']})")
    
    # List skills
    skills = client.list_skills()
    print(f"✅ Found {len(skills)} skills")
    print(f"   Example: {skills[0]['name']} ({skills[0]['id']})")
    
    # Search knowledge
    try:
        results = client.search_knowledge("how to build SaaS")
        print(f"✅ Knowledge search: {results.get('count', 0)} results")
    except Exception as e:
        print(f"⚠️ Knowledge search failed: {e}")
    
    # Chat
    try:
        chat_res = client.chat("Build me a landing page for my AI agency")
        print(f"✅ Chat response: {chat_res.get('response', '')[:100]}...")
    except Exception as e:
        print(f"⚠️ Chat failed: {e}")
    
    print("\n🎉 SDK works!")
    print("\nInstall: pip install requests")
    print("Usage: from ai_agency_sdk import AIAgencyClient")
    print("       client = AIAgencyClient(base_url='https://your-agency.os', api_key='...')")
