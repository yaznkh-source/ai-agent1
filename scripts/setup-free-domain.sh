#!/bin/bash
# Setup Free Domain via DigitalPlat FreeDomain — Task D1 — $0
# Guide to get free domain .US.KG, .DPDNS.ORG, .QZZ.IO, .XX.KG, .QD.JE

set -e

DOMAIN_NAME=${1:-ai-agency-os}
EXTENSION=${2:-us.kg}

echo "🌍 AI Agency OS — Free Domain Setup — DigitalPlat FreeDomain — $0"
echo "📅 Date: $(date)"
echo "🔗 Repo: https://github.com/DigitalPlatDev/FreeDomain — 199k stars"
echo "📊 500k+ domains registered — nonprofit — PSL Cloudflare accepted"
echo ""
echo "📝 Requested: $DOMAIN_NAME.$EXTENSION"
echo "🌐 Available extensions: .DPDNS.ORG, .US.KG, .QZZ.IO, .XX.KG, .QD.JE"
echo ""

cat <<EOF
📚 Steps to get free domain $DOMAIN_NAME.$EXTENSION — 5 minutes — $0:

1️⃣ Register Account — https://dash.domain.digitalplat.org/
   - Sign in with GitHub (KYC)
   - Verify email

2️⃣ Register Domain
   - Dashboard → Register Domain
   - Extension: $EXTENSION (recommended: us.kg or dpdns.org)
   - Name: $DOMAIN_NAME → $DOMAIN_NAME.$EXTENSION
   - Submit — instant or few hours approval

3️⃣ Configure DNS — Cloudflare (Recommended) — $0
   - Cloudflare → Add Site → $DOMAIN_NAME.$EXTENSION
   - Add DNS records:
     A    @     → YOUR_SERVER_IP (e.g., 1.2.3.4)
     A    api   → YOUR_SERVER_IP (api.$DOMAIN_NAME.$EXTENSION)
     A    docs  → YOUR_SERVER_IP (docs.$DOMAIN_NAME.$EXTENSION)
     CNAME www  → $DOMAIN_NAME.$EXTENSION
   - Cloudflare gives nameservers: *.ns.cloudflare.com
   - DigitalPlat Dashboard → Your Domain → Custom Nameservers → Enter Cloudflare NS
   - Wait 5-60 min DNS propagation
   - Cloudflare SSL → Full (strict) — free $0

4️⃣ Deploy AI Agency OS
   export DOMAIN=$DOMAIN_NAME.$EXTENSION
   export API_DOMAIN=api.$DOMAIN_NAME.$EXTENSION
   echo "CORS_ORIGINS=https://\$DOMAIN,https://\$API_DOMAIN" >> .env.prod
   echo "VITE_API_URL=https://\$API_DOMAIN" >> .env.prod
   docker-compose -f docker-compose.prod.yml up -d
   curl https://\$API_DOMAIN/api/health
   curl https://\$DOMAIN/api/docs

5️⃣ SSL — $0
   - Cloudflare proxy (orange cloud) → automatic SSL $0
   - Or Let's Encrypt: docker-compose -f docker-compose.prod.yml --profile ssl up -d certbot

EOF

echo ""
echo "💡 Examples:"
echo "  $0 ai-agency-os us.kg → ai-agency-os.us.kg"
echo "  $0 ai-agency dpdns.org → ai-agency.dpdns.org"
echo "  $0 my-agency qzz.io → my-agency.qzz.io"
echo ""
echo "🔗 Links:"
echo "  Dashboard: https://dash.domain.digitalplat.org/"
echo "  Tutorial: https://github.com/DigitalPlatDev/FreeDomain/blob/main/documents/tutorial/index.md"
echo "  LEARN.md: https://github.com/DigitalPlatDev/FreeDomain/blob/main/LEARN.md"
echo "  App source: https://github.com/DigitalPlatDev/Domain-OSS"
echo "  PSL: https://publicsuffix.org/list/ — qzz.io, us.kg in PSL, Cloudflare accepts"
echo ""
echo "📊 For AI Agency OS:"
echo "  Beta 10: Use free domain $0 — e.g., ai-agency-os.us.kg — for demo"
echo "  Prod 100: Use paid ai-agency.os \$12/year — more professional — or keep free \$0 for 100% margin"
echo "  White-label: Each client can get free domain via same process — $0"
echo ""
echo "✅ Guide complete — go register at https://dash.domain.digitalplat.org/ — $0 — 5 minutes"
