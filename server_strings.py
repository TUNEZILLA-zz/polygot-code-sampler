#!/usr/bin/env python3
"""
🎭 String FX FastAPI Server - FX Graph Runtime Integration
========================================================

FastAPI server for string effects with:
- FX graph runtime (declarative chains)
- Deterministic seeded chaos
- Intensity knob (one slider to rule them all)
- Safe output modes (raw/ansi/html)
- Performance guardrails
- MIDI/hotkey integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
import json
import time
import sys
from pathlib import Path

# Add the string_fx directory to the path
sys.path.insert(0, str(Path(__file__).parent / "string_fx"))

from runtime import (
    apply_chain,
    FXConfig,
    OutputMode,
    create_preset,
    get_preset_pack,
    export_preset,
)


app = FastAPI(
    title="🎭 String FX Server",
    description="Mind-Bending String Effects with FX Graph Runtime",
    version="1.0.0",
)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class FXStep(BaseModel):
    """Single effect step in a chain"""

    name: str = Field(..., description="Effect name")
    params: Dict[str, Any] = Field(
        default_factory=dict, description="Effect parameters"
    )


class FXRequest(BaseModel):
    """Request for string effects"""

    text: str = Field(..., description="Input text to transform")
    chain: List[FXStep] = Field(..., description="Effect chain")
    seed: Optional[int] = Field(None, description="Seed for deterministic effects")
    intensity: float = Field(
        0.75, ge=0.0, le=1.0, description="Intensity knob (0.0-1.0)"
    )
    mode: str = Field("ansi", description="Output mode (raw/ansi/html)")
    max_length: int = Field(8000, ge=1, le=50000, description="Maximum output length")
    budget_ms: int = Field(
        100, ge=10, le=1000, description="Processing budget in milliseconds"
    )


class FXResponse(BaseModel):
    """Response from string effects"""

    output: str = Field(..., description="Transformed text")
    seed: Optional[int] = Field(None, description="Seed used")
    intensity: float = Field(..., description="Intensity used")
    mode: str = Field(..., description="Output mode")
    processing_time_ms: float = Field(
        ..., description="Processing time in milliseconds"
    )
    chain: List[FXStep] = Field(..., description="Effect chain used")


class PresetRequest(BaseModel):
    """Request for preset-based effects"""

    text: str = Field(..., description="Input text to transform")
    preset: str = Field(..., description="Preset name")
    seed: Optional[int] = Field(None, description="Seed for deterministic effects")
    intensity: float = Field(
        0.75, ge=0.0, le=1.0, description="Intensity knob (0.0-1.0)"
    )
    mode: str = Field("ansi", description="Output mode (raw/ansi/html)")


class PresetInfo(BaseModel):
    """Preset information"""

    name: str = Field(..., description="Preset name")
    description: str = Field(..., description="Preset description")
    chain: List[FXStep] = Field(..., description="Effect chain")


class PresetListResponse(BaseModel):
    """List of available presets"""

    presets: List[PresetInfo] = Field(..., description="Available presets")


# ============================================================================
# API ENDPOINTS
# ============================================================================


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API documentation"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎭 String FX Server</title>
        <style>
            body { font-family: 'Courier New', monospace; background: #000; color: #fff; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .title { font-size: 3em; text-align: center; margin-bottom: 30px; 
                     background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .endpoint { background: #111; padding: 20px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #00ffff; }
            .method { color: #00ffff; font-weight: bold; }
            .path { color: #ffff00; }
            .description { color: #ccc; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">🎭 String FX Server</h1>
            <p style="text-align: center; font-size: 1.2em; color: #888;">Mind-Bending String Effects with FX Graph Runtime</p>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/fx/run</div>
                <div class="description">Apply string effects with custom chain</div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST</div>
                <div class="path">/fx/preset</div>
                <div class="description">Apply string effects using a preset</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/fx/presets</div>
                <div class="description">List all available presets</div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="path">/fx/health</div>
                <div class="description">Health check endpoint</div>
            </div>
            
            <p style="text-align: center; margin-top: 30px; color: #666;">
                Visit <a href="/docs" style="color: #00ffff;">/docs</a> for interactive API documentation
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/fx/run", response_model=FXResponse)
async def run_fx(request: FXRequest):
    """Apply string effects with custom chain"""
    try:
        start_time = time.time()

        # Create FX config
        config = FXConfig(
            intensity=request.intensity,
            seed=request.seed,
            mode=OutputMode(request.mode),
            max_length=request.max_length,
            budget_ms=request.budget_ms,
        )

        # Convert chain to runtime format
        chain = []
        for step in request.chain:
            chain.append({"name": step.name, "params": step.params})

        # Apply effects
        result = apply_chain(request.text, chain, config)

        processing_time = (time.time() - start_time) * 1000

        return FXResponse(
            output=result,
            seed=request.seed,
            intensity=request.intensity,
            mode=request.mode,
            processing_time_ms=processing_time,
            chain=request.chain,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error applying effects: {str(e)}")


@app.post("/fx/preset", response_model=FXResponse)
async def run_preset(request: PresetRequest):
    """Apply string effects using a preset"""
    try:
        start_time = time.time()

        # Get preset
        presets = get_preset_pack()
        if request.preset not in presets:
            raise HTTPException(
                status_code=404, detail=f"Preset '{request.preset}' not found"
            )

        preset = presets[request.preset]

        # Create FX config
        config = FXConfig(
            intensity=request.intensity,
            seed=request.seed,
            mode=OutputMode(request.mode),
            max_length=8000,
            budget_ms=100,
        )

        # Apply effects
        result = apply_chain(request.text, preset["chain"], config)

        processing_time = (time.time() - start_time) * 1000

        # Convert chain to response format
        chain = [
            FXStep(name=step["name"], params=step.get("params", {}))
            for step in preset["chain"]
        ]

        return FXResponse(
            output=result,
            seed=request.seed,
            intensity=request.intensity,
            mode=request.mode,
            processing_time_ms=processing_time,
            chain=chain,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error applying preset: {str(e)}")


@app.get("/fx/presets", response_model=PresetListResponse)
async def list_presets():
    """List all available presets"""
    presets = get_preset_pack()

    preset_list = []
    for name, preset in presets.items():
        chain = [
            FXStep(name=step["name"], params=step.get("params", {}))
            for step in preset["chain"]
        ]
        preset_list.append(
            PresetInfo(name=name, description=preset["description"], chain=chain)
        )

    return PresetListResponse(presets=preset_list)


@app.get("/fx/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "String FX Server",
        "version": "1.0.0",
        "timestamp": time.time(),
    }


# ============================================================================
# MIDI/HOTKEY INTEGRATION
# ============================================================================


class MIDIControl(BaseModel):
    """MIDI control mapping"""

    cc_number: int = Field(..., ge=0, le=127, description="MIDI CC number")
    parameter: str = Field(..., description="Parameter to control")
    min_value: float = Field(0.0, description="Minimum value")
    max_value: float = Field(1.0, description="Maximum value")


@app.post("/fx/midi/control")
async def set_midi_control(control: MIDIControl):
    """Set MIDI control mapping"""
    # In a real implementation, this would store the mapping
    # and handle MIDI input to control parameters
    return {
        "message": f"MIDI CC {control.cc_number} mapped to {control.parameter}",
        "range": f"{control.min_value} - {control.max_value}",
    }


# ============================================================================
# EXPORT FUNCTIONALITY
# ============================================================================


@app.post("/fx/export")
async def export_preset_data(
    name: str, chain: List[FXStep], description: str = "", seed: Optional[int] = None
):
    """Export a preset as JSON"""
    try:
        # Convert chain to runtime format
        runtime_chain = []
        for step in chain:
            runtime_chain.append({"name": step.name, "params": step.params})

        # Create and export preset
        preset_data = create_preset(name, runtime_chain, description)
        export_data = export_preset(preset_data, seed)

        return {"preset": export_data, "download_url": f"/fx/download/{name}.json"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting preset: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
