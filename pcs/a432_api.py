#!/usr/bin/env python3
"""
🎵 Code Live - A=432 Hz Fantasy Mode API
========================================

FastAPI integration for the 432 Hz fantasy mode easter egg.
Provides audio generation, theme switching, and microtuning features.
"""

import io
import math
import struct
import wave
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class A432Request(BaseModel):
    """Request model for 432 Hz audio generation"""
    seconds: float = 2.5
    gain: float = 0.05
    chorus: bool = True
    detune_hz: float = 1.2
    sample_rate: int = 48000


class A432Response(BaseModel):
    """Response model for 432 Hz audio generation"""
    success: bool
    message: str
    audio_url: Optional[str] = None
    duration: Optional[float] = None


class MicrotuningRequest(BaseModel):
    """Request model for microtuning"""
    queue_depth: float = 50.0  # 0-100
    base_frequency: float = 432.0
    cents_range: float = 40.0  # ±40 cents


class MicrotuningResponse(BaseModel):
    """Response model for microtuning"""
    tuned_frequency: float
    cents_offset: float
    queue_depth: float


# FastAPI app
app = FastAPI(
    title="🎵 Code Live - A=432 Hz Fantasy Mode",
    description="A playful easter egg inspired by the 432 Hz lore - use for atmosphere, not as guaranteed medicinal tuning!",
    version="1.0.0"
)

# Cache for generated audio files
audio_cache: Dict[str, bytes] = {}


def cents_to_ratio(cents: float) -> float:
    """Convert cents to frequency ratio"""
    return math.pow(2, cents / 1200)


def generate_432_audio(
    seconds: float = 2.5,
    sample_rate: int = 48000,
    gain: float = 0.05,
    chorus: bool = True,
    detune_hz: float = 1.2,
) -> bytes:
    """Generate 432 Hz audio as WAV bytes"""
    frames = []
    
    for n in range(int(seconds * sample_rate)):
        t = n / sample_rate
        
        # Base 432 Hz sine wave
        y = math.sin(2 * math.pi * 432 * t)
        
        # Optional gentle chorus (detuned copy)
        if chorus:
            y += 0.6 * math.sin(2 * math.pi * (432 + detune_hz) * t)
        
        # ADSR envelope (avoid clicks, keep quiet)
        a, d, s, r = 0.05, 0.3, 0.6, 0.4
        if t < a:
            env = t / a
        elif t < a + d:
            env = 1 - (1 - s) * ((t - a) / d)
        elif t > seconds - r:
            env = max(0.0, (seconds - t) / r)
        else:
            env = s
        
        # Apply envelope and gain
        z = max(-1.0, min(1.0, y * env * gain))
        frames.append(struct.pack('<h', int(z * 32767)))
    
    # Create WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(b''.join(frames))
    
    return wav_buffer.getvalue()


