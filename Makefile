# Makefile for Code Live - The Ableton Live of Code

.PHONY: help build start stop restart logs clean test lint format

# Default target
help:
	@echo "🎛️ Code Live - The Ableton Live of Code"
	@echo "======================================"
	@echo ""
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  start     - Start all services"
	@echo "  stop      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  logs      - View service logs"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  test      - Run tests"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  status    - Check service status"
	@echo "  health    - Check service health"
	@echo ""

# Build Docker images
build:
	@echo "🔨 Building Code Live services..."
	docker-compose build

# Start all services
start:
	@echo "🚀 Starting Code Live services..."
	./scripts/start.sh

# Stop all services
stop:
	@echo "🛑 Stopping Code Live services..."
	./scripts/stop.sh

# Restart all services
restart: stop start

# View service logs
logs:
	@echo "📋 Viewing Code Live logs..."
	docker-compose logs -f

# Clean up containers and volumes
clean:
	@echo "🗑️ Cleaning up Code Live..."
	docker-compose down -v --rmi all
	docker system prune -f

# Run tests
test:
	@echo "🧪 Running Code Live tests..."
	docker-compose exec code-live python -m pytest tests/ -v

# Run linting
lint:
	@echo "🔍 Running Code Live linting..."
	docker-compose exec code-live python -m flake8 .
	docker-compose exec code-live python -m mypy .

# Format code
format:
	@echo "🎨 Formatting Code Live code..."
	docker-compose exec code-live python -m black .
	docker-compose exec code-live python -m isort .

# Check service status
status:
	@echo "📊 Code Live service status:"
	docker-compose ps

# Check service health
health:
	@echo "🏥 Checking Code Live health..."
	@curl -f http://localhost:8787/health && echo "✅ Backend is healthy" || echo "❌ Backend is not responding"

# Development targets
dev:
	@echo "🔧 Starting development environment..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

dev-logs:
	@echo "📋 Viewing development logs..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Production targets
prod:
	@echo "🚀 Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-logs:
	@echo "📋 Viewing production logs..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Database targets
db-migrate:
	@echo "🗄️ Running database migrations..."
	docker-compose exec code-live python -m alembic upgrade head

db-seed:
	@echo "🌱 Seeding database..."
	docker-compose exec code-live python scripts/seed_db.py

# Backup and restore
backup:
	@echo "💾 Creating backup..."
	docker-compose exec code-live python scripts/backup.py

restore:
	@echo "🔄 Restoring from backup..."
	docker-compose exec code-live python scripts/restore.py

# Monitoring
monitor:
	@echo "📊 Starting monitoring..."
	docker-compose exec code-live python scripts/monitor.py

# Performance testing
perf:
	@echo "⚡ Running performance tests..."
	docker-compose exec code-live python scripts/performance_test.py

# Security scan
security:
	@echo "🔒 Running security scan..."
	docker-compose exec code-live python -m safety check
	docker-compose exec code-live python -m bandit -r .

# Update dependencies
update:
	@echo "📦 Updating dependencies..."
	docker-compose exec code-live pip install --upgrade -r requirements.txt

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	docker-compose exec code-live python -m sphinx-build -b html docs/ docs/_build/html

# Deploy to production
deploy:
	@echo "🚀 Deploying to production..."
	git push origin main
	# Add your deployment script here

# Quick start for new users
quickstart: build start
	@echo "🎉 Code Live is ready!"
	@echo "🌐 Access at: http://localhost:8787"
	@echo "📱 Interfaces:"
	@echo "   • Code Live: http://localhost:8787/site/code-live.html"
	@echo "   • Code DAW: http://localhost:8787/site/code-daw.html"
	@echo "   • Code Motion: http://localhost:8787/site/code-motion.html"
	@echo "   • Playground: http://localhost:8787/site/playground.html"
