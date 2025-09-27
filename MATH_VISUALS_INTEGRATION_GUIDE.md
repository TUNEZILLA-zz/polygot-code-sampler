# 🎛️ Code Live Mathematical Visuals Integration Guide

## 🌈 **Fibonacci, Color Frequencies, and Fractals for Tasteful Mathy Visuals**

This guide shows exactly how to integrate mathematical visual effects into Code Live that are both beautiful and performant, with live metrics integration that makes them meaningful.

---

## 🎯 **Mathematical Visual Effects Overview**

### **Core Philosophy: Tasteful, Mathy Visuals That Still Feel Performant**
- **Phyllotaxis**: Fibonacci flower patterns tied to request rate and success rate
- **Fibonacci Spiral**: Overlay guide that screams "order" during idle
- **Mandelbrot/Julia Set**: GPU-smooth fractal backgrounds tied to latency
- **Color Frequencies**: Golden-angle walk palette for spectral coloring

### **Performance & Accessibility Guardrails**
- **Respect prefers-reduced-motion**: Swap shaders for static gradient
- **Visual Quality toggle**: Off (CSS) / Balanced (Canvas) / High (WebGL)
- **Cap Canvas loop at 60fps**: Drop to ~30fps if queue_depth > 80
- **GPU-accelerated effects**: Use WebGL for smooth fractal rendering

---

## 🌻 **1. Phyllotaxis (Fibonacci Flower) — Canvas**

### **Why**: Dense, elegant, cheap to render
### **How**: Tie dot count to request rate; hue to success rate

```html
<canvas id="phylo" style="width:100%;height:220px"></canvas>
<script>
const C = document.getElementById('phylo');
const ctx = C.getContext('2d', { alpha: false });
function fit() { C.width = C.clientWidth; C.height = C.clientHeight; } fit();
addEventListener('resize', fit);

// golden angle (radians)
const GA = Math.PI * (3 - Math.sqrt(5));

function renderPhylo({N=1000, sat=70, light=55, scale=5, hueBase=200}={}) {
  ctx.fillStyle = '#0b0b12'; ctx.fillRect(0,0,C.width,C.height);
  const cx = C.width/2, cy = C.height/2;
  for (let n=0; n<N; n++) {
    const a = n * GA;
    const r = scale * Math.sqrt(n);
    const x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
    const hue = (hueBase + n*0.5) % 360;
    ctx.fillStyle = `hsl(${hue} ${sat}% ${light}%)`;
    ctx.beginPath(); ctx.arc(x,y, 1.2, 0, Math.PI*2); ctx.fill();
  }
}

// hook to live metrics:
function updateFromMetrics({reqRate=12, success=0.86}) {
  const N = Math.min(2000, Math.floor(80 * reqRate));
  const hueBase = 120*success + 10; // greener when healthier
  renderPhylo({N, hueBase, scale: 4.5});
}
updateFromMetrics({});
</script>
```

### **Integration with Code Live Metrics**
```javascript
// In your Code Live performance monitoring
function updatePhyllotaxis(metrics) {
    const N = Math.min(2000, Math.floor(80 * metrics.requestRate));
    const hueBase = 120 * metrics.successRate + 10; // greener when healthier
    renderPhylo({N, hueBase, scale: 4.5});
}

// Call this whenever metrics update
updatePhyllotaxis({
    requestRate: 12.4,
    successRate: 0.858
});
```

---

## 🌀 **2. Fibonacci Spiral (Overlay Guide) — Canvas Path**

### **Why**: Subtle, low-poly overlay that screams "order"
### **How**: Toggle on during idle

```javascript
function drawFibSpiral(ctx, cx, cy, unit=10, turns=8, hue=180) {
  ctx.strokeStyle = `hsl(${hue} 60% 65% / .25)`; ctx.lineWidth = 1.5;
  let a=1, b=1;
  for (let i=0; i<turns; i++){ const s=a; a=b; b+=s; }
  ctx.beginPath();
  let x=cx, y=cy, r=unit; let angle=0;
  for (let i=0; i<turns; i++) {
    ctx.arc(x, y, r, angle, angle + Math.PI/2);
    angle += Math.PI/2;
    x += r * Math.cos(angle); y += r * Math.sin(angle); r *= 1.6180339887;
  }
  ctx.stroke();
}

// Call after phyllotaxis to add tasteful guide
drawFibSpiral(ctx, C.width*0.15, C.height*0.75, 6, 9);
```

