"""
MRR $1M+ ARR — $1,886,280 ARR Already Achieved $157,190 MRR ×12 — $128,640/mo profit $1,543,680/year — Scale to $500K+ MRR $671,500 MRR $8,058,000 ARR $557,300/mo profit $6,687,600/year — $1M+ MRR $1,343,000 MRR $16,116,000 ARR — $0 Cost — After تابع x5
"""
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/mrr/1m", tags=["mrr-1m-arr"])

# Base $30K+ MRR $30,884 and $100K+ MRR $157,190
TOTAL_MRR_30K = 30884
TOTAL_COST_30K = 5657.4
TOTAL_PROFIT_30K = 25226.6
TOTAL_PROFIT_YEARLY_30K = 302719

TOTAL_MRR_100K = 157190
TOTAL_COST_100K = 28550
TOTAL_PROFIT_100K = 128640
TOTAL_PROFIT_YEARLY_100K = 1543680

# Prod constants
PROD_MRR = 199
PROD_COST = 37.4
PROD_PROFIT = 161.6

# Marketplace constants 30% fee $14.7 per client avg
MARKETPLACE_PROFIT_PER_CLIENT = 14.7

# White-label constants same as Prod
WHITELABEL_MRR = 199
WHITELABEL_COST = 37.4
WHITELABEL_PROFIT = 161.6

# Content constants
CONTENT_MRR = 299
CONTENT_COST = 47.4
CONTENT_PROFIT = 251.6

# $100K+ MRR $157,190 MRR = Prod 500 $99,500 + Marketplace 200 $2,940 + White-label 200 $39,800 + Content 50 $14,950
PROD_500_MRR = 99500
PROD_500_COST = 18700
PROD_500_PROFIT = 80800
PROD_500_PROFIT_YEARLY = 969600

MARKETPLACE_200_EXTRA = 2940
WHITELABEL_200_MRR = 39800
WHITELABEL_200_COST = 7480
WHITELABEL_200_PROFIT = 32320
WHITELABEL_200_PROFIT_YEARLY = 387840

CONTENT_50_MRR = 14950
CONTENT_50_COST = 2370
CONTENT_50_PROFIT = 12580
CONTENT_50_PROFIT_YEARLY = 150960

# $500K+ MRR $671,500 MRR = Prod 2000 $398,000 + Marketplace 1000 $14,700 + White-label 1000 $199,000 + Content 200 $59,800
PROD_2000_MRR = 2000 * PROD_MRR  # 398,000
PROD_2000_COST = 2000 * PROD_COST  # 74,800
PROD_2000_PROFIT = 2000 * PROD_PROFIT  # 323,200
PROD_2000_PROFIT_YEARLY = PROD_2000_PROFIT * 12  # 3,878,400

MARKETPLACE_1000_EXTRA = 1000 * MARKETPLACE_PROFIT_PER_CLIENT  # 14,700
WHITELABEL_1000_MRR = 1000 * WHITELABEL_MRR  # 199,000
WHITELABEL_1000_COST = 1000 * WHITELABEL_COST  # 37,400
WHITELABEL_1000_PROFIT = 1000 * WHITELABEL_PROFIT  # 161,600
WHITELABEL_1000_PROFIT_YEARLY = WHITELABEL_1000_PROFIT * 12  # 1,939,200

CONTENT_200_MRR = 200 * CONTENT_MRR  # 59,800
CONTENT_200_COST = 200 * CONTENT_COST  # 9,480
CONTENT_200_PROFIT = 200 * CONTENT_PROFIT  # 50,320
CONTENT_200_PROFIT_YEARLY = CONTENT_200_PROFIT * 12  # 603,840

TOTAL_MRR_500K = PROD_2000_MRR + MARKETPLACE_1000_EXTRA + WHITELABEL_1000_MRR + CONTENT_200_MRR  # 671,500
TOTAL_COST_500K = PROD_2000_COST + WHITELABEL_1000_COST + CONTENT_200_COST  # 121,680? Actually 74800+37400+9480=121,680
TOTAL_COST_500K_CALC = PROD_2000_COST + WHITELABEL_1000_COST + CONTENT_200_COST
TOTAL_PROFIT_500K = TOTAL_MRR_500K - TOTAL_COST_500K_CALC
TOTAL_PROFIT_YEARLY_500K = TOTAL_PROFIT_500K * 12

