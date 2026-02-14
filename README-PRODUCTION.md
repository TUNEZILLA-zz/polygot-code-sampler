# 🎛️ Code Live - Production Launch Guide

**The Ableton Live of Code - Production-Ready Creative Suite**

## 🚀 Quick Launch (Local/Prod)

### **Local Smoke Test (5 min)**
```bash
# Start services
./scripts/start.sh

# Health check
curl -fsS http://localhost:8787/health        # expect {"status":"ok"}

# Batch render test
curl -fsS -X POST http://localhost:8787/render/batch \
  -H 'content-type: application/json' \
  -d '{"tracks":[{"backend":"rust","code":"sum(i*i for i in range(10))","parallel":true}]}'

# Open interfaces
open http://localhost:8787/site/
open http://localhost:8787/site/live/code-live.html
open http://localhost:8787/site/demos/code-daw.html
open http://localhost:8787/site/demos/code-motion.html
open http://localhost:8787/site/mixer/code-mixer.html
open http://localhost:8787/site/demos/playground.html
```

### **Production (One-Box)**
```bash
# Set environment
export LOG_LEVEL=INFO
export PYTHONUNBUFFERED=1
export CORS_ORIGINS=https://your-domain.com

# Start with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale code-live=2

# Set resource limits
docker update --cpus=2 --memory=2g <container>
```

## 🔒 90-Minute Production Hardening

### **1. Security**
- ✅ **Rate Limits**: `/render` limited to 5 r/s, small burst
- ✅ **CSP Headers**: `default-src 'self'; connect-src 'self' https://api.domain`
- ✅ **Request Limits**: 256 KB body size, Python AST parser timeouts
- ✅ **CORS**: Only allowed origins (no `*`)

### **2. Observability**
- ✅ **RED Metrics**: Requests/Errors/Duration tracking
- ✅ **Histograms**: `/render` latency distribution
- ✅ **Counters**: Fallbacks/glitch activations
- ✅ **Gauges**: Queue depth / batch size
- ✅ **Structured Logs**: JSON with request ID & session ID
- ✅ **Metrics Endpoint**: `/metrics` (Prometheus)

### **3. Health & Readiness**
- ✅ **Liveness**: `/health` (cheap)
- ✅ **Readiness**: `/ready` (can render within N ms)
- ✅ **Startup Probe**: Pre-warms renderer on boot

### **4. Persistence & Config**
- ✅ **Volumes**: Presets/projects in `/data/projects`
- ✅ **Backup**: Daily backups configured
- ✅ **Versioning**: Policy.yml checksum logged on boot
- ✅ **Feature Flags**: Glitch/LFO/MIDI (default off in prod)

### **5. Performance**
- ✅ **Batching**: Coalescing on slider spam, 10 Hz cap per client
- ✅ **Concurrency**: Scale until p95 < 150ms, then scale replicas
- ✅ **Compression**: Gzip/HTTP/2 on proxy
- ✅ **Caching**: `Cache-Control: max-age=0` for dynamic JSON

## 📊 Day-2 Operations Playbook

### **Smoke Checks**
```bash
# Health check
curl -s http://localhost:8787/health | jq

# Static files
curl -s http://localhost:8787/site/benchmarks.json | head

# Logs
docker-compose logs -f code-live | jq -r '.msg, .latency_ms, .route'
```

### **Common Alerts**
- **p95 /render > 500ms** for 5m
- **5xx rate > 1%** for 5m
- **Fallback ratio > 10%** for 10m
- **Ready probe failures > 0** over 2m

### **Troubleshooting Cheatsheet**
- **CORS/404 on JSON** → check CORS_ORIGINS, use relative `./benchmarks.json?v=ts`
- **Stale assets** → add cache-bust query and no-store on fetch
- **High CPU on sliders** → batch debouncing (≥50–100ms), cap concurrent renders
- **Thread safety (Julia/Rust)** → ensure "unsafe" only via flag; watch for races in reductions
- **SQL timeouts** → clamp LIMIT, disable heavy windows in demo mode

## 🧪 Regression Smoke Test