def calculate_microtuning(
    queue_depth: float,
    base_frequency: float = 432.0,
    cents_range: float = 40.0,
) -> tuple[float, float]:
    """Calculate microtuned frequency based on queue depth"""
    # Map queue depth (0-100) to cents offset (-cents_range/2 to +cents_range/2)
    cents_offset = (queue_depth - 50) * (cents_range / 50)
    tuned_frequency = base_frequency * cents_to_ratio(cents_offset)
    return tuned_frequency, cents_offset


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the 432 Hz fantasy mode interface"""
    html_path = Path("site/a432-egg.html")
    if html_path.exists():
        return FileResponse(html_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>🎵 A=432 Hz Fantasy Mode</title></head>
            <body>
                <h1>🎵 A=432 Hz Fantasy Mode</h1>
                <p>A playful easter egg inspired by the 432 Hz lore</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)


@app.get("/a432/audio")
async def get_432_audio(
    seconds: float = Query(2.5, ge=0.1, le=10.0, description="Duration in seconds"),
    gain: float = Query(0.05, ge=0.0, le=0.2, description="Audio gain (0.0-1.0)"),
    chorus: bool = Query(True, description="Enable chorus effect"),
    detune_hz: float = Query(1.2, ge=0.0, le=5.0, description="Chorus detune in Hz"),
    sample_rate: int = Query(48000, ge=22050, le=96000, description="Sample rate"),
):
    """Generate and return 432 Hz audio as WAV file"""
    try:
        # Create cache key
        cache_key = f"a432_{seconds}_{gain}_{chorus}_{detune_hz}_{sample_rate}"
        
        # Check cache
        if cache_key not in audio_cache:
            audio_cache[cache_key] = generate_432_audio(
                seconds=seconds,
                sample_rate=sample_rate,
                gain=gain,
                chorus=chorus,
                detune_hz=detune_hz,
            )
        
        # Return WAV file
        return FileResponse(
            io.BytesIO(audio_cache[cache_key]),
            media_type="audio/wav",
            filename=f"a432_fantasy_{seconds}s.wav",
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating 432 Hz audio: {e}")


@app.post("/a432/audio", response_model=A432Response)
async def generate_432_audio_endpoint(request: A432Request):
    """Generate 432 Hz audio with custom parameters"""
    try:
        # Create cache key
        cache_key = f"a432_{request.seconds}_{request.gain}_{request.chorus}_{request.detune_hz}_{request.sample_rate}"
        
        # Check cache
        if cache_key not in audio_cache:
            audio_cache[cache_key] = generate_432_audio(
                seconds=request.seconds,
                sample_rate=request.sample_rate,
                gain=request.gain,
                chorus=request.chorus,
                detune_hz=request.detune_hz,
            )
        
        return A432Response(
            success=True,
            message=f"Generated 432 Hz audio ({request.seconds}s)",
            audio_url=f"/a432/audio?seconds={request.seconds}&gain={request.gain}&chorus={request.chorus}",
            duration=request.seconds,
        )
        
    except Exception as e:
        return A432Response(
            success=False,
            message=f"Error generating 432 Hz audio: {e}",
        )


@app.post("/a432/microtuning", response_model=MicrotuningResponse)
async def calculate_microtuning_endpoint(request: MicrotuningRequest):
    """Calculate microtuned frequency based on queue depth"""
    try:
        tuned_freq, cents_offset = calculate_microtuning(
            queue_depth=request.queue_depth,
            base_frequency=request.base_frequency,
            cents_range=request.cents_range,
        )
        
        return MicrotuningResponse(
            tuned_frequency=tuned_freq,
            cents_offset=cents_offset,
            queue_depth=request.queue_depth,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating microtuning: {e}")


@app.get("/a432/theme")
async def get_432_theme():
    """Get 432 Hz fantasy mode CSS theme"""
    theme_css = """
/* 🎵 A=432 Hz Fantasy Mode Theme */
.theme-a432 {
    --fx-primary: #4b6cff;   /* indigo */
    --fx-accent: #2dd4bf;    /* teal */
    --fx-secondary: #8b5cf6; /* purple */
    --fx-background: #0f172a; /* dark slate */
    --fx-text: #e2e8f0;      /* light gray */
    
    /* Breathing animation derived from 432 Hz */
    --breath-tempo: 108;     /* 432/4 = 108 BPM */
    --breath-duration: 2.22s; /* 60/108 * 4 = 2.22s */
}

.theme-a432 .fx-particle {
    animation: a432-breathe var(--breath-duration) ease-in-out infinite;
}

.theme-a432 .fx-background {
    background: linear-gradient(45deg, 
        var(--fx-primary) 0%, 
        var(--fx-accent) 50%, 
        var(--fx-secondary) 100%);
    opacity: 0.1;
}

@keyframes a432-breathe {
    0%, 100% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1.0; }
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    .theme-a432 .fx-particle {
        animation: none;
    }
}
"""
    
    return {"css": theme_css}


@app.get("/a432/webaudio")
async def get_432_webaudio():
    """Get 432 Hz WebAudio JavaScript"""
    webaudio_js = """
