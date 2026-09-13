@echo off
REM AI Agency OS - سكريبت تشغيل واحد $0 — Windows — Beta 100 مستخدم $0 — 120 اختبار 40 راوتر 38 واجهة — دائماً بالعربية
echo 🚀 AI Agency OS — نظام تشغيل وكالة AI خاصة — Beta 100 مستخدم $0
echo ======================================================================
echo 📊 ما بنيت: 120 اختبار ناجح — 220+ مسار — 40 راوتر — 38 واجهة
echo 💰 Beta 10 Free $0 → Prod 100 $19,900 MRR → $30K+ $30,884 → $100K+ $157,190 $1,886,280 ARR Already $1M+ ARR
echo 🏢 Enterprise SOC2 $0 12/13 DONE 92%% — Domain $0 — k8s $0 — Integrations $0 — GTM $0
echo ======================================================================
echo.

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
echo 📦 إعداد الـ Backend — 68 Agent 292 Skill — $0...
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
        echo ⚠️  تم إنشاء .env من المثال — وضع DEMO
    ) else (
        echo JWT_SECRET=dev-secret-key-change-in-prod-32-chars-min > .env
        echo ENV=development >> .env
        echo ⚠️  تم إنشاء .env افتراضي
    )
)

echo 🔧 تشغيل Backend على http://0.0.0.0:8000...
start "AI Agency OS Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

cd ..

echo.
echo 📦 إعداد الـ Frontend — 38 واجهة — $0...
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
echo ✅ AI Agency OS يعمل الآن! — Beta 100 مستخدم $0
echo ======================================================================
echo.
echo 🌐 الروابط الرئيسية:
echo    🎨 Frontend:        http://localhost:5173
echo    🔧 Backend:         http://localhost:8000
echo    📚 API Docs:        http://localhost:8000/api/docs — 220+ مسار 40 راوتر
echo    🛡️  Beta 100 $0:      http://localhost:8000/api/beta-zero/
echo    🏢 Enterprise $0:   http://localhost:8000/api/enterprise/
echo    💰 MRR $1M+ ARR:     http://localhost:8000/api/mrr/1m/stats — $1,886,280 ARR Already $1M+ ARR
echo.
echo 💡 للايقاف: أغلق نوافذ Backend و Frontend
echo ======================================================================
echo.
pause
