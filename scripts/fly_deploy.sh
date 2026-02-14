#!/bin/bash
# fly_deploy.sh - Fly.io deployment script for Code Live

set -e

echo "🚀 Code Live - Fly.io Deployment"
echo "================================="

# Check if flyctl is installed
if ! command -v flyctl > /dev/null 2>&1; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "   curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami > /dev/null 2>&1; then
    echo "❌ Not logged in to Fly.io. Please run:"
    echo "   flyctl auth login"
    exit 1
fi

# Create fly.toml if it doesn't exist
if [ ! -f "fly.toml" ]; then
    echo "📝 Creating fly.toml..."
    cat > fly.toml << 'EOF'
# fly.toml for Code Live - The Ableton Live of Code
app = "code-live"
primary_region = "sjc"

[build]

[env]
  PYTHONPATH = "/app"
  PYTHONUNBUFFERED = "1"
  LOG_LEVEL = "INFO"
  CORS_ORIGINS = "https://code-live.fly.dev,https://www.code-live.fly.dev"

[http_service]
  internal_port = 8787
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    timeout = "5s"
    path = "/health"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 1024

[[statics]]
  guest_path = "/app/site"
  url_prefix = "/site"
EOF
    echo "✅ fly.toml created"
fi

# Create Dockerfile for Fly.io if it doesn't exist
if [ ! -f "Dockerfile.fly" ]; then
    echo "📝 Creating Dockerfile.fly..."
    cat > Dockerfile.fly << 'EOF'
# Dockerfile.fly - Optimized for Fly.io deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/cache

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8787
ENV HOST=0.0.0.0

# Expose port
EXPOSE 8787

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8787/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "server_enhanced:app", "--host", "0.0.0.0", "--port", "8787"]
EOF
    echo "✅ Dockerfile.fly created"
fi

# Deploy to Fly.io
echo "🚀 Deploying to Fly.io..."
flyctl deploy --dockerfile Dockerfile.fly

# Get app info
echo "📊 Getting app info..."
flyctl info

# Check health
echo "🏥 Checking health..."
flyctl status

# Get logs
echo "📋 Recent logs:"
flyctl logs --lines 20

echo ""
echo "🎉 Code Live deployed to Fly.io!"
echo ""
echo "🌐 Access your app:"
echo "   • Main app: https://code-live.fly.dev"
echo "   • Health: https://code-live.fly.dev/health"
echo "   • Metrics: https://code-live.fly.dev/metrics"
echo "   • Site Index: https://code-live.fly.dev/site/"
echo "   • Code Live: https://code-live.fly.dev/site/live/code-live.html"
echo "   • Code DAW: https://code-live.fly.dev/site/demos/code-daw.html"
echo "   • Code Motion: https://code-live.fly.dev/site/demos/code-motion.html"
echo "   • Code Mixer: https://code-live.fly.dev/site/mixer/code-mixer.html"
echo "   • Playground: https://code-live.fly.dev/site/demos/playground.html"
echo ""
echo "🔧 Management commands:"
echo "   • View logs: flyctl logs"
echo "   • Scale app: flyctl scale count 2"
echo "   • Restart app: flyctl restart"
echo "   • Open app: flyctl open"
echo "   • SSH into app: flyctl ssh console"
