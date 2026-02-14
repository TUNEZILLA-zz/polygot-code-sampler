# 🎛️ Code Live - The Ableton Live of Code

**Dockerized Creative Suite for Code Generation**

## 🚀 Quick Start

### One-Command Setup
```bash
./scripts/start.sh
```

### Manual Setup
```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🎯 What You Get

### **Complete Creative Suite**
- **🎚️ Code Mixer** - Interactive fader-based code generation
- **🎛️ Code DAW** - Digital Audio Workstation for code
- **🎬 Code Motion** - Timeline-based code animation
- **🎵 Code Live** - Live performance interface
- **🎮 Playground** - Simple web demo

### **Production-Ready Backend**
- **FastAPI Server** - Type-safe API with full validation
- **Real-time Rendering** - Connect UI to actual code generation
- **Performance Monitoring** - Track generation time, LOC, fallbacks
- **Adaptive Mixing** - Sidechain rules that respond to metrics
- **Professional Workflow** - Presets, projects, undo/redo

### **Advanced Features**
- **Timeline Animation** - Keyframe-based optimization sequences
- **Glitch Mode** - Stress testing with seeded randomization
- **A/B Comparison** - Instant toggle between approaches
- **MIDI Support** - Hardware controller integration
- **Spectral Analysis** - Visualize performance as frequency spectrum

## 🌐 Access Points

| Interface | URL | Description |
|-----------|-----|-------------|
| **Site Index** | http://localhost:8787/site/ | Navigation hub |
| **Code Live** | http://localhost:8787/site/live/code-live.html | Main live performance interface |
| **Code DAW** | http://localhost:8787/site/demos/code-daw.html | Digital Audio Workstation for code |
| **Code Motion** | http://localhost:8787/site/demos/code-motion.html | Timeline-based animation |
| **Code Mixer** | http://localhost:8787/site/mixer/code-mixer.html | Interactive fader interface |
| **Playground** | http://localhost:8787/site/demos/playground.html | Simple web demo |
| **API Health** | http://localhost:8787/health | Backend health check |

## 🔧 Management Commands

### **Start Services**
```bash
./scripts/start.sh
```

### **Stop Services**
```bash
./scripts/stop.sh
```

### **View Logs**
```bash
docker-compose logs -f
```

### **Restart Services**
```bash
docker-compose restart
```

### **Update Services**
```bash
docker-compose pull && docker-compose up -d
```

### **Clean Up**
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (data)
docker-compose down -v

# Remove images (complete cleanup)
docker-compose down --rmi all
```

## 🏗️ Architecture

### **Services**
- **code-live** - FastAPI backend with full creative suite
- **redis** - Caching and session storage (optional)
- **nginx** - Reverse proxy and static file serving (optional)

### **Volumes**
- **./site** - Static web interfaces (read-only)
- **./logs** - Application logs
- **./data** - Persistent data storage
- **redis-data** - Redis data persistence

### **Networks**
- **code-live-network** - Internal service communication

## 🎵 Creative Workflow

### **1. Audition Styles**
- Use **Clip Launcher** to try different transformation flavors
- Click "Punchy" for aggressive parallelization
- Click "Hi-Fi" for clean, readable code

### **2. Fine-tune Balance**
- Use **Mixer Board** to perfect each backend's contribution
- Drag faders to adjust optimization intensity
- Use pan knobs to blend readability vs performance

### **3. Record Sequences**
- Use **Timeline** to capture optimization journeys
- Create keyframes at different optimization milestones
- Play back sequences to see code evolve

### **4. Add Chaos**
- Use **Creative Chaos** tools to stress-test
- Enable Glitch Mode for randomized transformations
- Use Spectral Analysis to visualize performance

### **5. Perform Live**
- Use **Macro Knobs** for one-knob control
- Map MIDI controllers to parameters
- Watch real-time code generation

## 🔒 Security Features

### **Rate Limiting**
- API endpoints: 10 requests/second
- Render endpoints: 5 requests/second
- Burst protection with nginx

### **Security Headers**
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy: Strict

### **Input Validation**
- Python syntax validation
- Pydantic model validation
- Request size limits
- Type safety throughout

## 📊 Performance Features

### **Optimization**
- Gzip compression for static assets
- HTTP/2 support
- Connection pooling
- Caching headers

### **Monitoring**
- Health checks
- Structured logging
- Metrics collection
- Performance overlays

### **Scalability**
- Horizontal scaling ready
- Redis for session storage
- Database support available
- Load balancer ready

## 🎛️ API Endpoints

### **Core Rendering**
- `POST /render` - Single code generation
- `POST /render/batch` - Batch rendering with coalescing
- `GET /health` - Health check

### **Creative Features**
- `POST /sidechain` - Apply adaptive mixing rules
- `POST /timeline` - Keyframe interpolation
- `POST /glitch` - Apply glitch effects
- `POST /ab-compare` - A/B state comparison

### **Preset Management**
- `GET /presets` - List available presets
- `POST /presets` - Create new preset
- `PUT /presets/{id}` - Update preset
- `DELETE /presets/{id}` - Delete preset

### **MIDI Integration**
- `POST /midi` - Apply MIDI CC mapping
- `GET /midi/mappings` - List MIDI mappings
- `POST /midi/mappings` - Create MIDI mapping

## 🧪 Testing

### **Run Tests**
```bash
# Run all tests
docker-compose exec code-live python -m pytest

# Run specific test file
docker-compose exec code-live python -m pytest tests/test_mixer_core.py

# Run with coverage
docker-compose exec code-live python -m pytest --cov=mixer_core
```

### **Test Coverage**
- **Interpolation** - All easing functions and state interpolation
- **Quantization** - Time and grid-based quantization
- **Solo Logic** - Classic DAW solo behavior
- **Sidechain Rules** - Rule evaluation and state updates
- **MIDI Mapping** - CC mapping and state updates
- **Preset Management** - Export/import with validation
- **Glitch Mode** - Seeded randomization and safety
- **A/B Compare** - State comparison and diff analysis

## 🚀 Production Deployment

### **Environment Variables**
```bash
# Required
PYTHONPATH=/app
PYTHONUNBUFFERED=1

# Optional
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-domain.com
REDIS_URL=redis://redis:6379
DATABASE_URL=postgresql://user:pass@db:5432/codelive
```

### **SSL/HTTPS**
1. Update `nginx.conf` with your SSL certificates
2. Uncomment HTTPS server block
3. Set `CORS_ORIGINS` to your domain
4. Restart services

### **Scaling**
```bash
# Scale backend services
docker-compose up -d --scale code-live=3

# Use external load balancer
# Update nginx.conf upstream configuration
```

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
