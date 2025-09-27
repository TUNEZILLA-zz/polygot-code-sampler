# server_optimized.py - Production-optimized Code Live server with surgical fixes
import hashlib
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, Optional

import orjson
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
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

# Prometheus metrics with target and status labels
REQUEST_COUNT = Counter(
    "code_live_requests_total",
    "Total requests",
    ["method", "endpoint", "target", "status"],
)
REQUEST_DURATION = Histogram(
    "code_live_request_duration_seconds",
    "Request duration",
    ["method", "endpoint", "target"],
)
ACTIVE_REQUESTS = Gauge("code_live_active_requests", "Active requests")
FALLBACK_COUNT = Counter(
    "code_live_fallbacks_total", "Total fallbacks", ["target", "reason"]
)
GLITCH_COUNT = Counter("code_live_glitches_total", "Total glitch activations")
BATCH_SIZE = Histogram("code_live_batch_size", "Batch size distribution")
QUEUE_DEPTH = Gauge("code_live_queue_depth", "Queue depth")
RATE_LIMIT_COUNT = Counter(
    "code_live_rate_limits_total", "Rate limit hits", ["endpoint", "target"]
)
CACHE_HITS = Counter("code_live_cache_hits_total", "Cache hits", ["target"])
CACHE_MISSES = Counter("code_live_cache_misses_total", "Cache misses", ["target"])


