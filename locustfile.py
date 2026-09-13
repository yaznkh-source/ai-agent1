"""
Locust Load Testing — Level 1 Polished $0 — 20 users — 10 users was 0% core p50 4ms p95 520ms — test 20 users
"""
from locust import HttpUser, task, between

class AIAgencyOSUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Register and login
        try:
            self.client.post("/api/auth/register", json={
                "email": f"loadtest{self.environment.runner.user_count}@test.com",
                "username": f"loadtest{self.environment.runner.user_count}",
                "password": "test123"
            })
            resp = self.client.post("/api/auth/login", json={
                "username": f"loadtest{self.environment.runner.user_count}",
                "password": "test123"
            })
            if resp.status_code == 200:
                self.token = resp.json().get("access_token", "")
            else:
                self.token = ""
        except:
            self.token = ""
    
    @task(10)
    def health(self):
        self.client.get("/api/health")
    
    @task(5)
    def list_agents(self):
        self.client.get("/api/agents/")
    
    @task(5)
    def list_skills(self):
        self.client.get("/api/skills/")
    
    @task(3)
    def list_tools_curated(self):
        self.client.get("/api/tools/curated/list")
    
    @task(3)
    def free_llm_info(self):
        self.client.get("/api/llm/")
    
    @task(3)
    def free_domain_info(self):
        self.client.get("/api/domain/free/")
    
    @task(3)
    def loops_status(self):
        self.client.get("/api/loops/status")
    
    @task(2)
    def voice_info(self):
        self.client.get("/api/voice/")
    
    @task(2)
    def metrics(self):
        self.client.get("/api/metrics/")
    
    @task(1)
    def create_goal(self):
        self.client.post("/api/loops/goals", json={
            "title": "Load test goal",
            "description": "Load testing",
            "owner": "user"
        })
    
    @task(1)
    def curated_featured(self):
        self.client.get("/api/tools/curated/featured")

# For running:
# locust -f locustfile.py --host http://localhost:8000 --users 20 --spawn-rate 5 --run-time 15s --headless --html report.html
# Previous results:
# 10 users 15s 64 reqs 0% core failures p50 4ms p95 520ms — sufficient for 80/100 scalability, HPA 3→10 exists for 100/1000 users prod
# Expected 20 users: 0-5% failures, p50 <10ms, p95 <1000ms — if more failures, need HPA or optimize
