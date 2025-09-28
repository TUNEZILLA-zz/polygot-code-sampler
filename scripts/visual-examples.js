/**
 * CodeSampler Live - Stunning Visual Examples
 * Copy and paste these into your CodeSampler Live sandbox!
 */

// ========================================
// 🌈 BEAT-REACTIVE RAINBOW WAVE
// ========================================
// Spawns colorful particles that dance to the beat
if (ENV.beat) {
  for (let i = 0; i < 100; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 300 + 100;
    const hue = (ENV.t * 50 + i * 3.6) % 360;
    window.spawnParticle(
      window.innerWidth / 2, 
      window.innerHeight / 2,
      Math.cos(angle) * speed, 
      Math.sin(angle) * speed,
      hue
    );
  }
}

// Bass-reactive background color
if (ENV.bands.bass > 0.3) {
  document.body.style.backgroundColor = 
    `hsl(${ENV.bands.bass * 360}, 70%, ${20 + ENV.bands.bass * 30}%)`;
}

// ========================================
// 🎵 BPM-SYNCED GEOMETRIC PATTERNS
// ========================================
// Creates rotating geometric shapes
const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvas.style.position = 'fixed';
canvas.style.top = '0';
canvas.style.left = '0';
canvas.style.pointerEvents = 'none';
canvas.style.zIndex = '1000';
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
const bpmSpeed = ENV.bpm / 60;
const time = ENV.t * bpmSpeed;

// Rotating hexagons
ctx.clearRect(0, 0, canvas.width, canvas.height);
ctx.save();
ctx.translate(canvas.width / 2, canvas.height / 2);
ctx.rotate(time * 0.5);

for (let i = 0; i < 6; i++) {
  const angle = (i / 6) * Math.PI * 2;
  const radius = 100 + Math.sin(time + i) * 50;
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;
  
  ctx.fillStyle = `hsla(${i * 60}, 80%, 60%, 0.7)`;
  ctx.beginPath();
  ctx.arc(x, y, 20 + Math.sin(time * 2 + i) * 10, 0, Math.PI * 2);
  ctx.fill();
}
ctx.restore();

// ========================================
// 🌊 AUDIO-REACTIVE WAVE FIELD
// ========================================
// Creates flowing wave patterns based on audio
const waveCanvas = document.createElement('canvas');
waveCanvas.width = window.innerWidth;
waveCanvas.height = window.innerHeight;
waveCanvas.style.position = 'fixed';
waveCanvas.style.top = '0';
waveCanvas.style.left = '0';
waveCanvas.style.pointerEvents = 'none';
waveCanvas.style.zIndex = '999';
document.body.appendChild(waveCanvas);

const waveCtx = waveCanvas.getContext('2d');
const bassLevel = ENV.bands.bass;
const midLevel = ENV.bands.mid;

waveCtx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
waveCtx.strokeStyle = `hsla(${bassLevel * 360}, 70%, 60%, 0.8)`;
waveCtx.lineWidth = 2 + bassLevel * 5;

waveCtx.beginPath();
for (let x = 0; x < waveCanvas.width; x += 5) {
  const y = waveCanvas.height / 2 + 
    Math.sin(x * 0.01 + ENV.t * 2) * 50 * bassLevel +
    Math.sin(x * 0.03 + ENV.t * 3) * 30 * midLevel;
  
  if (x === 0) {
    waveCtx.moveTo(x, y);
  } else {
    waveCtx.lineTo(x, y);
  }
}
waveCtx.stroke();

// ========================================
// ⚡ BEAT-DRIVEN LIGHTNING STRIKES
// ========================================
// Creates dramatic lightning effects on beat
if (ENV.beat && ENV.bands.bass > 0.5) {
  const lightning = document.createElement('div');
  lightning.style.position = 'fixed';
  lightning.style.top = '0';
  lightning.style.left = '0';
  lightning.style.width = '100%';
  lightning.style.height = '100%';
  lightning.style.background = 'linear-gradient(45deg, transparent 30%, white 50%, transparent 70%)';
  lightning.style.pointerEvents = 'none';
  lightning.style.zIndex = '2000';
  lightning.style.opacity = '0.8';
  document.body.appendChild(lightning);
  
  setTimeout(() => {
    document.body.removeChild(lightning);
  }, 100);
}

