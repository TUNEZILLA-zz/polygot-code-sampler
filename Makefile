# Makefile for Polyglot Code Sampler - Julia Backend Dev Workflow

.PHONY: help test-julia test-fixtures test-differential benchmark-julia clean-julia dev-workflow

# Default target
help:
	@echo "🚀 Polyglot Code Sampler - Julia Backend Dev Workflow"
	@echo "=================================================="
	@echo ""
	@echo "Available targets:"
	@echo "  test-julia      - Run all Julia backend tests"
	@echo "  test-fixtures   - Test IR fixture → 4 goldens regression safety net"
	@echo "  test-differential - Run differential tests (IR → Julia vs reference)"
	@echo "  benchmark-julia - Run Julia performance benchmarks"
	@echo "  dev-workflow    - Complete dev workflow (test + benchmark)"
	@echo "  clean-julia     - Clean Julia test artifacts"
	@echo ""
	@echo "Benchmark targets:"
	@echo "  bench           - Run all backend benchmarks (Julia, Rust, Go, TS, C#)"
	@echo "  bench-agg       - Aggregate benchmark results for dashboard"
	@echo "  bench-publish   - Publish benchmark dashboard to GitHub Pages"
	@echo "  bench-full      - Run benchmarks and aggregate results"
	@echo "  bench-status    - Show benchmark status and results"
	@echo ""
	@echo "Phase 2: Advanced benchmarking:"
	@echo "  bench-multi     - Run comprehensive multi-test benchmark suite"
	@echo "  trend-alerts    - Check for performance regressions with alerts"
	@echo "  bench-phase2    - Complete Phase 2 benchmark suite"
	@echo "  dashboard-preview - Preview enhanced dashboard locally"
	@echo ""
	@echo "Quick refresh:"
	@echo "  bench-refresh   - One-liner: run benchmarks, aggregate, commit & push"
	@echo ""

# Test Julia backend
test-julia:
	@echo "🧪 Running Julia Backend Tests..."
	python3 -m pytest tests/test_one_ir_many_goldens.py -v
	@echo "✅ Julia backend tests completed"

# Test fixture golden files
test-fixtures:
	@echo "🧪 Testing IR Fixture → 4 Goldens Regression Safety Net..."
	python3 scripts/test_fixture_goldens.py
	@echo "✅ Fixture golden tests completed"

# Run differential tests
test-differential:
	@echo "🧪 Running Differential Tests (IR → Julia vs Reference)..."
	python3 scripts/test_differential.py
	@echo "✅ Differential tests completed"

# Run Julia performance benchmarks
benchmark-julia:
	@echo "⚡ Running Julia Performance Benchmarks..."
	@if command -v julia >/dev/null 2>&1; then \
		echo "📊 Sequential vs Parallel Performance Comparison:"; \
		julia --project -e 'include("examples/julia/sanity_perf_check.jl")'; \
		echo "✅ Julia benchmarks completed"; \
	else \
		echo "⚠️  Julia not found - skipping benchmarks"; \
		echo "   Install Julia to run performance benchmarks"; \
	fi

# Complete dev workflow
dev-workflow: test-julia test-fixtures test-differential benchmark-julia
	@echo ""
	@echo "🎉 Complete Dev Workflow Completed!"
	@echo "✅ All tests passed"
	@echo "✅ Regression safety net intact"
	@echo "✅ Performance benchmarks completed"
	@echo ""
	@echo "🚀 Julia backend is ready for production!"

# Clean Julia test artifacts
clean-julia:
	@echo "🧹 Cleaning Julia test artifacts..."
	@rm -f tests/generated_*.jl
	@rm -f tests/diff_*.jl
	@rm -f *.jl
	@echo "✅ Julia artifacts cleaned"

# Quick test (for development)
quick-test:
	@echo "⚡ Quick Julia Backend Test..."
	python3 -m pcs --code "sum(i*i for i in range(1, 10) if i%2==0)" --target julia --mode auto --parallel
	@echo "✅ Quick test completed"