// 🎵 A=432 Hz Fantasy Mode - WebAudio Easter Egg
(function() {
    'use strict';
    
    // Check for 432 Hz mode activation
    const params = new URLSearchParams(location.search);
    const is432Mode = params.get('a432') === '1' || params.get('pitch') === '432';
    
    if (!is432Mode) return;
    
    // Apply 432 Hz theme
    function apply432Theme() {
        const style = document.createElement('style');
        style.textContent = `""" + theme_css.replace('`', '\\`') + """`;
        document.head.appendChild(style);
        document.body.classList.add('theme-a432');
        
        // Add subtle visual indicator
        const indicator = document.createElement('div');
        indicator.innerHTML = '🎵 A=432 Hz Fantasy Mode';
        indicator.style.cssText = `
            position: fixed; top: 10px; right: 10px; z-index: 1000;
            background: rgba(75, 108, 255, 0.9); color: white;
            padding: 8px 12px; border-radius: 20px; font-size: 12px;
            font-family: monospace; pointer-events: none;
        `;
        document.body.appendChild(indicator);
    }
    
    // Generate 432 Hz tone with WebAudio
    function play432Hz(options = {}) {
        const { seconds = 3, gain = 0.08, chorus = false } = options;
        
        try {
            const AC = window.AudioContext || window.webkitAudioContext;
            const ctx = new AC();
            const now = ctx.currentTime;
            
            // Master gain with soft ADSR
            const master = ctx.createGain();
            master.gain.value = 0;
            master.connect(ctx.destination);
            
            const osc = ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = 432; // A4 = 432 Hz
            osc.connect(master);
            
            // Optional gentle chorus
            let lfoNode;
            if (chorus) {
                const lfo = ctx.createOscillator();
                const lfoGain = ctx.createGain();
                lfo.frequency.value = 0.2;       // slow wow
                lfoGain.gain.value = 1.5;        // ~±1.5 Hz
                lfo.connect(lfoGain);
                lfoGain.connect(osc.frequency);
                lfo.start();
                lfoNode = lfo;
            }
            
            // ADSR envelope (avoid clicks, keep quiet by default)
            const a = 0.08, d = 0.3, s = 0.5, r = 0.8;
            master.gain.linearRampToValueAtTime(gain, now + a);
            master.gain.linearRampToValueAtTime(gain * s, now + a + d);
            master.gain.setTargetAtTime(0, now + Math.max(0.2, seconds - r), 0.25);
            
            osc.start();
            osc.stop(now + seconds + 0.2);
            
            osc.onended = () => { 
                lfoNode?.stop?.(); 
                ctx.close(); 
            };
            
        } catch (error) {
            console.log('432 Hz audio not available:', error);
        }
    }
    
    // Microtuning based on metrics
    function getTunedFrequency(queueDepth = 50) {
        const cents = (Math.min(100, queueDepth) - 50) * (40 / 50); // ±40 cents span
        return 432 * Math.pow(2, cents / 1200);
    }
    
    // Initialize 432 Hz mode
    function init432Mode() {
        apply432Theme();
        
        // Respect reduced motion & user gesture policies
        if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            // Start on first user gesture to satisfy autoplay policies
            const once = () => { 
                play432Hz({ chorus: true }); 
                window.removeEventListener('click', once); 
            };
            window.addEventListener('click', once, { once: true });
        }
        
        // Log activation for telemetry
        if (window.gtag) {
            window.gtag('event', 'easter_egg_activated', {
                'event_category': 'a432',
                'event_label': 'fantasy_mode'
            });
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init432Mode);
    } else {
        init432Mode();
    }
})();
"""
    
    return {"javascript": webaudio_js}


@app.get("/a432/info")
async def get_432_info():
    """Get information about 432 Hz fantasy mode"""
    return {
        "name": "A=432 Hz Fantasy Mode",
        "description": "A playful easter egg inspired by the 432 Hz lore",
        "disclaimer": "Use for atmosphere, not as guaranteed medicinal tuning!",
        "features": [
            "Gentle A=432 Hz tone with optional chorus",
            "Indigo/teal theme with breathing animations",
            "Microtuning based on queue depth metrics",
            "WebAudio integration with user gesture respect",
            "CSS theme switching",
            "FastAPI audio generation"
        ],
        "activation": [
            "URL parameter: ?a432=1 or ?pitch=432",
            "CLI flag: --egg a432",
            "API endpoint: /a432/audio",
            "Web interface: /a432/theme"
        ],
        "scientific_note": "The 432 Hz claims lack robust scientific evidence. This mode is purely for creative fun and ambient effects."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
