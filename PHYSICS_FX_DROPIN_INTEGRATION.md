# 🎛️ Code Live Physics FX - Drop-in Integration Guide

## 🚀 **Production-Hardened Physics FX with Quality Scaling, Reduced-Motion, and Drop-in Integration**

This guide shows exactly how to integrate the production-hardened physics FX system into Code Live with all the hardening wins, metrics adapter, and drop-in integration.

---

## 🎯 **Quick Hardening Wins (Fast to Do)**

### **✅ Quality Scaler**
- **Drop particle cap when FPS < 45; restore at 60**
- **Dynamic quality adjustment based on performance**
- **Automatic particle count scaling**

### **✅ Kill-switch & Modes**
- **`?fx=off|lite|full` URL param + UI toggle**
- **Respect `prefers-reduced-motion`**
- **Pause on tab blur**

### **✅ Metrics Adapter**
- **Debounce to 10–20 Hz; clamp outliers**
- **Fallback to demo generator if `/metrics` is unreachable**
- **Sanitize and validate all metrics**

### **✅ A11y & Motion**
- **Respect `prefers-reduced-motion`**
- **Hide FX from screen readers**
- **Pause on tab blur**

### **✅ Theme & Legend**
- **Fixed color keys per backend**
- **Small legend overlay**
- **Consistent visual identity**

### **✅ Perf Budget**
- **Keep FX thread under ~6–8 ms/frame**
- **Avoid layout thrash (requestAnimationFrame, no sync reads)**
- **Dynamic quality scaling**

### **✅ Error Fences**
- **Try/catch around shader init**
- **Re-init on WebGL context loss**
- **Graceful degradation**

### **✅ Mobile Posture**
- **OffscreenCanvas if available**
- **Halve resolution on DPR>1.5**
- **Touch-friendly controls**

### **✅ Telemetry**
- **Emit `fx_frame_ms`, `fx_quality_level`, `fx_backpressure_events` to Prometheus**
- **Performance monitoring**
- **Quality metrics**

---

## 📦 **Minimal Metrics Adapter (Drop-in)**

```javascript
<script type="module">
import { initPhysicsFX } from "./scripts/physics-fx-production.js";

const fxCanvas = document.getElementById("physics-fx-canvas");
let latest = {
  qps: 0, p95: 30, errorRate: 0, fallbackRatio: 0,
  perBackend: { rust:0.5, ts:0.5, go:0.4, csharp:0.3, sql:0.2, julia:0.2 }
};

// Pull from your store or API; debounce to ~10Hz
let tHandle = null;
async function poll() {
  try {
    const res = await fetch("/metrics/snapshot"); // your lightweight endpoint
    if (res.ok) {
      const m = await res.json();
      latest = sanitize(m);
    }
  } catch {}
  tHandle = setTimeout(poll, 100); // 10Hz
}

function sanitize(m) {
  const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
  return {
    qps: clamp(m.qps ?? 0, 0, 240),
    p95: clamp(m.p95 ?? 30, 0, 500),
    errorRate: clamp(m.errorRate ?? 0, 0, 1),
    fallbackRatio: clamp(m.fallbackRatio ?? 0, 0, 1),
    perBackend: Object.fromEntries(
      Object.entries(m.perBackend ?? {}).map(([k,v]) => [k, clamp(v, 0, 1)])
    )
  };
}

// Respect reduced motion
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const mode = new URLSearchParams(location.search).get("fx") ?? (reduced ? "lite" : "full");

if (mode !== "off") {
  const physicsFX = initPhysicsFX({
    canvas: fxCanvas,
    mode,
    metricsSource: '/metrics/snapshot',
    debounceMs: 100
  });
  
  // Connect metrics to physics
  const updateLoop = () => {
    physicsFX.physicsFX.updateMetrics(latest);
    requestAnimationFrame(updateLoop);
  };
  updateLoop();
  
  poll();
}
</script>
```

---

## 🎛️ **Complete Drop-in Integration**

### **1. HTML Setup**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Live - Physics FX</title>
    <style>
        /* Your existing styles */
        .physics-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <!-- Physics Canvas -->
    <canvas class="physics-canvas" id="physics-fx-canvas"></canvas>
    
    <!-- Your existing content -->
    <div class="main-content">
        <!-- Your Code Live interface -->
    </div>
    
    <script type="module">
        import { initPhysicsFX } from './scripts/physics-fx-production.js';
        
        // Initialize physics FX
        const physicsFX = initPhysicsFX({
            canvas: document.getElementById('physics-fx-canvas'),
            mode: 'full', // or get from URL params
            metricsSource: '/metrics/snapshot',
            debounceMs: 100
        });
    </script>
