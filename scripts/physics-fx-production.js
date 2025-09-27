/**
 * Code Live Physics FX - Production Hardened System
 * Complete drop-in physics FX with quality scaling, reduced-motion, legend, and Prom metrics hooks
 */

import { Engine, Render, Runner, Bodies, Composite, Body, Vector } from 'https://cdn.skypack.dev/matter-js@0.19.0';

class PhysicsFXProduction {
    constructor(options = {}) {
        this.canvas = options.canvas;
        this.mode = options.mode || 'full';
        this.qualityLevel = 1.0;
        this.isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        this.isTabVisible = !document.hidden;
        this.frameCount = 0;
        this.lastFrameTime = performance.now();
        this.fps = 60;
        this.telemetry = {
            fx_frame_ms: 0,
            fx_quality_level: 1.0,
            fx_backpressure_events: 0
        };
        
        this.initialize();
    }

    initialize() {
        if (this.mode === 'off' || this.isReducedMotion) {
            return;
        }

        this.setupEventListeners();
        this.initializePhysics();
        this.initializeQualityScaler();
        this.initializeTheme();
        this.startPhysicsLoop();
    }

    setupEventListeners() {
        // Respect reduced motion
        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            this.isReducedMotion = e.matches;
            if (this.isReducedMotion) {
                this.pausePhysics();
            } else {
                this.resumePhysics();
            }
        });

        // Pause on tab blur
        document.addEventListener('visibilitychange', () => {
            this.isTabVisible = !document.hidden;
            if (!this.isTabVisible) {
                this.pausePhysics();
            } else {
                this.resumePhysics();
            }
        });

        // Handle WebGL context loss
        this.canvas.addEventListener('webglcontextlost', (e) => {
            e.preventDefault();
            this.handleContextLoss();
        });

        this.canvas.addEventListener('webglcontextrestored', () => {
            this.handleContextRestore();
        });
    }

    initializePhysics() {
        try {
            // Engine & renderer
            this.engine = Engine.create();
            this.engine.gravity.y = 0;
            this.render = Render.create({
                canvas: this.canvas,
                engine: this.engine,
                options: { 
                    wireframes: false, 
                    background: '#0b0f14', 
                    width: this.canvas.clientWidth, 
                    height: this.canvas.clientHeight 
                }
            });
            Render.run(this.render);
            this.runner = Runner.create();
            Runner.run(this.runner, this.engine);

            // Bounds
            const W = this.canvas.clientWidth, H = this.canvas.clientHeight;
            this.walls = [
                Bodies.rectangle(W/2, -10, W, 20, { isStatic: true }),
                Bodies.rectangle(W/2, H+10, W, 20, { isStatic: true }),
                Bodies.rectangle(-10, H/2, 20, H, { isStatic: true }),
                Bodies.rectangle(W+10, H/2, 20, H, { isStatic: true }),
            ];
            Composite.add(this.engine.world, this.walls);

            // Backend attractors (corners)
            this.attractors = {
                rust:   Vector.create(W*0.20, H*0.30),
                ts:     Vector.create(W*0.80, H*0.30),
                go:     Vector.create(W*0.20, H*0.70),
                csharp: Vector.create(W*0.80, H*0.70),
                sql:    Vector.create(W*0.50, H*0.15),
                julia:  Vector.create(W*0.50, H*0.85),
            };

            // Fixed color keys per backend
            this.colors = { 
                rust:'#f74c00', 
                ts:'#2f9cf4', 
                go:'#00add8', 
                csharp:'#68217a', 
                sql:'#e09f3e', 
                julia:'#9558b2' 
            };

            // Particle pool
            this.pool = [];
            this.MAX = 400;
            this.lastSpawn = 0;
            this.metrics = {
                qps: 0, p95: 30, errorRate: 0, fallbackRatio: 0,
                perBackend: { rust:0.5, ts:0.5, go:0.4, csharp:0.3, sql:0.2, julia:0.2 }
            };

            this.createLegend();
            this.createQualityIndicator();

        } catch (error) {
            console.error('Physics FX initialization failed:', error);
            this.handleError(error);
        }
    }

    initializeQualityScaler() {
        this.qualityScaler = {
            targetFPS: 60,
            minFPS: 45,
            maxParticles: 400,
            minParticles: 100,
            qualityStep: 0.1
        };
    }

    initializeTheme() {
        // Create theme CSS
        const style = document.createElement('style');
        style.textContent = `
            .physics-fx-legend {
                position: fixed;
                top: 10px;
                left: 10px;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
            }
            .physics-fx-quality {
                position: fixed;
                bottom: 10px;
                left: 10px;
                background: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-family: monospace;
                font-size: 10px;
                z-index: 1000;
                pointer-events: none;
            }
        `;
        document.head.appendChild(style);
    }

    createLegend() {
        const legend = document.createElement('div');
        legend.className = 'physics-fx-legend';
        legend.innerHTML = `
            <div><span style="color: #f74c00;">●</span> Rust</div>
            <div><span style="color: #2f9cf4;">●</span> TypeScript</div>
            <div><span style="color: #00add8;">●</span> Go</div>
            <div><span style="color: #68217a;">●</span> C#</div>
            <div><span style="color: #e09f3e;">●</span> SQL</div>
            <div><span style="color: #9558b2;">●</span> Julia</div>
        `;
        document.body.appendChild(legend);
    }

    createQualityIndicator() {
        const quality = document.createElement('div');
        quality.className = 'physics-fx-quality';
        quality.id = 'physics-fx-quality';
        document.body.appendChild(quality);
    }

    startPhysicsLoop() {
        if (this.mode === 'off' || this.isReducedMotion) {
            return;
        }

        const tick = () => {
            const startTime = performance.now();
            
            if (this.isTabVisible && !this.isReducedMotion) {
                this.updatePhysics();
                this.updateQualityScaler();
                this.updateTelemetry();
            }
            
            const frameTime = performance.now() - startTime;
            this.telemetry.fx_frame_ms = frameTime;
            
            // Keep FX thread under ~6–8 ms/frame
            if (frameTime > 8) {
                this.telemetry.fx_backpressure_events++;
                this.reduceQuality();
            }
            
            this.frameCount++;
            this.updateFPS();
            
            requestAnimationFrame(tick);
        };
        
        tick();
    }

    updatePhysics() {
        const now = performance.now();
        const m = this.metrics;

        // Spawn proportional to QPS (capped)
        const spawnHz = Math.min(120, (m.qps || 0));
        const spawnInterval = 1000 / (spawnHz + 1e-6);
        while (now - this.lastSpawn > spawnInterval) {
            this.spawnParticle();
            this.lastSpawn += spawnInterval;
        }

        // Global damping from latency
        const damping = Math.min(0.25, (m.p95 || 0) / 300.0);
        this.engine.world.bodies.forEach(b => { 
            if (!b.isStatic) b.frictionAir = 0.02 + damping; 
        });

        // Turbulent wind from error rate
        const err = Math.min(1, m.errorRate || 0);
        const wind = Vector.create( 
            (Math.sin(now*0.002)+Math.random()*0.3) * err * 0.005,
            (Math.cos(now*0.0017)+Math.random()*0.3) * err * 0.005 
        );

        // Per-particle attraction towards its backend anchor + wind
        for (const b of this.pool) {
            const target = this.attractors[b.__target] || Vector.create(this.canvas.clientWidth/2, this.canvas.clientHeight/2);
            const dir = Vector.normalise(Vector.sub(target, b.position));
            const pull = 0.0025;
            Body.applyForce(b, b.position, Vector.add(Vector.mult(dir, pull), wind));
        }

        // Color flash on high fallback
        if ((m.fallbackRatio || 0) > 0.1) {
            const pulse = 0.5 + 0.5*Math.sin(now*0.02);
            for (const b of this.pool) b.render.opacity = 0.6 + 0.4*pulse;
        } else {
            for (const b of this.pool) b.render.opacity = 1.0;
        }
    }

    spawnParticle() {
        const W = this.canvas.clientWidth;
        const H = this.canvas.clientHeight;
        const x = W/2 + (Math.random()-0.5)*40;
        const y = H/2 + (Math.random()-0.5)*40;
        const r = 3 + Math.random()*2;
        
        // Choose backend weighted by perBackend
        const keys = Object.keys(this.metrics.perBackend || this.colors);
        const weights = keys.map(k => Math.max(0, this.metrics.perBackend?.[k] || 0.1));
        const sum = weights.reduce((a,b) => a+b, 0) || 1;
        let rnd = Math.random() * sum;
        let choice = keys[0];
        for (let i=0; i<keys.length; i++){ 
            rnd -= weights[i]; 
            if (rnd <= 0){ 
                choice = keys[i]; 
                break; 
            } 
        }
        
        const fill = this.colors[choice] || '#8ab';
        const p = Bodies.circle(x, y, r, {
            restitution: 0.2, 
            frictionAir: 0.02, 
            render: { fillStyle: fill, strokeStyle: 'transparent' }
        });
        p.__target = choice;
        this.pool.push(p);
        Composite.add(this.engine.world, p);
        
        // Quality-based particle cap
        const maxParticles = Math.floor(this.qualityScaler.maxParticles * this.qualityLevel);
        if (this.pool.length > maxParticles) {
            const old = this.pool.shift();
            Composite.remove(this.engine.world, old);
        }
    }

    updateQualityScaler() {
        // Drop particle cap when FPS < 45; restore at 60
        if (this.fps < this.qualityScaler.minFPS) {
            this.reduceQuality();
        } else if (this.fps > this.qualityScaler.targetFPS) {
            this.increaseQuality();
        }
        
        this.telemetry.fx_quality_level = this.qualityLevel;
    }

    reduceQuality() {
        this.qualityLevel = Math.max(0.5, this.qualityLevel - this.qualityScaler.qualityStep);
        this.updateQualityDisplay();
    }

    increaseQuality() {
        this.qualityLevel = Math.min(1.0, this.qualityLevel + this.qualityScaler.qualityStep);
        this.updateQualityDisplay();
    }

    updateQualityDisplay() {
        const qualityEl = document.getElementById('physics-fx-quality');
        if (qualityEl) {
            qualityEl.textContent = `Quality: ${Math.round(this.qualityLevel * 100)}% | FPS: ${this.fps}`;
        }
    }

    updateFPS() {
        const now = performance.now();
        const deltaTime = now - this.lastFrameTime;
        
        if (deltaTime >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / deltaTime);
            this.lastFrameTime = now;
            this.frameCount = 0;
        }
    }

    updateTelemetry() {
        // Emit telemetry to Prometheus
        if (window.gtag) {
            gtag('event', 'physics_fx_telemetry', {
                fx_frame_ms: this.telemetry.fx_frame_ms,
                fx_quality_level: this.telemetry.fx_quality_level,
                fx_backpressure_events: this.telemetry.fx_backpressure_events
            });
        }
    }

    pausePhysics() {
        if (this.runner) {
            Runner.stop(this.runner);
        }
    }

    resumePhysics() {
        if (this.runner) {
            Runner.run(this.runner, this.engine);
        }
    }

    handleContextLoss() {
        console.warn('WebGL context lost, pausing physics FX');
        this.pausePhysics();
    }

    handleContextRestore() {
        console.log('WebGL context restored, resuming physics FX');
        this.initializePhysics();
        this.resumePhysics();
    }

    handleError(error) {
        console.error('Physics FX error:', error);
        this.pausePhysics();
    }

    // Public API
    updateMetrics(metrics) {
        this.metrics = this.sanitizeMetrics(metrics);
    }

    sanitizeMetrics(m) {
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

    setMode(mode) {
        this.mode = mode;
        if (mode === 'off') {
            this.pausePhysics();
        } else {
            this.resumePhysics();
        }
    }

    destroy() {
        this.pausePhysics();
        if (this.engine) {
            Engine.clear(this.engine);
        }
        if (this.render) {
            Render.stop(this.render);
        }
    }
}

