#!/bin/bash
# smoke_test.sh - Quick smoke test for Code Live

set -e

echo "🧪 Code Live Smoke Test"
echo "======================"

# Test 1: Health check
echo "1. Testing health endpoint..."
if curl -fsS http://localhost:8787/health > /dev/null; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test 2: Batch render
echo "2. Testing batch render..."
response=$(curl -fsS -X POST http://localhost:8787/render/batch \
  -H 'content-type: application/json' \
  -d '{"tracks":[{"backend":"rust","code":"sum(i*i for i in range(10))","parallel":true}]}')

if echo "$response" | jq -e '.tracks[0].code' > /dev/null; then
    echo "✅ Batch render passed"
    echo "   Generated code length: $(echo "$response" | jq -r '.tracks[0].code | length')"
    echo "   Latency: $(echo "$response" | jq -r '.tracks[0].metrics.latency_ms')ms"
else
    echo "❌ Batch render failed"
    echo "Response: $response"
    exit 1
fi

# Test 3: Single render
echo "3. Testing single render..."
response=$(curl -fsS -X POST http://localhost:8787/render \
  -H 'content-type: application/json' \
  -d '{"backend":"ts","code":"[x*x for x in range(5)]","parallel":false}')

if echo "$response" | jq -e '.code' > /dev/null; then
    echo "✅ Single render passed"
    echo "   Generated code length: $(echo "$response" | jq -r '.code | length')"
else
    echo "❌ Single render failed"
    echo "Response: $response"
    exit 1
fi

# Test 4: Rate limiting (should be fast)
echo "4. Testing rate limiting..."
start_time=$(date +%s)
for i in {1..3}; do
    curl -fsS -X POST http://localhost:8787/render \
      -H 'content-type: application/json' \
      -d '{"backend":"go","code":"[i for i in range(3)]"}' > /dev/null
done
end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $duration -lt 5 ]; then
    echo "✅ Rate limiting working (${duration}s for 3 requests)"
else
    echo "⚠️  Rate limiting may be too slow (${duration}s for 3 requests)"
fi

# Test 5: Static files
echo "5. Testing static files..."
if curl -fsS http://localhost:8787/site/code-live.html > /dev/null; then
    echo "✅ Static files served"
else
    echo "❌ Static files failed"
    exit 1
fi

echo ""
echo "🎉 All smoke tests passed!"
echo ""
echo "🌐 Access Code Live:"
echo "   • Code Live: http://localhost:8787/site/code-live.html"
echo "   • Code DAW: http://localhost:8787/site/code-daw.html"
echo "   • Code Motion: http://localhost:8787/site/code-motion.html"
echo "   • Code Mixer: http://localhost:8787/site/code-mixer.html"
echo "   • Playground: http://localhost:8787/site/playground.html"