### **Integration with Code Live Metrics**
```javascript
// Show spiral during idle periods
function updateFibonacciSpiral(metrics) {
    if (metrics.requestRate < 5) {
        // Show spiral during idle
        drawFibSpiral(ctx, canvas.width*0.15, canvas.height*0.75, 6, 9);
    }
}
```

---

## 🌀 **3. Mandelbrot / Julia Set — WebGL Shader**

### **Why**: GPU-smooth, mesmerizing idle background
### **How**: Tie zoom to latency p95; flip to Julia set when Julia backend is active

```html
<canvas id="fract" style="width:100%;height:240px;display:block"></canvas>
<script>
const cv = document.getElementById('fract');
const gl = cv.getContext('webgl');
function fit(){cv.width=cv.clientWidth;cv.height=cv.clientHeight;}
fit(); addEventListener('resize', fit);

const vs = `attribute vec2 p; void main(){ gl_Position=vec4(p,0.,1.); }`;
const fs = `
precision highp float;
uniform vec2 res; uniform float t; uniform vec2 center; uniform float zoom;
uniform int mode; uniform vec2 jc; // julia constant
vec3 pal(float x){ return vec3(.5+.5*cos(6.28318*(x+vec3(0.,.33,.67))));}
void main(){
  vec2 uv = (gl_FragCoord.xy - .5*res)/res.y;
  vec2 c = center + uv*zoom;
  vec2 z = (mode==0)? vec2(0.0): c; // 0: Mandelbrot, 1: Julia
  vec2 K = (mode==0)? c: jc;
  float i, m=0.0; const int MAX=128;
  for(int it=0; it<MAX; it++){
    z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + K;
    if(dot(z,z)>4.0){ i=float(it); break; }
    m = float(it);
  }
  float n = i/float(MAX);
  vec3 col = pow(pal(n), vec3(0.9));
  gl_FragColor = vec4(col,1.0);
}`;

function sh(type, src){ const s=gl.createShader(type); gl.shaderSource(s,src); gl.compileShader(s); return s; }
const prog = gl.createProgram();
gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs));
gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
gl.linkProgram(prog); gl.useProgram(prog);

const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
const loc = gl.getAttribLocation(prog,'p'); gl.enableVertexAttribArray(loc);
gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);

const U = {
  res: gl.getUniformLocation(prog,'res'),
  t: gl.getUniformLocation(prog,'t'),
  center: gl.getUniformLocation(prog,'center'),
  zoom: gl.getUniformLocation(prog,'zoom'),
  mode: gl.getUniformLocation(prog,'mode'),
  jc: gl.getUniformLocation(prog,'jc'),
};

let t0=performance.now(), center=[-0.75,0.0], zoom=1.8, mode=0, jc=[-0.70176, -0.3842];
function tick(p95=0.012, juliaActive=false){
  const t = (performance.now()-t0)/1000;
  gl.viewport(0,0,cv.width,cv.height);
  gl.uniform2f(U.res, cv.width, cv.height);
  gl.uniform1f(U.t,t);
  gl.uniform2f(U.center, center[0], center[1]);
  gl.uniform1f(U.zoom, zoom);
  gl.uniform1i(U.mode, juliaActive?1:0);
  gl.uniform2f(U.jc, jc[0], jc[1]);
  gl.drawArrays(gl.TRIANGLE_STRIP,0,4);
  // tie zoom to latency: higher p95 → zoom out slightly
  zoom = 1.6 + Math.min(1.2, p95*40.0);
  requestAnimationFrame(()=>tick(p95, juliaActive));
}
tick();
</script>
```

### **Integration with Code Live Metrics**
```javascript
// Call tick(currentP95, juliaActive) from your stats loop
function updateFractal(metrics) {
    const p95 = metrics.p95Latency;
    const juliaActive = metrics.juliaActive;

    // Update zoom based on latency
    zoom = 1.6 + Math.min(1.2, p95 * 40.0);

    // Switch to Julia set when Julia backend is active
    mode = juliaActive ? 1 : 0;

    tick(p95, juliaActive);
}
```

---

