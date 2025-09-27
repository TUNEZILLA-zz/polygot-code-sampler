#!/bin/bash
# import_grafana_dashboard.sh - Import Code Live spectrum dashboard into Grafana

set -e

echo "📊 Importing Code Live Spectrum Dashboard into Grafana"
echo "====================================================="

# Check if Grafana is running
if ! curl -fsS http://localhost:3000 > /dev/null 2>&1; then
    echo "❌ Grafana is not running. Please start it first:"
    echo "   docker-compose -f docker-compose.prod.yml up -d grafana"
    exit 1
fi

# Check if Prometheus is running
if ! curl -fsS http://localhost:9090 > /dev/null 2>&1; then
    echo "❌ Prometheus is not running. Please start it first:"
    echo "   docker-compose -f docker-compose.prod.yml up -d prometheus"
    exit 1
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check Grafana health
echo "🏥 Checking Grafana health..."
if curl -fsS http://localhost:3000/api/health > /dev/null; then
    echo "✅ Grafana is healthy"
else
    echo "❌ Grafana health check failed"
    exit 1
fi

# Check Prometheus health
echo "🏥 Checking Prometheus health..."
if curl -fsS http://localhost:9090/-/healthy > /dev/null; then
    echo "✅ Prometheus is healthy"
else
    echo "❌ Prometheus health check failed"
    exit 1
fi

# Check if Code Live is generating metrics
echo "📈 Checking Code Live metrics..."
if curl -fsS http://localhost:8787/metrics > /dev/null; then
    echo "✅ Code Live metrics endpoint accessible"
else
    echo "❌ Code Live metrics endpoint failed"
    exit 1
fi

# Test Prometheus query
echo "🔍 Testing Prometheus query..."
if curl -fsS "http://localhost:9090/api/v1/query?query=code_live_requests_total" > /dev/null; then
    echo "✅ Prometheus can query Code Live metrics"
else
    echo "❌ Prometheus query failed"
    exit 1
fi

# Import dashboard
echo "📊 Importing Code Live Spectrum Dashboard..."
if curl -fsS -X POST \
  -H "Content-Type: application/json" \
  -d @grafana/dashboards/code-live-spectrum.json \
  http://localhost:3000/api/dashboards/db > /dev/null; then
    echo "✅ Dashboard imported successfully"
else
    echo "❌ Dashboard import failed"
    exit 1
fi

echo ""
echo "🎉 Code Live Spectrum Dashboard imported!"
echo ""
echo "📊 Access your dashboard:"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo "   • Dashboard: http://localhost:3000/d/code-live-spectrum"
echo "   • Prometheus: http://localhost:9090"
echo "   • Code Live: http://localhost:8787"
echo ""
echo "🎛️ Dashboard features:"
echo "   • Request Rate (Requests/sec) - Green/Yellow/Red gauges"
echo "   • Error Rate (%) - Performance health indicator"
echo "   • Fallback Rate (%) - Backend optimization needed"
echo "   • Glitch Activations - Creative chaos effects"
echo "   • Queue Depth - System load indicator"
echo "   • Active Requests - Concurrent load"
echo "   • p95/p50 Latency - Performance spectrum"
echo "   • Backend Performance - Per-backend gauges"
echo "   • Fallbacks by Backend - Optimization targets"
echo "   • Glitches by Backend - Creative effects"
echo "   • Batch Size Distribution - Workload patterns"
echo "   • Real-time Performance - Live spectrum analysis"
echo ""
echo "🎵 Like a real DAW spectrum analyzer, but for code generation!"
echo ""
echo "🔧 To generate some test data:"
echo "   ./scripts/smoke_test.sh"
echo "   ./scripts/regression_smoke.sh"
echo ""
echo "🎛️ The performance spectrum is now live!"
