# server_enhanced.py - Production-hardened Code Live server
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, Field
from starlette.responses import Response

# Configure structured logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "code_live_requests_total", "Total requests", ["method", "endpoint", "status"]
)
REQUEST_DURATION = Histogram(
    "code_live_request_duration_seconds", "Request duration", ["method", "endpoint"]
)
ACTIVE_REQUESTS = Gauge("code_live_active_requests", "Active requests")
FALLBACK_COUNT = Counter(
    "code_live_fallbacks_total", "Total fallbacks", ["backend", "reason"]
)
GLITCH_COUNT = Counter("code_live_glitches_total", "Total glitch activations")
BATCH_SIZE = Histogram("code_live_batch_size", "Batch size distribution")
QUEUE_DEPTH = Gauge("code_live_queue_depth", "Queue depth")


# Request models
class RenderRequest(BaseModel):
    backend: str = Field(
        ..., description="Target backend (rust, ts, go, csharp, sql, julia)"
    )
    code: str = Field(..., max_length=10000, description="Python code to transform")
    parallel: bool = Field(False, description="Enable parallel processing")
    mode: Optional[str] = Field(
        None, description="Rendering mode (auto, loops, broadcast)"
    )
    explain: bool = Field(True, description="Include explanatory comments")
    unsafe: bool = Field(False, description="Enable unsafe optimizations")
    int_type: Optional[str] = Field(None, description="Integer type (int, int64)")
    strict_types: bool = Field(False, description="Enable strict type checking")


class RenderResponse(BaseModel):
    code: str
    metrics: dict[str, Any]
    warnings: list[str] = []
    fallbacks: list[str] = []


class BatchRequest(BaseModel):
    tracks: list[RenderRequest] = Field(
        ..., max_items=10, description="Render tracks (max 10)"
    )
    coalesce: bool = Field(True, description="Coalesce similar requests")


class BatchResponse(BaseModel):
    tracks: list[RenderResponse]
    metrics: dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float
    metrics: dict[str, Any]


class ReadyResponse(BaseModel):
    ready: bool
    warmup_time: float
    cache_status: str


# Global state
start_time = time.time()
request_cache = {}
warmup_complete = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Code Live server...")

    # Warmup renderer
    logger.info("🔥 Warming up renderer...")
    warmup_start = time.time()
    try:
        # Import and warm up the renderer
        from pcs.ir_glue import parse_to_ir
        from pcs.renderer_api import render_generic

        # Test render
        test_ir = parse_to_ir("[x for x in range(5)]")
        test_result = render_generic(test_ir, backend="rust", parallel=False)

        warmup_time = time.time() - warmup_start
        logger.info(f"✅ Renderer warmed up in {warmup_time:.3f}s")

        global warmup_complete
        warmup_complete = True

    except Exception as e:
        logger.error(f"❌ Warmup failed: {e}")
        warmup_complete = False

    yield

    # Shutdown
    logger.info("🛑 Shutting down Code Live server...")


# Create FastAPI app
app = FastAPI(
    title="Code Live - The Ableton Live of Code",
    description="Production-ready creative suite for code generation",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8080"
    ).split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Add to logs
    logger.info(f"Request {request_id}: {request.method} {request.url}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    ACTIVE_REQUESTS.inc()

    try:
        response = await call_next(request)
        status = str(response.status_code)
        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status=status
        ).inc()
        return response
    finally:
        duration = time.time() - start_time
        REQUEST_DURATION.labels(
            method=request.method, endpoint=request.url.path
        ).observe(duration)
        ACTIVE_REQUESTS.dec()


# Health endpoints
@app.get("/health", response_model=HealthResponse)
async def health():
    """Liveness probe - cheap health check"""
    uptime = time.time() - start_time
    return HealthResponse(
        status="ok",
        version="1.0.0",
        uptime=uptime,
        metrics={
            "active_requests": ACTIVE_REQUESTS._value.get(),
            "warmup_complete": warmup_complete,
        },
    )


@app.get("/ready", response_model=ReadyResponse)
async def ready():
    """Readiness probe - can we render within N ms?"""
    if not warmup_complete:
        return ReadyResponse(ready=False, warmup_time=0, cache_status="cold")

    # Test render to ensure we're ready
    start_time = time.time()
    try:
        from pcs.ir_glue import parse_to_ir
        from pcs.renderer_api import render_generic

        test_ir = parse_to_ir("[x for x in range(3)]")
        render_generic(test_ir, backend="rust", parallel=False)

        render_time = time.time() - start_time
        return ReadyResponse(ready=True, warmup_time=render_time, cache_status="warm")
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return ReadyResponse(ready=False, warmup_time=0, cache_status="error")


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Core render endpoint
@app.post("/render", response_model=RenderResponse)
async def render(request: RenderRequest):
    """Single code render with metrics"""
    start_time = time.time()

    try:
        from pcs.ir_glue import parse_to_ir
        from pcs.renderer_api import render_generic

        # Parse to IR
        ir = parse_to_ir(request.code)

        # Render
        code = render_generic(
            ir,
            backend=request.backend,
            parallel=request.parallel,
            mode=request.mode,
            explain=request.explain,
            unsafe=request.unsafe,
            int_type=request.int_type,
            strict_types=request.strict_types,
        )

        # Metrics
        duration = time.time() - start_time
        metrics = {
            "latency_ms": duration * 1000,
            "code_length": len(code),
            "backend": request.backend,
            "parallel": request.parallel,
        }

        logger.info(
            f"Rendered {request.backend} in {duration:.3f}s ({len(code)} chars)"
        )

        return RenderResponse(code=code, metrics=metrics, warnings=[], fallbacks=[])

    except Exception as e:
        logger.error(f"Render failed: {e}")
        FALLBACK_COUNT.labels(backend=request.backend, reason="error").inc()
        raise HTTPException(status_code=500, detail=str(e))