## 🌈 **4. Color Frequencies Palette (Golden-Angle Walk)**

### **Why**: Pleasant, evenly spaced palette generator that feels spectral
### **How**: Use it to color backends, dots, or bars

```javascript
// golden-angle step on hue; s/l are gentle for readability
function nextColor(i, s=65, l=55) {
  const hue = (i * 137.50776405) % 360;
  return `hsl(${hue} ${s}% ${l}%)`;
}

// map a metric to wavelength-ish hue (rough metaphor)
function metricToHue(x, min=0, max=1){
  const n = Math.max(0, Math.min(1, (x-min)/(max-min)));
  // 420nm (violet) → 650nm (red) mapped to 270→0 hue
  return 270 - 270*n;
}

// Use nextColor(i) to assign stable, "spectral" colors across series
// Use metricToHue(p95, 0.005, 0.120) to tint by latency
```

### **Integration with Code Live Metrics**
```javascript
// Color backends with spectral colors
function updateBackendColors(metrics) {
    const backends = ['rust', 'ts', 'go', 'csharp', 'sql', 'julia'];

    backends.forEach((backend, index) => {
        const color = nextColor(index);
        const element = document.querySelector(`[data-backend="${backend}"]`);
        if (element) {
            element.style.color = color;
        }
    });
}

// Tint by latency
function updateLatencyTint(metrics) {
    const hue = metricToHue(metrics.p95Latency, 0.005, 0.120);
    document.documentElement.style.setProperty('--latency-tint', `hsl(${hue} 70% 50%)`);
}
```

---

## 🎛️ **How to Wire Them to Your Environment**

### **Phyllotaxis Integration**
```javascript
// N ← request_rate, hueBase ← success_rate
function updatePhyllotaxis(metrics) {
    const N = Math.min(2000, Math.floor(80 * metrics.requestRate));
    const hueBase = 120 * metrics.successRate + 10; // greener when healthier
    renderPhylo({N, hueBase, scale: 4.5});
}
```

### **Fractal Integration**
```javascript
// zoom ← p95_latency, mode ← juliaActive
function updateFractal(metrics) {
    const zoom = 1.6 + Math.min(1.2, metrics.p95Latency * 40.0);
    const mode = metrics.juliaActive ? 1 : 0;
    // Update fractal parameters
}
```

### **Palette Integration**
```javascript
// hue per backend ← nextColor(index), with saturation scaled by throughput
function updateBackendPalette(metrics) {
    const backends = ['rust', 'ts', 'go', 'csharp', 'sql', 'julia'];

    backends.forEach((backend, index) => {
        const color = nextColor(index);
        const saturation = Math.floor(65 * metrics.successRate);
        const element = document.querySelector(`[data-backend="${backend}"]`);
        if (element) {
            element.style.color = color;
            element.style.filter = `saturate(${saturation}%)`;
        }
    });
}
```

### **Glitch Hint Integration**
```javascript
// briefly add CSS filter on the panel that fell back
function showGlitchHint(panelId) {
    const panel = document.getElementById(panelId);
    if (panel) {
        panel.style.filter = 'contrast(105%) saturate(120%) hue-rotate(2deg)';
        setTimeout(() => {
            panel.style.filter = '';
        }, 120);
    }
}
```

---

## 🚀 **Performance Switches**

### **Respect prefers-reduced-motion**
```javascript
// Swap shaders for static gradient
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Disable animations, use static gradients
    document.body.classList.add('reduced-motion');
}
```

### **Visual Quality Toggle**
```javascript
// Off (CSS) / Balanced (Canvas) / High (WebGL)
function setVisualQuality(quality) {
    switch (quality) {
        case 'off':
            // Disable all visual effects
            document.body.classList.add('visual-quality-off');
            break;
        case 'balanced':
            // Enable Canvas effects only
            document.body.classList.add('visual-quality-balanced');
            break;
        case 'high':
            // Enable all effects including WebGL
            document.body.classList.add('visual-quality-high');
            break;
    }
}
```

### **Frame Rate Management**
```javascript
// Cap Canvas loop at 60fps; if queue_depth > 80, drop to ~30fps
function manageFrameRate(metrics) {
    const targetFPS = metrics.queueDepth > 80 ? 30 : 60;
    const frameInterval = 1000 / targetFPS;

    // Adjust animation intervals based on queue depth
    if (metrics.queueDepth > 80) {
        // Reduce animation frequency
        clearInterval(this.animationInterval);
        this.animationInterval = setInterval(this.animate, frameInterval);
    }
}
```

