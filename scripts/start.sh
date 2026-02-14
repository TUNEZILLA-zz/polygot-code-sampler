#!/bin/bash
# start.sh - Start Code Live - The Ableton Live of Code

set -e

echo "🎛️ Starting Code Live - The Ableton Live of Code"
echo "================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs data cache

# Set permissions
chmod 755 logs data cache

# Build and start services
echo "🔨 Building Code Live services..."
docker-compose build

echo "🚀 Starting Code Live services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."
if curl -f http://localhost:8787/health > /dev/null 2>&1; then
    echo "✅ Code Live backend is healthy"
else
    echo "❌ Code Live backend is not responding"
    echo "📋 Checking logs..."
    docker-compose logs code-live
    exit 1
fi

# Check if nginx is running (if enabled)
if docker-compose ps nginx | grep -q "Up"; then
    echo "✅ Nginx reverse proxy is running"
    echo "🌐 Code Live is available at: http://localhost"
else
    echo "✅ Code Live backend is available at: http://localhost:8787"
fi

echo ""
echo "🎉 Code Live is now running!"
echo ""
echo "📱 Access Code Live:"
echo "   • Backend API: http://localhost:8787"
echo "   • Web UI: http://localhost (if nginx is enabled)"
echo "   • Health Check: http://localhost:8787/health"
echo ""
echo "🎛️ Available interfaces:"
echo "   • Site Index: http://localhost:8787/site/"
echo "   • Code Mixer: http://localhost:8787/site/mixer/code-mixer.html"
echo "   • Code DAW: http://localhost:8787/site/demos/code-daw.html"
echo "   • Code Motion: http://localhost:8787/site/demos/code-motion.html"
echo "   • Code Live: http://localhost:8787/site/live/code-live.html"
echo "   • Playground: http://localhost:8787/site/demos/playground.html"
echo ""
echo "🔧 Management commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart services: docker-compose restart"
echo "   • Update services: docker-compose pull && docker-compose up -d"
echo ""
echo "🎵 Happy coding with Code Live!"