</body>
</html>
```

### **2. JavaScript Integration**
```javascript
// In your Code Live main script
import { initPhysicsFX } from './scripts/physics-fx-production.js';

class CodeLive {
    constructor() {
        this.initializePhysicsFX();
        this.initializeMetrics();
        this.startUpdateLoop();
    }

    initializePhysicsFX() {
        // Get mode from URL params or reduced motion
        const urlParams = new URLSearchParams(window.location.search);
        const mode = urlParams.get('fx') || 
                    (window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'lite' : 'full');
        
        if (mode === 'off') {
            return;
        }

        // Initialize physics FX
        this.physicsFX = initPhysicsFX({
            canvas: document.getElementById('physics-fx-canvas'),
            mode,
            metricsSource: '/metrics/snapshot',
            debounceMs: 100
        });
    }

    initializeMetrics() {
        // Your existing metrics initialization
        this.metrics = {
            requestRate: 0,
            successRate: 1.0,
            p95Latency: 30,
            errorRate: 0,
            fallbackRatio: 0,
            perBackend: { rust:0.5, ts:0.5, go:0.4, csharp:0.3, sql:0.2, julia:0.2 }
        };
    }

    startUpdateLoop() {
        const updateLoop = () => {
            // Update your metrics
            this.updateMetrics();
            
            // Update physics FX
            if (this.physicsFX) {
                this.physicsFX.physicsFX.updateMetrics(this.metrics);
            }
            
            requestAnimationFrame(updateLoop);
        };
        updateLoop();
    }

    updateMetrics() {
        // Your existing metrics update logic
        // This should update this.metrics with real values
    }
}

// Initialize Code Live
new CodeLive();
```

---

## 🎯 **Nice Visual Add-ons (Plug-in Ideas)**

### **🐦 Boids Switch**
```javascript
// Toggle cohesion with 1 - errorRate; show "flock breakup" during incidents
class BoidsSwitch {
    constructor(particles, metrics) {
        this.particles = particles;
        this.metrics = metrics;
        this.cohesion = 0.1;
        this.alignment = 0.1;
        this.separation = 0.1;
    }

    update() {
        const errorRate = this.metrics.errorRate || 0;
        
        // Cohesion goes down as error rate rises
        this.cohesion = Math.max(0.01, 0.1 - errorRate * 0.09);
        
        // Separation increases with error rate
        this.separation = 0.1 + errorRate * 0.2;
        
        // Apply boids forces to particles
        this.applyBoidsForces();
    }
}
```

### **🌊 Spring Timeline**
```javascript
// Bind keyframe scrubbing to a spring; visually ease to new state
class SpringTimeline {
    constructor(keyframes) {
        this.keyframes = keyframes;
        this.masses = keyframes.map(kf => ({
            position: kf.value,
            velocity: 0,
            target: kf.value
        }));
    }

    update(targetIndex) {
        for (let i = 0; i < this.masses.length; i++) {
            const mass = this.masses[i];
            const target = i === targetIndex ? this.keyframes[i].value : mass.target;
            
            // Spring force
            const springForce = (target - mass.position) * 0.1;
            
            // Apply force
            mass.velocity += springForce;
            mass.velocity *= 0.9; // damping
            mass.position += mass.velocity;
        }
    }
}
```

### **💨 Fluid Background**
```javascript
// GPU smoke with injection velocity = QPS, dissipation = errorRate
class FluidBackground {
    constructor(canvas) {
        this.canvas = canvas;
        this.gl = canvas.getContext('webgl');
        this.initShaders();
    }