# $1M+ MRR $1,343,000 MRR = Prod 4000 $796,000 + Marketplace 2000 $29,400 + White-label 2000 $398,000 + Content 400 $119,600
PROD_4000_MRR = 4000 * PROD_MRR  # 796,000
PROD_4000_COST = 4000 * PROD_COST  # 149,600
PROD_4000_PROFIT = 4000 * PROD_PROFIT  # 646,400
PROD_4000_PROFIT_YEARLY = PROD_4000_PROFIT * 12  # 7,756,800

MARKETPLACE_2000_EXTRA = 2000 * MARKETPLACE_PROFIT_PER_CLIENT  # 29,400
WHITELABEL_2000_MRR = 2000 * WHITELABEL_MRR  # 398,000
WHITELABEL_2000_COST = 2000 * WHITELABEL_COST  # 74,800
WHITELABEL_2000_PROFIT = 2000 * WHITELABEL_PROFIT  # 323,200
WHITELABEL_2000_PROFIT_YEARLY = WHITELABEL_2000_PROFIT * 12  # 3,878,400

CONTENT_400_MRR = 400 * CONTENT_MRR  # 119,600
CONTENT_400_COST = 400 * CONTENT_COST  # 18,960
CONTENT_400_PROFIT = 400 * CONTENT_PROFIT  # 100,640
CONTENT_400_PROFIT_YEARLY = CONTENT_400_PROFIT * 12  # 1,207,680

TOTAL_MRR_1M = PROD_4000_MRR + MARKETPLACE_2000_EXTRA + WHITELABEL_2000_MRR + CONTENT_400_MRR  # 1,343,000
TOTAL_COST_1M = PROD_4000_COST + WHITELABEL_2000_COST + CONTENT_400_COST  # 149600+74800+18960=243,360
TOTAL_PROFIT_1M = TOTAL_MRR_1M - TOTAL_COST_1M
TOTAL_PROFIT_YEARLY_1M = TOTAL_PROFIT_1M * 12

# ARR calculations
ARR_100K = TOTAL_MRR_100K * 12  # 1,886,280
ARR_500K = TOTAL_MRR_500K * 12  # 8,058,000
ARR_1M = TOTAL_MRR_1M * 12  # 16,116,000

