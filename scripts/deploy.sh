#!/bin/bash
# CodeSampler Live - Production Deploy Script
# 
# One-liner deployment for show-time:
# ./scripts/deploy.sh v1.0.0

set -e

VERSION=${1:-"latest"}
echo "🚀 DEPLOYING CODESAMPLER LIVE v$VERSION"
echo "====================================="

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "❌ PM2 not found. Install with: npm install -g pm2"
    exit 1
fi

# Pull latest code
echo "📥 Pulling code..."
git fetch --tags
if [ "$VERSION" != "latest" ]; then
    git checkout "tags/$VERSION"
else
    git pull origin main
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --production

# Build (if needed)
if [ -f "package.json" ] && grep -q '"build"' package.json; then
    echo "🔨 Building..."
    npm run build
fi

# Copy environment
if [ ! -f ".env" ] && [ -f "env.example" ]; then
    echo "📋 Copying environment..."
    cp env.example .env
    echo "⚠️  Please edit .env with your production values!"
fi

# Restart PM2 processes
echo "🔄 Restarting services..."
pm2 delete all 2>/dev/null || true
pm2 start ecosystem.config.cjs
pm2 save

# Run smoke tests
echo "🧪 Running smoke tests..."
if [ -f "scripts/smoke-tests.js" ]; then
    node scripts/smoke-tests.js
else
    echo "⚠️  Smoke tests not found, skipping..."
fi

echo "✅ DEPLOYMENT COMPLETE!"
echo "======================"
echo "🎭 CodeSampler Live is ready for show-time!"
echo "📊 Check status: pm2 status"
echo "📋 View logs: pm2 logs"
echo "🌐 App: http://localhost:5173"
echo "👥 Crowd: http://localhost:5173/crowd/"
