#!/bin/bash
# ops_playbook.sh - Day-2 operations playbook for Code Live

set -e

echo "🎛️ Code Live Operations Playbook"
echo "================================="

# Function to check service health
check_health() {
    echo "🏥 Checking service health..."

    # Health check
    if curl -fsS http://localhost:8787/health > /dev/null; then
        echo "✅ Backend health check passed"
    else
        echo "❌ Backend health check failed"
        return 1
    fi

    # Readiness check
    if curl -fsS http://localhost:8787/ready > /dev/null; then
        echo "✅ Backend readiness check passed"
    else
        echo "❌ Backend readiness check failed"
        return 1
    fi

    # Static files
    if curl -fsS http://localhost:8787/site/code-live.html > /dev/null; then
        echo "✅ Static files served"
    else
        echo "❌ Static files failed"
        return 1
    fi
}

# Function to check metrics
check_metrics() {
    echo "📊 Checking metrics..."

    # Prometheus metrics
    if curl -fsS http://localhost:8787/metrics > /dev/null; then
        echo "✅ Metrics endpoint accessible"
    else
        echo "❌ Metrics endpoint failed"
        return 1
    fi

    # Check specific metrics
    echo "📈 Key metrics:"
    curl -s http://localhost:8787/metrics | grep -E "(code_live_requests_total|code_live_request_duration_seconds|code_live_fallbacks_total)" | head -5
}

# Function to check logs
check_logs() {
    echo "📋 Checking logs..."

    # Recent logs
    echo "📝 Recent logs (last 10 lines):"
    docker-compose logs --tail=10 code-live

    # Error logs
    echo "🚨 Error logs:"
    docker-compose logs code-live | grep -i error | tail -5

    # Performance logs
    echo "⚡ Performance logs:"
    docker-compose logs code-live | grep -E "(latency|duration|performance)" | tail -5
}

# Function to check common issues
check_common_issues() {
    echo "🔍 Checking common issues..."

    # CORS issues
    echo "🌐 Checking CORS..."
    if curl -fsS -H "Origin: http://localhost:3000" http://localhost:8787/health > /dev/null; then
        echo "✅ CORS working"
    else
        echo "❌ CORS issue detected"
    fi

    # Rate limiting
    echo "🚦 Checking rate limiting..."
    for i in {1..3}; do
        curl -fsS -X POST http://localhost:8787/render \
          -H 'content-type: application/json' \
          -d '{"backend":"rust","code":"[x for x in range(3)]"}' > /dev/null
    done
    echo "✅ Rate limiting test completed"

    # Memory usage
    echo "💾 Checking memory usage..."
    docker stats --no-stream code-live | tail -1

    # Disk usage
    echo "💿 Checking disk usage..."
    df -h | grep -E "(Filesystem|/dev/)"
}

# Function to run performance test
performance_test() {
    echo "⚡ Running performance test..."

    # Test single render
    echo "🧪 Single render test..."
    start_time=$(date +%s)
    curl -fsS -X POST http://localhost:8787/render \
      -H 'content-type: application/json' \
      -d '{"backend":"rust","code":"[x*x for x in range(100)]","parallel":true}' > /dev/null
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "   Single render: ${duration}s"

    # Test batch render
    echo "🧪 Batch render test..."
    start_time=$(date +%s)
    curl -fsS -X POST http://localhost:8787/render/batch \
      -H 'content-type: application/json' \
      -d '{"tracks":[{"backend":"rust","code":"[x*x for x in range(50)]","parallel":true},{"backend":"ts","code":"[x*x for x in range(50)]","parallel":false}]}' > /dev/null
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "   Batch render: ${duration}s"

    # Test concurrent requests
    echo "🧪 Concurrent requests test..."
    start_time=$(date +%s)
    for i in {1..5}; do
        curl -fsS -X POST http://localhost:8787/render \
          -H 'content-type: application/json' \
          -d "{\"backend\":\"go\",\"code\":\"[x for x in range($i)]\"}" > /dev/null &
    done
    wait
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "   Concurrent requests: ${duration}s"
}

# Function to check alerts
check_alerts() {
    echo "🚨 Checking alerts..."

    # Check if Prometheus is running
    if curl -fsS http://localhost:9090 > /dev/null; then
        echo "✅ Prometheus is running"

        # Check alert rules
        echo "📋 Alert rules status:"
        curl -s http://localhost:9090/api/v1/rules | jq -r '.data.groups[].rules[].alert' 2>/dev/null || echo "   No alerts configured"
    else
        echo "❌ Prometheus is not running"
    fi

    # Check Grafana
    if curl -fsS http://localhost:3000 > /dev/null; then
        echo "✅ Grafana is running"
    else
        echo "❌ Grafana is not running"
    fi
}

# Function to show dashboard URLs
show_dashboards() {
    echo "🌐 Dashboard URLs:"
    echo "   • Code Live: http://localhost:8787/site/code-live.html"
    echo "   • Code DAW: http://localhost:8787/site/code-daw.html"
    echo "   • Code Motion: http://localhost:8787/site/code-motion.html"
    echo "   • Code Mixer: http://localhost:8787/site/code-mixer.html"
    echo "   • Playground: http://localhost:8787/site/playground.html"
    echo "   • Prometheus: http://localhost:9090"
    echo "   • Grafana: http://localhost:3000 (admin/admin)"
    echo "   • Health: http://localhost:8787/health"
    echo "   • Metrics: http://localhost:8787/metrics"
}

# Function to show troubleshooting tips
show_troubleshooting() {
    echo "🔧 Troubleshooting Tips:"
    echo ""
    echo "Common Issues:"
    echo "  • CORS/404 on JSON → check CORS_ORIGINS, use relative ./benchmarks.json?v=ts"
    echo "  • Stale assets → add cache-bust query and no-store on fetch"
    echo "  • High CPU on sliders → batch debouncing (≥50–100ms), cap concurrent renders"
    echo "  • Thread safety (Julia/Rust) → ensure 'unsafe' only via flag; watch for races in reductions"
    echo "  • SQL timeouts → clamp LIMIT, disable heavy windows in demo mode"
    echo ""
    echo "Quick Fixes:"
    echo "  • Restart services: docker-compose restart"
    echo "  • View logs: docker-compose logs -f"
    echo "  • Check health: curl http://localhost:8787/health"
    echo "  • Check metrics: curl http://localhost:8787/metrics"
    echo ""
    echo "Emergency Commands:"
    echo "  • Stop all: docker-compose down"
    echo "  • Clean restart: docker-compose down && docker-compose up -d"
    echo "  • Full reset: docker-compose down -v --rmi all && docker-compose up -d"
}

# Main execution
case "${1:-all}" in
    "health")
        check_health
        ;;
    "metrics")
        check_metrics
        ;;
    "logs")
        check_logs
        ;;
    "issues")
        check_common_issues
        ;;
    "performance")
        performance_test
        ;;
    "alerts")
        check_alerts
        ;;
    "dashboards")
        show_dashboards
        ;;
    "troubleshooting")
        show_troubleshooting
        ;;
    "all")
        echo "🔍 Running full health check..."
        check_health
        check_metrics
        check_logs
        check_common_issues
        performance_test
        check_alerts
        show_dashboards
        show_troubleshooting
        ;;
    *)
        echo "Usage: $0 [health|metrics|logs|issues|performance|alerts|dashboards|troubleshooting|all]"
        exit 1
        ;;
esac

echo ""
echo "🎉 Operations check completed!"
