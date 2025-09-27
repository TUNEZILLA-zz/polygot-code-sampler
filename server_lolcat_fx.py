# server_lolcat_fx.py - Code Live with Lolcat FX Rack
import os
import random
import sys
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

# Import Lolcat FX
from lolcat_fx import LolcatFXConfig, lolcat_fx


# Lolcat FX Models
class LolcatFXRequest(BaseModel):
    target: str
    code: str
    parallel: bool = False
    # Lolcat FX Parameters
    preset: str = "classic"  # party, glitch, wave, classic
    # Core FX
    stretch: float = 0.3
    echo: float = 0.2
    pitch_shift: float = 0.4
    reverb: float = 0.25
    # Color FX
    rainbow: float = 0.6
    glitch_colors: float = 0.3
    neon: float = 0.4
    invert: float = 0.2
    # Spacing FX
    stutter: float = 0.25
    waveform: float = 0.35
    cluster: float = 0.2
    # Chaos FX
    random_insert: float = 0.3
    scramble: float = 0.15
    ascii_melt: float = 0.25


class LolcatFXResponse(BaseModel):
    code: str
    notes: list[str] = []
    degraded: bool = False
    metrics: dict[str, Any]
    warnings: list[str] = []
    fallbacks: list[str] = []
    lolcat_effects: dict[str, Any] = {}
    fx_applied: list[str] = []


