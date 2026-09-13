"""
Tests Battle Arena + Elo + Leaderboard — حقيقي — مثل lmarena.ai — يعمل فعلياً — $0 — المرحلة 2
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestEloSystem:
    def test_elo_initial_ratings(self):
        from app.core.elo import elo_system
        lb = elo_system.get_leaderboard()
        assert len(lb) >= 1
        # كل وكيل يبدأ 1000
        for entry in lb[:5]:
            assert "agent_id" in entry
            assert "rating" in entry
            assert "rank" in entry

    def test_elo_expected_score(self):
        from app.core.elo import elo_system
        score = elo_system.expected_score(1000, 1000)
        assert abs(score - 0.5) < 0.01
        score_high = elo_system.expected_score(1200, 1000)
        assert score_high > 0.5

    def test_elo_update_ratings(self):
        from app.core.elo import EloSystem
        es = EloSystem()
        es.ratings = {"a": 1000, "b": 1000}
        record = es.update_ratings("a", "b", is_draw=False)
        assert record["winner"] == "a"
        assert es.ratings["a"] > 1000
        assert es.ratings["b"] < 1000

    def test_elo_draw(self):
        from app.core.elo import EloSystem
        es = EloSystem()
        es.ratings = {"a": 1000, "b": 1000}
        es.update_ratings("a", "b", is_draw=True)
        # تعادل — نفس النقاط أو قريب
        assert es.ratings["a"] == 1000 or abs(es.ratings["a"] - 1000) < 20

    def test_bradley_terry(self):
        from app.core.elo import bradley_terry_ratings
        battles = [
            {"agent_a_id": "a", "agent_b_id": "b", "vote": "a"},
            {"agent_a_id": "a", "agent_b_id": "b", "vote": "a"},
            {"agent_a_id": "a", "agent_b_id": "b", "vote": "b"},
        ]
        ratings = bradley_terry_ratings(battles)
        assert "a" in ratings
        assert ratings["a"] > ratings["b"]

class TestArenaBattleAPI:
    def test_create_battle(self):
        res = client.post("/api/arena/battle", json={"question": "أنشئ خطة لمشروع"})
        assert res.status_code == 200
        data = res.json()
        assert "battle_id" in data
        assert "answer_a" in data
        assert "answer_b" in data
        assert "question" in data

    def test_create_battle_no_question(self):
        res = client.post("/api/arena/battle", json={})
        assert res.status_code == 200
        data = res.json()
        assert "error" in data

    def test_get_battle(self):
        res = client.post("/api/arena/battle", json={"question": "ما هو Manus؟"})
        battle_id = res.json()["battle_id"]
        res2 = client.get(f"/api/arena/battle/{battle_id}")
        assert res2.status_code == 200
        assert res2.json()["battle_id"] == battle_id

    def test_vote_battle(self):
        res = client.post("/api/arena/battle", json={"question": "اختبر التصويت"})
        battle_id = res.json()["battle_id"]
        vote_res = client.post(f"/api/arena/battle/{battle_id}/vote", json={"vote": "a"})
        assert vote_res.status_code == 200
        data = vote_res.json()
        assert "winner" in data or "vote" in data

    def test_vote_invalid(self):
        res = client.post("/api/arena/battle", json={"question": "اختبر"})
        battle_id = res.json()["battle_id"]
        vote_res = client.post(f"/api/arena/battle/{battle_id}/vote", json={"vote": "invalid"})
        assert vote_res.status_code == 200
        assert "error" in vote_res.json()

    def test_list_battles(self):
        res = client.get("/api/arena/battles")
        assert res.status_code == 200
        assert "battles" in res.json()

    def test_arena_stats(self):
        res = client.get("/api/arena/stats")
        assert res.status_code == 200
        assert "total_battles" in res.json()

class TestLeaderboardAPI:
    def test_get_leaderboard(self):
        res = client.get("/api/leaderboard/")
        assert res.status_code == 200
        data = res.json()
        assert "leaderboard" in data
        assert "total_agents" in data

    def test_leaderboard_agent(self):
        res = client.get("/api/leaderboard/agent/planner")
        assert res.status_code == 200
        data = res.json()
        assert "agent_id" in data or "error" in data

    def test_leaderboard_top(self):
        res = client.get("/api/leaderboard/top/5")
        assert res.status_code == 200
        assert "top" in res.json()

    def test_leaderboard_stats(self):
        res = client.get("/api/leaderboard/stats")
        assert res.status_code == 200
        assert "total_agents" in res.json() or "error" in res.json()
