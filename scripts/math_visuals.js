/**
 * Code Live Mathematical Visual Effects
 * Fibonacci, Color Frequencies, and Fractals for Tasteful Mathy Visuals
 */

class MathVisualsSystem {
    constructor() {
        this.canvases = {};
        this.contexts = {};
        this.animations = {};
        this.metrics = {
            requestRate: 12.4,
            successRate: 0.858,
            p95Latency: 0.045,
            juliaActive: false
        };

        this.initialize();
    }

    initialize() {
        this.setupEventListeners();
        this.startPerformanceMonitoring();
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.handleResize());
    }

    handleResize() {
        Object.values(this.canvases).forEach(canvas => {
            this.fitCanvas(canvas);
        });
    }

    fitCanvas(canvas) {
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        const ctx = canvas.getContext('2d');
        if (ctx) {
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        }
    }

    startPerformanceMonitoring() {
        setInterval(() => {
            // Simulate performance metrics
            this.metrics.requestRate = 5 + Math.random() * 15;
            this.metrics.successRate = 0.8 + Math.random() * 0.2;
            this.metrics.p95Latency = 0.01 + Math.random() * 0.05;
            this.metrics.juliaActive = Math.random() > 0.5;

            this.updateVisuals();
        }, 1000);
    }

    updateVisuals() {
        // Update all active visual effects
        Object.values(this.animations).forEach(animation => {
            if (animation.active) {
                animation.update(this.metrics);
            }
        });
    }

    // 1) Phyllotaxis (Fibonacci flower) — Canvas
    createPhyllotaxis(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d', { alpha: false });
        this.fitCanvas(canvas);

        const config = {
            N: 1000,
            sat: 70,
            light: 55,
            scale: 5,
            hueBase: 200,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderPhyllotaxis(canvasId),
            update: (metrics) => this.updatePhyllotaxis(canvasId, metrics)
        };

        this.renderPhyllotaxis(canvasId);
        this.startAnimation(canvasId);
    }

    renderPhyllotaxis(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = '#0b0b12';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const GA = Math.PI * (3 - Math.sqrt(5)); // golden angle

        for (let n = 0; n < config.N; n++) {
            const a = n * GA;
            const r = config.scale * Math.sqrt(n);
            const x = cx + r * Math.cos(a);
            const y = cy + r * Math.sin(a);
            const hue = (config.hueBase + n * 0.5) % 360;

            ctx.fillStyle = `hsl(${hue} ${config.sat}% ${config.light}%)`;
            ctx.beginPath();
            ctx.arc(x, y, 1.2, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    updatePhyllotaxis(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Tie dot count to request rate
        animation.config.N = Math.min(2000, Math.floor(80 * metrics.requestRate));

        // Tie hue to success rate (greener when healthier)
        animation.config.hueBase = 120 * metrics.successRate + 10;

        this.renderPhyllotaxis(canvasId);
    }

    // 2) Fibonacci Spiral (overlay guide) — Canvas path
    createFibonacciSpiral(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d');
        this.fitCanvas(canvas);

        const config = {
            unit: 10,
            turns: 8,
            hue: 180,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderFibonacciSpiral(canvasId),
            update: (metrics) => this.updateFibonacciSpiral(canvasId, metrics)
        };

        this.renderFibonacciSpiral(canvasId);
        this.startAnimation(canvasId);
    }

    renderFibonacciSpiral(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = '#0b0b12';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const cx = canvas.width * 0.15;
        const cy = canvas.height * 0.75;

        this.drawFibSpiral(ctx, cx, cy, config.unit, config.turns, config.hue);
    }

    drawFibSpiral(ctx, cx, cy, unit = 10, turns = 8, hue = 180) {
        ctx.strokeStyle = `hsl(${hue} 60% 65% / 0.25)`;
        ctx.lineWidth = 1.5;

        let a = 1, b = 1;
        for (let i = 0; i < turns; i++) {
            const s = a;
            a = b;
            b += s;
        }

        ctx.beginPath();
        let x = cx, y = cy, r = unit;
        let angle = 0;

        for (let i = 0; i < turns; i++) {
            ctx.arc(x, y, r, angle, angle + Math.PI / 2);
            angle += Math.PI / 2;
            x += r * Math.cos(angle);
            y += r * Math.sin(angle);
            r *= 1.6180339887;
        }

        ctx.stroke();
    }

    updateFibonacciSpiral(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Toggle on during idle (low request rate)
        animation.active = metrics.requestRate < 5;

        if (animation.active) {
            this.renderFibonacciSpiral(canvasId);
        }
    }

    // 3) Mandelbrot / Julia set — WebGL shader
    createFractal(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.fitCanvas(canvas);

        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) return;

        const config = {
            zoom: 1.8,
            center: [-0.75, 0.0],
            mode: 0, // 0: Mandelbrot, 1: Julia
            jc: [-0.70176, -0.3842], // Julia constant
            enabled: true,
            ...options
        };

        this.initializeFractalShader(gl, canvasId, config);
    }

    initializeFractalShader(gl, canvasId, config) {
        const vertexShaderSource = `
            attribute vec2 p;
            void main() {
                gl_Position = vec4(p, 0.0, 1.0);
            }
        `;

        const fragmentShaderSource = `
            precision highp float;
            uniform vec2 res;
            uniform float t;
            uniform vec2 center;
            uniform float zoom;
            uniform int mode;
            uniform vec2 jc;

            vec3 pal(float x) {
                return vec3(0.5 + 0.5 * cos(6.28318 * (x + vec3(0.0, 0.33, 0.67))));
            }

            void main() {
                vec2 uv = (gl_FragCoord.xy - 0.5 * res) / res.y;
                vec2 c = center + uv * zoom;
                vec2 z = (mode == 0) ? vec2(0.0) : c;
                vec2 K = (mode == 0) ? c : jc;

                float i, m = 0.0;
                const int MAX = 128;

                for (int it = 0; it < MAX; it++) {
                    z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + K;
                    if (dot(z, z) > 4.0) {
                        i = float(it);
                        break;
                    }
                    m = float(it);
                }

                float n = i / float(MAX);
                vec3 col = pow(pal(n), vec3(0.9));
                gl_FragColor = vec4(col, 1.0);
            }
        `;

        const createShader = (type, source) => {
            const shader = gl.createShader(type);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            return shader;
        };

        const program = gl.createProgram();
        gl.attachShader(program, createShader(gl.VERTEX_SHADER, vertexShaderSource));
        gl.attachShader(program, createShader(gl.FRAGMENT_SHADER, fragmentShaderSource));
        gl.linkProgram(program);
        gl.useProgram(program);

        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);

        const positionLocation = gl.getAttribLocation(program, 'p');
        gl.enableVertexAttribArray(positionLocation);
        gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

        const uniforms = {
            res: gl.getUniformLocation(program, 'res'),
            t: gl.getUniformLocation(program, 't'),
            center: gl.getUniformLocation(program, 'center'),
            zoom: gl.getUniformLocation(program, 'zoom'),
            mode: gl.getUniformLocation(program, 'mode'),
            jc: gl.getUniformLocation(program, 'jc')
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            gl: gl,
            program: program,
            uniforms: uniforms,
            startTime: performance.now(),
            render: () => this.renderFractal(canvasId),
            update: (metrics) => this.updateFractal(canvasId, metrics)
        };

        this.renderFractal(canvasId);
        this.startAnimation(canvasId);
    }

    renderFractal(canvasId) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        const gl = animation.gl;
        const canvas = this.canvases[canvasId];
        const t = (performance.now() - animation.startTime) / 1000;

        gl.viewport(0, 0, canvas.width, canvas.height);
        gl.uniform2f(animation.uniforms.res, canvas.width, canvas.height);
        gl.uniform1f(animation.uniforms.t, t);
        gl.uniform2f(animation.uniforms.center, animation.config.center[0], animation.config.center[1]);
        gl.uniform1f(animation.uniforms.zoom, animation.config.zoom);
        gl.uniform1i(animation.uniforms.mode, animation.config.mode);
        gl.uniform2f(animation.uniforms.jc, animation.config.jc[0], animation.config.jc[1]);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    updateFractal(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Tie zoom to latency: higher p95 → zoom out slightly
        animation.config.zoom = 1.6 + Math.min(1.2, metrics.p95Latency * 40.0);

        // Flip to Julia set when Julia backend is active
        animation.config.mode = metrics.juliaActive ? 1 : 0;
    }

    // 4) Color Frequencies Palette (golden-angle walk)
    createColorFrequencies(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d');
        this.fitCanvas(canvas);

        const config = {
            count: 20,
            sat: 65,
            light: 55,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderColorFrequencies(canvasId),
            update: (metrics) => this.updateColorFrequencies(canvasId, metrics)
        };

        this.renderColorFrequencies(canvasId);
        this.startAnimation(canvasId);
    }

    renderColorFrequencies(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = '#0b0b12';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = canvas.width / config.count;

        for (let i = 0; i < config.count; i++) {
            const color = this.nextColor(i, config.sat, config.light);
            ctx.fillStyle = color;
            ctx.fillRect(i * barWidth, 0, barWidth, canvas.height);
        }
    }

    updateColorFrequencies(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Scale saturation by throughput
        animation.config.sat = Math.floor(65 * metrics.successRate);

        this.renderColorFrequencies(canvasId);
    }

    // Utility functions
    nextColor(i, s = 65, l = 55) {
        const hue = (i * 137.50776405) % 360;
        return `hsl(${hue} ${s}% ${l}%)`;
    }

    metricToHue(x, min = 0, max = 1) {
        const n = Math.max(0, Math.min(1, (x - min) / (max - min)));
        return 270 - 270 * n;
    }

    startAnimation(canvasId) {
        const animate = () => {
            const animation = this.animations[canvasId];
            if (animation && animation.active) {
                animation.render();
            }
            requestAnimationFrame(animate);
        };
        animate();
    }

    // Public API
    enableVisual(canvasId) {
        if (this.animations[canvasId]) {
            this.animations[canvasId].active = true;
        }
    }

    disableVisual(canvasId) {
        if (this.animations[canvasId]) {
            this.animations[canvasId].active = false;
        }
    }

    updateMetrics(metrics) {
        this.metrics = { ...this.metrics, ...metrics };
        this.updateVisuals();
    }
}

// Export for use in Code Live
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MathVisualsSystem;
} else {
    window.MathVisualsSystem = MathVisualsSystem;
}
