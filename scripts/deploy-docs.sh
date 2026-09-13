#!/bin/bash
# AI Agency OS - Deploy Docs Site to Vercel / GitHub Pages / Cloudflare Pages
# Docusaurus build + deploy - docs.ai-agency.os

set -e

GREEN='\033[0;32m'
VIOLET='\033[0;35m'
NC='\033[0m'

echo -e "${VIOLET}📚 AI Agency OS - Deploy Docs Site - Docusaurus${NC}"
echo "=================================================="
echo "68 Agents, 292 Skills, 20 Routers, 28 Views, Docs Site"
echo ""

# Check
check_requirements() {
    echo "🔍 Checking requirements..."
    if ! command -v node &> /dev/null; then echo "❌ Node not found"; exit 1; fi
    if ! command -v npm &> /dev/null; then echo "❌ NPM not found"; exit 1; fi
    echo -e "${GREEN}✅ Node $(node -v) + NPM $(npm -v) OK${NC}"
}

# Setup Docusaurus if not exists
setup_docusaurus() {
    echo ""
    echo "📦 Setting up Docusaurus..."
    
    if [ ! -d "docs-site" ]; then
        echo "Creating docs-site via npx create-docusaurus..."
        npx create-docusaurus@latest docs-site classic --typescript --skip-install
    fi
    
    cd docs-site
    
    # Install
    npm install
    
    # Copy our custom config if exists
    if [ -f "../docs-site/docusaurus.config.js" ]; then
        echo "✅ Custom docusaurus.config.js exists - using ours (violet theme)"
    fi
    
    if [ -f "../docs-site/src/css/custom.css" ]; then
        echo "✅ Custom CSS violet theme exists"
    fi
    
    if [ -f "../docs-site/src/pages/index.js" ]; then
        echo "✅ Custom homepage hero 68/292 exists"
    fi
    
    # Copy docs
    echo "📄 Copying docs from ../docs/ to ./docs/..."
    mkdir -p docs
    cp ../docs/*.md docs/ 2>/dev/null || echo "No docs/*.md to copy"
    cp ../FINAL_PRODUCTION_READY.md docs/ 2>/dev/null || true
    cp ../RELEASE_NOTES.md docs/ 2>/dev/null || true
    cp ../README.md docs/ 2>/dev/null || true
    
    echo -e "${GREEN}✅ Docusaurus setup done${NC}"
    cd ..
}

# Build
build_docs() {
    echo ""
    echo "🔨 Building docs site..."
    cd docs-site
    npm run build
    
    echo ""
    echo -e "${GREEN}✅ Build done - static files in docs-site/build/${NC}"
    echo "   Size: $(du -sh build | cut -f1)"
    echo "   Files: $(find build -type f | wc -l) files"
    cd ..
}

# Deploy Vercel
deploy_vercel() {
    echo ""
    echo "🚀 Deploy to Vercel - docs.ai-agency.os"
    echo "   Vercel: Best for Docusaurus - instant, global CDN, custom domain"
    
    if ! command -v vercel &> /dev/null; then
        echo "Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    cd docs-site
    vercel --prod --yes
    
    echo ""
    echo -e "${GREEN}✅ Deployed to Vercel${NC}"
    echo "   URL: https://docs-site-...vercel.app"
    echo "   Custom domain: Add docs.ai-agency.os in Vercel dashboard → Domains → Add → CNAME"
    echo "   Env: No env needed for docs"
    cd ..
}

# Deploy GitHub Pages
deploy_github_pages() {
    echo ""
    echo "🚀 Deploy to GitHub Pages - yaznkh-source.github.io/ai-agent1"
    echo "   Free, GitHub native, custom domain via CNAME file"
    
    cd docs-site
    
    # Setup for GH Pages
    # docusaurus.config.js should have url: https://yaznkh-source.github.io, baseUrl: /ai-agent1/
    # For custom domain docs.ai-agency.os, add CNAME file in static/
    
    echo "docs.ai-agency.os" > static/CNAME
    
    npm run deploy
    
    echo ""
    echo -e "${GREEN}✅ Deployed to GitHub Pages${NC}"
    echo "   URL: https://yaznkh-source.github.io/ai-agent1/"
    echo "   Custom domain: https://docs.ai-agency.os (via static/CNAME)"
    echo "   Enable in GitHub repo → Settings → Pages → Source: gh-pages branch"
    cd ..
}

# Deploy Cloudflare Pages
deploy_cloudflare() {
    echo ""
    echo "🚀 Deploy to Cloudflare Pages - docs.ai-agency.os"
    echo "   Fastest, global, free, custom domain, best for production"
    
    if ! command -v wrangler &> /dev/null; then
        echo "Installing Wrangler..."
        npm install -g wrangler
    fi
    
    cd docs-site
    
    # Build already done
    wrangler pages publish build --project-name=ai-agency-os-docs
    
    echo ""
    echo -e "${GREEN}✅ Deployed to Cloudflare Pages${NC}"
    echo "   URL: https://ai-agency-os-docs.pages.dev"
    echo "   Custom domain: Cloudflare dashboard → Pages → ai-agency-os-docs → Custom domains → Add docs.ai-agency.os"
    cd ..
}

# Main
main() {
    check_requirements
    setup_docusaurus
    build_docs
    
    echo ""
    echo "Choose deploy target:"
    echo "1. Vercel (recommended for Docusaurus)"
    echo "2. GitHub Pages (free, GitHub native)"
    echo "3. Cloudflare Pages (fastest, production)"
    echo "4. All three"
    echo "5. Skip deploy - just build"
    
    read -p "Enter choice (1-5): " -n 1 -r
    echo
    
    case $REPLY in
        1) deploy_vercel ;;
        2) deploy_github_pages ;;
        3) deploy_cloudflare ;;
        4) deploy_vercel; deploy_github_pages; deploy_cloudflare ;;
        5) echo "Skipped deploy - build only" ;;
        *) echo "Invalid choice - skipped deploy" ;;
    esac
    
    echo ""
    echo -e "${VIOLET}🎉 Docs site build + deploy complete!${NC}"
    echo ""
    echo "Next:"
    echo "- Docs live at your chosen URL"
    echo "- Custom domain docs.ai-agency.os - add CNAME + configure DNS"
    echo "- Update README.md with docs link"
    echo "- Add Algolia DocSearch for search - https://docsearch.algolia.com/apply/"
    echo "- SEO: Submit sitemap to Google Search Console - /sitemap.xml"
    echo ""
    echo "Docs content:"
    echo "- Quickstart 5min, Architecture 68/292, API 20 routers 134 paths, Agents 68, Skills 292, Pipelines, Agency Projects/Clients/Tasks, SaaS Billing White-label Marketplace Teams, Production Deployment K8s Security Realtime White-label, Integrations Zapier HubSpot Slack GitHub, SDKs Python TS, Mobile PWA RN, Business Pricing Business Plan Video Script, SOC2 Compliance, Production Checklist"
    echo ""
    echo "Happy docs! 📚"
}

main
