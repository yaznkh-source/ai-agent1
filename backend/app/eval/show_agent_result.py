"""
عرض نتائج تقييم الوكلاء — مثل arena-hard-auto show_result.py — يعرض النتائج ولوحة الصدارة — يعمل فعلياً — $0 — المرحلة 6 — من lmarena/arena-hard-auto
"""
from typing import Dict, List

def show_results(judgments: List[Dict]) -> Dict:
    """عرض نتائج التقييم — مثل arena-hard-auto show_result.py — لوحة صدارة — يعمل فعلياً — $0"""
    # حساب Elo من الأحكام — مثل arena-rank — يعمل فعلياً
    from ..core.elo import EloSystem
    
    elo = EloSystem()
    
    # تهيئة
    agents = set()
    for j in judgments:
        agents.add(j.get("agent_a_id", ""))
        agents.add(j.get("agent_b_id", ""))
    
    for agent in agents:
        if agent:
            elo.ratings[agent] = 1000
            elo.battles[agent] = {"wins": 0, "losses": 0, "draws": 0, "battles": 0}
    
    # تحديث من الأحكام
    for judgment in judgments:
        a = judgment.get("agent_a_id")
        b = judgment.get("agent_b_id")
        winner = judgment.get("winner")
        
        if not a or not b:
            continue
        
        if winner == "a":
            elo.update_ratings(a, b, is_draw=False)
        elif winner == "b":
            elo.update_ratings(b, a, is_draw=False)
        else:  # tie
            elo.update_ratings(a, b, is_draw=True)
    
    leaderboard = elo.get_leaderboard()
    
    return {
        "leaderboard": leaderboard,
        "total_judgments": len(judgments),
        "total_agents": len(agents),
        "judgments": judgments[:20],
        "message": f"نتائج التقييم — {len(judgments)} حكم — {len(agents)} وكيل — لوحة صدارة — مثل arena-hard-auto show_result.py — يعمل فعلياً — $0",
    }