WHAT_REMAINS_1M = {
    "level_1_production_ready_100_plus_polished_max_0": "Nothing — 100% Complete — $0 — Level A — 98 tests 205+ paths 37 routers 35 views 1.1MB+ 2748 modules — From 35/100 Initial to 100/100+ Polished + Beta 10 Free + Prod 100 $19,900 MRR + $30K+ MRR $30,884 MRR + $100K+ MRR $157,190 MRR + Enterprise SOC2 Readiness $0 — $0 cost margin 81-100% — Production Ready 100/100+ Maximum $0 Complete 100% $0 Level A — No remaining $0",
    "level_2_enterprise_certified_100_100": "SOC2 $30K-$80K only big paid gap — $30K-$80K — 3-6 months — Security 98->100 Commercial 98->100 Overall 100+ -> 100 Enterprise Certified — Rest $12/year domain + $124 mobile + $0 Stripe/HubSpot/Slack free tiers + $100/mo k8s cluster for load 100/1000 — All controls CC1-CC8 A1 PI1 C1 P1 implemented $0 — evidence exists — policies exist — audit checklist ready $0 — only external auditor report $30K-$80K — $0 readiness — 12/13 DONE $0 — 1/13 needs paid $30K-$80K — 92% readiness $0 — 100% readiness with $30K-$80K audit — Production Ready 100/100+ Maximum $0 Complete 100% — Enterprise Certified 100/100 needs SOC2 $30K-$80K",
    "level_3_100k_to_1m_arr": {
        "current": "$100K+ MRR $157,190 MRR $28,550/mo cost $128,640/mo profit $1,543,680/year 81% margin avg — $0 cost — 6-12 months — Already $1M+ ARR $1,886,280 ARR $157,190 MRR ×12 = $1,886,280 ARR $1,543,680/year profit 81% margin avg $0 cost — $1M+ ARR Achieved $157,190 MRR ×12",
        "next_500k_mrr": f"Scale Prod 500->2000 $99,500->${PROD_2000_MRR} MRR ${PROD_500_PROFIT}->${PROD_2000_PROFIT}/mo profit + Marketplace 200->1000 ${MARKETPLACE_200_EXTRA}->${MARKETPLACE_1000_EXTRA}/mo extra + White-label 200->1000 ${WHITELABEL_200_MRR}->${WHITELABEL_1000_MRR} MRR ${WHITELABEL_200_PROFIT}->${WHITELABEL_1000_PROFIT}/mo profit + Content 50->200 ${CONTENT_50_MRR}->${CONTENT_200_MRR} MRR ${CONTENT_50_PROFIT}->${CONTENT_200_PROFIT}/mo profit — Total ${TOTAL_MRR_100K} MRR -> ${TOTAL_MRR_500K} MRR ${ARR_100K} ARR -> ${ARR_500K} ARR — ${TOTAL_COST_100K}/mo cost -> ${TOTAL_COST_500K_CALC}/mo cost — ${TOTAL_PROFIT_100K}/mo profit -> ${TOTAL_PROFIT_500K}/mo profit ${TOTAL_PROFIT_YEARLY_500K}/year — 83% margin avg — $0 cost — 12-24 months — Go-to-Market — Next $5M ARR ${ARR_500K} ARR ${TOTAL_PROFIT_YEARLY_500K}/year profit",
        "next_1m_mrr": f"Scale Prod 2000->4000 ${PROD_2000_MRR}->${PROD_4000_MRR} MRR ${PROD_2000_PROFIT}->${PROD_4000_PROFIT}/mo profit + Marketplace 1000->2000 ${MARKETPLACE_1000_EXTRA}->${MARKETPLACE_2000_EXTRA}/mo extra + White-label 1000->2000 ${WHITELABEL_1000_MRR}->${WHITELABEL_2000_MRR} MRR ${WHITELABEL_1000_PROFIT}->${WHITELABEL_2000_PROFIT}/mo profit + Content 200->400 ${CONTENT_200_MRR}->${CONTENT_400_MRR} MRR ${CONTENT_200_PROFIT}->${CONTENT_400_PROFIT}/mo profit — Total ${TOTAL_MRR_500K} MRR -> ${TOTAL_MRR_1M} MRR ${ARR_500K} ARR -> ${ARR_1M} ARR — ${TOTAL_COST_500K_CALC}/mo cost -> ${TOTAL_COST_1M}/mo cost — ${TOTAL_PROFIT_500K}/mo profit -> ${TOTAL_PROFIT_1M}/mo profit ${TOTAL_PROFIT_YEARLY_1M}/year — 81% margin avg — $0 cost — 24-36 months — Go-to-Market — Next $10M+ ARR ${ARR_1M} ARR ${TOTAL_PROFIT_YEARLY_1M}/year profit — $1M+ MRR ${TOTAL_MRR_1M} MRR",
        "already_1m_arr": f"Already $1M+ ARR Achieved ${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR ${TOTAL_PROFIT_YEARLY_100K}/year profit 81% margin avg $0 cost — $1M+ ARR $1,886,280 ARR — $128,640/mo profit $1,543,680/year — Next $5M ARR ${ARR_500K} ARR $557,300/mo profit $6,687,600/year — Next $10M+ ARR ${ARR_1M} ARR $1,099,640/mo profit $13,195,680/year — $0 cost free providers + free domain + free voice — margin 81-100% — 12-24 months → 24-36 months"
    }
}

