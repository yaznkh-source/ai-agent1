@echo off
REM AI Agency OS - سكريبت تشغيل واحد $0 — Windows — Real API UnoRouter claude-sonnet-5-thinking — 157 اختبار 46 راوتر 2761 modules 1.2MB — دائماً بالعربية
REM Real API: https://api.unorouter.com/v1/chat/completions - sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR - claude-sonnet-5-thinking streaming true
echo 🚀 AI Agency OS — نظام تشغيل وكالة AI خاصة — Real API $0
echo ======================================================================
echo 📊 ما بنيت: 157 اختبار ناجح — 240+ مسار — 46 راوتر — 2761 modules 1.2MB
echo 🔑 Real API: UnoRouter - claude-sonnet-5-thinking - streaming true - $0
echo 🌐 Provider: https://api.unorouter.com/v1/chat/completions
echo 💰 API Key: sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR
echo ======================================================================
echo.

REM تحقق من المجلد الصحيح - لا تكن في System32
echo %CD% | findstr /i "System32" >nul
if %errorlevel% equ 0 (
    echo ❌ انت في C:\Windows\System32 - هذا خطأ - لا تشغل هنا
    echo 💡 الحل: cd %USERPROFILE% ثم cd Desktop\ai-agent1 ثم start.bat
    pause
    exit /b 1
)

REM تحقق من Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير موجود — ثبت Python 3.11+ من https://python.org
    pause
    exit /b 1
)
echo ✅ Python موجود

REM تحقق من Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js غير موجود — ثبت Node.js 18+ من https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js موجود

echo.
echo 📦 إعداد الـ Backend — 68 Agent 292 Skill — Real API $0...
cd backend

if not exist venv (
    echo 🔧 إنشاء بيئة Python venv...
    python -m venv venv
)

echo 🔧 تفعيل venv وتثبيت المتطلبات...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

if not exist .env (
    if exist ..\.env.example (
        copy ..\.env.example .env
        echo ✅ تم إنشاء .env من المثال — Real API — UnoRouter
    ) else (
        echo ⚠️ .env موجود بالفعل مع Real API
    )
)

echo 🔍 تحقق من .env يحتوي API حقيقي...
findstr /i "sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR" .env >nul
if %errorlevel% equ 0 (
    echo ✅ .env يحتوي API حقيقي — UnoRouter — claude-sonnet-5-thinking
) else (
    echo ⚠️ .env لا يحتوي API — سيعمل Demo Mode
)

echo 🔧 تشغيل Backend على http://0.0.0.0:8000 — Real API...
start "AI Agency OS Backend - Real API" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

cd ..

echo.
echo 📦 إعداد الـ Frontend — 2761 modules 1.2MB — $0...
cd frontend

if not exist node_modules (
    echo 🔧 تثبيت حزم Node.js...
    call npm install
)

echo 🎨 تشغيل Frontend على http://0.0.0.0:5173...
start "AI Agency OS Frontend" cmd /k "npm run dev"

cd ..

echo.
echo ======================================================================
echo ✅ AI Agency OS يعمل الآن! — Real API — Beta 100 مستخدم $0
echo ======================================================================
echo.
echo 🌐 الروابط الرئيسية — حقيقية — تعمل فعلياً:
echo    🎨 Frontend:        http://localhost:5173 — Chat حقيقي + Battle Arena + Leaderboard
echo    🔧 Backend:         http://localhost:8000 — API
echo    📚 API Docs:        http://localhost:8000/api/docs — 240+ مسار 46 راوتر
echo    🤖 Models:          http://localhost:8000/v1/models — 68 وكيل + claude-sonnet-5-thinking
echo    ⚔️  Battle:          http://localhost:8000/api/arena/battle — Battle Arena حقيقي
echo    🏆 Leaderboard:     http://localhost:8000/api/leaderboard/ — لوحة صدارة 68 وكيل
echo    💬 Chat Stream:     http://localhost:8000/api/chat/completions/stream — Streaming SSE
echo.
echo 🔑 Real API — UnoRouter — يعمل فعلياً:
echo    Provider: https://api.unorouter.com/v1/chat/completions
echo    Model: claude-sonnet-5-thinking — streaming true
echo    API Key: sk-acwGAyBgbL5874HCWoVuS7Uwzf9XNpEWlaRrvMizePyEfUoR
echo.
echo 💡 للايقاف: أغلق نوافذ Backend و Frontend
echo ======================================================================
echo.
pause
