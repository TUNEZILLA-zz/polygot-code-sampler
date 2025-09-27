/**
 * Code Live Physics FX Plugin
 * Physics-Driven Living System with Particles, Boids, Springs, and Flows
 */

export function createPhysicsFX(canvas, getMetrics) {
    // Engine & renderer
    const engine = Engine.create();
    engine.gravity.y = 0;
    const render = Render.create({
        canvas,
        engine,
        options: {
            wireframes: false,
            background: '#0b0f14',
            width: canvas.clientWidth,
            height: canvas.clientHeight
        }
    });
    Render.run(render);
    const runner = Runner.create();
    Runner.run(runner, engine);

    // Bounds
    const W = canvas.clientWidth, H = canvas.clientHeight;
    const walls = [
        Bodies.rectangle(W/2, -10, W, 20, { isStatic: true }),
        Bodies.rectangle(W/2, H+10, W, 20, { isStatic: true }),
        Bodies.rectangle(-10, H/2, 20, H, { isStatic: true }),
        Bodies.rectangle(W+10, H/2, 20, H, { isStatic: true }),
    ];
    Composite.add(engine.world, walls);

    // Backend attractors (corners)
    const attractors = {
        rust:   Vector.create(W*0.20, H*0.30),
        ts:     Vector.create(W*0.80, H*0.30),
        go:     Vector.create(W*0.20, H*0.70),
        csharp: Vector.create(W*0.80, H*0.70),
        sql:    Vector.create(W*0.50, H*0.15),
        julia:  Vector.create(W*0.50, H*0.85),
    };
    const colors = {
        rust:'#f74c00',
        ts:'#2f9cf4',
        go:'#00add8',
        csharp:'#68217a',
        sql:'#e09f3e',
        julia:'#9558b2'
    };

    // Particle pool
    const pool = [];
    const MAX = 400;
    let lastSpawn = 0;

    function spawnParticle(targetKey) {
        const x = W/2 + (Math.random()-0.5)*40, y = H/2 + (Math.random()-0.5)*40;
        const r = 3 + Math.random()*2;
        const fill = colors[targetKey] || '#8ab';
        const p = Bodies.circle(x, y, r, {
            restitution: 0.2, frictionAir: 0.02, render: { fillStyle: fill, strokeStyle: 'transparent' }
        });
        p.__target = targetKey;
        pool.push(p);
        Composite.add(engine.world, p);
        if (pool.length > MAX) {
            const old = pool.shift();
            Composite.remove(engine.world, old);
        }
    }

    // Main loop: map metrics → forces
    (function tick() {
        const m = getMetrics(); // { qps, p95, errorRate, perBackend: {rust:0..1,...} }

        // Spawn proportional to QPS (capped)
        const now = performance.now();
        const spawnHz = Math.min(120, (m.qps || 0));            // cap spawn rate
        const spawnInterval = 1000 / (spawnHz + 1e-6);
        while (now - lastSpawn > spawnInterval) {
            // choose backend weighted by perBackend
            const keys = Object.keys(m.perBackend || colors);
            const weights = keys.map(k => Math.max(0, m.perBackend?.[k] || 0.1));
            const sum = weights.reduce((a,b)=>a+b,0) || 1;
            let r = Math.random() * sum;
            let choice = keys[0];
            for (let i=0;i<keys.length;i++){ r-=weights[i]; if (r<=0){ choice=keys[i]; break; } }
            spawnParticle(choice);
            lastSpawn += spawnInterval;
        }

        // Global damping from latency
        const damping = Math.min(0.25, (m.p95 || 0) / 300.0);   // p95 ms → 0..0.25
        engine.world.bodies.forEach(b => { if (!b.isStatic) b.frictionAir = 0.02 + damping; });

        // Turbulent wind from error rate
        const err = Math.min(1, m.errorRate || 0);
        const wind = Vector.create(
            (Math.sin(now*0.002)+Math.random()*0.3) * err * 0.005,
            (Math.cos(now*0.0017)+Math.random()*0.3) * err * 0.005
        );

        // Per-particle attraction towards its backend anchor + wind
        for (const b of pool) {
            const target = attractors[b.__target] || Vector.create(W/2, H/2);
            const dir = Vector.normalise(Vector.sub(target, b.position));
            const pull = 0.0025; // base attraction
            Body.applyForce(b, b.position, Vector.add(Vector.mult(dir, pull), wind));
        }

        // Color flash on high fallback
        if ((m.fallbackRatio || 0) > 0.1) {
            const pulse = 0.5 + 0.5*Math.sin(now*0.02);
            for (const b of pool) b.render.opacity = 0.6 + 0.4*pulse;
        } else {
            for (const b of pool) b.render.opacity = 1.0;
        }

        requestAnimationFrame(tick);
    })();

    // Resize handling
    addEventListener('resize', () => {
        render.canvas.width = canvas.clientWidth;
        render.canvas.height = canvas.clientHeight;
    });

    return { engine, render };
}

