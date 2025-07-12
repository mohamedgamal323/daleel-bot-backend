#!/bin/bash
echo "🏗️  Building Daleel Bot for Production..."

# Build frontend
echo "🎨 Building Vue.js frontend..."
cd src/frontend
npm run build

# Build backend (if needed)
echo "🔧 Preparing FastAPI backend..."
cd ../backend

# Copy frontend build to backend static directory
echo "📦 Copying frontend build to backend..."
rm -rf static
mkdir -p static
cp -r ../frontend/dist/* static/

echo "✅ Build completed successfully!"
echo "Backend is ready to serve at: http://localhost:8000"
