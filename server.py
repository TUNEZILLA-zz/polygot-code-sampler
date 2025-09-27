#!/usr/bin/env python3
"""
🎛️ Polyglot Code Mixer - FastAPI Render Service

Real-time code generation service that powers the Code Mixer interface.
Maps audio production metaphors to actual renderer_api.render() calls.
"""

import logging
import time
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pcs.core import PyToIR

# Import the central renderer API
from pcs.renderer_api import render as render_generic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🎛️ Polyglot Code Mixer API",
    description="Real-time code generation service for the Code Mixer interface",
    version="1.0.0",
)

# CORS middleware for the mixer interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RenderRequest(BaseModel):
    """Request model for code generation"""

    code: str = Field(..., description="Python comprehension code")
    target: Literal["rust", "ts", "go", "csharp", "julia", "sql"] = Field(
        ..., description="Target backend"
    )

    # Mixer-driven flags (all optional, adapter safely filters per-backend)
    parallel: Optional[bool] = Field(None, description="Enable parallel processing")
    mode: Optional[Literal["auto", "loops", "broadcast"]] = Field(
        None, description="Code generation mode"
    )
    unsafe: Optional[bool] = Field(None, description="Enable unsafe optimizations")
    explain: Optional[bool] = Field(None, description="Include explanatory comments")
    dialect: Optional[Literal["postgresql", "sqlite", "duckdb", "bigquery"]] = Field(
        None, description="SQL dialect"
    )

    # Effects rack toggles
    effects: Dict[str, bool] = Field(
        default_factory=dict, description="Optimization effects"
    )

    # Automation lane settings
    grace_period: Optional[int] = Field(
        None, description="Grace period in milliseconds"
    )
    regression_threshold: Optional[float] = Field(
        None, description="Regression threshold percentage"
    )
    emergency_override: Optional[bool] = Field(
        None, description="Emergency override flag"
    )


class RenderResponse(BaseModel):
    """Response model for generated code"""

    ok: bool
    target: str
    code: str
    meta: Dict[str, Any] = Field(default_factory=dict)
    timing: Dict[str, float] = Field(default_factory=dict)


# Initialize the parser
parser = PyToIR()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "🎛️ Polyglot Code Mixer API",
        "version": "1.0.0",
        "status": "ready",
        "endpoints": {"render": "/render", "health": "/health", "docs": "/docs"},
    }


@app.get("/health")
async def health():
    """Health check with basic functionality test"""
    try:
        # Test basic parsing
        test_ir = parser.parse("[x for x in range(5)]")
        return {"status": "healthy", "parser": "working", "timestamp": time.time()}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")


@app.post("/render", response_model=RenderResponse)
async def render_code(request: RenderRequest):
    """
    Generate code for a specific backend based on mixer settings.

    Maps audio production metaphors to actual renderer flags:
    - Fader level > 60% → parallel=True
    - Fader level > 85% → unsafe=True
    - Effects toggles → optimization flags
    - Preset → mode selection
    """
    start_time = time.time()

    try:
        logger.info(f"Rendering {request.target} for code: {request.code[:50]}...")

        # Parse Python code to IR
        parse_start = time.time()
        ir = parser.parse(request.code)
        parse_time = time.time() - parse_start

        # Map effects to renderer flags
        render_flags = {
            "parallel": request.parallel,
            "mode": request.mode,
            "unsafe": request.unsafe,
            "explain": request.explain if request.explain is not None else True,
            "dialect": request.dialect,
        }

        # Add effects-based flags
        if request.effects.get("predicate_pushdown", False):
            render_flags["predicate_pushdown"] = True
        if request.effects.get("constant_folding", False):
            render_flags["constant_folding"] = True
        if request.effects.get("parallel_safety", False):
            render_flags["parallel_safety"] = True
        if request.effects.get("type_inference", False):
            render_flags["type_inference"] = True

        # Generate code using the central renderer API
        render_start = time.time()
        code = render_generic(request.target, ir, **render_flags)
        render_time = time.time() - render_start

        total_time = time.time() - start_time

        logger.info(
            f"Generated {len(code)} chars for {request.target} in {total_time:.3f}s"
        )

        return RenderResponse(
            ok=True,
            target=request.target,
            code=code,
            meta={
                "effects": request.effects,
                "flags": render_flags,
                "input_length": len(request.code),
                "output_length": len(code),
            },
            timing={
                "parse_ms": parse_time * 1000,
                "render_ms": render_time * 1000,
                "total_ms": total_time * 1000,
            },
        )

    except Exception as e:
        logger.error(f"Render failed for {request.target}: {e}")
        raise HTTPException(status_code=400, detail=f"Code generation failed: {str(e)}")


@app.post("/render/batch")
async def render_batch(requests: list[RenderRequest]):
    """
    Batch render multiple targets for the same Python code.
    Useful for the mixer interface to generate all active tracks at once.
    """
    start_time = time.time()
    results = []

    for request in requests:
        try:
            result = await render_code(request)
            results.append(result)
        except Exception as e:
            logger.error(f"Batch render failed for {request.target}: {e}")
            results.append(
                RenderResponse(
                    ok=False,
                    target=request.target,
                    code=f"Error: {str(e)}",
                    meta={"error": str(e)},
                    timing={"total_ms": 0},
                )
            )

    total_time = time.time() - start_time

    return {
        "results": results,
        "batch_timing": {"total_ms": total_time * 1000, "count": len(requests)},
    }


@app.get("/presets")
async def get_presets():
    """Get available mixer presets"""
    return {
        "presets": {
            "hifi": {
                "name": "🎵 Hi-Fi Sequential",
                "description": "Clean, readable code with minimal optimizations",
                "settings": {
                    "parallel": False,
                    "mode": "loops",
                    "unsafe": False,
                    "explain": True,
                    "effects": {
                        "predicate_pushdown": True,
                        "constant_folding": True,
                        "parallel_safety": True,
                        "type_inference": False,
                    },
                },
            },
            "punchy": {
                "name": "⚡ Punchy Parallel",
                "description": "Maximum throughput with aggressive parallelization",
                "settings": {
                    "parallel": True,
                    "mode": "loops",
                    "unsafe": True,
                    "explain": False,
                    "effects": {
                        "predicate_pushdown": True,
                        "constant_folding": True,
                        "parallel_safety": True,
                        "type_inference": True,
                    },
                },
            },
            "lofi": {
                "name": "🎧 Lo-Fi Minimalist",
                "description": "Simple loops with no abstractions",
                "settings": {
                    "parallel": False,
                    "mode": "loops",
                    "unsafe": False,
                    "explain": False,
                    "effects": {
                        "predicate_pushdown": False,
                        "constant_folding": False,
                        "parallel_safety": False,
                        "type_inference": False,
                    },
                },
            },
            "sql_club": {
                "name": "🎛️ SQL Club Mix",
                "description": "Heavy use of window functions and optimizations",
                "settings": {
                    "parallel": False,
                    "mode": "loops",
                    "unsafe": False,
                    "explain": True,
                    "dialect": "postgresql",
                    "effects": {
                        "predicate_pushdown": True,
                        "constant_folding": True,
                        "parallel_safety": False,
                        "type_inference": True,
                    },
                },
            },
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8787, reload=True, log_level="info")