// Example wiring:
export function createExamplePhysicsFX() {
    const canvas = document.getElementById('fx');
    if (!canvas) return;

    const metricsSource = (() => {
        // Replace with real Prometheus-scraped values or your app store
        let t = 0;
        return () => {
            t += 1;
            return {
                qps: 30 + 20*Math.sin(t*0.02),
                p95: 40 + 30*Math.sin(t*0.017),
                errorRate: Math.max(0, 0.05*Math.sin(t*0.01)),
                fallbackRatio: Math.max(0, 0.08*Math.cos(t*0.012)),
                perBackend: { rust:0.9, ts:0.8, go:0.7, csharp:0.6, sql:0.5, julia:0.4 }
            };
        };
    })();

    return createPhysicsFX(canvas, metricsSource);
}

// Boids/Swarm Behavior
export class BoidsSystem {
    constructor(particles, metrics) {
        this.particles = particles;
        this.metrics = metrics;
        this.cohesion = 0.1;
        this.alignment = 0.1;
        this.separation = 0.1;
        this.maxSpeed = 2;
        this.maxForce = 0.1;
    }

    update() {
        const errorRate = this.metrics.errorRate || 0;

        // Cohesion goes down as error rate rises
        this.cohesion = Math.max(0.01, 0.1 - errorRate * 0.09);

        // Separation increases with error rate
        this.separation = 0.1 + errorRate * 0.2;

        for (const particle of this.particles) {
            const flock = this.getFlock(particle);
            const cohesionForce = this.cohesionForce(particle, flock);
            const alignmentForce = this.alignmentForce(particle, flock);
            const separationForce = this.separationForce(particle, flock);

            // Apply forces
            this.applyForce(particle, cohesionForce);
            this.applyForce(particle, alignmentForce);
            this.applyForce(particle, separationForce);
        }
    }

    getFlock(particle) {
        const perceptionRadius = 50;
        return this.particles.filter(p => {
            const distance = Math.sqrt(
                Math.pow(p.position.x - particle.position.x, 2) +
                Math.pow(p.position.y - particle.position.y, 2)
            );
            return distance < perceptionRadius && p !== particle;
        });
    }

    cohesionForce(particle, flock) {
        if (flock.length === 0) return { x: 0, y: 0 };

        const centerX = flock.reduce((sum, p) => sum + p.position.x, 0) / flock.length;
        const centerY = flock.reduce((sum, p) => sum + p.position.y, 0) / flock.length;

        const steerX = centerX - particle.position.x;
        const steerY = centerY - particle.position.y;

        return this.limitForce({ x: steerX * this.cohesion, y: steerY * this.cohesion });
    }

    alignmentForce(particle, flock) {
        if (flock.length === 0) return { x: 0, y: 0 };

        const avgVelX = flock.reduce((sum, p) => sum + p.velocity.x, 0) / flock.length;
        const avgVelY = flock.reduce((sum, p) => sum + p.velocity.y, 0) / flock.length;

        return this.limitForce({ x: avgVelX * this.alignment, y: avgVelY * this.alignment });
    }

    separationForce(particle, flock) {
        let steerX = 0, steerY = 0;

        for (const other of flock) {
            const distance = Math.sqrt(
                Math.pow(particle.position.x - other.position.x, 2) +
                Math.pow(particle.position.y - other.position.y, 2)
            );

            if (distance < 25) {
                const diffX = particle.position.x - other.position.x;
                const diffY = particle.position.y - other.position.y;
                const diff = Math.sqrt(diffX * diffX + diffY * diffY);

                if (diff > 0) {
                    steerX += diffX / diff;
                    steerY += diffY / diff;
                }
            }
        }

        return this.limitForce({ x: steerX * this.separation, y: steerY * this.separation });
    }

    limitForce(force) {
        const magnitude = Math.sqrt(force.x * force.x + force.y * force.y);
        if (magnitude > this.maxForce) {
            return {
                x: (force.x / magnitude) * this.maxForce,
                y: (force.y / magnitude) * this.maxForce
            };
        }
        return force;
    }