# Generate all golden files from fixture
regenerate-goldens:
	@echo "🔄 Regenerating Golden Files from Fixture..."
	@echo "⚠️  This will overwrite existing golden files!"
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	python3 scripts/regenerate_goldens.py
	@echo "✅ Golden files regenerated"

# Show Julia backend status
status:
	@echo "📊 Julia Backend Status:"
	@echo "========================"
	@echo "Python version: $$(python3 --version)"
	@echo "Julia version: $$(julia --version 2>/dev/null || echo 'Not installed')"
	@echo "PCS version: $$(python3 -m pcs --version 2>/dev/null || echo 'Not available')"
	@echo ""
	@echo "Test files:"
	@ls -la tests/fixtures/ 2>/dev/null || echo "  No fixtures found"
	@ls -la tests/golden/julia/ 2>/dev/null || echo "  No golden files found"
	@echo ""
	@echo "Scripts:"
	@ls -la scripts/test_*.py 2>/dev/null || echo "  No test scripts found"

# Benchmark targets
bench:
	@echo "🚀 Running all backend benchmarks..."
	python3 scripts/bench_all.py

bench-agg:
	@echo "📊 Aggregating benchmark results..."
	python3 scripts/aggregate_bench.py

bench-publish:
	@echo "📈 Publishing benchmark dashboard..."
	@if command -v gh-pages >/dev/null 2>&1; then \
		gh-pages -d site; \
	else \
		echo "⚠️  gh-pages not found. Install with: npm install -g gh-pages"; \
		echo "   Or use GitHub Actions for automatic publishing"; \
	fi

bench-full: bench bench-agg
	@echo "🎉 Full benchmark suite completed!"

bench-status:
	@echo "📊 Benchmark Status:"
	@echo "==================="
	@echo "Results directory:"
	@ls -la bench/results/ 2>/dev/null || echo "  No results found"
	@echo ""
	@echo "Site directory:"
	@ls -la site/ 2>/dev/null || echo "  No site files found"
	@echo ""
	@echo "Last benchmark:"
	@ls -t bench/results/*.ndjson 2>/dev/null | head -1 | xargs ls -la 2>/dev/null || echo "  No benchmarks found"

# Phase 2: Advanced benchmarking features
bench-multi:
	@echo "🚀 Running multi-test benchmark suite..."
	python3 scripts/bench_multi_test.py

trend-alerts:
	@echo "🔍 Checking for performance regressions..."
	python3 scripts/trend_alerts.py

bench-phase2: bench-multi bench-agg trend-alerts
	@echo "🎉 Phase 2 benchmark suite completed!"

# Enhanced dashboard features
dashboard-preview:
	@echo "📈 Previewing enhanced dashboard..."
	@if command -v python3 >/dev/null 2>&1; then \
		cd site && python3 -m http.server 8080; \
	else \
		echo "⚠️  Python3 not found. Open site/index.html in your browser"; \
	fi

# One-liner refresh: run benchmarks, aggregate, commit & push
bench-refresh:
	@echo "🔄 Running complete benchmark refresh..."
	@echo "1️⃣ Running benchmarks..."
	$(MAKE) bench
	@echo "2️⃣ Aggregating results..."
	$(MAKE) bench-agg
	@echo "3️⃣ Checking for regressions..."
	python3 scripts/regression_check.py --input site/benchmarks.json
	@echo "4️⃣ Committing and pushing..."
	git add bench/results site/benchmarks.json
ifdef DRY_RUN
	@echo "🔍 DRY RUN: Would commit with message: bench: refresh $(shell date -u +%Y-%m-%d)"
	@echo "🔍 DRY RUN: Would push to origin main"
else
	git commit -m "bench: refresh $(shell date -u +%Y-%m-%d)" || echo "No changes to commit"
	git push origin main
endif
	@echo "✅ Benchmark refresh complete!"