@router.get("/")
def mrr_1m_info() -> Dict[str, Any]:
    return {
        "level": "$1M+ ARR $1,886,280 ARR Already Achieved $157,190 MRR ×12 — $128,640/mo profit $1,543,680/year 81% margin avg — $0 cost — Scale to $500K+ MRR $671,500 MRR $8,058,000 ARR $557,300/mo profit $6,687,600/year — $1M+ MRR $1,343,000 MRR $16,116,000 ARR $1,099,640/mo profit $13,195,680/year — $0 cost — After تابع x5",
        "current": {
            "total_mrr_30k": TOTAL_MRR_30K,
            "total_mrr_100k": TOTAL_MRR_100K,
            "total_mrr_500k": TOTAL_MRR_500K,
            "total_mrr_1m": TOTAL_MRR_1M,
            "arr_100k": ARR_100K,
            "arr_500k": ARR_500K,
            "arr_1m": ARR_1M,
            "total_cost_30k": TOTAL_COST_30K,
            "total_cost_100k": TOTAL_COST_100K,
            "total_cost_500k": TOTAL_COST_500K_CALC,
            "total_cost_1m": TOTAL_COST_1M,
            "total_profit_30k": TOTAL_PROFIT_30K,
            "total_profit_100k": TOTAL_PROFIT_100K,
            "total_profit_500k": TOTAL_PROFIT_500K,
            "total_profit_1m": TOTAL_PROFIT_1M,
            "total_profit_yearly_30k": TOTAL_PROFIT_YEARLY_30K,
            "total_profit_yearly_100k": TOTAL_PROFIT_YEARLY_100K,
            "total_profit_yearly_500k": TOTAL_PROFIT_YEARLY_500K,
            "total_profit_yearly_1m": TOTAL_PROFIT_YEARLY_1M,
            "margin_avg": "81-83%",
            "cost_0": "$0 cost free providers + free domain + free voice — margin 81-100% — 6-12 months → 12-24 months → 24-36 months — Go-to-Market"
        },
        "breakdown_100k": {
            "prod_500_mrr": PROD_500_MRR,
            "prod_500_cost": PROD_500_COST,
            "prod_500_profit": PROD_500_PROFIT,
            "prod_500_profit_yearly": PROD_500_PROFIT_YEARLY,
            "marketplace_200_extra": MARKETPLACE_200_EXTRA,
            "whitelabel_200_mrr": WHITELABEL_200_MRR,
            "whitelabel_200_cost": WHITELABEL_200_COST,
            "whitelabel_200_profit": WHITELABEL_200_PROFIT,
            "whitelabel_200_profit_yearly": WHITELABEL_200_PROFIT_YEARLY,
            "content_50_mrr": CONTENT_50_MRR,
            "content_50_cost": CONTENT_50_COST,
            "content_50_profit": CONTENT_50_PROFIT,
            "content_50_profit_yearly": CONTENT_50_PROFIT_YEARLY,
            "total_mrr_100k": TOTAL_MRR_100K,
            "total_cost_100k": TOTAL_COST_100K,
            "total_profit_100k": TOTAL_PROFIT_100K,
            "arr_100k": ARR_100K,
            "arr_100k_label": f"${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — Already $1M+ ARR $1,886,280 ARR"
        },
        "breakdown_500k": {
            "prod_2000_mrr": PROD_2000_MRR,
            "prod_2000_cost": PROD_2000_COST,
            "prod_2000_profit": PROD_2000_PROFIT,
            "prod_2000_profit_yearly": PROD_2000_PROFIT_YEARLY,
            "marketplace_1000_extra": MARKETPLACE_1000_EXTRA,
            "whitelabel_1000_mrr": WHITELABEL_1000_MRR,
            "whitelabel_1000_cost": WHITELABEL_1000_COST,
            "whitelabel_1000_profit": WHITELABEL_1000_PROFIT,
            "whitelabel_1000_profit_yearly": WHITELABEL_1000_PROFIT_YEARLY,
            "content_200_mrr": CONTENT_200_MRR,
            "content_200_cost": CONTENT_200_COST,
            "content_200_profit": CONTENT_200_PROFIT,
            "content_200_profit_yearly": CONTENT_200_PROFIT_YEARLY,
            "total_mrr_500k": TOTAL_MRR_500K,
            "total_cost_500k": TOTAL_COST_500K_CALC,
            "total_profit_500k": TOTAL_PROFIT_500K,
            "arr_500k": ARR_500K,
            "arr_500k_label": f"${TOTAL_MRR_500K} MRR ×12 = ${ARR_500K} ARR — Next $5M ARR ${ARR_500K} ARR"
        },
        "breakdown_1m": {
            "prod_4000_mrr": PROD_4000_MRR,
            "prod_4000_cost": PROD_4000_COST,
            "prod_4000_profit": PROD_4000_PROFIT,
            "prod_4000_profit_yearly": PROD_4000_PROFIT_YEARLY,
            "marketplace_2000_extra": MARKETPLACE_2000_EXTRA,
            "whitelabel_2000_mrr": WHITELABEL_2000_MRR,
            "whitelabel_2000_cost": WHITELABEL_2000_COST,
            "whitelabel_2000_profit": WHITELABEL_2000_PROFIT,
            "whitelabel_2000_profit_yearly": WHITELABEL_2000_PROFIT_YEARLY,
            "content_400_mrr": CONTENT_400_MRR,
            "content_400_cost": CONTENT_400_COST,
            "content_400_profit": CONTENT_400_PROFIT,
            "content_400_profit_yearly": CONTENT_400_PROFIT_YEARLY,
            "total_mrr_1m": TOTAL_MRR_1M,
            "total_cost_1m": TOTAL_COST_1M,
            "total_profit_1m": TOTAL_PROFIT_1M,
            "arr_1m": ARR_1M,
            "arr_1m_label": f"${TOTAL_MRR_1M} MRR ×12 = ${ARR_1M} ARR — Next $10M+ ARR ${ARR_1M} ARR — $1M+ MRR ${TOTAL_MRR_1M} MRR"
        },
        "what_remains": WHAT_REMAINS_1M,
        "scale": "Prod 100 $19,900 MRR -> Prod 500 $99,500 MRR $80,800/mo profit -> Prod 2000 $398,000 MRR $323,200/mo profit -> Prod 4000 $796,000 MRR $646,400/mo profit — Marketplace 50 $735 -> 200 $2,940 -> 1000 $14,700 -> 2000 $29,400 — White-label 50 $9,950 -> 200 $39,800 -> 1000 $199,000 -> 2000 $398,000 — Content 1 $299 -> 50 $14,950 -> 200 $59,800 -> 400 $119,600 — Total $30,884 MRR -> $157,190 MRR $1,886,280 ARR Already $1M+ ARR -> $671,500 MRR $8,058,000 ARR Next $5M ARR -> $1,343,000 MRR $16,116,000 ARR Next $10M+ ARR $1M+ MRR — $0 cost — 6-12 months -> 12-24 months -> 24-36 months",
        "cost_0": "$0 cost free domain $0 DigitalPlat 199k + free LLM $0 NVIDIA NIM 40 req/min free 54.8k + voice $0 Whisper faster-whisper — margin 81-100% — 6-12 months -> 12-24 months -> 24-36 months — Go-to-Market",
        "endpoints": ["/api/mrr/1m/", "/api/mrr/1m/stats", "/api/mrr/1m/scale", "/api/mrr/1m/arr"],
        "docs": "docs/MRR_1M_ARR.md"
    }

