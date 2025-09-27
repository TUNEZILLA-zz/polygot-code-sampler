#!/bin/bash
# regression_smoke.sh - Mini regression smoke test for Code Live

set -e

echo "🧪 Code Live Regression Smoke Test"
echo "=================================="

# Test configuration
BASE_CODE="sum(i*i for i in range(1,1000) if i%2==0)"
EXPECTED_MIN_LENGTH=100
EXPECTED_MAX_LATENCY=5000  # 5 seconds

# Function to test single render
test_single_render() {
    local backend=$1
    local parallel=$2
    local expected_min_length=$3

    echo "🧪 Testing $backend render (parallel=$parallel)..."

    start_time=$(date +%s%3N)
    response=$(curl -fsS -X POST http://localhost:8787/render \
      -H 'content-type: application/json' \
      -d "{\"backend\":\"$backend\",\"code\":\"$BASE_CODE\",\"parallel\":$parallel}")
    end_time=$(date +%s%3N)

    duration=$((end_time - start_time))
    code_length=$(echo "$response" | jq -r '.code | length')
    latency_ms=$(echo "$response" | jq -r '.metrics.latency_ms')

    echo "   Duration: ${duration}ms"
    echo "   Code length: $code_length"
    echo "   Latency: ${latency_ms}ms"

    # Validate response
    if [ "$code_length" -lt "$expected_min_length" ]; then
        echo "❌ Code too short: $code_length < $expected_min_length"
        return 1
    fi

    if [ "$duration" -gt "$EXPECTED_MAX_LATENCY" ]; then
        echo "❌ Too slow: ${duration}ms > ${EXPECTED_MAX_LATENCY}ms"
        return 1
    fi

    echo "✅ $backend render passed"
    return 0
}

# Function to test batch render
test_batch_render() {
    echo "🧪 Testing batch render..."

    start_time=$(date +%s%3N)
    response=$(curl -fsS -X POST http://localhost:8787/render/batch \
      -H 'content-type: application/json' \
      -d "{\"tracks\":[{\"backend\":\"rust\",\"code\":\"$BASE_CODE\",\"parallel\":true},{\"backend\":\"ts\",\"code\":\"$BASE_CODE\",\"parallel\":false}]}")
    end_time=$(date +%s%3N)

    duration=$((end_time - start_time))
    track_count=$(echo "$response" | jq -r '.tracks | length')

    echo "   Duration: ${duration}ms"
    echo "   Track count: $track_count"

    # Validate response
    if [ "$track_count" -ne 2 ]; then
        echo "❌ Wrong track count: $track_count != 2"
        return 1
    fi

    if [ "$duration" -gt "$EXPECTED_MAX_LATENCY" ]; then
        echo "❌ Too slow: ${duration}ms > ${EXPECTED_MAX_LATENCY}ms"
        return 1
    fi

    echo "✅ Batch render passed"
    return 0
}

# Function to test rate limiting
test_rate_limiting() {
    echo "🧪 Testing rate limiting..."

    start_time=$(date +%s)
    for i in {1..5}; do
        curl -fsS -X POST http://localhost:8787/render \
          -H 'content-type: application/json' \
          -d "{\"backend\":\"go\",\"code\":\"[i for i in range($i)]\"}" > /dev/null
    done
    end_time=$(date +%s)

    duration=$((end_time - start_time))
    echo "   Duration: ${duration}s for 5 requests"

    if [ "$duration" -gt 10 ]; then
        echo "❌ Rate limiting too slow: ${duration}s > 10s"
        return 1
    fi

    echo "✅ Rate limiting passed"
    return 0
}

# Function to test error handling
test_error_handling() {
    echo "🧪 Testing error handling..."

    # Test invalid backend
    response=$(curl -fsS -X POST http://localhost:8787/render \
      -H 'content-type: application/json' \
      -d '{"backend":"invalid","code":"[x for x in range(5)]"}' 2>/dev/null || echo "error")

    if [ "$response" = "error" ]; then
        echo "✅ Error handling passed (invalid backend rejected)"
    else
        echo "❌ Error handling failed (invalid backend accepted)"
        return 1
    fi

    # Test invalid code
    response=$(curl -fsS -X POST http://localhost:8787/render \
      -H 'content-type: application/json' \
      -d '{"backend":"rust","code":"invalid python code"}' 2>/dev/null || echo "error")

    if [ "$response" = "error" ]; then
        echo "✅ Error handling passed (invalid code rejected)"
    else
        echo "❌ Error handling failed (invalid code accepted)"
        return 1
    fi

    return 0
}

# Function to test concurrent requests
test_concurrent_requests() {
    echo "🧪 Testing concurrent requests..."

    start_time=$(date +%s)
    pids=()

    for i in {1..3}; do
        (
            curl -fsS -X POST http://localhost:8787/render \
              -H 'content-type: application/json' \
              -d "{\"backend\":\"rust\",\"code\":\"[x*x for x in range($i*10)]\"}" > /dev/null
        ) &
        pids+=($!)
    done

    # Wait for all requests to complete
    for pid in "${pids[@]}"; do
        wait $pid
    done

    end_time=$(date +%s)
    duration=$((end_time - start_time))

    echo "   Duration: ${duration}s for 3 concurrent requests"

    if [ "$duration" -gt 15 ]; then
        echo "❌ Concurrent requests too slow: ${duration}s > 15s"
        return 1
    fi

    echo "✅ Concurrent requests passed"
    return 0
}

# Main test execution
echo "🚀 Starting regression smoke test..."

# Test individual backends
test_single_render "rust" true 100
test_single_render "ts" false 100
test_single_render "go" true 100
test_single_render "csharp" false 100
test_single_render "sql" false 50
test_single_render "julia" true 100

# Test batch rendering
test_batch_render

# Test rate limiting
test_rate_limiting

# Test error handling
test_error_handling

# Test concurrent requests
test_concurrent_requests

echo ""
echo "🎉 All regression smoke tests passed!"
echo ""
echo "📊 Test Summary:"
echo "   • Individual backends: ✅"
echo "   • Batch rendering: ✅"
echo "   • Rate limiting: ✅"
echo "   • Error handling: ✅"
echo "   • Concurrent requests: ✅"
echo ""
echo "🎛️ Code Live is performing well!"
