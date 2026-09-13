"""
Free Domain Router - Task D1 - From DigitalPlatDev/FreeDomain 199k stars
Provides free domain guide via DigitalPlat FreeDomain $0
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/domain/free", tags=["domain-free"])

@router.get("/")
async def free_domain_info():
    return {
        "domain": "Free Domain via DigitalPlat FreeDomain — 199k stars — 500k+ domains — $0",
        "reality": "REAL_GUIDE - Real free domains via DigitalPlat, not mock — $0 cost",
        "repo": "https://github.com/DigitalPlatDev/FreeDomain — 199k stars, 4.4k forks",
        "dashboard": "https://dash.domain.digitalplat.org/ — Register free domain",
        "extensions": {
            ".DPDNS.ORG": "Recommended for AI Agency OS — tech vibe",
            ".US.KG": "Recommended — short, memorable — e.g., ai-agency-os.us.kg",
            ".QZZ.IO": "Tech vibe — e.g., ai-agency.qzz.io",
            ".XX.KG": "Short — e.g., ai-agency.xx.kg",
            ".QD.JE": "New extension"
        },
        "psl": "All extensions in PSL (Public Suffix List) — Cloudflare accepts as real domains — https://publicsuffix.org/list/",
        "trusted": "500k+ domains registered — nonprofit — DigitalPlat Foundation — Edward Hsing founder — AGPL-3.0",
        "quick_start": {
            "1_register_account": "Go to https://dash.domain.digitalplat.org/ → Sign in with GitHub (KYC) → Verify email — 1 min",
            "2_register_domain": "Dashboard → Register Domain → Choose extension e.g., .US.KG → Name e.g., ai-agency-os → ai-agency-os.us.kg → Submit — instant or few hours — $0",
            "3_configure_dns_cloudflare": "Cloudflare → Add Site → ai-agency-os.us.kg → Add A records: @ → YOUR_IP, api → YOUR_IP, docs → YOUR_IP → Cloudflare gives NS → DigitalPlat Dashboard → Custom Nameservers → Enter Cloudflare NS → Wait 5-60 min — $0",
            "4_deploy": "Set DOMAIN=ai-agency-os.us.kg + API_DOMAIN=api.ai-agency-os.us.kg + CORS_ORIGINS=https://... + VITE_API_URL=https://api... + docker-compose -f docker-compose.prod.yml up -d — $0",
            "5_ssl": "Cloudflare proxy orange cloud → automatic SSL $0 — or Let's Encrypt via certbot profile $0"
        },
        "examples": {
            "ai_agency_os_us_kg": "ai-agency-os.us.kg — for main site",
            "api_us_kg": "api.ai-agency-os.us.kg — for API",
            "docs_us_kg": "docs.ai-agency-os.us.kg — for docs",
            "ai_agency_dpdns_org": "ai-agency-os.dpdns.org — alternative"
        },
        "cost_comparison": {
            "free_us_kg": "$0 — Free, 500k+ trusted, PSL Cloudflare accepted, nonprofit — cons: non-standard TLD, could disappear but 500k suggests sustainable",
            "paid_com": "$12/year — Professional, standard, you own it — cons: costs $12/year",
            "paid_os": "$12-50/year — Brand match ai-agency.os — cons: costs"
        },
        "recommendation": {
            "beta_10": "Use free domain $0 — e.g., ai-agency-os.us.kg — for Beta 10 free demo — 5 min setup — $0",
            "prod_100": "Use paid ai-agency.os $12/year — more professional — or keep free $0 for 100% margin — $12/year vs $0",
            "white_label": "Each white-label client can get free domain via same process — $0 — 50 clients × $0 domain = $0 cost vs $12*50=$600/year"
        },
        "script": "./scripts/setup-free-domain.sh ai-agency-os us.kg — automates guide — $0",
        "docs": "docs/FREE_DOMAIN_GUIDE.md — Full guide with Cloudflare, FreeDNS, Hostry, SSL, deployment",
        "tutorial": "https://github.com/DigitalPlatDev/FreeDomain/blob/main/documents/tutorial/index.md",
        "learn": "https://github.com/DigitalPlatDev/FreeDomain/blob/main/LEARN.md — book-style DNS, website, email, operations, advanced",
        "app_source": "https://github.com/DigitalPlatDev/Domain-OSS — AGPL-3.0 — application source",
        "endpoints": {
            "info": "GET /api/domain/free/ — this guide",
            "check": "GET /api/domain/free/check/{domain} — check if domain available (mock, real via dashboard)",
            "guide": "GET /api/domain/free/guide — detailed guide"
        }
    }

@router.get("/check/{domain}")
async def check_domain(domain: str):
    # Mock check — real check via DigitalPlat dashboard
    # In real, would call DigitalPlat API if available, but dashboard is manual
    available_extensions = [".dpdns.org", ".us.kg", ".qzz.io", ".xx.kg", ".qd.je"]
    
    # Simple mock availability — if contains test, available, else check
    is_available = True
    if len(domain) < 3:
        is_available = False
    
    return {
        "domain": domain,
        "checked": True,
        "available": is_available,
        "available_with_extensions": [f"{domain}{ext}" for ext in available_extensions] if is_available else [],
        "mode": "mock",
        "reality": "MOCK_CHECK - Real check via https://dash.domain.digitalplat.org/ — dashboard manual",
        "how_to_check_real": f"Go to https://dash.domain.digitalplat.org/ → Register Domain → Enter {domain} → Choose extension → Check availability — $0",
        "note": "DigitalPlat FreeDomain does not have public API for availability check — must use dashboard — this endpoint is mock guide"
    }

@router.get("/guide")
async def detailed_guide():
    return {
        "guide": "Free Domain Detailed Guide — DigitalPlat FreeDomain — $0",
        "steps": [
            {
                "step": 1,
                "title": "Register Account",
                "action": "Go to https://dash.domain.digitalplat.org/",
                "details": "Sign in with GitHub (KYC) — Verify email — 1 min — $0",
                "evidence": "Repo 199k stars, 500k+ domains"
            },
            {
                "step": 2,
                "title": "Register Domain",
                "action": "Dashboard → Register Domain → Choose extension .US.KG or .DPDNS.ORG → Name ai-agency-os → ai-agency-os.us.kg → Submit",
                "details": "Instant or few hours approval — $0 — 500k+ domains registered",
                "extensions": [".DPDNS.ORG", ".US.KG", ".QZZ.IO", ".XX.KG", ".QD.JE"]
            },
            {
                "step": 3,
                "title": "Configure DNS Cloudflare $0",
                "action": "Cloudflare → Add Site → ai-agency-os.us.kg → Add A records @, api, docs → Cloudflare NS → DigitalPlat Custom Nameservers",
                "details": "Cloudflare accepts free domains because they are in PSL — https://publicsuffix.org/list/ — qzz.io, us.kg in PSL — community tested — Wait 5-60 min — SSL Full strict free $0"
            },
            {
                "step": 4,
                "title": "Deploy AI Agency OS",
                "action": "Set DOMAIN, API_DOMAIN, CORS_ORIGINS, VITE_API_URL env + docker-compose -f docker-compose.prod.yml up -d",
                "details": "Backend 8000, frontend 80/443, postgres, redis, chroma, minio, ollama — full stack — $0 + domain $0",
                "commands": [
                    "export DOMAIN=ai-agency-os.us.kg",
                    "export API_DOMAIN=api.ai-agency-os.us.kg",
                    "echo \"CORS_ORIGINS=https://$DOMAIN,https://$API_DOMAIN\" >> .env.prod",
                    "docker-compose -f docker-compose.prod.yml up -d",
                    "curl https://$API_DOMAIN/api/health"
                ]
            },
            {
                "step": 5,
                "title": "SSL $0",
                "action": "Cloudflare proxy orange cloud → automatic SSL $0 — or Let's Encrypt via certbot profile",
                "details": "docker-compose -f docker-compose.prod.yml --profile ssl up -d certbot — certonly --webroot",
                "commands": [
                    "docker-compose -f docker-compose.prod.yml --profile ssl up -d",
                    "certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@ai-agency-os.us.kg --agree-tos --no-eff-email -d ai-agency-os.us.kg -d api.ai-agency-os.us.kg"
                ]
            }
        ],
        "cost": "$0 free domain + $0 Cloudflare + $0 SSL + $0 deployment — vs $12/year paid domain",
        "script": "./scripts/setup-free-domain.sh ai-agency-os us.kg",
        "docs": "docs/FREE_DOMAIN_GUIDE.md"
    }
