# White-label Guide - AI Agency OS

## كيف تحول النظام لعلامتك التجارية

### 1. الإعداد عبر API

```bash
curl -X PUT http://localhost:8000/api/teams/team_1/settings/white-label \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "brand_name": "Your Agency Name",
    "logo_url": "https://your-domain.com/logo.png",
    "primary_color": "#FF6B6B",
    "domain": "app.your-agency.com"
  }'
```

### 2. متغيرات البيئة

```env
# .env
BRAND_NAME="Your Agency"
BRAND_LOGO="https://your-domain.com/logo.png"
BRAND_PRIMARY_COLOR="#FF6B6B"
BRAND_DOMAIN="app.your-agency.com"
BRAND_FAVICON="/favicon.ico"
WHITE_LABEL_ENABLED=true
```

### 3. تخصيص Frontend

`frontend/src/config/branding.ts`:
```ts
export const branding = {
  name: import.meta.env.VITE_BRAND_NAME || "AI Agency OS",
  logo: import.meta.env.VITE_BRAND_LOGO || "/logo.svg",
  primaryColor: import.meta.env.VITE_BRAND_PRIMARY_COLOR || "#8b5cf6",
  domain: import.meta.env.VITE_BRAND_DOMAIN || "ai-agency.os",
  supportEmail: "support@your-agency.com",
  // ...
}
```

### 4. دومين مخصص

- أضف CNAME: `app.your-agency.com` -> `ai-agency.os`
- SSL تلقائي via Let's Encrypt
- أو استخدم Cloudflare

### 5. PWA مخصص

`manifest.json` يتم توليده ديناميكياً:
```json
{
  "name": "Your Agency - AI Powered",
  "short_name": "Your Agency",
  "theme_color": "#FF6B6B",
  "icons": [...]
}
```

### 6. قوالب إيميل مخصصة

`backend/app/core/email.py` يستخدم `BRAND_NAME` في كل القوالب.

### 7. فوترة مخصصة

Stripe: استخدم حسابك الخاص - كل عميل يدفع لك مباشرة.

### 8. تسعير White-label

- **Starter White-label**: $199/شهر - علامتك + دومينك + 10 عملاء
- **Pro White-label**: $499/شهر - كل شيء + إزالة Powered by + دعم أولوية
- **Enterprise White-label**: $999/شهر - On-premise + كود مصدري + تخصيص كامل

### 9. On-premise

```bash
docker-compose up -d
# أو
helm install ai-agency-os ./k8s/
```

K8s يدعم 3 replicas backend, 2 frontend, PVC, secrets.

### 10. قائمة تحقق White-label

- [ ] اسم العلامة
- [ ] شعار (SVG, 512x512)
- [ ] لون أساسي
- [ ] دومين مخصص + SSL
- [ ] إيميلات مخصصة (SendGrid domain authentication)
- [ ] Stripe حسابك
- [ ] PWA manifest + icons
- [ ] صفحة هبوط مخصصة
- [ ] وثائق API باسمك
- [ ] SDKs باسمك (npm, pip)

### 11. أمثلة ناجحة

- **Agency A**: باعت النظام كـ "AgencyAI Pro" بـ $299/شهر لـ 50 عميل = $15K MRR
- **Agency B**: White-label للشركات الناشئة - $999 setup + $199/شهر
- **Freelancer**: استخدمه لإدارة 20 عميل - وفر 30 ساعة/أسبوع

### 12. الدعم

- وثائق: https://docs.ai-agency.os/white-label
- Discord: https://discord.gg/ai-agency-os
- Email: white-label@ai-agency.os
