"""
Touring Rig API Server
======================

FastAPI server for the touring rig system with complete API hooks.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import time
import os

# Import the touring rig
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from string_fx.touring_rig import TouringRig, ShowConfig, MorphCurve, MomentaryButton

# Create FastAPI app
app = FastAPI(
    title="Touring Rig API",
    description="Professional show controller API for touring rig system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global touring rig instance
rig = TouringRig()

# Pydantic models
class LoadShowRequest(BaseModel):
    rackset_url: str
    seed: int = 777

class PlayShowRequest(BaseModel):
    start_scene: int = 0
    loop: bool = False

class NextSceneRequest(BaseModel):
    morph: Optional[float] = 2.0

class JumpSceneRequest(BaseModel):
    scene_id: int
    morph: Optional[float] = 2.0

class SetParameterRequest(BaseModel):
    path: str
    value: float

class BlackoutRequest(BaseModel):
    state: bool

class MetricsUpdateRequest(BaseModel):
    qps: float = 0.0
    p95: float = 0.0
    error_rate: float = 0.0
    cpu_percent: float = 0.0
    frame_time_ms: float = 0.0

class IntensityRequest(BaseModel):
    intensity: float

class MetricsLinkRequest(BaseModel):
    strength: float

class MomentaryButtonRequest(BaseModel):
    button: str  # "flash_strobe", "blackout", "all_white_bloom"
    state: bool

class ShowStatusResponse(BaseModel):
    show_name: str
    bpm: float
    scenes: int
    current_scene: int
    is_playing: bool
    live_intensity: float
    metrics_link_enabled: bool
    metrics_link_strength: float
    motion_reduced: bool
    heat_guard_active: bool
    quality_level: int
    show_clock: Dict[str, float]
    momentary_states: Dict[str, bool]
    strobe_state: Dict[str, Any]
    current_metrics: Dict[str, float]
    scene_thumbnails: Dict[str, Dict[str, Any]]

# API Endpoints

@app.post("/show/load")
async def load_show(request: LoadShowRequest):
    """Load a show from rackset URL"""
    try:
        # Load show from file
        with open(request.rackset_url, 'r') as f:
            data = json.load(f)
        
        show = ShowConfig(
            name=data.get("name", "Untitled Show"),
            bpm=data.get("bpm", 110.0),
            scenes=data.get("scenes", []),
            intensity=data.get("intensity", 100.0),
            metrics_link_strength=data.get("metrics_link_strength", 100.0)
        )
        
        rig.load_show(show)
        
        return {
            "status": "success",
            "message": f"Show '{show.name}' loaded successfully",
            "show_name": show.name,
            "scenes": len(show.scenes),
            "bpm": show.bpm
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading show: {str(e)}")

@app.post("/show/play")
async def play_show(request: PlayShowRequest):
    """Start playing the show"""
    try:
        rig.play_show(request.start_scene, request.loop)
        return {
            "status": "success",
            "message": "Show started",
            "start_scene": request.start_scene,
            "loop": request.loop
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error playing show: {str(e)}")

@app.post("/show/next")
async def next_scene(request: NextSceneRequest):
    """Advance to next scene"""
    try:
        rig.next_scene(request.morph or 2.0)
        return {
            "status": "success",
            "message": "Advanced to next scene",
            "morph_time": request.morph or 2.0
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error advancing scene: {str(e)}")

@app.post("/show/jump")
async def jump_to_scene(request: JumpSceneRequest):
    """Jump to specific scene"""
    try:
        rig.jump_to_scene(request.scene_id, request.morph or 2.0)
        return {
            "status": "success",
            "message": f"Jumped to scene {request.scene_id}",
            "scene_id": request.scene_id,
            "morph_time": request.morph or 2.0
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error jumping to scene: {str(e)}")

@app.post("/show/param")
async def set_parameter(request: SetParameterRequest):
    """Set a parameter value"""
    try:
        rig.set_parameter(request.path, request.value)
        return {
            "status": "success",
            "message": f"Parameter set: {request.path} = {request.value}",
            "path": request.path,
            "value": request.value
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting parameter: {str(e)}")

@app.post("/show/blackout")
async def toggle_blackout(request: BlackoutRequest):
    """Toggle blackout state"""
    try:
        rig.toggle_blackout(request.state)
        return {
            "status": "success",
            "message": f"Blackout {'activated' if request.state else 'deactivated'}",
            "state": request.state
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error toggling blackout: {str(e)}")

@app.post("/show/momentary")
async def toggle_momentary_button(request: MomentaryButtonRequest):
    """Toggle momentary button"""
    try:
        button_map = {
            "flash_strobe": MomentaryButton.FLASH_STROBE,
            "blackout": MomentaryButton.BLACKOUT,
            "all_white_bloom": MomentaryButton.ALL_WHITE_BLOOM
        }
        
        if request.button not in button_map:
            raise HTTPException(status_code=400, detail=f"Invalid button: {request.button}")
        
        button = button_map[request.button]
        
        if button == MomentaryButton.FLASH_STROBE:
            rig.toggle_flash_strobe(request.state)
        elif button == MomentaryButton.BLACKOUT:
            rig.toggle_blackout(request.state)
        elif button == MomentaryButton.ALL_WHITE_BLOOM:
            rig.toggle_all_white_bloom(request.state)
        
        return {
            "status": "success",
            "message": f"{request.button} {'activated' if request.state else 'deactivated'}",
            "button": request.button,
            "state": request.state
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error toggling momentary button: {str(e)}")

@app.post("/show/intensity")
async def set_intensity(request: IntensityRequest):
    """Set live intensity"""
    try:
        rig.set_live_intensity(request.intensity)
        return {
            "status": "success",
            "message": f"Live intensity set to {request.intensity}%",
            "intensity": request.intensity
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting intensity: {str(e)}")

@app.post("/show/metrics-link")
async def set_metrics_link(request: MetricsLinkRequest):
    """Set metrics link strength"""
    try:
        rig.set_metrics_link_strength(request.strength)
        return {
            "status": "success",
            "message": f"Metrics link strength set to {request.strength}%",
            "strength": request.strength
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting metrics link: {str(e)}")

@app.post("/show/metrics")
async def update_metrics(request: MetricsUpdateRequest):
    """Update live metrics for sidechain"""
    try:
        metrics = {
            "qps": request.qps,
            "p95": request.p95,
            "error_rate": request.error_rate,
            "cpu_percent": request.cpu_percent,
            "frame_time_ms": request.frame_time_ms
        }
        
        rig.update_metrics(metrics)
        
        return {
            "status": "success",
            "message": "Metrics updated",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating metrics: {str(e)}")

@app.get("/show/status")
async def get_show_status():
    """Get complete show status"""
    try:
        status = rig.get_show_status()
        return ShowStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting status: {str(e)}")

@app.post("/show/undo")
async def undo_action():
    """Undo last action"""
    try:
        if rig.undo():
            return {
                "status": "success",
                "message": "Undo successful"
            }
        else:
            return {
                "status": "error",
                "message": "Nothing to undo"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error undoing: {str(e)}")

@app.post("/show/redo")
async def redo_action():
    """Redo last undone action"""
    try:
        if rig.redo():
            return {
                "status": "success",
                "message": "Redo successful"
            }
        else:
            return {
                "status": "error",
                "message": "Nothing to redo"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error redoing: {str(e)}")

@app.get("/show/thumbnails")
async def get_scene_thumbnails():
    """Get scene thumbnails"""
    try:
        status = rig.get_show_status()
        thumbnails = status.get("scene_thumbnails", {})
        return {
            "status": "success",
            "thumbnails": thumbnails
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting thumbnails: {str(e)}")

@app.get("/show/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Touring Rig API",
        "version": "1.0.0",
        "endpoints": [
            "POST /show/load",
            "POST /show/play",
            "POST /show/next",
            "POST /show/jump",
            "POST /show/param",
            "POST /show/blackout",
            "POST /show/momentary",
            "POST /show/intensity",
            "POST /show/metrics-link",
            "POST /show/metrics",
            "GET /show/status",
            "POST /show/undo",
            "POST /show/redo",
            "GET /show/thumbnails",
            "GET /show/health"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
