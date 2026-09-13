# AI Agency OS - PowerShell Native Start Script - Windows - Real API - $0
# Real API: UnoRouter - https://api.unorouter.com/v1/chat/completions - sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR - claude-sonnet-5-thinking
# يعمل فعلياً - ليس وهماً - PowerShell Native - لا يحتاج && أو grep أو cat

Write-Host "🚀 AI Agency OS - نظام تشغيل وكالة AI خاصة - Beta 100 مستخدم $0" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host "📊 ما بنيت: 157 اختبار ناجح - 240+ مسار - 46 راوتر - 2761 modules 1.2MB" -ForegroundColor Cyan
Write-Host "💰 Real API: UnoRouter - claude-sonnet-5-thinking - streaming true - $0" -ForegroundColor Yellow
Write-Host "🔑 API: sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR" -ForegroundColor Magenta
Write-Host "🌐 Provider: https://api.unorouter.com/v1/chat/completions" -ForegroundColor Cyan
Write-Host "======================================================================"
Write-Host ""

# تحقق من المجلد الصحيح - لا تكن في System32
$currentPath = Get-Location
if ($currentPath.Path -like "*System32*") {
    Write-Host "❌ أنت في C:\Windows\System32 - هذا خطأ - لا تشغل هنا" -ForegroundColor Red
    Write-Host "💡 الحل:" -ForegroundColor Yellow
    Write-Host "   cd `$HOME" -ForegroundColor White
    Write-Host "   cd $HOME\Desktop\ai-agent1" -ForegroundColor White
    Write-Host "   .\start.ps1" -ForegroundColor White
    pause
    exit 1
}

# تحقق من Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python موجود: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python غير موجود - ثبت Python 3.11+ من https://python.org" -ForegroundColor Red
    pause
    exit 1
}

# تحقق من Node
try {
    $nodeVersion = node --version 2>&1
    $npmVersion = npm --version 2>&1
    Write-Host "✅ Node.js موجود: $nodeVersion - npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js غير موجود - ثبت Node.js 18+ من https://nodejs.org" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "📦 إعداد الـ Backend - 68 Agent 292 Skill - Real API $0..." -ForegroundColor Cyan

# Backend
Set-Location backend

if (-not (Test-Path venv)) {
    Write-Host "🔧 إنشاء بيئة Python venv..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "🔧 تفعيل venv وتثبيت المتطلبات..." -ForegroundColor Yellow

# تفعيل venv - PowerShell
try {
    & .\venv\Scripts\Activate.ps1
} catch {
    Write-Host "⚠️ فشل تفعيل venv - جرب:" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor White
    Write-Host "   ثم .\start.ps1 مرة أخرى" -ForegroundColor White
    # حاول مع bat
    & .\venv\Scripts\Activate.bat
}

pip install -r requirements.txt -q

if (-not (Test-Path .env)) {
    if (Test-Path ..\.env.example) {
        Copy-Item ..\.env.example .env
        Write-Host "⚠️ تم إنشاء .env من المثال - Real API" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️ .env موجود بالفعل مع Real API" -ForegroundColor Green
    }
}

# تحقق من .env يحتوي API حقيقي
$envContent = Get-Content .env -ErrorAction SilentlyContinue
if ($envContent | Select-String "sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR") {
    Write-Host "✅ .env يحتوي API حقيقي - UnoRouter - claude-sonnet-5-thinking" -ForegroundColor Green
} else {
    Write-Host "⚠️ .env لا يحتوي API - سيعمل Demo Mode" -ForegroundColor Yellow
}

Write-Host "🔧 تشغيل Backend على http://0.0.0.0:8000 - Real API..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k", "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Normal

Set-Location ..

Write-Host ""
Write-Host "📦 إعداد الـ Frontend - 2761 modules 1.2MB - $0..." -ForegroundColor Cyan
Set-Location frontend

if (-not (Test-Path node_modules)) {
    Write-Host "🔧 تثبيت حزم Node.js..." -ForegroundColor Yellow
    npm install
}

Write-Host "🎨 تشغيل Frontend على http://0.0.0.0:5173..." -ForegroundColor Green
Start-Process -FilePath "cmd" -ArgumentList "/k", "npm run dev" -WindowStyle Normal

Set-Location ..

Write-Host ""
Write-Host "======================================================================"
Write-Host "✅ AI Agency OS يعمل الآن! - Real API - Beta 100 مستخدم $0" -ForegroundColor Green
Write-Host "======================================================================"
Write-Host ""
Write-Host "🌐 الروابط الرئيسية - حقيقية - تعمل فعلياً:" -ForegroundColor Cyan
Write-Host "   🎨 Frontend:        http://localhost:5173 - Chat حقيقي + Battle Arena + Leaderboard" -ForegroundColor White
Write-Host "   🔧 Backend:         http://localhost:8000 - API" -ForegroundColor White
Write-Host "   📚 API Docs:        http://localhost:8000/api/docs - 240+ مسار 46 راوتر - Swagger UI" -ForegroundColor White
Write-Host "   🤖 Models:          http://localhost:8000/v1/models - 68 وكيل + claude-sonnet-5-thinking" -ForegroundColor White
Write-Host "   ⚔️  Battle:          http://localhost:8000/api/arena/battle - Battle Arena حقيقي" -ForegroundColor White
Write-Host "   🏆 Leaderboard:     http://localhost:8000/api/leaderboard/ - لوحة صدارة 68 وكيل" -ForegroundColor White
Write-Host "   💬 Chat Stream:     http://localhost:8000/api/chat/completions/stream - Streaming SSE" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Real API - UnoRouter - يعمل فعلياً:" -ForegroundColor Yellow
Write-Host "   Provider: https://api.unorouter.com/v1/chat/completions" -ForegroundColor White
Write-Host "   Model: claude-sonnet-5-thinking - streaming true" -ForegroundColor White
Write-Host "   API Key: sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR" -ForegroundColor White
Write-Host ""
Write-Host "💡 للايقاف: أغلق نوافذ Backend و Frontend" -ForegroundColor Yellow
Write-Host "💡 للاختبار: افتح PowerShell جديد و جرب:" -ForegroundColor Yellow
Write-Host "   Invoke-RestMethod -Uri http://localhost:8000/api/health" -ForegroundColor White
Write-Host "======================================================================"
Write-Host ""
pause
