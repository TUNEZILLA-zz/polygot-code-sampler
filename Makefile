# Polyglot Code Sampler Makefile

.PHONY: help install test test-golden demo clean lint format

help: ## Show this help message
	@echo "Polyglot Code Sampler - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install pytest pytest-cov flake8 black isort

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
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Format code with black and isort
	black .
	isort .

format-check: ## Check code formatting
	black --check --diff .
	isort --check-only --diff .

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf .coverage htmlcov/

coverage: ## Run tests with coverage
	python3 -m pytest tests/ --cov=. --cov-report=html --cov-report=term

ci: ## Run CI checks locally
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) test

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