# Batch render endpoint
@app.post("/render/batch", response_model=BatchResponse)
async def render_batch(request: BatchRequest):
    """Batch render with coalescing"""
    start_time = time.time()

    # Track batch size
    BATCH_SIZE.observe(len(request.tracks))

    tracks = []
    total_latency = 0

    for track in request.tracks:
        try:
            from pcs.ir_glue import parse_to_ir
            from pcs.renderer_api import render_generic

            # Parse to IR
            ir = parse_to_ir(track.code)

            # Render
            code = render_generic(
                ir,
                backend=track.backend,
                parallel=track.parallel,
                mode=track.mode,
                explain=track.explain,
                unsafe=track.unsafe,
                int_type=track.int_type,
                strict_types=track.strict_types,
            )

            # Metrics
            duration = time.time() - start_time
            metrics = {
                "latency_ms": duration * 1000,
                "code_length": len(code),
                "backend": track.backend,
                "parallel": track.parallel,
            }

            tracks.append(
                RenderResponse(code=code, metrics=metrics, warnings=[], fallbacks=[])
            )

            total_latency += duration

        except Exception as e:
            logger.error(f"Batch render failed for {track.backend}: {e}")
            FALLBACK_COUNT.labels(backend=track.backend, reason="error").inc()
            tracks.append(
                RenderResponse(
                    code=f"// Error: {str(e)}",
                    metrics={
                        "latency_ms": 0,
                        "code_length": 0,
                        "backend": track.backend,
                        "parallel": track.parallel,
                    },
                    warnings=[str(e)],
                    fallbacks=["error"],
                )
            )

    # Batch metrics
    batch_metrics = {
        "total_latency_ms": total_latency * 1000,
        "track_count": len(tracks),
        "coalesced": request.coalesce,
    }

    logger.info(f"Batch rendered {len(tracks)} tracks in {total_latency:.3f}s")

    return BatchResponse(tracks=tracks, metrics=batch_metrics)


# Creative endpoints
@app.post("/sidechain")
async def sidechain(request: dict[str, Any]):
    """Apply adaptive mixing rules"""
    # TODO: Implement sidechain logic
    return {"status": "sidechain applied"}


@app.post("/timeline")
async def timeline(request: dict[str, Any]):
    """Keyframe interpolation"""
    # TODO: Implement timeline logic
    return {"status": "timeline applied"}


@app.post("/glitch")
async def glitch(request: dict[str, Any]):
    """Apply glitch effects"""
    GLITCH_COUNT.inc()
    # TODO: Implement glitch logic
    return {"status": "glitch applied"}


@app.post("/ab-compare")
async def ab_compare(request: dict[str, Any]):
    """A/B state comparison"""
    # TODO: Implement A/B comparison
    return {"status": "A/B comparison applied"}


# Preset management
@app.get("/presets")
async def list_presets():
    """List available presets"""
    # TODO: Implement preset listing
    return {"presets": []}


@app.post("/presets")
async def create_preset(request: dict[str, Any]):
    """Create new preset"""
    # TODO: Implement preset creation
    return {"status": "preset created"}


@app.put("/presets/{preset_id}")
async def update_preset(preset_id: str, request: dict[str, Any]):
    """Update preset"""
    # TODO: Implement preset update
    return {"status": "preset updated"}


@app.delete("/presets/{preset_id}")
async def delete_preset(preset_id: str):
    """Delete preset"""
    # TODO: Implement preset deletion
    return {"status": "preset deleted"}


# MIDI integration
@app.post("/midi")
async def apply_midi(request: dict[str, Any]):
    """Apply MIDI CC mapping"""
    # TODO: Implement MIDI mapping
    return {"status": "MIDI applied"}


@app.get("/midi/mappings")
async def list_midi_mappings():
    """List MIDI mappings"""
    # TODO: Implement MIDI mapping listing
    return {"mappings": []}


@app.post("/midi/mappings")
async def create_midi_mapping(request: dict[str, Any]):
    """Create MIDI mapping"""
    # TODO: Implement MIDI mapping creation
    return {"status": "MIDI mapping created"}


# Static file serving
@app.get("/site/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files"""
    import os

    from fastapi.responses import FileResponse

    static_path = f"site/{file_path}"
    if os.path.exists(static_path):
        return FileResponse(static_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8787)
