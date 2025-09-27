#!/usr/bin/env python3
"""
🎭 Code Opera - FastAPI Server
=============================

FastAPI server for Code Opera conductor panel and state management.
Provides REST API for BPM, key, and per-voice gain/FX controls.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
from pathlib import Path

from server.opera_state import (
    Conductor, Voice, FX, 
    get_state, update_state, 
    set_seed, get_seed, 
    advance_act, reset_performance, 
    update_metrics
)

# FastAPI app
app = FastAPI(
    title="🎭 Code Opera - Conductor Panel",
    description="Multi-voice creative coding performance with real-time controls",
    version="1.0.0"
)

# CORS middleware
app.middleware("cors")(CORSMiddleware(
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
))

# Mount static files
app.mount("/static", StaticFiles(directory="out"), name="static")


class StateUpdate(BaseModel):
    """Model for state updates"""
    bpm: Optional[int] = None
    key: Optional[str] = None
    mode: Optional[str] = None
    seed: Optional[str] = None
    act: Optional[int] = None
    voices: Optional[Dict[str, Dict[str, Any]]] = None
    p95_latency: Optional[float] = None
    error_rate: Optional[float] = None
    qps: Optional[float] = None


class MetricsUpdate(BaseModel):
    """Model for metrics updates"""
    p95_latency: float
    error_rate: float
    qps: float


@app.get("/")
async def root():
    """Serve the Code Opera harmony visualization"""
    harmony_file = Path("out/opera/code_opera_harmony.html")
    if harmony_file.exists():
        return FileResponse(harmony_file)
    else:
        return HTMLResponse("""
        <html>
            <head><title>🎭 Code Opera</title></head>
            <body>
                <h1>🎭 Code Opera</h1>
                <p>Multi-voice creative coding performance</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)


@app.get("/opera/state")
async def get_opera_state():
    """Get current conductor state"""
    state = get_state()
    return state.dict()


@app.post("/opera/state")
async def set_opera_state(update: StateUpdate):
    """Update conductor state"""
    try:
        # Convert to dict, excluding None values
        update_data = update.dict(exclude_unset=True)
        
        # Update state
        updated_state = update_state(update_data)
        
        return updated_state.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/opera/seed")
async def set_opera_seed(seed: str):
    """Set deterministic seed"""
    try:
        set_seed(seed)
        return {"seed": seed, "message": "Seed set successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/opera/seed")
async def get_opera_seed():
    """Get current seed"""
    seed = get_seed()
    return {"seed": seed}


@app.post("/opera/advance")
async def advance_opera_act():
    """Advance to next act"""
    try:
        act = advance_act()
        return {"act": act, "message": f"Advanced to Act {act}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/opera/reset")
async def reset_opera_performance():
    """Reset performance to Act I"""
    try:
        reset_performance()
        return {"message": "Performance reset to Act I"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/opera/metrics")
async def update_opera_metrics(metrics: MetricsUpdate):
    """Update performance metrics"""
    try:
        update_metrics(
            metrics.p95_latency,
            metrics.error_rate,
            metrics.qps
        )
        return {"message": "Metrics updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/opera/voices")
async def get_opera_voices():
    """Get all voice configurations"""
    state = get_state()
    return {
        "voices": {name: voice.dict() for name, voice in state.voices.items()},
        "dynamics": state.get_dynamics(),
        "tempo_modifier": state.get_tempo_modifier(),
        "motif_length": state.get_motif_length()
    }


@app.get("/opera/performance")
async def get_opera_performance():
    """Get performance data for visualization"""
    state = get_state()
    return {
        "act": state.act,
        "key": state.key,
        "bpm": state.bpm,
        "dynamics": state.get_dynamics(),
        "tempo_modifier": state.get_tempo_modifier(),
        "motif_length": state.get_motif_length(),
        "metrics": {
            "p95_latency": state.p95_latency,
            "error_rate": state.error_rate,
            "qps": state.qps
        },
        "voices": {
            name: {
                "gain": voice.gain,
                "muted": voice.muted,
                "solo": voice.solo,
                "fx": voice.fx.dict()
            }
            for name, voice in state.voices.items()
        }
    }


@app.get("/opera/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Code Opera Conductor Panel",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8787)
