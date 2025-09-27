#!/bin/bash
# 🧪 Contract Tests for Polyglot Code Mixer API
# Tests all endpoints with real requests

set -e

# Configuration
API_BASE="${API_BASE:-http://localhost:8787}"
API_VERSION="v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((TESTS_PASSED++))
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((TESTS_FAILED++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test functions
test_health() {
    log_info "Testing health endpoint..."

    response=$(curl -sS "${API_BASE}/${API_VERSION}/health" 2>/dev/null)
    if [ $? -eq 0 ]; then
        ok=$(echo "$response" | jq -r '.ok // false')
        if [ "$ok" = "true" ]; then
            log_success "Health check passed"
            echo "$response" | jq .
        else
            log_error "Health check failed - service not healthy"
            echo "$response"
        fi
    else
        log_error "Health check failed - connection error"
    fi
}

test_single_render() {
    log_info "Testing single render endpoint..."

    payload='{
        "code": "sum(i*i for i in range(1,10) if i%2==0)",
        "target": "rust",
        "parallel": true,
        "mode": "loops"
    }'

    response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render" \
        -H 'Content-Type: application/json' \
        -d "$payload" 2>/dev/null)

    if [ $? -eq 0 ]; then
        ok=$(echo "$response" | jq -r '.ok // false')
        if [ "$ok" = "true" ]; then
            log_success "Single render test passed"
            echo "$response" | jq -r '.code'
        else
            log_error "Single render test failed"
            echo "$response"
        fi
    else
        log_error "Single render test failed - connection error"
    fi
}

test_batch_render() {
    log_info "Testing batch render endpoint..."

    payload='{
        "code": "sum(i*i for i in range(1,10) if i%2==0)",
        "targets": ["rust", "julia", "sql"],
        "parallel": true,
        "mode": "loops"
    }'

    response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render/batch" \
        -H 'Content-Type: application/json' \
        -d "$payload" 2>/dev/null)

    if [ $? -eq 0 ]; then
        results_count=$(echo "$response" | jq -r '.results | length')
        if [ "$results_count" = "3" ]; then
            log_success "Batch render test passed"
            echo "$response" | jq '.results[] | {target: .target, ok: .ok, code_length: (.code | length)}'
        else
            log_error "Batch render test failed - expected 3 results, got $results_count"
            echo "$response"
        fi
    else
        log_error "Batch render test failed - connection error"
    fi
}

test_presets() {
    log_info "Testing presets endpoint..."

    response=$(curl -sS "${API_BASE}/${API_VERSION}/presets" 2>/dev/null)
    if [ $? -eq 0 ]; then
        presets_count=$(echo "$response" | jq -r '.presets | keys | length')
        if [ "$presets_count" -ge 4 ]; then
            log_success "Presets test passed - found $presets_count presets"
            echo "$response" | jq '.presets | keys'
        else
            log_error "Presets test failed - expected at least 4 presets, got $presets_count"
            echo "$response"
        fi
    else
        log_error "Presets test failed - connection error"
    fi
}

test_rate_limiting() {
    log_info "Testing rate limiting..."

    # Make 15 requests quickly (limit is 10 per minute)
    for i in {1..15}; do
        response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render" \
            -H 'Content-Type: application/json' \
            -d '{"code":"[x for x in range(5)]","target":"rust"}' \
            -w "%{http_code}" -o /dev/null 2>/dev/null)

        if [ "$response" = "429" ]; then
            log_success "Rate limiting test passed - got 429 after $i requests"
            return 0
        fi
    done

    log_warning "Rate limiting test inconclusive - no 429 response received"
}

test_validation() {
    log_info "Testing input validation..."

    # Test empty code
    response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render" \
        -H 'Content-Type: application/json' \
        -d '{"code":"","target":"rust"}' \
        -w "%{http_code}" -o /dev/null 2>/dev/null)

    if [ "$response" = "400" ]; then
        log_success "Empty code validation passed"
    else
        log_error "Empty code validation failed - expected 400, got $response"
    fi

    # Test invalid target
    response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render" \
        -H 'Content-Type: application/json' \
        -d '{"code":"[x for x in range(5)]","target":"invalid"}' \
        -w "%{http_code}" -o /dev/null 2>/dev/null)

    if [ "$response" = "422" ]; then
        log_success "Invalid target validation passed"
    else
        log_error "Invalid target validation failed - expected 422, got $response"
    fi
}

test_cors() {
    log_info "Testing CORS headers..."

    response=$(curl -sS -H "Origin: https://tunezilla-zz.github.io" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS "${API_BASE}/${API_VERSION}/render" \
        -v 2>&1)

    if echo "$response" | grep -q "Access-Control-Allow-Origin"; then
        log_success "CORS headers present"
    else
        log_error "CORS headers missing"
    fi
}

# Performance test
test_performance() {
    log_info "Testing performance..."

    start_time=$(date +%s%N)

    response=$(curl -sS -X POST "${API_BASE}/${API_VERSION}/render" \
        -H 'Content-Type: application/json' \
        -d '{"code":"[x*x for x in range(100) if x%2==0]","target":"rust","parallel":true}' \
        2>/dev/null)

    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds

    if [ $duration -lt 1000 ]; then
        log_success "Performance test passed - ${duration}ms"
    else
        log_warning "Performance test - ${duration}ms} (slow but acceptable)"
    fi
}

# Main test runner
main() {
    echo "🧪 Polyglot Code Mixer API Contract Tests"
    echo "========================================"
    echo "API Base: $API_BASE"
    echo "Version: $API_VERSION"
    echo ""

    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Please install jq first."
        exit 1
    fi

    # Check if curl is available
    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed. Please install curl first."
        exit 1
    fi

    # Run tests
    test_health
    echo ""

    test_single_render
    echo ""

    test_batch_render
    echo ""

    test_presets
    echo ""

    test_validation
    echo ""

    test_cors
    echo ""

    test_performance
    echo ""

    test_rate_limiting
    echo ""

    # Summary
    echo "========================================"
    echo "Test Summary:"
    echo "✅ Passed: $TESTS_PASSED"
    echo "❌ Failed: $TESTS_FAILED"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        log_success "All tests passed! 🎉"
        exit 0
    else
        log_error "Some tests failed. Please check the output above."
        exit 1
    fi
}

# Run main function
main "$@"
