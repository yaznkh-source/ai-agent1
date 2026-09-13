"""
Curated AI Tools Router - Task D2 - From cporter202/ai-agent-tools 477 stars
Curated list of AI tools for marketplace expansion
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/tools/curated", tags=["tools-curated"])

CURATED_TOOLS = [
    {
        "id": "viralwave-studio",
        "name": "ViralWave Studio",
        "category": "Social Media + Video + Content",
        "featured": True,
        "description": "AI-powered platform to transform social media content creation, scheduling, management across multiple platforms",
        "website": "https://viralwavestudio.com/",
        "features": [
            "Video Generator Sora 2: Text-to-video 1080p, 10s 7 tokens $0.34 vs $1 elsewhere, 15s 12 tokens $0.58 vs $1.50 — direct posting — no camera needed",
            "Brand Authority Image Nano Banana Pro: Upload 3 images of yourself, AI places you in every generated image — consistent brand",
            "Post Generator: AI content, multi-platform FB IG LinkedIn Threads Pinterest TikTok YouTube WordPress, brand voice customization, hashtag optimization",
            "Blog Generator: WordPress 1500-2000 words SEO-optimized, meta tags, featured images, one-click publishing",
            "Multi-Platform Management: Connect 8 platforms — unified dashboard, cross-posting, platform-specific optimization",
            "Bulk Content Generation: Mass content weeks/months from single topic, campaign planning",
            "Free Plan: 10 free posts/mo no credit card — token-based 1 text 3 image 7-12 video"
        ],
        "pricing": "$49/mo",
        "profit_30pct": "$14.7/mo per client via marketplace 30% fee",
        "integration": "content-creator agent bulk content, Sora 2 video $0.34, white-label Pro $199/mo includes social automation",
        "stars": "Featured Monthly in ai-agent-tools repo"
    },
    {
        "id": "postiz",
        "name": "Postiz",
        "category": "Social Scheduling",
        "featured": True,
        "description": "Agentic AI social media scheduling 20+ platforms — Canva-like design + AI image gen + auto actions + analytics + API/n8n/Make/Zapier",
        "website": "https://postiz.com/",
        "features": [
            "Agentic AI social media scheduling",
            "20+ platforms: FB, IG, LinkedIn, Threads, Pinterest, TikTok, YouTube, WordPress, etc",
            "Canva-like design tool",
            "AI image generation",
            "Automatic actions and workflows",
            "Social media analytics",
            "API, n8n, Make.com, Zapier integration"
        ],
        "pricing": "$29/mo",
        "profit_30pct": "$8.7/mo",
        "integration": "Agency social scheduling for clients — Pro $199/mo includes $29 Postiz — cost $29 revenue $199 profit $170",
        "stars": "From ai-agent-tools list"
    },
    {
        "id": "sora-2",
        "name": "Sora 2",
        "category": "Video Generation",
        "featured": True,
        "description": "Text-to-video 1080p via ViralWave Studio $0.34/10s $0.58/15s — no camera needed",
        "website": "https://viralwavestudio.com/",
        "features": ["Text-to-video 1080p", "10s $0.34, 15s $0.58", "Direct posting to social", "No camera needed"],
        "pricing": "$0.34/10s video",
        "profit_30pct": "$0.10 per video",
        "integration": "content-creator agent video generation for clients — sell $10/video cost $0.34 profit $9.66 96% margin"
    },
    {
        "id": "dall-e-2",
        "name": "DALL·E 2",
        "category": "Image Generation",
        "description": "Realistic images from text — OpenAI",
        "website": "https://openai.com/dall-e-2/",
        "pricing": "$0.02/image",
        "integration": "ui-ux-designer, brand-strategist agents — image gen for clients"
    },
    {
        "id": "elevenlabs",
        "name": "ElevenLabs",
        "category": "Voice Generation",
        "description": "AI voice generation — realistic voices",
        "website": "https://elevenlabs.io/",
        "pricing": "$5/mo starter",
        "integration": "support-agent, content-creator — AI voice for clients"
    },
    {
        "id": "whisper-local",
        "name": "Whisper Local",
        "category": "Speech-to-Text",
        "description": "OpenAI Whisper local free via free-claude-code integration — speech-to-text $0",
        "website": "https://github.com/openai/whisper",
        "pricing": "$0 local free",
        "integration": "Voice notes via free-claude-code — $0 — 100% margin — from free-claude-code repo",
        "free": True
    },
    {
        "id": "copy-ai",
        "name": "Copy.ai",
        "category": "Marketing Copy",
        "description": "AI copywriting — marketing copy generation",
        "website": "https://copy.ai/",
        "pricing": "$49/mo",
        "integration": "seo-specialist, content-creator agents — copy for clients"
    },
    {
        "id": "otter-ai",
        "name": "Otter.ai",
        "category": "Meeting Transcription",
        "description": "AI meeting assistant — transcription",
        "website": "https://otter.ai/",
        "pricing": "$16/mo",
        "integration": "Transcribe client calls — agency operations"
    },
    {
        "id": "perplexity-ai",
        "name": "Perplexity AI",
        "category": "Research + Search",
        "description": "AI-powered search engine and chatbot",
        "website": "https://perplexity.ai/",
        "pricing": "Free + $20/mo Pro",
        "integration": "researcher agent — deep research workflows"
    },
    {
        "id": "github-copilot",
        "name": "GitHub Copilot",
        "category": "Code with AI",
        "description": "AI pair programmer — code completion",
        "website": "https://github.com/features/copilot",
        "pricing": "$10/mo",
        "integration": "backend-dev, frontend-dev agents — code completion tool"
    }
]

@router.get("/")
async def curated_tools_info():
    return {
        "tools": "Curated AI Tools — From cporter202/ai-agent-tools 477 stars — Marketplace Expansion",
        "reality": "REAL_CURATED_LIST - Real tools from awesome-ai-tools repo, not mock — marketplace expansion ideas",
        "repo": "https://github.com/cporter202/ai-agent-tools — 477 stars, 124 forks, 13 commits — documentation, not executable code",
        "categories": ["AI Text Chatbots", "Code with AI", "Generative Images", "Generative Video", "Generative Audio", "Marketing", "Phone Call Agents", "Productivity", "Research"],
        "count": len(CURATED_TOOLS),
        "featured": [t for t in CURATED_TOOLS if t.get("featured")],
        "tools": CURATED_TOOLS,
        "monetization": {
            "marketplace_30pct": "Tool costs $49/mo, charge client $49/mo, keep $14.7 30% — like Apple App Store",
            "white_label": "Include tools in Pro $199/mo — cost $29 Postiz + $0.34*10 videos $3.4 + $5 ElevenLabs = $37.4 cost, $199 revenue, $161.6 profit 81% margin",
            "bulk_content": "Generate weeks/months content from single topic — sell as service $299/mo — cost $37.4 tools + $10 LLM = $47.4, profit $251.6 84% margin",
            "authflow_pattern": "From awesome-ai-tools — Authflow enables monetize custom GPTs with paywalls — we implement similar via marketplace 30% fee"
        },
        "integration_plan": {
            "backend": "Add to marketplace.py — new skills/tools — 20+ tools",
            "frontend": "Add to MarketplaceView.tsx — featured + search",
            "agents": "Update content-creator, seo-specialist, support-agent to use new tools",
            "docs": "docs/CURATED_AI_TOOLS.md + docs/MARKETPLACE_GUIDE.md"
        },
        "endpoints": {
            "info": "GET /api/tools/curated/ — this",
            "list": "GET /api/tools/curated/list — list all curated tools",
            "featured": "GET /api/tools/curated/featured — featured tools ViralWave Postiz Sora2",
            "category": "GET /api/tools/curated/category/{category} — filter by category"
        }
    }

@router.get("/list")
async def list_curated_tools():
    return {
        "tools": CURATED_TOOLS,
        "count": len(CURATED_TOOLS),
        "categories": list(set([t["category"] for t in CURATED_TOOLS])),
        "featured_count": len([t for t in CURATED_TOOLS if t.get("featured")]),
        "free_count": len([t for t in CURATED_TOOLS if t.get("free")])
    }

@router.get("/featured")
async def featured_tools():
    featured = [t for t in CURATED_TOOLS if t.get("featured")]
    return {
        "featured": featured,
        "count": len(featured),
        "note": "Featured Monthly: ViralWave Studio — Sora 2 video $0.34/10s, Nano Banana Pro brand authority, bulk content, 10 free posts/mo"
    }

@router.get("/category/{category}")
async def by_category(category: str):
    filtered = [t for t in CURATED_TOOLS if category.lower() in t["category"].lower()]
    return {
        "category": category,
        "tools": filtered,
        "count": len(filtered)
    }
