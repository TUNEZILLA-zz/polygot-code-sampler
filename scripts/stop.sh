#!/bin/bash
# stop.sh - Stop Code Live - The Ableton Live of Code

set -e

echo "🛑 Stopping Code Live - The Ableton Live of Code"
echo "==============================================="

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Stop services
echo "🛑 Stopping Code Live services..."
docker-compose down

# Optional: Remove volumes (uncomment if you want to clean up data)
# echo "🗑️ Removing volumes..."
# docker-compose down -v

# Optional: Remove images (uncomment if you want to clean up images)
# echo "🗑️ Removing images..."
# docker-compose down --rmi all

echo "✅ Code Live services stopped"
echo ""
echo "🔧 To start again, run: ./scripts/start.sh"
echo "🗑️ To clean up completely, run: docker-compose down -v --rmi all"
