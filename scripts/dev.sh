#!/bin/bash
echo "🚀 Starting Daleel Bot Development Environment..."

# Kill any existing processes
echo "🔄 Stopping existing processes..."
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Wait a moment for processes to stop
sleep 2

# Start backend in background
echo "🔧 Starting FastAPI backend..."
cd "$(dirname "$0")/.."
python -m uvicorn src.backend.main:app --reload --port 8001 --host 0.0.0.0 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting Vue.js frontend..."
cd src/frontend
source ~/.bashrc
npm run dev &
FRONTEND_PID=$!

# Display startup info
echo ""
echo "✅ Development environment started successfully!"
echo "=================================================="
echo "🔧 Backend (FastAPI):     http://localhost:8001"
echo "📚 API Documentation:     http://localhost:8001/docs"
echo "🎨 Frontend (Vue.js):     http://localhost:3000"
echo "=================================================="
echo ""
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

# Setup trap for cleanup
trap cleanup EXIT INT TERM

# Wait for user interrupt
wait
