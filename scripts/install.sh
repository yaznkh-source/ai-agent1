#!/bin/bash
# AI Agency OS - On-Premise Installer v10
# One-command installer for your own server

set -e

echo "🤖 AI Agency OS - On-Premise Installer v10"
echo "=========================================="
echo "68 agents, 292 skills, 18 routers, 21 views, Enterprise Ready"
echo ""

# Colors
GREEN='\033[0;32m'
VIOLET='\033[0;35m'
NC='\033[0m' # No Color

# Check requirements
check_requirements() {
    echo "🔍 Checking requirements..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Installing..."
        curl -fsSL https://get.docker.com | sh
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose not found. Please install docker-compose"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Requirements OK${NC}"
}

# Setup env
setup_env() {
    echo ""
    echo "📝 Setting up environment..."
    
    if [ ! -f .env.prod ]; then
        cp .env.prod.example .env.prod
        echo "📄 Created .env.prod from example"
        echo "⚠️  Please edit .env.prod with your secrets:"
        echo "   - POSTGRES_PASSWORD"
        echo "   - REDIS_PASSWORD"
        echo "   - JWT_SECRET"
        echo "   - OPENAI_API_KEY (or use Ollama)"
        echo "   - STRIPE keys (optional)"
        echo "   - SENDGRID key (optional)"
        echo ""
        read -p "Press enter after editing .env.prod or Ctrl+C to edit now..."
    fi
    
    echo -e "${GREEN}✅ Env setup done${NC}"
}

# Pull and start
start_services() {
    echo ""
    echo "🚀 Starting AI Agency OS..."
    
    # Use prod compose
    if docker compose version &> /dev/null; then
        COMPOSE="docker compose -f docker-compose.prod.yml"
    else
        COMPOSE="docker-compose -f docker-compose.prod.yml"
    fi
    
    $COMPOSE pull
    $COMPOSE up -d
    
    echo ""
    echo "⏳ Waiting for services to be healthy..."
    sleep 10
    
    # Check backend health
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            echo -e "${GREEN}✅ Backend healthy${NC}"
            break
        fi
        echo "Waiting for backend... $i/30"
        sleep 2
    done
    
    echo ""
    echo -e "${VIOLET}🎉 AI Agency OS is running!${NC}"
    echo ""
    echo "Frontend: http://localhost (or http://your-server-ip)"
    echo "Backend: http://localhost:8000/api/docs"
    echo "Agents: http://localhost:8000/api/agents/ (68)"
    echo "Skills: http://localhost:8000/api/skills/ (292)"
    echo ""
    echo "Optional services:"
    echo "  MinIO (S3): http://localhost:9001 (minioadmin / from .env.prod)"
    echo "  Ollama: http://localhost:11434"
    echo "  Prometheus: http://localhost:9090 (with --profile monitoring)"
    echo "  Grafana: http://localhost:3000 (with --profile monitoring)"
    echo ""
    echo "To enable monitoring:"
    echo "  $COMPOSE --profile monitoring up -d"
    echo ""
    echo "To view logs:"
    echo "  $COMPOSE logs -f backend"
    echo "  $COMPOSE logs -f frontend"
    echo ""
    echo "To stop:"
    echo "  $COMPOSE down"
    echo ""
    echo "To update:"
    echo "  git pull && $COMPOSE pull && $COMPOSE up -d"
}

# White-label setup
setup_whitelabel() {
    echo ""
    read -p "Do you want to setup white-label branding? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Brand name: " BRAND_NAME
        read -p "Primary color (e.g. #FF6B6B): " PRIMARY_COLOR
        read -p "Logo URL: " LOGO_URL
        read -p "Domain (e.g. app.your-agency.com): " DOMAIN
        
        echo ""
        echo "Updating white-label via API..."
        curl -X PUT http://localhost:8000/api/teams/team_1/settings/white-label \
          -H "Content-Type: application/json" \
          -d "{\"enabled\": true, \"brand_name\": \"$BRAND_NAME\", \"primary_color\": \"$PRIMARY_COLOR\", \"logo_url\": \"$LOGO_URL\", \"domain\": \"$DOMAIN\"}" \
          || echo "⚠️  Failed to update white-label - do it manually via UI or API later"
        
        echo -e "${GREEN}✅ White-label setup done${NC}"
    fi
}

# Main
main() {
    check_requirements
    setup_env
    start_services
    setup_whitelabel
    
    echo ""
    echo -e "${VIOLET}🎉 Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Open http://localhost - you should see Landing Page"
    echo "2. Create account, create project"
    echo "3. Run agent: backend-dev 'Build REST API'"
    echo "4. Check client portal, billing, analytics"
    echo "5. Setup Stripe, SendGrid, S3 for production"
    echo "6. For custom domain + SSL: see docs/WHITELABEL.md and use certbot profile"
    echo ""
    echo "Docs: ./docs/ - BUSINESS_PLAN, WHITELABEL, ARCHITECTURE, API, VIDEO_SCRIPT"
    echo "SDKs: ./sdk/python + ./sdk/typescript"
    echo "Support: https://github.com/yaznkh-source/ai-agent1/issues"
    echo ""
    echo "Happy building! 🚀"
}

main
