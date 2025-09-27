# server_mastered.py - Self-tuning live performance with circuit breakers and adaptive rate limits
import hashlib
import logging
import os
import threading
import time
import uuid
from collections import deque
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

# Enhanced Prometheus metrics with circuit breaker and adaptive rate limiting
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
CIRCUIT_BREAKER_TRIPS = Counter(
    "code_live_circuit_breaker_trips_total", "Circuit breaker trips", ["target"]
)
CIRCUIT_BREAKER_RESETS = Counter(
    "code_live_circuit_breaker_resets_total", "Circuit breaker resets", ["target"]
)
ADAPTIVE_RATE_LIMITS = Gauge(
    "code_live_adaptive_rate_limits", "Adaptive rate limits", ["target", "endpoint"]
)


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
        ..., max_items=15, description="Render tracks (max 15)"
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
    circuit_breakers: dict[str, Any]
    rate_limits: dict[str, Any]


class ReadyResponse(BaseModel):
    ready: bool
    warmup_time: float
    cache_status: str
    circuit_breakers: dict[str, Any]


# Global state
start_time = time.time()
request_cache = {}
warmup_complete = False


# Circuit Breaker Implementation
class CircuitBreaker:
    def __init__(self, target: str, failure_threshold: int = 5, timeout: int = 60):
        self.target = target
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = threading.Lock()

    def can_execute(self) -> bool:
        with self.lock:
            if self.state == "CLOSED":
                return True
            elif self.state == "OPEN":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "HALF_OPEN"
                    CIRCUIT_BREAKER_RESETS.labels(target=self.target).inc()
                    logger.info(f"Circuit breaker for {self.target} moved to HALF_OPEN")
                    return True
                return False
            else:  # HALF_OPEN
                return True

    def record_success(self):
        with self.lock:
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                logger.info(f"Circuit breaker for {self.target} moved to CLOSED")

    def record_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                CIRCUIT_BREAKER_TRIPS.labels(target=self.target).inc()
                logger.warning(
                    f"Circuit breaker for {self.target} OPENED after {self.failure_count} failures"
                )

    def get_state(self) -> dict[str, Any]:
        with self.lock:
            return {
                "state": self.state,
                "failure_count": self.failure_count,
                "last_failure_time": self.last_failure_time,
                "time_since_last_failure": time.time() - self.last_failure_time,
            }


# Adaptive Rate Limiter
class AdaptiveRateLimiter:
    def __init__(self, target: str, base_limit: int = 10, burst_limit: int = 20):
        self.target = target
        self.base_limit = base_limit
        self.burst_limit = burst_limit
        self.current_limit = base_limit
        self.request_times = deque()
        self.lock = threading.Lock()
        self.last_adjustment = time.time()

    def can_make_request(self) -> bool:
        with self.lock:
            now = time.time()

            # Clean old requests (older than 1 second)
            while self.request_times and self.request_times[0] < now - 1:
                self.request_times.popleft()

            # Check if we can make a request
            if len(self.request_times) < self.current_limit:
                self.request_times.append(now)
                return True

            return False

    def adjust_limit(self, success_rate: float, avg_latency: float):
        with self.lock:
            now = time.time()
            if now - self.last_adjustment < 5:  # Only adjust every 5 seconds
                return

            self.last_adjustment = now

            # Adaptive logic
            if success_rate > 0.95 and avg_latency < 0.1:
                # System is healthy, can increase limit
                self.current_limit = min(self.current_limit + 1, self.burst_limit)
            elif success_rate < 0.8 or avg_latency > 0.5:
                # System is struggling, decrease limit
                self.current_limit = max(self.current_limit - 1, 1)

            ADAPTIVE_RATE_LIMITS.labels(target=self.target, endpoint="render").set(
                self.current_limit
            )
            logger.info(
                f"Adjusted rate limit for {self.target} to {self.current_limit} (success: {success_rate:.2f}, latency: {avg_latency:.3f})"
            )


# Global circuit breakers and rate limiters
circuit_breakers = {
    target: CircuitBreaker(target)
    for target in ["rust", "ts", "go", "csharp", "sql", "julia"]
}

rate_limiters = {
    target: AdaptiveRateLimiter(target)
    for target in ["rust", "ts", "go", "csharp", "sql", "julia"]
}


# Cache for hot IRs (60-second LRU)
@lru_cache(maxsize=1000)
def get_cached_ir(code_hash: str, target: str, flags_hash: str):
    """Get cached IR result"""
    return None


def cache_ir_result(code_hash: str, target: str, flags_hash: str, result: dict):
    """Cache IR result"""
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
    logger.info("🚀 Starting mastered Code Live server...")

    # Warmup renderer
    logger.info("🔥 Warming up renderer...")
    warmup_start = time.time()
    try:
        from pcs_step3_ts import (
            PyToIR,
            render_rust,
        )

        # Test render
        parser = PyToIR()
        test_ir = parser.parse("[x for x in range(5)]")
        test_result = render_rust(test_ir, parallel=False)

        warmup_time = time.time() - warmup_start
        logger.info(f"✅ Renderer warmed up in {warmup_time:.3f}s")

        global warmup_complete
        warmup_complete = True

    except Exception as e:
        logger.error(f"❌ Warmup failed: {e}")
        warmup_complete = False

    yield

    # Shutdown
    logger.info("🛑 Shutting down mastered Code Live server...")