---

## 🎯 **Integration Examples**

### **Complete Code Live Integration**
```javascript
class CodeLiveMathVisuals {
    constructor() {
        this.metrics = {
            requestRate: 12.4,
            successRate: 0.858,
            p95Latency: 0.045,
            juliaActive: false,
            queueDepth: 3
        };

        this.initializeVisuals();
        this.startMetricsMonitoring();
    }

    initializeVisuals() {
        // Initialize all visual effects
        this.createPhyllotaxis('phylo-canvas');
        this.createFibonacciSpiral('spiral-canvas');
        this.createFractal('fractal-canvas');
        this.createColorFrequencies('color-canvas');
    }

    startMetricsMonitoring() {
        setInterval(() => {
            // Update metrics from Code Live
            this.updateMetrics();

            // Update all visuals
            this.updatePhyllotaxis();
            this.updateFibonacciSpiral();
            this.updateFractal();
            this.updateColorFrequencies();
        }, 1000);
    }

    updateMetrics() {
        // Get real metrics from Code Live
        this.metrics = {
            requestRate: this.getRequestRate(),
            successRate: this.getSuccessRate(),
            p95Latency: this.getP95Latency(),
            juliaActive: this.isJuliaActive(),
            queueDepth: this.getQueueDepth()
        };
    }

    updatePhyllotaxis() {
        const N = Math.min(2000, Math.floor(80 * this.metrics.requestRate));
        const hueBase = 120 * this.metrics.successRate + 10;
        this.renderPhyllotaxis({N, hueBase, scale: 4.5});
    }

    updateFibonacciSpiral() {
        if (this.metrics.requestRate < 5) {
            this.showFibonacciSpiral();
        } else {
            this.hideFibonacciSpiral();
        }
    }

    updateFractal() {
        const zoom = 1.6 + Math.min(1.2, this.metrics.p95Latency * 40.0);
        const mode = this.metrics.juliaActive ? 1 : 0;
        this.updateFractalParams({zoom, mode});
    }

    updateColorFrequencies() {
        const backends = ['rust', 'ts', 'go', 'csharp', 'sql', 'julia'];
        backends.forEach((backend, index) => {
            const color = this.nextColor(index);
            const saturation = Math.floor(65 * this.metrics.successRate);
            this.updateBackendColor(backend, color, saturation);
        });
    }
}
```

---

## 🎉 **Expected Benefits**

### **For Developers**
- **Visual Feedback**: See performance metrics in beautiful mathematical forms
- **Professional Feel**: Tasteful, mathy visuals that don't distract
- **Performance Awareness**: Real-time visual representation of system health
- **Engagement**: More fun and interactive experience

### **For Users**
- **Visual Appeal**: Beautiful, engaging mathematical patterns
- **Performance Understanding**: See system health through visual metaphors
- **Customization**: Choose visual quality and effects
- **Accessibility**: Respects user preferences and performance

### **For Code Live**
- **Differentiation**: Unique mathematical visual identity
- **Professional Quality**: Production-ready visual effects
- **Scalability**: Performance-adaptive effects
- **Accessibility**: Inclusive design principles

---

## 🎛️ **The Result: Tasteful, Mathy Visuals**

**Code Live becomes the ultimate mathematical visual experience where:**
- **Phyllotaxis** = Fibonacci flower patterns tied to request rate and success rate
- **Fibonacci Spiral** = Overlay guide that screams "order" during idle
- **Mandelbrot/Julia Set** = GPU-smooth fractal backgrounds tied to latency
- **Color Frequencies** = Golden-angle walk palette for spectral coloring

**This creates the perfect balance between mathematical beauty and real-time performance metrics - just like having tasteful, mathy visuals that still feel performant!**

**Code Live becomes the "Mathematical Visual Environment" where developers work in a beautiful, performance-aware, and mathematically inspired visual space!** 🎛️✨🌈

---

*The Mathematical Visual Effects System - where developers work in a beautiful, performance-aware environment that enhances the experience with tasteful, mathy visuals that still feel performant!* 🎛️🌈💥