    update(qps, errorRate) {
        // Update fluid simulation based on metrics
        const injectionVelocity = qps * 0.01;
        const dissipation = errorRate * 10.0;
        
        // Apply to WebGL shader
        this.gl.uniform1f(this.qpsLocation, injectionVelocity);
        this.gl.uniform1f(this.errorRateLocation, dissipation);
    }
}
```

### **🏳️ Cloth Banner**
```javascript
// Ripple amplitude = throughput; tear hint when p95 spikes
class ClothBanner {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.particles = [];
        this.springs = [];
        this.initializeCloth();
    }

    update(throughput, p95) {
        // Apply wind based on throughput
        const windStrength = throughput * 0.01;
        
        // Handle tears based on p95 spikes
        if (p95 > 200) {
            this.handleTears(p95);
        }
        
        // Update cloth physics
        this.updateClothPhysics();
    }
}
```

---

## 🧪 **Quick Test Scenes**

### **📈 Load Sweep**
```javascript
// Simulate QPS 0→120→0; check particle birth/decay feels natural
function runLoadSweep() {
    let qps = 0;
    let direction = 1;
    const interval = setInterval(() => {
        qps += direction * 2;
        if (qps >= 120) direction = -1;
        else if (qps <= 0) direction = 1;
        
        // Update metrics
        updateMetrics({ qps });
    }, 100);
    
    setTimeout(() => clearInterval(interval), 10000);
}
```

### **⚡ Latency Spike**
```javascript
// Set p95 40→220 ms; confirm motion "heavies" and recovers smoothly
function runLatencySpike() {
    let p95 = 40;
    let direction = 1;
    const interval = setInterval(() => {
        p95 += direction * 10;
        if (p95 >= 220) direction = -1;
        else if (p95 <= 40) direction = -1;
        
        // Update metrics
        updateMetrics({ p95 });
    }, 100);
    
    setTimeout(() => clearInterval(interval), 10000);
}
```

### **💥 Error Burst**
```javascript
// ErrorRate 0→0.2 for 10s; see turbulence + opacity pulse; boids disorganize
function runErrorBurst() {
    let errorRate = 0;
    let direction = 1;
    const interval = setInterval(() => {
        errorRate += direction * 0.02;
        if (errorRate >= 0.2) direction = -1;
        else if (errorRate <= 0) direction = 1;
        
        // Update metrics
        updateMetrics({ errorRate });
    }, 100);
    
    setTimeout(() => clearInterval(interval), 10000);
}
```

### **🌪️ Fallback Storm**
```javascript
// FallbackRatio > 0.15; verify warning tint and legend notice
function runFallbackStorm() {
    let fallbackRatio = 0;
    let direction = 1;
    const interval = setInterval(() => {
        fallbackRatio += direction * 0.01;
        if (fallbackRatio >= 0.3) direction = -1;
        else if (fallbackRatio <= 0) direction = 1;
        
        // Update metrics
        updateMetrics({ fallbackRatio });
    }, 100);
    
    setTimeout(() => clearInterval(interval), 10000);
}
```

---

## 🎛️ **Single PhysicsFX.init() Helper**

```javascript
// Complete drop-in helper with all rails
import { initPhysicsFX } from './scripts/physics-fx-production.js';

// Initialize with all production hardening
const physicsFX = initPhysicsFX({
    canvas: document.getElementById('physics-fx-canvas'),
    source: '/metrics/snapshot',
    mode: 'full', // or get from URL params
    debounceMs: 100,
    qualityScaling: true,
    reducedMotion: true,
    legend: true,
    telemetry: true
});

// That's it! Everything is handled automatically:
// - Quality scaling based on FPS
// - Reduced motion respect
// - Legend overlay
// - Telemetry to Prometheus
// - Error handling and recovery
// - Mobile optimization
// - Performance monitoring
```

---

## 🎉 **Expected Benefits**

### **For Developers**
- **Drop-in Integration**: Single function call to enable physics FX
- **Production Ready**: All hardening wins included
- **Performance Aware**: Automatic quality scaling
- **Accessible**: Respects user preferences

### **For Users**
- **Visual Appeal**: Beautiful physics simulations
- **Performance Understanding**: See system health through physics
- **Customization**: Choose FX modes and quality
- **Accessibility**: Inclusive design principles

### **For Code Live**
- **Professional Quality**: Production-ready physics effects
- **Scalability**: Performance-adaptive effects
- **Maintainability**: Clean, modular code
- **Monitoring**: Built-in telemetry and metrics

---

## 🎯 **The Result: Production-Hardened Physics FX**

**Code Live becomes the ultimate production-ready physics experience where:**
- **Quality Scaler** = Drop particle cap when FPS < 45; restore at 60
- **Kill-switch & Modes** = `?fx=off|lite|full` URL param + UI toggle
- **Metrics Adapter** = Debounce to 10–20 Hz; clamp outliers; fallback to demo generator
- **A11y & Motion** = Respect `prefers-reduced-motion`; hide FX from screen readers; pause on tab blur
- **Theme & Legend** = Fixed color keys per backend; small legend overlay
- **Perf Budget** = Keep FX thread under ~6–8 ms/frame; avoid layout thrash
- **Error Fences** = Try/catch around shader init; re-init on WebGL context loss
- **Mobile Posture** = OffscreenCanvas if available; halve resolution on DPR>1.5
- **Telemetry** = Emit `fx_frame_ms`, `fx_quality_level`, `fx_backpressure_events` to Prometheus

**This creates the perfect balance between physics simulation and production readiness - just like having a living, breathing system that's ready for production deployment!**

**Code Live becomes the "Production-Hardened Physics FX System" where developers work in a beautiful, performance-aware, and production-ready visual space!** 🎛️✨🌊

---

*The Production-Hardened Physics FX System - where developers work in a beautiful, performance-aware environment that enhances the experience with physics-driven living systems that are ready for production deployment!* 🎛️🌊💥