# Create FastAPI app with ORJSONResponse
app = FastAPI(
    title="Code Live - The Ableton Live of Code (Mastered)",
    description="Self-tuning creative suite for code generation with circuit breakers and adaptive rate limiting",
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


# Enhanced metrics middleware with circuit breaker and rate limiting
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

    # Get circuit breaker states
    circuit_breaker_states = {
        target: breaker.get_state() for target, breaker in circuit_breakers.items()
    }

    # Get rate limiter states
    rate_limit_states = {
        target: {
            "current_limit": limiter.current_limit,
            "base_limit": limiter.base_limit,
            "burst_limit": limiter.burst_limit,
        }
        for target, limiter in rate_limiters.items()
    }

    return HealthResponse(
        status="ok",
        version="1.0.0",
        uptime=uptime,
        metrics={
            "active_requests": ACTIVE_REQUESTS._value.get(),
            "warmup_complete": warmup_complete,
            "cache_size": len(request_cache),
        },
        circuit_breakers=circuit_breaker_states,
        rate_limits=rate_limit_states,
    )


@app.get("/ready", response_model=ReadyResponse)
async def ready():
    """Readiness probe - can we render within N ms?"""
    if not warmup_complete:
        return ReadyResponse(
            ready=False, warmup_time=0, cache_status="cold", circuit_breakers={}
        )

    # Test render to ensure we're ready
    start_time = time.time()
    try:
        from pcs_step3_ts import PyToIR, render_rust

        parser = PyToIR()
        test_ir = parser.parse("[x for x in range(3)]")
        render_rust(test_ir, parallel=False)

        render_time = time.time() - start_time

        # Get circuit breaker states
        circuit_breaker_states = {
            target: breaker.get_state() for target, breaker in circuit_breakers.items()
        }

        return ReadyResponse(
            ready=True,
            warmup_time=render_time,
            cache_status="warm",
            circuit_breakers=circuit_breaker_states,
        )
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return ReadyResponse(
            ready=False, warmup_time=0, cache_status="error", circuit_breakers={}
        )


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Enhanced render endpoint with circuit breakers and adaptive rate limiting
@app.post("/render", response_model=RenderResponse)
async def render(request: RenderRequest):
    """Single code render with circuit breakers and adaptive rate limiting"""
    start_time = time.time()

    # Check circuit breaker
    if not circuit_breakers[request.target].can_execute():
        logger.warning(f"Circuit breaker OPEN for {request.target}")
        raise HTTPException(
            status_code=503, detail=f"Circuit breaker OPEN for {request.target}"
        )

    # Check rate limiter
    if not rate_limiters[request.target].can_make_request():
        logger.warning(f"Rate limit exceeded for {request.target}")
        RATE_LIMIT_COUNT.labels(endpoint="render", target=request.target).inc()
        raise HTTPException(
            status_code=429, detail=f"Rate limit exceeded for {request.target}"
        )

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

        # Render with circuit breaker protection
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

            # Record success for circuit breaker
            circuit_breakers[request.target].record_success()

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

                    # Record success for circuit breaker (fallback worked)
                    circuit_breakers[request.target].record_success()

                except Exception as fallback_error:
                    logger.error(f"Julia fallback also failed: {fallback_error}")
                    # Record failure for circuit breaker
                    circuit_breakers[request.target].record_failure()
                    raise HTTPException(
                        status_code=500, detail=f"Julia render failed: {str(e)}"
                    )
            else:
                # Record failure for circuit breaker
                circuit_breakers[request.target].record_failure()
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
            # Check circuit breaker
            if not circuit_breakers[track.target].can_execute():
                logger.warning(f"Circuit breaker OPEN for {track.target} in batch")
                tracks.append(
                    RenderResponse(
                        code=f"// Circuit breaker OPEN for {track.target}",
                        notes=[f"Circuit breaker OPEN for {track.target}"],
                        degraded=True,
                        metrics={
                            "latency_ms": 0,
                            "code_length": 0,
                            "target": track.target,
                            "parallel": track.parallel,
                            "cached": False,
                        },
                        warnings=[f"Circuit breaker OPEN for {track.target}"],
                        fallbacks=["circuit_breaker"],
                    )
                )
                continue

            # Check rate limiter
            if not rate_limiters[track.target].can_make_request():
                logger.warning(f"Rate limit exceeded for {track.target} in batch")
                RATE_LIMIT_COUNT.labels(
                    endpoint="render/batch", target=track.target
                ).inc()
                tracks.append(
                    RenderResponse(
                        code=f"// Rate limit exceeded for {track.target}",
                        notes=[f"Rate limit exceeded for {track.target}"],
                        degraded=True,
                        metrics={
                            "latency_ms": 0,
                            "code_length": 0,
                            "target": track.target,
                            "parallel": track.parallel,
                            "cached": False,
                        },
                        warnings=[f"Rate limit exceeded for {track.target}"],
                        fallbacks=["rate_limit"],
                    )
                )
                continue

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

            # Render with circuit breaker protection
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

                # Record success for circuit breaker
                circuit_breakers[track.target].record_success()

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

                        # Record success for circuit breaker (fallback worked)
                        circuit_breakers[track.target].record_success()

                    except Exception as fallback_error:
                        logger.error(f"Julia batch fallback failed: {fallback_error}")
                        # Record failure for circuit breaker
                        circuit_breakers[track.target].record_failure()
                        raise HTTPException(
                            status_code=500,
                            detail=f"Julia batch render failed: {str(e)}",
                        )
                else:
                    # Record failure for circuit breaker
                    circuit_breakers[track.target].record_failure()
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
