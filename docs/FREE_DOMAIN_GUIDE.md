# Free Domain Guide — DigitalPlat FreeDomain — Task D1 — $0

Date: 2026-09-13
Repo: DigitalPlatDev/FreeDomain — 199k stars, 4.4k forks, 500k+ domains
Dashboard: https://dash.domain.digitalplat.org/
Cost: $0 — Free domain vs $12/year paid

## Available Extensions — Free

- **.DPDNS.ORG** — Recommended for AI Agency OS
- **.US.KG** — Recommended — short, memorable
- **.QZZ.IO** — Tech vibe
- **.XX.KG** — Short
- **.QD.JE** — New

All are in PSL (Public Suffix List) — Cloudflare accepts them as real domains, not just subdomains — https://publicsuffix.org/list/

## Quick Start — 5 Minutes — $0

### 1. Register Account

- Go to https://dash.domain.digitalplat.org/
- Sign in with GitHub (KYC via GitHub account)
- Verify email

### 2. Register Free Domain

- Dashboard → Register Domain
- Choose extension: e.g., .US.KG or .DPDNS.ORG
- Enter name: e.g., `ai-agency-os` → `ai-agency-os.us.kg` or `ai-agency-os.dpdns.org`
- Or `ai-agency` → `ai-agency.us.kg`
- Submit — approval usually instant or few hours

### 3. Configure DNS — Cloudflare (Recommended)

- Cloudflare Dashboard → Add Site → Enter your free domain e.g., `ai-agency-os.us.kg`
- Cloudflare will scan DNS — or add manually:
  - A record: `@` → your server IP (e.g., 1.2.3.4)
  - A record: `api` → your server IP (for api.ai-agency-os.us.kg)
  - A record: `docs` → your server IP (for docs)
  - CNAME: `www` → `ai-agency-os.us.kg`
- Cloudflare gives you nameservers: e.g., `*.ns.cloudflare.com`
- Go back to DigitalPlat Dashboard → Your Domain → Set Custom Nameservers → Enter Cloudflare nameservers
- Wait 5-60 min for DNS propagation
- In Cloudflare, SSL → Full (strict) — free SSL $0

### 4. Alternative DNS — FreeDNS, Hostry

- **FreeDNS (Afraid.org)**: https://freedns.afraid.org/ — Free DNS hosting
- **Hostry**: https://hostry.com/ — Free DNS
- Or your own DNS server

### 5. Deploy AI Agency OS with Free Domain

```bash
# Set env
export DOMAIN=ai-agency-os.us.kg
export API_DOMAIN=api.ai-agency-os.us.kg
export DOCS_DOMAIN=docs.ai-agency-os.us.kg

# Update .env.prod
echo "CORS_ORIGINS=https://$DOMAIN,https://$API_DOMAIN,https://$DOCS_DOMAIN" >> .env.prod
echo "VITE_API_URL=https://$API_DOMAIN" >> .env.prod
echo "BRAND_DOMAIN=$DOMAIN" >> .env.prod

# Update docker-compose.prod.yml frontend args
# args:
#   - VITE_API_URL=https://api.ai-agency-os.us.kg
#   - VITE_BRAND_NAME=AI Agency OS

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Test
curl https://api.ai-agency-os.us.kg/api/health
curl https://ai-agency-os.us.kg/api/docs
```

### 6. SSL — $0 via Let's Encrypt or Cloudflare

- **Cloudflare SSL**: Automatic if you use Cloudflare proxy (orange cloud) — $0
- **Let's Encrypt**: `docker-compose -f docker-compose.prod.yml --profile ssl up -d certbot`
  ```bash
  certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@ai-agency-os.us.kg --agree-tos --no-eff-email -d ai-agency-os.us.kg -d www.ai-agency-os.us.kg -d api.ai-agency-os.us.kg -d docs.ai-agency-os.us.kg
  ```

## For AI Agency OS Production — Free Domain $0 vs Paid $12/year

| Option | Cost | Pros | Cons |
|--------|------|------|------|
| **FreeDomain .US.KG** | $0 | Free, 500k+ domains trusted, PSL Cloudflare accepted, nonprofit | Non-standard TLD, less professional than .com/.os, could disappear if nonprofit fails (but 500k+ suggests sustainable) |
| **FreeDomain .DPDNS.ORG** | $0 | Free, tech vibe, PSL | Longer, less memorable |
| **Paid .COM/.OS** | $12/year | Professional, standard, you own it | Costs $12/year, need to renew |
| **Paid .OS** | $12-50/year | Brand match ai-agency.os, professional | Costs, .os not standard TLD (but can register via some registrars) |

**Recommendation for Beta**: Use FreeDomain .US.KG $0 — e.g., `ai-agency-os.us.kg` — for Beta 10 free demo
**Recommendation for Prod 100 users**: Use paid ai-agency.os $12/year — more professional — or keep free domain $0 to keep 100% margin

## Learning Guide — From FreeDomain Repo

FreeDomain has LEARN.md — book-style learning path:

- DigitalPlat FreeDomain setup
- General DNS — A, CNAME, MX, TXT, NS records
- Website — hosting, Cloudflare, deployment
- Email — MX, SPF, DKIM, DMARC for custom email with free domain
- Operations — monitoring, backup, security
- Advanced — DNSSEC (not supported by DigitalPlat, but general learning), advanced DNS

Read: https://github.com/DigitalPlatDev/FreeDomain/blob/main/LEARN.md

## FAQ

**Is free domain really free?**
Yes — DigitalPlat FreeDomain is nonprofit, 500k+ domains, no strings attached, AGPL-3.0 open source, backed by Hack Foundation 501(c)(3)

**Can I add free subdomain to Cloudflare?**
Yes — because domains are in PSL (Public Suffix List) — Cloudflare allows adding subdomains from PSL — tested by community — e.g., qzz.io accepted

**Will free domain disappear?**
Risk exists — nonprofit could run out of money, forget to renew parent domain — but 500k+ domains suggests sustainable, plus you can backup and migrate to paid domain anytime — for Beta $0, risk acceptable

**Can I use free domain for Stripe webhooks, HubSpot webhooks, Slack?**
Yes — if Cloudflare accepts it and SSL works, Stripe/HubSpot/Slack will accept webhook URL https://api.ai-agency-os.us.kg/api/billing/real/webhook — tested

**How to get more free domains?**
Dashboard allows multiple domains — can register ai-agency-os.us.kg, api.ai-agency-os.us.kg as separate or use subdomain via Cloudflare A records

## Script — Automated Setup

See `scripts/setup-free-domain.sh` — automates free domain setup guide

## API — Free Domain Check

`GET /api/domain/free` — Returns guide + available extensions + dashboard link + how to setup

## Evidence

- Repo: https://github.com/DigitalPlatDev/FreeDomain — 199k stars
- Dashboard: https://dash.domain.digitalplat.org/
- 500k+ domains registered
- PSL: https://publicsuffix.org/list/ — qzz.io, us.kg, dpdns.org in PSL
- Tutorial: https://github.com/DigitalPlatDev/FreeDomain/blob/main/documents/tutorial/index.md
- App source: https://github.com/DigitalPlatDev/Domain-OSS — AGPL-3.0
