/**
 * Code Live Techno-Creative Visual FX System
 * Fibonacci Bloom, Fractals, Wave Interference, and Lolcat Strings
 */

class TechnoCreativeFX {
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

    // 1) Fibonacci Bloom Effect
    createFibonacciBloom(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d', { alpha: false });
        this.fitCanvas(canvas);

        const config = {
            intensity: 0.5,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderFibonacciBloom(canvasId),
            update: (metrics) => this.updateFibonacciBloom(canvasId, metrics)
        };

        this.renderFibonacciBloom(canvasId);
        this.startAnimation(canvasId);
    }

    renderFibonacciBloom(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = '#0b0b12';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const GA = Math.PI * (3 - Math.sqrt(5)); // golden angle

        // Tie dot count to request rate
        const N = Math.min(2000, Math.floor(80 * this.metrics.requestRate));
        // Tie hue to success rate
        const hueBase = 120 * this.metrics.successRate + 10;

        for (let n = 0; n < N; n++) {
            const a = n * GA;
            const r = 4.5 * Math.sqrt(n);
            const x = cx + r * Math.cos(a);
            const y = cy + r * Math.sin(a);
            const hue = (hueBase + n * 0.5) % 360;

            ctx.fillStyle = `hsl(${hue} 70% 55%)`;
            ctx.beginPath();
            ctx.arc(x, y, 1.2, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    updateFibonacciBloom(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Update based on metrics
        this.metrics = metrics;
        this.renderFibonacciBloom(canvasId);
    }

    // 2) Fractal Background
    createFractalBackground(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d');
        this.fitCanvas(canvas);

        const config = {
            zoom: 0.3,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderFractalBackground(canvasId),
            update: (metrics) => this.updateFractalBackground(canvasId, metrics)
        };

        this.renderFractalBackground(canvasId);
        this.startAnimation(canvasId);
    }

    renderFractalBackground(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = '#0b0b12';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const time = Date.now() * 0.001;
        const zoom = 1.6 + Math.min(1.2, this.metrics.p95Latency * 40.0);

        for (let x = 0; x < canvas.width; x += 4) {
            for (let y = 0; y < canvas.height; y += 4) {
                const nx = x / canvas.width;
                const ny = y / canvas.height;

                const value = Math.sin(nx * zoom * 10) * Math.cos(ny * zoom * 10) +
                             Math.sin(nx * zoom * 20 + time) * Math.cos(ny * zoom * 20 + time);

                if (value > 0.5) {
                    const hue = (nx * 360 + time * 50) % 360;
                    ctx.fillStyle = `hsl(${hue} 60% 40%)`;
                    ctx.fillRect(x, y, 4, 4);
                }
            }
        }
    }

    updateFractalBackground(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Update zoom based on latency
        animation.config.zoom = 1.6 + Math.min(1.2, metrics.p95Latency * 40.0);
        this.metrics = metrics;
    }

    // 3) Wave Interference
    createWaveInterference(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d');
        this.fitCanvas(canvas);

        const config = {
            density: 0.4,
            enabled: true,
            ...options
        };

        this.animations[canvasId] = {
            active: config.enabled,
            config: config,
            render: () => this.renderWaveInterference(canvasId),
            update: (metrics) => this.updateWaveInterference(canvasId, metrics)
        };

        this.renderWaveInterference(canvasId);
        this.startAnimation(canvasId);
    }

    renderWaveInterference(canvasId) {
        const canvas = this.canvases[canvasId];
        const ctx = this.contexts[canvasId];
        const config = this.animations[canvasId].config;

        if (!canvas || !ctx) return;

        ctx.fillStyle = 'rgba(11, 11, 18, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const time = Date.now() * 0.001;
        const amplitude = this.metrics.requestRate * 2;
        const frequency = this.metrics.p95Latency * 10;

        ctx.strokeStyle = `hsl(${time * 50 % 360} 70% 50%)`;
        ctx.lineWidth = 2;
        ctx.beginPath();

        for (let x = 0; x < canvas.width; x += 2) {
            const y = canvas.height / 2 +
                     Math.sin(x * frequency * 0.01 + time) * amplitude +
                     Math.sin(x * frequency * 0.02 + time * 1.5) * amplitude * 0.5;

            if (x === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }

        ctx.stroke();
    }

    updateWaveInterference(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Update wave parameters based on metrics
        this.metrics = metrics;
    }

    // 4) Color Frequencies
    createColorFrequencies(canvasId, options = {}) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        this.canvases[canvasId] = canvas;
        this.contexts[canvasId] = canvas.getContext('2d');
        this.fitCanvas(canvas);

        const config = {
            count: 20,
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
            const color = this.getBackendColor(i);
            ctx.fillStyle = color;
            ctx.fillRect(i * barWidth, 0, barWidth, canvas.height);
        }
    }

    updateColorFrequencies(canvasId, metrics) {
        const animation = this.animations[canvasId];
        if (!animation) return;

        // Update colors based on metrics
        this.metrics = metrics;
    }

    getBackendColor(index) {
        const backends = ['rust', 'ts', 'go', 'csharp', 'sql', 'julia'];
        const backend = backends[index % backends.length];

        // Map backends to wavelength-inspired hues
        const colorMap = {
            'rust': 'hsl(120, 70%, 50%)',    // ~500nm (green-blue, fast + efficient)
            'ts': 'hsl(200, 70%, 50%)',      // ~450nm (blue, fast)
            'go': 'hsl(60, 70%, 50%)',       // ~580nm (yellow, balanced)
            'csharp': 'hsl(300, 70%, 50%)',  // ~400nm (violet, .NET)
            'sql': 'hsl(0, 70%, 50%)',       // ~650nm (red-orange, slower, heavier)
            'julia': 'hsl(280, 70%, 50%)'    // ~400nm (violet, scientific)
        };

        return colorMap[backend] || 'hsl(180, 70%, 50%)';
    }

    // 5) Lolcat FX for Strings
    applyLolcatFX(text, intensity = 0.5) {
        if (intensity === 0) return text;

        let processedText = text;

        // Stretch effect
        if (intensity > 0.3) {
            processedText = processedText.replace(/([aeiou])/gi, '$1'.repeat(Math.floor(intensity * 3) + 1));
        }

        // Add emojis
        if (intensity > 0.5) {
            const emojis = ['😸', '🌈', '✨', '💥', '🎶', '🐾'];
            const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
            processedText += ` ${randomEmoji}`;
        }

        // Add random spacing
        if (intensity > 0.7) {
            processedText = processedText.split('').join(' '.repeat(Math.floor(intensity * 2)));
        }

        return processedText;
    }

    // 6) Glitch Effect
    triggerGlitch(duration = 120) {
        const glitchLayer = document.getElementById('glitchLayer');
        if (!glitchLayer) return;

        glitchLayer.classList.add('active');

        setTimeout(() => {
            glitchLayer.classList.remove('active');
        }, duration);
    }

    // 7) Spectrogram Panel
    createSpectrogram(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const config = {
            barCount: 64,
            enabled: true,
            ...options
        };

        // Create spectrogram bars
        for (let i = 0; i < config.barCount; i++) {
            const bar = document.createElement('div');
            bar.className = 'spectrogram-bar';
            bar.style.height = Math.random() * 100 + '%';
            container.appendChild(bar);
        }

        this.animations[containerId] = {
            active: config.enabled,
            config: config,
            update: (metrics) => this.updateSpectrogram(containerId, metrics)
        };
    }

    updateSpectrogram(containerId, metrics) {
        const bars = document.querySelectorAll(`#${containerId} .spectrogram-bar`);
        bars.forEach((bar, index) => {
            const height = Math.random() * 100;
            bar.style.height = height + '%';

            // Color based on performance
            if (height > 80) {
                bar.style.background = 'linear-gradient(to top, #ff0000, #ffaa00)';
            } else if (height > 50) {
                bar.style.background = 'linear-gradient(to top, #ffaa00, #ffff00)';
            } else {
                bar.style.background = 'linear-gradient(to top, #00ff00, #ffff00)';
            }
        });
    }

    // Utility functions
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

    setMode(mode) {
        switch (mode) {
            case 'performance':
                // Minimal visuals for ops dashboards
                Object.keys(this.animations).forEach(id => {
                    this.disableVisual(id);
                });
                break;
            case 'creative':
                // Unlock Fibonacci, fractals, lolcat strings
                this.enableVisual('fibonacciBloom');
                this.enableVisual('fractalBackground');
                this.enableVisual('colorFrequencies');
                break;
            case 'techno':
                // Full techno-creative experience
                Object.keys(this.animations).forEach(id => {
                    this.enableVisual(id);
                });
                break;
        }
    }
}

// Export for use in Code Live
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TechnoCreativeFX;
} else {
    window.TechnoCreativeFX = TechnoCreativeFX;
}