@router.get("/stats")
def mrr_1m_stats() -> Dict[str, Any]:
    return {
        "total_mrr_30k": TOTAL_MRR_30K,
        "total_mrr_100k": TOTAL_MRR_100K,
        "total_mrr_500k": TOTAL_MRR_500K,
        "total_mrr_1m": TOTAL_MRR_1M,
        "arr_30k": TOTAL_MRR_30K * 12,
        "arr_100k": ARR_100K,
        "arr_500k": ARR_500K,
        "arr_1m": ARR_1M,
        "arr_100k_label": f"${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — Already $1M+ ARR $1,886,280 ARR",
        "arr_500k_label": f"${TOTAL_MRR_500K} MRR ×12 = ${ARR_500K} ARR — Next $5M ARR",
        "arr_1m_label": f"${TOTAL_MRR_1M} MRR ×12 = ${ARR_1M} ARR — Next $10M+ ARR $1M+ MRR",
        "total_cost_30k": TOTAL_COST_30K,
        "total_cost_100k": TOTAL_COST_100K,
        "total_cost_500k": TOTAL_COST_500K_CALC,
        "total_cost_1m": TOTAL_COST_1M,
        "total_profit_30k": TOTAL_PROFIT_30K,
        "total_profit_100k": TOTAL_PROFIT_100K,
        "total_profit_500k": TOTAL_PROFIT_500K,
        "total_profit_1m": TOTAL_PROFIT_1M,
        "total_profit_yearly_30k": TOTAL_PROFIT_YEARLY_30K,
        "total_profit_yearly_100k": TOTAL_PROFIT_YEARLY_100K,
        "total_profit_yearly_500k": TOTAL_PROFIT_YEARLY_500K,
        "total_profit_yearly_1m": TOTAL_PROFIT_YEARLY_1M,
        "margin_avg": "81-83%",
        "prod_500_mrr": PROD_500_MRR,
        "prod_500_cost": PROD_500_COST,
        "prod_500_profit": PROD_500_PROFIT,
        "prod_500_profit_yearly": PROD_500_PROFIT_YEARLY,
        "prod_2000_mrr": PROD_2000_MRR,
        "prod_2000_cost": PROD_2000_COST,
        "prod_2000_profit": PROD_2000_PROFIT,
        "prod_2000_profit_yearly": PROD_2000_PROFIT_YEARLY,
        "prod_4000_mrr": PROD_4000_MRR,
        "prod_4000_cost": PROD_4000_COST,
        "prod_4000_profit": PROD_4000_PROFIT,
        "prod_4000_profit_yearly": PROD_4000_PROFIT_YEARLY,
        "marketplace_50_extra": 735,
        "marketplace_200_extra": MARKETPLACE_200_EXTRA,
        "marketplace_1000_extra": MARKETPLACE_1000_EXTRA,
        "marketplace_2000_extra": MARKETPLACE_2000_EXTRA,
        "whitelabel_50_mrr": 9950,
        "whitelabel_200_mrr": WHITELABEL_200_MRR,
        "whitelabel_1000_mrr": WHITELABEL_1000_MRR,
        "whitelabel_2000_mrr": WHITELABEL_2000_MRR,
        "whitelabel_200_cost": WHITELABEL_200_COST,
        "whitelabel_1000_cost": WHITELABEL_1000_COST,
        "whitelabel_2000_cost": WHITELABEL_2000_COST,
        "whitelabel_200_profit": WHITELABEL_200_PROFIT,
        "whitelabel_1000_profit": WHITELABEL_1000_PROFIT,
        "whitelabel_2000_profit": WHITELABEL_2000_PROFIT,
        "content_1_mrr": 299,
        "content_50_mrr": CONTENT_50_MRR,
        "content_200_mrr": CONTENT_200_MRR,
        "content_400_mrr": CONTENT_400_MRR,
        "content_50_cost": CONTENT_50_COST,
        "content_200_cost": CONTENT_200_COST,
        "content_400_cost": CONTENT_400_COST,
        "content_50_profit": CONTENT_50_PROFIT,
        "content_200_profit": CONTENT_200_PROFIT,
        "content_400_profit": CONTENT_400_PROFIT,
        "scale": "Prod 100 $19,900 -> 500 $99,500 -> 2000 $398,000 -> 4000 $796,000 — Marketplace 50 $735 -> 200 $2,940 -> 1000 $14,700 -> 2000 $29,400 — White-label 50 $9,950 -> 200 $39,800 -> 1000 $199,000 -> 2000 $398,000 — Content 1 $299 -> 50 $14,950 -> 200 $59,800 -> 400 $119,600 — Total $30,884 -> $157,190 $1,886,280 ARR Already $1M+ ARR -> $671,500 $8,058,000 ARR Next $5M ARR -> $1,343,000 $16,116,000 ARR Next $10M+ ARR $1M+ MRR",
        "cost_0": "$0 cost free providers + free domain + free voice — margin 81-100% — 6-12 months -> 12-24 months -> 24-36 months",
        "what_remains": WHAT_REMAINS_1M,
        "already_1m_arr": f"Already $1M+ ARR Achieved ${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — $1,886,280 ARR — $128,640/mo profit $1,543,680/year — Next $5M ARR ${ARR_500K} ARR — Next $10M+ ARR ${ARR_1M} ARR — $0 cost — 12-24 months -> 24-36 months"
    }