    applyForce(particle, force) {
        particle.velocity.x += force.x;
        particle.velocity.y += force.y;

        // Limit speed
        const speed = Math.sqrt(particle.velocity.x * particle.velocity.x + particle.velocity.y * particle.velocity.y);
        if (speed > this.maxSpeed) {
            particle.velocity.x = (particle.velocity.x / speed) * this.maxSpeed;
            particle.velocity.y = (particle.velocity.y / speed) * this.maxSpeed;
        }
    }
}

// Spring-Mass Timeline
export class SpringTimeline {
    constructor(keyframes, springConstant = 0.1, damping = 0.9) {
        this.keyframes = keyframes;
        this.springConstant = springConstant;
        this.damping = damping;
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
            const springForce = (target - mass.position) * this.springConstant;

            // Apply force
            mass.velocity += springForce;
            mass.velocity *= this.damping;
            mass.position += mass.velocity;
        }
    }

    getInterpolatedValue(progress) {
        const index = Math.floor(progress * (this.masses.length - 1));
        const nextIndex = Math.min(index + 1, this.masses.length - 1);
        const localProgress = (progress * (this.masses.length - 1)) - index;

        return this.masses[index].position +
               (this.masses[nextIndex].position - this.masses[index].position) * localProgress;
    }
}

// Cloth/Flag Banner
export class ClothBanner {
    constructor(width, height, segments = 20) {
        this.width = width;
        this.height = height;
        this.segments = segments;
        this.particles = [];
        this.springs = [];

        this.initializeCloth();
    }

    initializeCloth() {
        const segmentWidth = this.width / this.segments;
        const segmentHeight = this.height / this.segments;

        // Create particles
        for (let y = 0; y < this.segments; y++) {
            for (let x = 0; x < this.segments; x++) {
                this.particles.push({
                    position: { x: x * segmentWidth, y: y * segmentHeight },
                    velocity: { x: 0, y: 0 },
                    fixed: y === 0, // Top row is fixed
                    mass: 1
                });
            }
        }

        // Create springs
        for (let y = 0; y < this.segments; y++) {
            for (let x = 0; x < this.segments; x++) {
                const index = y * this.segments + x;

                // Horizontal springs
                if (x < this.segments - 1) {
                    this.springs.push({
                        p1: index,
                        p2: index + 1,
                        restLength: segmentWidth,
                        stiffness: 0.1
                    });
                }

                // Vertical springs
                if (y < this.segments - 1) {
                    this.springs.push({
                        p1: index,
                        p2: index + this.segments,
                        restLength: segmentHeight,
                        stiffness: 0.1
                    });
                }
            }
        }
    }

    update(throughput, errorRate) {
        // Apply wind based on throughput
        const windStrength = throughput * 0.01;
        const windX = Math.sin(Date.now() * 0.001) * windStrength;
        const windY = Math.cos(Date.now() * 0.001) * windStrength;

        // Apply forces
        for (const particle of this.particles) {
            if (!particle.fixed) {
                // Wind force
                particle.velocity.x += windX;
                particle.velocity.y += windY;

                // Gravity
                particle.velocity.y += 0.1;

                // Damping
                particle.velocity.x *= 0.99;
                particle.velocity.y *= 0.99;

                // Update position
                particle.position.x += particle.velocity.x;
                particle.position.y += particle.velocity.y;
            }
        }

        // Update springs
        for (const spring of this.springs) {
            const p1 = this.particles[spring.p1];
            const p2 = this.particles[spring.p2];

            const dx = p2.position.x - p1.position.x;
            const dy = p2.position.y - p1.position.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const force = (distance - spring.restLength) * spring.stiffness;

            const fx = (dx / distance) * force;
            const fy = (dy / distance) * force;

            if (!p1.fixed) {
                p1.velocity.x += fx / p1.mass;
                p1.velocity.y += fy / p1.mass;
            }

            if (!p2.fixed) {
                p2.velocity.x -= fx / p2.mass;
                p2.velocity.y -= fy / p2.mass;
            }
        }

        // Handle tears/creases on spikes/failures
        if (errorRate > 0.1) {
            this.handleTears(errorRate);
        }
    }

    handleTears(errorRate) {
        // Randomly break springs based on error rate
        for (const spring of this.springs) {
            if (Math.random() < errorRate * 0.01) {
                spring.stiffness *= 0.5; // Weaken spring
            }
        }
    }

    render(ctx) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 1;

        for (const spring of this.springs) {
            const p1 = this.particles[spring.p1];
            const p2 = this.particles[spring.p2];

            ctx.beginPath();
            ctx.moveTo(p1.position.x, p1.position.y);
            ctx.lineTo(p2.position.x, p2.position.y);
            ctx.stroke();
        }
    }
}

