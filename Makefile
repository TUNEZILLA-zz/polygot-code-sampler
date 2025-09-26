# Polyglot Code Sampler Makefile

.PHONY: help install test test-golden demo clean lint format

help: ## Show this help message
	@echo "Polyglot Code Sampler - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements-test.txt

test: ## Run all tests
	python3 -m pytest tests/ -v

test-golden: ## Run golden file tests
	python3 -m pytest tests/test_golden.py -v

test-update: ## Update golden files
	python3 -m pytest tests/test_golden.py --update-golden -v

demo: ## Run interactive demo
	python3 pcs_step3_ts.py --demo

demo-rust: ## Demo Rust transformation
	python3 pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --target rust

demo-ts: ## Demo TypeScript transformation
	python3 pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --target ts

demo-complex: ## Demo complex nested transformation
	python3 pcs_step3_ts.py --code "data = {i: j for i in range(1,4) for j in range(1,4) if i != j}" --target rust

demo-parallel: ## Demo parallel Rust transformation
	python3 pcs_step3_ts.py --code "squares = [x**2 for x in range(1, 1000)]" --target rust --parallel

lint: ## Run linting checks
	ruff check pcs_step3_ts.py tests/
	black --check pcs_step3_ts.py tests/
	isort --check-only pcs_step3_ts.py tests/
	mypy pcs_step3_ts.py

format: ## Format code with black, isort, and ruff
	black pcs_step3_ts.py tests/
	isort pcs_step3_ts.py tests/
	ruff check --fix pcs_step3_ts.py tests/

format-check: ## Check code formatting
	black --check pcs_step3_ts.py tests/
	isort --check-only pcs_step3_ts.py tests/
	ruff check pcs_step3_ts.py tests/

type-check: ## Run type checking
	mypy pcs_step3_ts.py

lint-fix: ## Fix linting issues automatically
	ruff check --fix pcs_step3_ts.py tests/
	black pcs_step3_ts.py tests/
	isort pcs_step3_ts.py tests/

benchmark: ## Run performance benchmarks
	python3 benchmark.py

benchmark-quick: ## Run quick performance benchmarks (parsing + generation only)
	python3 benchmark.py --quick

benchmark-results: ## Show latest benchmark results
	@if [ -f benchmark_results.json ]; then \
		python3 -c "import json; data=json.load(open('benchmark_results.json')); print('Latest benchmark:', data.get('timestamp', 'unknown')); print('Mode:', data.get('mode', 'full')); print('Cases tested:', data.get('parsing', {}).get('total_cases', 0))"; \
	else \
		echo "No benchmark results found. Run 'make benchmark' first."; \
	fi

benchmark-report: ## Generate performance report from benchmark results
	@if [ -f benchmark_results.json ]; then \
		python3 benchmark_report.py; \
	else \
		echo "No benchmark results found. Run 'make benchmark' first."; \
	fi

benchmark-full: ## Run full benchmark suite and generate report
	python3 benchmark.py && python3 benchmark_report.py

dashboard: ## Generate performance dashboard from historical data
	python3 performance_dashboard.py

dashboard-print: ## Print performance dashboard to stdout
	python3 performance_dashboard.py --print

simulate-history: ## Generate simulated performance history for testing
	python3 simulate_performance_history.py

test-dashboard: ## Test dashboard with simulated data
	python3 simulate_performance_history.py && python3 performance_dashboard.py --files performance_data/benchmark_history_*.json --print

bench-rust: ## Run Rust-specific benchmarks
	python3 benchmark.py --target rust

bench-ts: ## Run TypeScript-specific benchmarks
	python3 benchmark.py --target ts

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf performance_data/
	rm -f benchmark_results.json benchmark_report.md performance_report.md
	rm -rf .coverage htmlcov/

coverage: ## Run tests with coverage
	python3 -m pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-report=xml

coverage-html: ## Generate HTML coverage report
	python3 -m pytest tests/ --cov=. --cov-report=html
	@echo "📊 Coverage report generated in htmlcov/index.html"

coverage-xml: ## Generate XML coverage report for CI
	python3 -m pytest tests/ --cov=. --cov-report=xml

ci: ## Run CI checks locally
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) coverage

all: ## Run all checks (format, lint, test)
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test

# Development helpers
dev-setup: install ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make demo' to see the transformer in action"

quick-test: ## Quick test of core functionality
	python3 pcs_step3_ts.py --code "test = [x for x in range(5)]" --target rust
	python3 pcs_step3_ts.py --code "test = [x for x in range(5)]" --target ts
	@echo "✅ Core functionality working!"

# Release helpers
version-check: ## Check if we're ready for release
	@echo "Checking release readiness..."
	$(MAKE) ci
	@echo "✅ Ready for release!"

# Examples
examples: ## Run all example transformations
	@echo "Running example transformations..."
	@echo "1. Dict comprehension:"
	python3 pcs_step3_ts.py --code "m = {i: i*i for i in range(1,6) if i % 2 == 1}" --target rust
	@echo "2. Set comprehension:"
	python3 pcs_step3_ts.py --code "s = {(i,j) for i in range(3) for j in range(3) if i != j}" --target ts
	@echo "3. Sum reduction:"
	python3 pcs_step3_ts.py --code "total = sum(x for x in range(1,11) if x % 2 == 0)" --target rust
	@echo "✅ All examples completed!"