// Metrics Adapter
class MetricsAdapter {
    constructor(source, options = {}) {
        this.source = source;
        this.debounceMs = options.debounceMs || 100; // 10Hz
        this.timeoutHandle = null;
        this.latest = {
            qps: 0, p95: 30, errorRate: 0, fallbackRatio: 0,
            perBackend: { rust:0.5, ts:0.5, go:0.4, csharp:0.3, sql:0.2, julia:0.2 }
        };
        
        this.startPolling();
    }

    async poll() {
        try {
            const res = await fetch(this.source);
            if (res.ok) {
                const m = await res.json();
                this.latest = this.sanitize(m);
            }
        } catch (error) {
            console.warn('Metrics fetch failed, using fallback:', error);
            this.useFallbackMetrics();
        }
        
        this.timeoutHandle = setTimeout(() => this.poll(), this.debounceMs);
    }

    sanitize(m) {
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

    useFallbackMetrics() {
        // Demo generator fallback
        const t = Date.now() * 0.001;
        this.latest = {
            qps: 30 + 20*Math.sin(t*0.02),
            p95: 40 + 30*Math.sin(t*0.017),
            errorRate: Math.max(0, 0.05*Math.sin(t*0.01)),
            fallbackRatio: Math.max(0, 0.08*Math.cos(t*0.012)),
            perBackend: { rust:0.9, ts:0.8, go:0.7, csharp:0.6, sql:0.5, julia:0.4 }
        };
    }

    startPolling() {
        this.poll();
    }

    stopPolling() {
        if (this.timeoutHandle) {
            clearTimeout(this.timeoutHandle);
        }
    }

    getMetrics() {
        return this.latest;
    }
}

// Drop-in initialization helper
export function initPhysicsFX(options = {}) {
    const canvas = options.canvas || document.getElementById('physics-fx-canvas');
    if (!canvas) {
        console.error('Physics FX canvas not found');
        return null;
    }

    // Get mode from URL params or reduced motion
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('fx') || (window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'lite' : 'full');
    
    if (mode === 'off') {
        return null;
    }

    // Initialize physics FX
    const physicsFX = new PhysicsFXProduction({
        canvas,
        mode,
        ...options
    });

    // Initialize metrics adapter
    const metricsSource = options.metricsSource || '/metrics/snapshot';
    const metricsAdapter = new MetricsAdapter(metricsSource, {
        debounceMs: options.debounceMs || 100
    });

    // Connect metrics to physics
    const updateLoop = () => {
        physicsFX.updateMetrics(metricsAdapter.getMetrics());
        requestAnimationFrame(updateLoop);
    };
    updateLoop();

    return {
        physicsFX,
        metricsAdapter,
        destroy: () => {
            physicsFX.destroy();
            metricsAdapter.stopPolling();
        }
    };
}

// Export for use
export { PhysicsFXProduction, MetricsAdapter };
export default initPhysicsFX;