// ========================================
// 🎨 FREQUENCY-SPECTRUM VISUALIZER
// ========================================
// Creates a real-time frequency spectrum display
const spectrumCanvas = document.createElement('canvas');
spectrumCanvas.width = 400;
spectrumCanvas.height = 200;
spectrumCanvas.style.position = 'fixed';
spectrumCanvas.style.top = '20px';
spectrumCanvas.style.right = '20px';
spectrumCanvas.style.border = '2px solid rgba(255,255,255,0.3)';
spectrumCanvas.style.borderRadius = '10px';
spectrumCanvas.style.zIndex = '1500';
document.body.appendChild(spectrumCanvas);

const specCtx = spectrumCanvas.getContext('2d');
const barCount = 32;
const barWidth = spectrumCanvas.width / barCount;

specCtx.clearRect(0, 0, spectrumCanvas.width, spectrumCanvas.height);

for (let i = 0; i < barCount; i++) {
  const height = (ENV.bands.bass + ENV.bands.low + ENV.bands.mid + ENV.bands.high) * 
    Math.sin(i * 0.2 + ENV.t * 3) * 100;
  
  const hue = (i / barCount) * 360;
  specCtx.fillStyle = `hsl(${hue}, 80%, 60%)`;
  specCtx.fillRect(i * barWidth, spectrumCanvas.height - height, barWidth - 2, height);
}

// ========================================
// 🌟 PARTICLE TRAIL SYSTEM
// ========================================
// Creates beautiful particle trails that follow mouse
let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

// Spawn particles that follow mouse with audio reactivity
if (ENV.bands.mid > 0.2) {
  for (let i = 0; i < 5; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 100 + 50;
    const hue = (ENV.t * 100 + i * 72) % 360;
    
    window.spawnParticle(
      mouseX + (Math.random() - 0.5) * 20,
      mouseY + (Math.random() - 0.5) * 20,
      Math.cos(angle) * speed * ENV.bands.mid,
      Math.sin(angle) * speed * ENV.bands.mid,
      hue
    );
  }
}

// ========================================
// 🎭 PERFORMANCE STATUS DISPLAY
// ========================================
// Shows real-time performance data
const statusDiv = document.createElement('div');
statusDiv.style.position = 'fixed';
statusDiv.style.bottom = '20px';
statusDiv.style.left = '20px';
statusDiv.style.background = 'rgba(0,0,0,0.8)';
statusDiv.style.color = 'white';
statusDiv.style.padding = '10px';
statusDiv.style.borderRadius = '5px';
statusDiv.style.fontFamily = 'monospace';
statusDiv.style.zIndex = '3000';
document.body.appendChild(statusDiv);

statusDiv.innerHTML = `
  <div>🎵 BPM: ${Math.round(ENV.bpm)}</div>
  <div>🥁 Beat: ${ENV.beat ? 'YES' : 'NO'}</div>
  <div>🔊 Bass: ${(ENV.bands.bass * 100).toFixed(1)}%</div>
  <div>🎶 Mid: ${(ENV.bands.mid * 100).toFixed(1)}%</div>
  <div>🎵 High: ${(ENV.bands.high * 100).toFixed(1)}%</div>
  <div>⏰ Time: ${ENV.t.toFixed(1)}s</div>
`;

// ========================================
// 🌈 COLOR-SHIFTING BACKGROUND
// ========================================
// Creates a mesmerizing color-shifting background
const bgHue = (ENV.t * 30 + ENV.bands.bass * 180) % 360;
const bgSaturation = 70 + ENV.bands.mid * 30;
const bgLightness = 20 + ENV.bands.high * 40;

document.body.style.background = 
  `linear-gradient(45deg, 
    hsl(${bgHue}, ${bgSaturation}%, ${bgLightness}%), 
    hsl(${(bgHue + 60) % 360}, ${bgSaturation}%, ${bgLightness + 20}%),
    hsl(${(bgHue + 120) % 360}, ${bgSaturation}%, ${bgLightness + 10}%)`;

// ========================================
// 🎪 RETURN PERFORMANCE DATA
// ========================================
// Return data for the sandbox display
return {
  time: new Date().toLocaleTimeString(),
  bpm: Math.round(ENV.bpm),
  beat: ENV.beat,
  bass: Number(ENV.bands.bass.toFixed(3)),
  mid: Number(ENV.bands.mid.toFixed(3)),
  high: Number(ENV.bands.high.toFixed(3)),
  performance: "🎭 STUNNING VISUALS ACTIVE! 🎭"
};