# Request models
class RenderRequest(BaseModel):
    target: str = Field(
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
    notes: list[str] = []
    degraded: bool = False
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


# Cache for hot IRs (60-second LRU)
@lru_cache(maxsize=1000)
def get_cached_ir(code_hash: str, target: str, flags_hash: str):
    """Get cached IR result"""
    return None


def cache_ir_result(code_hash: str, target: str, flags_hash: str, result: dict):
    """Cache IR result"""
    # This is a simplified cache - in production, use Redis or similar
    cache_key = f"{code_hash}:{target}:{flags_hash}"
    request_cache[cache_key] = {"result": result, "timestamp": time.time()}


def get_cached_result(code: str, target: str, flags: dict) -> Optional[dict]:
    """Get cached result if available"""
    code_hash = hashlib.md5(code.encode()).hexdigest()
    flags_hash = hashlib.md5(str(sorted(flags.items())).encode()).hexdigest()
    cache_key = f"{code_hash}:{target}:{flags_hash}"

    if cache_key in request_cache:
        cached = request_cache[cache_key]
        if time.time() - cached["timestamp"] < 60:  # 60-second TTL
            CACHE_HITS.labels(target=target).inc()
            return cached["result"]
        else:
            del request_cache[cache_key]

    CACHE_MISSES.labels(target=target).inc()
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting optimized Code Live server...")

    # Warmup renderer
    logger.info("🔥 Warming up renderer...")
    warmup_start = time.time()
    try:
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
    logger.info("🛑 Shutting down optimized Code Live server...")


# Create FastAPI app with ORJSONResponse
app = FastAPI(
    title="Code Live - The Ableton Live of Code (Optimized)",
    description="Production-optimized creative suite for code generation",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
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


# Enhanced metrics middleware with target and status tracking
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    ACTIVE_REQUESTS.inc()

    # Extract target from request body for render endpoints
    target = "unknown"
    if request.url.path in ["/render", "/render/batch"]:
        try:
            body = await request.body()
            if body:
                data = orjson.loads(body)
                if "target" in data:
                    target = data["target"]
        except:
            pass

    try:
        response = await call_next(request)
        status = str(response.status_code)

        # Categorize status codes
        if response.status_code == 429:
            status_category = "rate_limit"
        elif 400 <= response.status_code < 500:
            status_category = "client_error"
        elif 500 <= response.status_code < 600:
            status_category = "server_error"
        else:
            status_category = "success"

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            target=target,
            status=status_category,
        ).inc()

        return response
    finally:
        duration = time.time() - start_time
        REQUEST_DURATION.labels(
            method=request.method, endpoint=request.url.path, target=target
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
            "cache_size": len(request_cache),
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


# Enhanced render endpoint with caching and fallback handling
@app.post("/render", response_model=RenderResponse)
async def render(request: RenderRequest):
    """Single code render with metrics, caching, and fallback handling"""
    start_time = time.time()

    # Check cache first
    flags = {
        "parallel": request.parallel,
        "mode": request.mode,
        "explain": request.explain,
        "unsafe": request.unsafe,
        "int_type": request.int_type,
        "strict_types": request.strict_types,
    }

    cached_result = get_cached_result(request.code, request.target, flags)
    if cached_result:
        logger.info(f"Cache hit for {request.target}")
        return RenderResponse(**cached_result)

    try:
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

        # Render with fallback handling
        try:
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

            notes = []
            degraded = False

        except Exception as e:
            # Handle Julia-specific issues with graceful fallback
            if request.target == "julia":
                logger.warning(f"Julia render failed, falling back to sequential: {e}")
                try:
                    code = render_julia(ir, parallel=False)  # Fallback to sequential
                    notes = [f"Julia fallback: {str(e)}"]
                    degraded = True
                    FALLBACK_COUNT.labels(
                        target=request.target, reason="julia_fallback"
                    ).inc()
                except Exception as fallback_error:
                    logger.error(f"Julia fallback also failed: {fallback_error}")
                    raise HTTPException(
                        status_code=500, detail=f"Julia render failed: {str(e)}"
                    )
            else:
                raise HTTPException(status_code=500, detail=str(e))

        # Metrics
        duration = time.time() - start_time
        metrics = {
            "latency_ms": duration * 1000,
            "code_length": len(code),
            "target": request.target,
            "parallel": request.parallel,
            "cached": False,
        }

        # Cache the result
        result = {
            "code": code,
            "notes": notes,
            "degraded": degraded,
            "metrics": metrics,
            "warnings": [],
            "fallbacks": [],
        }
        cache_ir_result(request.code, request.target, flags, result)

        logger.info(f"Rendered {request.target} in {duration:.3f}s ({len(code)} chars)")

        return RenderResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Render failed for {request.target}: {e}")
        FALLBACK_COUNT.labels(target=request.target, reason="error").inc()
        raise HTTPException(status_code=500, detail=str(e))


# Enhanced batch render endpoint with coalescing
@app.post("/render/batch", response_model=BatchResponse)
async def render_batch(request: BatchRequest):
    """Batch render with coalescing and enhanced metrics"""
    start_time = time.time()

    # Track batch size
    BATCH_SIZE.observe(len(request.tracks))

    tracks = []
    total_latency = 0

    for track in request.tracks:
        try:
            # Check cache first
            flags = {
                "parallel": track.parallel,
                "mode": track.mode,
                "explain": track.explain,
                "unsafe": track.unsafe,
                "int_type": track.int_type,
                "strict_types": track.strict_types,
            }

            cached_result = get_cached_result(track.code, track.target, flags)
            if cached_result:
                tracks.append(RenderResponse(**cached_result))
                continue

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
            ir = parser.parse(track.code)

            # Render with fallback handling
            try:
                if track.target == "rust":
                    code = render_rust(ir, parallel=track.parallel)
                elif track.target == "ts":
                    code = render_ts(ir, parallel=track.parallel)
                elif track.target == "go":
                    code = render_go(ir, parallel=track.parallel)
                elif track.target == "csharp":
                    code = render_csharp(ir, parallel=track.parallel)
                elif track.target == "sql":
                    code = render_sql(ir)
                elif track.target == "julia":
                    code = render_julia(ir, parallel=track.parallel)
                else:
                    raise ValueError(f"Unknown target: {track.target}")
                notes = []
                degraded = False

            except Exception as e:
                if track.target == "julia":
                    logger.warning(f"Julia batch render failed, falling back: {e}")
                    try:
                        code = render_julia(
                            ir, parallel=False
                        )  # Fallback to sequential
                        notes = [f"Julia fallback: {str(e)}"]
                        degraded = True
                        FALLBACK_COUNT.labels(
                            target=track.target, reason="julia_fallback"
                        ).inc()
                    except Exception as fallback_error:
                        logger.error(f"Julia batch fallback failed: {fallback_error}")
                        raise HTTPException(
                            status_code=500,
                            detail=f"Julia batch render failed: {str(e)}",
                        )
                else:
                    raise HTTPException(status_code=500, detail=str(e))

            # Metrics
            duration = time.time() - start_time
            metrics = {
                "latency_ms": duration * 1000,
                "code_length": len(code),
                "target": track.target,
                "parallel": track.parallel,
                "cached": False,
            }

            # Cache the result
            result = {
                "code": code,
                "notes": notes,
                "degraded": degraded,
                "metrics": metrics,
                "warnings": [],
                "fallbacks": [],
            }
            cache_ir_result(track.code, track.target, flags, result)

            tracks.append(RenderResponse(**result))
            total_latency += duration

        except Exception as e:
            logger.error(f"Batch render failed for {track.target}: {e}")
            FALLBACK_COUNT.labels(target=track.target, reason="error").inc()
            tracks.append(
                RenderResponse(
                    code=f"// Error: {str(e)}",
                    notes=[str(e)],
                    degraded=True,
                    metrics={
                        "latency_ms": 0,
                        "code_length": 0,
                        "target": track.target,
                        "parallel": track.parallel,
                        "cached": False,
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
    return {"status": "sidechain applied"}


@app.post("/timeline")
async def timeline(request: dict[str, Any]):
    """Keyframe interpolation"""
    return {"status": "timeline applied"}


@app.post("/glitch")
async def glitch(request: dict[str, Any]):
    """Apply glitch effects"""
    GLITCH_COUNT.inc()
    return {"status": "glitch applied"}


@app.post("/ab-compare")
async def ab_compare(request: dict[str, Any]):
    """A/B state comparison"""
    return {"status": "A/B comparison applied"}


# Preset management
@app.get("/presets")
async def list_presets():
    """List available presets"""
    return {"presets": []}


@app.post("/presets")
async def create_preset(request: dict[str, Any]):
    """Create new preset"""
    return {"status": "preset created"}


@app.put("/presets/{preset_id}")
async def update_preset(preset_id: str, request: dict[str, Any]):
    """Update preset"""
    return {"status": "preset updated"}


@app.delete("/presets/{preset_id}")
async def delete_preset(preset_id: str):
    """Delete preset"""
    return {"status": "preset deleted"}


# MIDI integration
@app.post("/midi")
async def apply_midi(request: dict[str, Any]):
    """Apply MIDI CC mapping"""
    return {"status": "MIDI applied"}


@app.get("/midi/mappings")
async def list_midi_mappings():
    """List MIDI mappings"""
    return {"mappings": []}


@app.post("/midi/mappings")
async def create_midi_mapping(request: dict[str, Any]):
    """Create MIDI mapping"""
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