# Create FastAPI app
app = FastAPI(
    title="Code Live - Lolcat FX Rack",
    description="The Visual Glitch FX Layer for Code/Text Output",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/render/lolcat", response_model=LolcatFXResponse)
async def render_lolcat(request: LolcatFXRequest):
    """Render code with Lolcat FX Rack effects"""
    start_time = time.time()

    try:
        # Import renderers
        from pcs_step3_ts import (
            PyToIR,
            render_csharp,
            render_go,
            render_julia,
            render_rust,
            render_sql,
            render_ts,
        )

        # Parse to IR
        parser = PyToIR()
        ir = parser.parse(request.code)

        # Render based on target
        if request.target == "rust":
            code = render_rust(ir, parallel=request.parallel)
        elif request.target == "ts":
            code = render_ts(ir, parallel=request.parallel)
        elif request.target == "go":
            code = render_go(ir, parallel=request.parallel)
        elif request.target == "csharp":
            code = render_csharp(ir, parallel=request.parallel)
        elif request.target == "sql":
            code = render_sql(ir)
        elif request.target == "julia":
            code = render_julia(ir, parallel=request.parallel)
        else:
            raise ValueError(f"Unknown target: {request.target}")

        # Apply Lolcat FX to the generated code
        lolcat_config = LolcatFXConfig(
            stretch=request.stretch,
            echo=request.echo,
            pitch_shift=request.pitch_shift,
            reverb=request.reverb,
            rainbow=request.rainbow,
            glitch_colors=request.glitch_colors,
            neon=request.neon,
            invert=request.invert,
            stutter=request.stutter,
            waveform=request.waveform,
            cluster=request.cluster,
            random_insert=request.random_insert,
            scramble=request.scramble,
            ascii_melt=request.ascii_melt,
        )

        # Apply Lolcat FX
        lolcat_code = lolcat_fx(code, preset=request.preset, **lolcat_config.__dict__)

        # Calculate metrics
        duration = time.time() - start_time
        metrics = {
            "latency_ms": duration * 1000,
            "code_length": len(lolcat_code),
            "target": request.target,
            "parallel": request.parallel,
            "cached": False,
            "lolcat_fx": True,
        }

        # Generate Lolcat effects summary
        lolcat_effects = {
            "preset": request.preset,
            "stretch": request.stretch,
            "echo": request.echo,
            "pitch_shift": request.pitch_shift,
            "reverb": request.reverb,
            "rainbow": request.rainbow,
            "glitch_colors": request.glitch_colors,
            "neon": request.neon,
            "invert": request.invert,
            "stutter": request.stutter,
            "waveform": request.waveform,
            "cluster": request.cluster,
            "random_insert": request.random_insert,
            "scramble": request.scramble,
            "ascii_melt": request.ascii_melt,
        }

        # Generate FX applied list
        fx_applied = []
        if request.stretch > 0:
            fx_applied.append("Stretch")
        if request.echo > 0:
            fx_applied.append("Echo")
        if request.pitch_shift > 0:
            fx_applied.append("Pitch Shift")
        if request.reverb > 0:
            fx_applied.append("Reverb")
        if request.rainbow > 0:
            fx_applied.append("Rainbow Gradient")
        if request.glitch_colors > 0:
            fx_applied.append("Glitch Colors")
        if request.neon > 0:
            fx_applied.append("Neon Effect")
        if request.invert > 0:
            fx_applied.append("Invert")
        if request.stutter > 0:
            fx_applied.append("Stutter")
        if request.waveform > 0:
            fx_applied.append("Waveform")
        if request.cluster > 0:
            fx_applied.append("Cluster")
        if request.random_insert > 0:
            fx_applied.append("Random Insert")
        if request.scramble > 0:
            fx_applied.append("Scramble")
        if request.ascii_melt > 0:
            fx_applied.append("ASCII Melt")

        # Generate notes
        notes = []
        if request.preset == "party":
            notes.append("🎉 Party Mode: Rainbow + Echo + Stretch")
        elif request.preset == "glitch":
            notes.append("👾 Glitch Cat: Random Colors + Unicode Melt")
        elif request.preset == "wave":
            notes.append("🌊 Wave Rider: Sine Wave Spacing + Fade")
        elif request.preset == "classic":
            notes.append("😹 Classic Lolcat: Random Caps + Rainbow")

        if request.stretch > 0:
            notes.append(f"🔊 Stretch: {request.stretch:.2f} - Repeats letters")
        if request.echo > 0:
            notes.append(
                f"🔊 Echo: {request.echo:.2f} - Trailing spaces + exclamations"
            )
        if request.pitch_shift > 0:
            notes.append(f"🔊 Pitch Shift: {request.pitch_shift:.2f} - Random casing")
        if request.reverb > 0:
            notes.append(
                f"🔊 Reverb: {request.reverb:.2f} - Fade-out letters with spacing"
            )
        if request.rainbow > 0:
            notes.append(
                f"🌈 Rainbow Gradient: {request.rainbow:.2f} - Cycles letters through colors"
            )
        if request.glitch_colors > 0:
            notes.append(
                f"🌈 Glitch Colors: {request.glitch_colors:.2f} - Random ANSI colors per character"
            )
        if request.neon > 0:
            notes.append(f"🌈 Neon FX: {request.neon:.2f} - Bold + glow simulation")
        if request.invert > 0:
            notes.append(
                f"🌈 Invert FX: {request.invert:.2f} - Alternating background/foreground"
            )
        if request.stutter > 0:
            notes.append(
                f"🎨 Stutter: {request.stutter:.2f} - Extra spaces between letters"
            )
        if request.waveform > 0:
            notes.append(
                f"🎨 Waveform: {request.waveform:.2f} - Letters arranged in sine-wave pattern"
            )
        if request.cluster > 0:
            notes.append(
                f"🎨 Cluster: {request.cluster:.2f} - Random bursts of duplicated letters"
            )
        if request.random_insert > 0:
            notes.append(
                f"🌀 Random Insert: {request.random_insert:.2f} - Drops emojis, ASCII art, or symbols"
            )
        if request.scramble > 0:
            notes.append(f"🌀 Scramble: {request.scramble:.2f} - Shuffles letters")
        if request.ascii_melt > 0:
            notes.append(
                f"🌀 ASCII Melt: {request.ascii_melt:.2f} - Overlays with unicode glitch blocks"
            )

        return LolcatFXResponse(
            code=lolcat_code,
            notes=notes,
            degraded=False,
            metrics=metrics,
            warnings=[],
            fallbacks=[],
            lolcat_effects=lolcat_effects,
            fx_applied=fx_applied,
        )

    except Exception as e:
        # Handle errors with Lolcat-themed messages
        error_messages = [
            "🎛️ Lolcat FX Rack Error!",
            "🌈 Visual Glitch FX Layer failed!",
            "🌀 Chaos FX malfunction!",
            "✨ Sparkly transformation error!",
            "🎉 Party Mode crash!",
        ]

        error_message = random.choice(error_messages)
        notes = [f"{error_message} {str(e)}"]

        return LolcatFXResponse(
            code=f"// {error_message}\n// Error: {str(e)}",
            notes=notes,
            degraded=True,
            metrics={
                "latency_ms": 0,
                "code_length": 0,
                "target": request.target,
                "parallel": request.parallel,
                "cached": False,
            },
            warnings=[str(e)],
            fallbacks=["error"],
            lolcat_effects={},
            fx_applied=[],
        )


@app.get("/health")
async def health():
    """Health check with Lolcat theme"""
    return {
        "status": "ok",
        "message": "🎛️ Code Live Lolcat FX Rack is sparkly! ✨",
        "version": "1.0.0",
        "fx_features": [
            "🔊 Core FX (Stretch, Echo, Pitch Shift, Reverb)",
            "🌈 Color FX (Rainbow, Glitch, Neon, Invert)",
            "🎨 Spacing FX (Stutter, Waveform, Cluster)",
            "🌀 Chaos FX (Random Insert, Scramble, ASCII Melt)",
        ],
        "presets": [
            "🎉 Party Mode (Rainbow + Echo + Stretch)",
            "👾 Glitch Cat (Random Colors + Unicode Melt)",
            "🌊 Wave Rider (Sine Wave Spacing + Fade)",
            "😹 Classic Lolcat (Random Caps + Rainbow)",
        ],
    }


@app.get("/")
async def root():
    """Root endpoint with Lolcat welcome"""
    return {
        "message": "🎛️ Welcome to Code Live Lolcat FX Rack! 🎛️",
        "description": "The Visual Glitch FX Layer for Code/Text Output",
        "endpoints": {"render": "/render/lolcat", "health": "/health"},
        "fx_concepts": [
            "Core FX: Stretch → repeats letters (hello → heeelloooooo)",
            "Echo → trailing spaces + exclamations (hello → hello ! ! !)",
            "Pitch Shift → random casing (hello → HeLlOooO)",
            "Reverb → fade-out letters with spacing (hello → h e l l o o o)",
            "Color FX: Rainbow Gradient → cycles letters through colors",
            "Glitch Colors → random ANSI colors per character",
            "Neon FX → bold + glow simulation (HELLO → 💚H💙E💜L💖L💛O)",
            "Spacing FX: Stutter → extra spaces between letters (h   e   l   l   o)",
            "Waveform → letters arranged in sine-wave pattern",
            "Cluster → random bursts of duplicated letters (hello → heeeelllllllooo)",
            "Chaos FX: Random Insert → drops emojis, ASCII art, or symbols",
            "Scramble → shuffles letters (hello → lhelooo)",
            "ASCII Melt → overlays with unicode glitch blocks (hȅ̵͔͝l̸̤͎͑lǭ̴̙)",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8791)
