#!/bin/bash
# AI Agency OS - Start Script

echo "🚀 Starting AI Agency OS - ECC + Open WebUI Hybrid"
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Backend setup
echo "📦 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate 2>/dev/null || true
pip install -r requirements.txt -q

# Create .env if not exists
if [ ! -f ".env" ]; then
    cp ../.env.example .env
    echo "⚠️  Created .env from example - please add your API keys for full functionality"
    echo "   Running in DEMO mode without API keys is supported"
fi

# Start backend in background
echo "🔧 Starting backend on http://0.0.0.0:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

echo "🎨 Starting frontend on http://0.0.0.0:5173"
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ AI Agency OS is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo "   Dashboard: http://localhost:8000/api/agency/dashboard"
echo ""
echo "   Press Ctrl+C to stop"

# Wait for both
wait $BACKEND_PID $FRONTEND_PID