// Flow/Fluids (WebGL shader)
export class FluidSimulation {
    constructor(canvas) {
        this.canvas = canvas;
        this.gl = canvas.getContext('webgl');
        this.initShaders();
        this.initBuffers();
    }

    initShaders() {
        const vertexShader = `
            attribute vec2 position;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
            }
        `;

        const fragmentShader = `
            precision highp float;
            uniform vec2 resolution;
            uniform float time;
            uniform float qps;
            uniform float errorRate;

            void main() {
                vec2 uv = gl_FragCoord.xy / resolution.xy;
                vec2 center = vec2(0.5, 0.5);

                // Flow speed based on QPS
                float flowSpeed = qps * 0.01;

                // Turbulence based on error rate
                float turbulence = errorRate * 10.0;

                // Create flow pattern
                vec2 flow = vec2(
                    sin(uv.x * 10.0 + time * flowSpeed) * 0.1,
                    cos(uv.y * 10.0 + time * flowSpeed) * 0.1
                );

                // Add turbulence
                flow += vec2(
                    sin(uv.x * 20.0 + time * turbulence) * 0.05,
                    cos(uv.y * 20.0 + time * turbulence) * 0.05
                );

                // Color based on flow
                vec3 color = vec3(
                    0.1 + flow.x * 0.5,
                    0.2 + flow.y * 0.5,
                    0.4 + length(flow) * 0.3
                );

                gl_FragColor = vec4(color, 0.3);
            }
        `;

        this.program = this.createProgram(vertexShader, fragmentShader);
    }

    createProgram(vertexShader, fragmentShader) {
        const program = this.gl.createProgram();
        const vs = this.gl.createShader(this.gl.VERTEX_SHADER);
        const fs = this.gl.createShader(this.gl.FRAGMENT_SHADER);

        this.gl.shaderSource(vs, vertexShader);
        this.gl.shaderSource(fs, fragmentShader);
        this.gl.compileShader(vs);
        this.gl.compileShader(fs);

        this.gl.attachShader(program, vs);
        this.gl.attachShader(program, fs);
        this.gl.linkProgram(program);

        return program;
    }

    initBuffers() {
        const vertices = new Float32Array([
            -1, -1, 1, -1, -1, 1,
            1, -1, 1, 1, -1, 1
        ]);

        this.buffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, vertices, this.gl.STATIC_DRAW);
    }

    update(qps, errorRate) {
        this.gl.useProgram(this.program);

        const positionLocation = this.gl.getAttribLocation(this.program, 'position');
        this.gl.enableVertexAttribArray(positionLocation);
        this.gl.vertexAttribPointer(positionLocation, 2, this.gl.FLOAT, false, 0, 0);

        const resolutionLocation = this.gl.getUniformLocation(this.program, 'resolution');
        this.gl.uniform2f(resolutionLocation, this.canvas.width, this.canvas.height);

        const timeLocation = this.gl.getUniformLocation(this.program, 'time');
        this.gl.uniform1f(timeLocation, Date.now() * 0.001);

        const qpsLocation = this.gl.getUniformLocation(this.program, 'qps');
        this.gl.uniform1f(qpsLocation, qps);

        const errorRateLocation = this.gl.getUniformLocation(this.program, 'errorRate');
        this.gl.uniform1f(errorRateLocation, errorRate);

        this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);
    }
}

// Performance safety rails
export class PerformanceManager {
    constructor() {
        this.maxBodies = 400;
        this.targetFPS = 60;
        this.currentFPS = 60;
        this.qualityLevel = 1.0;
    }

    updatePerformanceMetrics(activeBodies, currentFPS) {
        this.currentFPS = currentFPS;

        // Adjust quality based on performance
        if (currentFPS < 30) {
            this.qualityLevel = Math.max(0.5, this.qualityLevel - 0.1);
        } else if (currentFPS > 55) {
            this.qualityLevel = Math.min(1.0, this.qualityLevel + 0.05);
        }

        // Cap active bodies
        if (activeBodies > this.maxBodies) {
            return Math.floor(this.maxBodies * this.qualityLevel);
        }

        return activeBodies;
    }

    shouldReduceQuality() {
        return this.currentFPS < 30 || this.qualityLevel < 0.8;
    }

    getQualityMultiplier() {
        return this.qualityLevel;
    }
}

// Export all components
export default {
    createPhysicsFX,
    createExamplePhysicsFX,
    BoidsSystem,
    SpringTimeline,
    ClothBanner,
    FluidSimulation,
    PerformanceManager
};