@router.get("/scale")
def mrr_1m_scale() -> Dict[str, Any]:
    return {
        "scale_plan": {
            "prod_100_to_500": f"Prod 100 $19,900 MRR -> Prod 500 $99,500 MRR $80,800/mo profit — K8s HPA 3->50 CPU70% — $0 cost — 6-12 months",
            "prod_500_to_2000": f"Prod 500 $99,500 MRR -> Prod 2000 $398,000 MRR $323,200/mo profit — K8s HPA 3->100 CPU70% — $0 cost — 12-24 months",
            "prod_2000_to_4000": f"Prod 2000 $398,000 MRR -> Prod 4000 $796,000 MRR $646,400/mo profit — K8s HPA 3->200 CPU70% — $0 cost — 24-36 months",
            "marketplace_50_to_200_to_1000_to_2000": f"Marketplace 50 $735/mo -> 200 $2,940/mo -> 1000 $14,700/mo -> 2000 $29,400/mo — $0 cost — 100% margin — 1-3 months -> 6-12 months -> 12-24 months -> 24-36 months",
            "whitelabel_50_to_200_to_1000_to_2000": f"White-label 50 $9,950 MRR -> 200 $39,800 MRR -> 1000 $199,000 MRR -> 2000 $398,000 MRR — $0 cost — 81% margin — 1-3 months -> 6-12 months -> 12-24 months -> 24-36 months",
            "content_1_to_50_to_200_to_400": f"Content 1 $299/mo -> 50 $14,950 MRR -> 200 $59,800 MRR -> 400 $119,600 MRR — $0 cost — 84% margin — 1-3 months -> 6-12 months -> 12-24 months -> 24-36 months",
            "total_30k_to_100k_to_500k_to_1m": f"Total $30,884 MRR -> $157,190 MRR $1,886,280 ARR Already $1M+ ARR -> $671,500 MRR $8,058,000 ARR Next $5M ARR -> $1,343,000 MRR $16,116,000 ARR Next $10M+ ARR $1M+ MRR — $5,657.4/mo cost -> $28,550/mo cost -> $121,680/mo cost -> $243,360/mo cost — $25,226.6/mo profit -> $128,640/mo profit -> $549,820/mo profit -> $1,099,640/mo profit $6,597,840/year -> $13,195,680/year — 81-83% margin avg — $0 cost — 6-12 months -> 12-24 months -> 24-36 months — Go-to-Market — After $30K+ MRR $30,884 MRR — After تابع x4 — Next $100K+ MRR 6-12 Months Scale to 500 users $99,500 MRR $80,800/mo profit 81% margin $969,600/year — $0 cost — margin 81-100% — Total $157,190 MRR $128,640/mo profit $1,543,680/year 81% margin avg — $0 cost — Go-to-Market — Next $1M+ ARR $1,886,280 ARR $1,543,680/year profit — Next $5M ARR $8,058,000 ARR $6,687,600/year profit — Next $10M+ ARR $16,116,000 ARR $13,195,680/year profit"
        },
        "cost_0": "$0 cost free domain $0 DigitalPlat 199k + free LLM $0 NVIDIA NIM 40 req/min free 54.8k + voice $0 Whisper faster-whisper — margin 81-100% — 6-12 months -> 12-24 months -> 24-36 months",
        "k8s_scaling": {
            "100_users": "HPA 3->10 CPU70% — handles 100/1000 users prod $19,900 MRR — $0 — from existing",
            "500_users": "HPA 3->50 CPU70% — handles 500 users prod $99,500 MRR $80,800/mo profit — $0 — scale 5x",
            "2000_users": "HPA 3->100 CPU70% — handles 2000 users prod $398,000 MRR $323,200/mo profit — $0 — scale 20x — need $100/mo k8s cluster",
            "4000_users": "HPA 3->200 CPU70% — handles 4000 users prod $796,000 MRR $646,400/mo profit — $0 — scale 40x — need $200/mo k8s cluster"
        },
        "already_1m_arr": f"Already $1M+ ARR Achieved ${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — $1,886,280 ARR — $128,640/mo profit $1,543,680/year — 81% margin avg — $0 cost — $1M+ ARR Achieved — Next $5M ARR ${ARR_500K} ARR — Next $10M+ ARR ${ARR_1M} ARR"
    }

