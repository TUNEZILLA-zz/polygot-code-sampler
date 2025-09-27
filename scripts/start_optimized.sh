#!/bin/bash
# start_optimized.sh - Start optimized Code Live server with performance enhancements

set -e

echo "🚀 Starting Optimized Code Live Server"
echo "======================================"

# Check if server is already running
if curl -fsS http://localhost:8787/health > /dev/null 2>&1; then
    echo "⚠️  Server is already running on port 8787"
    echo "   Stopping existing server..."
    pkill -f "uvicorn.*server" || true
    sleep 2
fi

# Install optimized dependencies
echo "📦 Installing optimized dependencies..."
pip3 install -r requirements-optimized.txt

# Set environment variables for optimization
export PYTHONPATH="/Users/brian/Library/Mobile Documents/com~apple~CloudDocs/rawtunezmedia/aiagent/code/step 2"
export PYTHONUNBUFFERED=1
export LOG_LEVEL=INFO

# Start optimized server with performance enhancements
echo "🎛️ Starting optimized Code Live server..."
echo "   • ORJSONResponse for faster JSON serialization"
echo "   • uvloop for faster event loop"
echo "   • httptools for faster HTTP parsing"
echo "   • Enhanced metrics with target/status tracking"
echo "   • IR caching with 60-second TTL"
echo "   • Julia fallback handling"
echo "   • Batch coalescing optimization"
echo ""

# Start with optimized settings
uvicorn server_optimized:app \
  --host 0.0.0.0 \
  --port 8787 \
  --loop uvloop \
  --http httptools \
  --workers 1 \
  --timeout-keep-alive 75 \
  --access-log \
  --log-level info