```bash
# Run mini regression test
./scripts/regression_smoke.sh

# Expected output:
# ✅ Individual backends: rust, ts, go, csharp, sql, julia
# ✅ Batch rendering: 2 tracks
# ✅ Rate limiting: 5 requests in <10s
# ✅ Error handling: invalid backend/code rejected
# ✅ Concurrent requests: 3 requests in <15s
```

## 🔧 Operations Commands

### **Health Monitoring**
```bash
# Full health check
./scripts/ops_playbook.sh all

# Specific checks
./scripts/ops_playbook.sh health      # Service health
./scripts/ops_playbook.sh metrics     # Prometheus metrics
./scripts/ops_playbook.sh logs        # Recent logs
./scripts/ops_playbook.sh issues      # Common issues
./scripts/ops_playbook.sh performance # Performance test
./scripts/ops_playbook.sh alerts      # Alert status
```

### **Service Management**
```bash
# Start/stop
make start
make stop
make restart

# Scaling
docker-compose up -d --scale code-live=3

# Resource limits
docker update --cpus=2 --memory=2g code-live

# Clean restart
docker-compose down && docker-compose up -d
```

### **Monitoring Dashboards**
- **Code Live**: http://localhost:8787/site/live/code-live.html
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Health**: http://localhost:8787/health
- **Metrics**: http://localhost:8787/metrics

## 🚀 Deployment Options

### **Option 1: Caddy (Recommended)**
```bash
# Use Caddyfile for TLS + CSP + rate limits
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### **Option 2: NGINX**
```bash
# Use nginx.conf for production
docker-compose up -d
```

### **Option 3: Fly.io / Render**
```bash
# Single command deploy
fly deploy
# or
render deploy
```

## 🔒 Security Features

### **Rate Limiting**
- **API endpoints**: 10 requests/second
- **Render endpoints**: 5 requests/second
- **Burst protection**: nginx + Caddy

### **Security Headers**
- **X-Frame-Options**: SAMEORIGIN
- **X-Content-Type-Options**: nosniff
- **X-XSS-Protection**: 1; mode=block
- **Content-Security-Policy**: Strict

### **Input Validation**
- **Python syntax validation**
- **Pydantic model validation**
- **Request size limits**
- **Type safety throughout**

## 📈 Performance Features

### **Optimization**
- **Gzip compression** for static assets
- **HTTP/2 support**
- **Connection pooling**
- **Caching headers**

### **Monitoring**
- **Health checks**
- **Structured logging**
- **Metrics collection**
- **Performance overlays**

### **Scalability**
- **Horizontal scaling** ready
- **Redis** for session storage
- **Database support** available
- **Load balancer** ready

## 🎛️ Creative Features

### **Live Performance**
- **Real-time code generation** with visual feedback
- **Clip-based optimization** with timeline scrubbing
- **Hardware controller integration** (MIDI)
- **Adaptive intelligence** with sidechain rules

### **Professional Workflow**
- **Preset management** with export/import
- **Project state** with undo/redo
- **A/B comparison** with instant toggle
- **Glitch mode** for stress testing

### **Advanced Features**
- **Timeline animation** with keyframe interpolation
- **Spectral analysis** for performance visualization
- **MIDI mapping** for hardware control
- **Batch rendering** with coalescing

## 🎉 What You've Built

This is **not just a tool** - it's a **complete creative platform** that transforms code generation from a static process into a dynamic, interactive, and creative experience.

### **Revolutionary Features**
- **Live Code Performance** - Real-time code generation with visual feedback
- **Creative Workflow** - Clip-based, timeline-driven optimization
- **Professional Interface** - DAW-style controls familiar to creators
- **Hardware Integration** - MIDI controller support for live performance
- **Adaptive Intelligence** - Sidechain rules that respond to performance metrics

### **Production Ready**
- **Type-safe contracts** for all API interactions
- **Comprehensive test coverage** for all core functionality
- **Professional error handling** and validation
- **Scalable architecture** for future enhancements
- **Security features** and rate limiting
- **Monitoring and logging** for production use

**Code Live is ready for production!** 🎛️✨

---

*The Ableton Live of Code - where developers compose optimization strategies like music.*