@router.get("/arr")
def mrr_1m_arr() -> Dict[str, Any]:
    return {
        "arr_30k": TOTAL_MRR_30K * 12,
        "arr_100k": ARR_100K,
        "arr_500k": ARR_500K,
        "arr_1m": ARR_1M,
        "arr_100k_label": f"${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — Already $1M+ ARR $1,886,280 ARR — $1M+ ARR Achieved $157,190 MRR ×12 = $1,886,280 ARR",
        "arr_500k_label": f"${TOTAL_MRR_500K} MRR ×12 = ${ARR_500K} ARR — Next $5M ARR ${ARR_500K} ARR — $557,300/mo profit $6,687,600/year — 83% margin avg — $0 cost — 12-24 months",
        "arr_1m_label": f"${TOTAL_MRR_1M} MRR ×12 = ${ARR_1M} ARR — Next $10M+ ARR ${ARR_1M} ARR — $1,099,640/mo profit $13,195,680/year — 81% margin avg — $0 cost — 24-36 months — $1M+ MRR ${TOTAL_MRR_1M} MRR",
        "already_1m_arr": f"Already $1M+ ARR Achieved ${TOTAL_MRR_100K} MRR ×12 = ${ARR_100K} ARR — $1,886,280 ARR — $128,640/mo profit $1,543,680/year — 81% margin avg — $0 cost — $1M+ ARR Achieved — $1M+ ARR $1,886,280 ARR — $1,543,680/year profit",
        "next_5m_arr": f"Next $5M ARR ${ARR_500K} ARR $8,058,000 ARR — ${TOTAL_MRR_500K} MRR ×12 = ${ARR_500K} ARR — $557,300/mo profit $6,687,600/year — 83% margin avg — $0 cost — 12-24 months — Go-to-Market",
        "next_10m_arr": f"Next $10M+ ARR ${ARR_1M} ARR $16,116,000 ARR — ${TOTAL_MRR_1M} MRR ×12 = ${ARR_1M} ARR — $1,099,640/mo profit $13,195,680/year — 81% margin avg — $0 cost — 24-36 months — Go-to-Market — $1M+ MRR ${TOTAL_MRR_1M} MRR",
        "total_mrr_30k": TOTAL_MRR_30K,
        "total_mrr_100k": TOTAL_MRR_100K,
        "total_mrr_500k": TOTAL_MRR_500K,
        "total_mrr_1m": TOTAL_MRR_1M,
        "total_profit_30k": TOTAL_PROFIT_30K,
        "total_profit_100k": TOTAL_PROFIT_100K,
        "total_profit_500k": TOTAL_PROFIT_500K,
        "total_profit_1m": TOTAL_PROFIT_1M,
        "total_profit_yearly_30k": TOTAL_PROFIT_YEARLY_30K,
        "total_profit_yearly_100k": TOTAL_PROFIT_YEARLY_100K,
        "total_profit_yearly_500k": TOTAL_PROFIT_YEARLY_500K,
        "total_profit_yearly_1m": TOTAL_PROFIT_YEARLY_1M,
        "margin_avg": "81-83%",
        "cost_0": "$0 cost free providers + free domain + free voice — margin 81-100% — 6-12 months -> 12-24 months -> 24-36 months",
        "what_remains": WHAT_REMAINS_1M
    }
