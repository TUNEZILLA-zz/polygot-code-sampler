#!/bin/bash
# grafana_setup.sh - Setup Grafana dashboard for Code Live

set -e

echo "📊 Setting up Grafana dashboard for Code Live"
echo "============================================="

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

echo ""
echo "🎉 Grafana setup completed!"
echo ""
echo "📊 Access your dashboards:"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo "   • Prometheus: http://localhost:9090"
echo "   • Code Live: http://localhost:8787"
echo ""
echo "🎛️ Dashboard features:"
echo "   • Request Rate (Requests/sec)"
echo "   • Error Rate (%)"
echo "   • Render Latency Distribution (Heatmap)"
echo "   • Backend Performance Spectrum (Bar Gauge)"
echo "   • Fallback Rate (%)"
echo "   • Glitch Activations (Time Series)"
echo "   • Queue Depth (Gauge)"
echo "   • Active Requests (Gauge)"
echo "   • Batch Size Distribution (Histogram)"
echo "   • Performance Spectrum (Real-time Time Series)"
echo ""
echo "🎵 Like a real DAW spectrum analyzer, but for code generation!"
echo ""
echo "🔧 To generate some test data:"
echo "   ./scripts/smoke_test.sh"
echo "   ./scripts/regression_smoke.sh"
