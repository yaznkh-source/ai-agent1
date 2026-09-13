"""
Load Testing with Locust - Task B2 - Production Hardened 80/100
Tests scalability: 10/50/100 users
Usage:
  pip install locust
  locust -f tests/locustfile.py --host http://localhost:8000
  # Or headless:
  locust -f tests/locustfile.py --host http://localhost:8000 --headless -u 10 -r 2 --run-time 30s
"""

from locust import HttpUser, task, between
import random
import json

class AgencyUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login on start"""
        # Try demo login
        try:
            response = self.client.post("/api/auth/login", json={
                "username": "admin",
                "password": "admin123"
            })
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.token = None
                self.headers = {}
        except:
            self.token = None
            self.headers = {}
    
    @task(5)
    def health(self):
        self.client.get("/api/health")
    
    @task(3)
    def list_agents(self):
        self.client.get("/api/agents/", headers=self.headers)
    
    @task(3)
    def list_skills(self):
        self.client.get("/api/skills/", headers=self.headers)
    
    @task(2)
    def dashboard(self):
        self.client.get("/api/agency/dashboard", headers=self.headers)
    
    @task(2)
    def list_projects(self):
        self.client.get("/api/agency/projects", headers=self.headers)
    
    @task(1)
    def openapi(self):
        self.client.get("/api/openapi.json")
    
    @task(1)
    def monitoring_mock(self):
        # This is mock but should handle load
        self.client.get("/api/monitoring/", headers=self.headers)
    
    @task(1)
    def billing_mock(self):
        self.client.get("/api/billing/real/", headers=self.headers)

class ChatUser(HttpUser):
    wait_time = between(2, 5)
    weight = 1
    
    def on_start(self):
        try:
            response = self.client.post("/api/auth/login", json={
                "username": "admin",
                "password": "admin123"
            })
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.headers = {}
        except:
            self.headers = {}
    
    @task(3)
    def chat_completion(self):
        self.client.post("/api/chat/completions", 
            headers=self.headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": "Hello, test load"}],
                "temperature": 0.7
            }
        )
    
    @task(2)
    def list_chats(self):
        self.client.get("/api/chats/", headers=self.headers)

# For quick test without locust server
if __name__ == "__main__":
    print("Locust file loaded - use: locust -f tests/locustfile.py --host http://localhost:8000")
    print("Headless 10 users 30s: locust -f tests/locustfile.py --host http://localhost:8000 --headless -u 10 -r 2 --run-time 30s")
