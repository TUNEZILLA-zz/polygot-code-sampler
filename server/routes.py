# server/routes.py - FastAPI route handlers
import time
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from ..pcs.core import PyToIR
from ..pcs.renderer_api import render as render_generic
from .contracts import *

router = APIRouter()

# === GLOBAL STATE ===
parser_obj = PyToIR()
render_queue = {}
render_cache = {}

# === CORE RENDER ENDPOINTS ===


@router.post("/render", response_model=RenderResponse)
async def render_single(request: RenderRequest):
    """Render a single Python comprehension to multiple backends."""
    start_time = time.perf_counter()

    # Validate Python syntax
    if not validate_python_syntax(request.python):
        raise HTTPException(status_code=400, detail="Invalid Python syntax")

    # Parse to IR
    try:
        ir = parser_obj.parse(request.python)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse Python: {e}")

    results = []
    total_gen_ms = 0

    for track in request.tracks:
        if not validate_backend_support(track.backend):
            results.append(
                RenderResult(
                    backend=track.backend,
                    code="",
                    stats=PerformanceStats(gen_ms=0, loc=0),
                    success=False,
                    error=f"Backend {track.backend} not supported",
                )
            )
            continue

        # Apply quantization if requested
        level = track.level
        if request.quantize:
            level = round(level / request.quantize_grid) * request.quantize_grid

        # Render code
        try:
            render_start = time.perf_counter()

            code = render_generic(
                track.backend,
                ir,
                parallel=track.parallel,
                mode=track.mode,
                unsafe=track.unsafe,
                explain=request.effects.parallel_safety,
                dialect="postgres" if track.backend == "sql" else None,
                **request.effects.dict(),
            )

            render_time = (time.perf_counter() - render_start) * 1000
            total_gen_ms += render_time

            # Calculate stats
            loc = len(code.split("\n"))
            fallbacks = []
            warnings = []

            if render_time > request.policy.max_gen_time_ms:
                warnings.append(f"Slow generation: {render_time:.1f}ms")

            if not track.parallel and track.level > 0.6:
                fallbacks.append("sequential_fallback")

            stats = PerformanceStats(
                gen_ms=render_time, loc=loc, fallbacks=fallbacks, warnings=warnings
            )

            results.append(
                RenderResult(
                    backend=track.backend, code=code, stats=stats, success=True
                )
            )

        except Exception as e:
            results.append(
                RenderResult(
                    backend=track.backend,
                    code="",
                    stats=PerformanceStats(gen_ms=0, loc=0),
                    success=False,
                    error=str(e),
                )
            )

    return RenderResponse(
        results=results, total_gen_ms=total_gen_ms, quantized=request.quantize
    )


@router.post("/render/batch", response_model=BatchRenderResponse)
async def render_batch(request: BatchRenderRequest):
    """Batch render multiple requests with optional coalescing."""
    start_time = time.perf_counter()

    if request.coalesce:
        # Coalesce similar requests
        coalesced = await coalesce_requests(request.requests)
        results = []

        for req in coalesced:
            result = await render_single(req)
            results.append(result)

        return BatchRenderResponse(
            results=results,
            total_time_ms=(time.perf_counter() - start_time) * 1000,
            coalesced=True,
        )
    else:
        # Process all requests individually
        results = []
        for req in request.requests:
            result = await render_single(req)
            results.append(result)

        return BatchRenderResponse(
            results=results,
            total_time_ms=(time.perf_counter() - start_time) * 1000,
            coalesced=False,
        )


# === SIDECHAIN RULES ===


@router.post("/sidechain", response_model=SidechainResponse)
async def apply_sidechain(request: SidechainRequest):
    """Apply sidechain rules to current state."""
    updated_state = request.current_state.copy()
    triggered_rules = []

    for rule in request.rules:
        if not rule.enabled:
            continue

        if not validate_sidechain_rule(rule):
            continue

        # Evaluate metric
        metric_value = get_nested_value(request.metrics, rule.when.path)
        condition_met = False

        if rule.when.op == ">":
            condition_met = metric_value > rule.when.value
        elif rule.when.op == "<":
            condition_met = metric_value < rule.when.value
        elif rule.when.op == "==":
            condition_met = metric_value == rule.when.value
        elif rule.when.op == ">=":
            condition_met = metric_value >= rule.when.value
        elif rule.when.op == "<=":
            condition_met = metric_value <= rule.when.value

        if condition_met:
            # Apply action
            target_value = get_nested_value(updated_state, rule.then.target)
            new_value = max(0, min(1, target_value + rule.then.delta))
            set_nested_value(updated_state, rule.then.target, new_value)
            triggered_rules.append(f"{rule.when.path} {rule.when.op} {rule.when.value}")

    return SidechainResponse(
        updated_state=updated_state, triggered_rules=triggered_rules
    )


# === TIMELINE & KEYFRAMES ===


@router.post("/timeline", response_model=TimelineResponse)
async def interpolate_timeline(request: TimelineRequest):
    """Interpolate between keyframes at current time."""
    if not request.keyframes:
        return TimelineResponse(interpolated_state={}, active_keyframes=[])

    # Sort keyframes by time
    sorted_keyframes = sorted(request.keyframes, key=lambda k: k.t)

    # Find surrounding keyframes
    before_keyframe = None
    after_keyframe = None

    for keyframe in sorted_keyframes:
        if keyframe.t <= request.current_time:
            before_keyframe = keyframe
        if keyframe.t >= request.current_time and after_keyframe is None:
            after_keyframe = keyframe
            break

    if before_keyframe and after_keyframe:
        # Interpolate between keyframes
        t = (request.current_time - before_keyframe.t) / (
            after_keyframe.t - before_keyframe.t
        )

        # Apply easing
        if before_keyframe.easing == "exp":
            t = t**1.8
        elif before_keyframe.easing == "s":
            t = 0.5 * (1 - math.cos(math.pi * t))
        # else: linear (t = t)

        interpolated_state = interpolate_states(
            before_keyframe.state, after_keyframe.state, t
        )

        active_keyframes = [f"{before_keyframe.t}s", f"{after_keyframe.t}s"]
    elif before_keyframe:
        # Use before keyframe
        interpolated_state = before_keyframe.state
        active_keyframes = [f"{before_keyframe.t}s"]
    else:
        # Use first keyframe
        interpolated_state = sorted_keyframes[0].state
        active_keyframes = [f"{sorted_keyframes[0].t}s"]

    # Apply quantization if requested
    if request.quantize:
        interpolated_state = quantize_state(interpolated_state)

    return TimelineResponse(
        interpolated_state=interpolated_state, active_keyframes=active_keyframes
    )


# === PRESET MANAGEMENT ===


@router.get("/presets", response_model=PresetListResponse)
async def list_presets():
    """List all available presets."""
    # This would typically come from a database
    presets = [
        Preset(
            name="Hi-Fi Sequential",
            state={"faders": {"rust": 0.3, "julia": 0.2, "sql": 0.1, "ts": 0.25}},
            notes="Clean, readable code with no parallelization",
        ),
        Preset(
            name="Punchy Parallel",
            state={"faders": {"rust": 0.9, "julia": 0.8, "sql": 0.3, "ts": 0.7}},
            notes="Aggressive parallelization for maximum performance",
        ),
        Preset(
            name="Lo-Fi Minimalist",
            state={"faders": {"rust": 0.15, "julia": 0.1, "sql": 0.05, "ts": 0.2}},
            notes="Simple loops with minimal abstractions",
        ),
    ]

    return PresetListResponse(presets=presets, total=len(presets))


@router.post("/presets", response_model=Preset)
async def create_preset(request: PresetRequest):
    """Create a new preset."""
    preset = Preset(
        name=request.name, state=request.state, notes=request.notes, tags=request.tags
    )

    # This would typically save to database
    return preset


# === MIDI MAPPING ===


@router.post("/midi", response_model=MidiResponse)
async def apply_midi(request: MidiRequest):
    """Apply MIDI CC to mixer state."""
    updated_state = {}
    triggered_mappings = []

    for mapping in request.mappings:
        if not mapping.enabled:
            continue

        if mapping.cc == request.cc:
            # Apply mapping
            normalized_value = request.value / 127.0

            if mapping.target.startswith("macros."):
                macro_name = mapping.target.split(".")[1]
                updated_state[f"macros.{macro_name}"] = normalized_value
            else:
                updated_state[mapping.target] = normalized_value

            triggered_mappings.append(f"CC{mapping.cc} -> {mapping.target}")

    return MidiResponse(
        updated_state=updated_state, triggered_mappings=triggered_mappings
    )


# === GLITCH MODE ===


@router.post("/glitch", response_model=GlitchResponse)
async def apply_glitch(request: GlitchRequest):
    """Apply glitch effects to mixer state."""
    import random

    if request.seed:
        random.seed(request.seed)

    glitched_state = {}

    # Apply glitch to faders
    for key, value in request.state.items():
        if isinstance(value, (int, float)):
            glitch_amount = (random.random() - 0.5) * request.intensity
            new_value = max(0, min(1, value + glitch_amount))
            glitched_state[key] = new_value
        else:
            glitched_state[key] = value

    # Apply safety rails if requested
    safe_applied = False
    if request.safe_mode:
        # Ensure no values go below 0 or above 1
        for key, value in glitched_state.items():
            if isinstance(value, (int, float)):
                glitched_state[key] = max(0, min(1, value))
        safe_applied = True

    return GlitchResponse(
        glitched_state=glitched_state,
        seed_used=request.seed or random.randint(0, 1000000),
        safe_applied=safe_applied,
    )


# === A/B COMPARE ===


@router.post("/ab-compare", response_model=ABCompareResponse)
async def ab_compare(request: ABCompareRequest):
    """Compare two mixer states."""
    active_state = request.state_a if request.active == "a" else request.state_b

    # Calculate diff summary
    diff_summary = {}
    for key in set(request.state_a.keys()) | set(request.state_b.keys()):
        val_a = request.state_a.get(key, 0)
        val_b = request.state_b.get(key, 0)
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            diff_summary[key] = {
                "a": val_a,
                "b": val_b,
                "diff": val_b - val_a,
                "percent_change": ((val_b - val_a) / val_a * 100) if val_a != 0 else 0,
            }

    return ABCompareResponse(active_state=active_state, diff_summary=diff_summary)


# === PERFORMANCE OVERLAYS ===


@router.post("/overlay", response_model=OverlayResponse)
async def get_performance_overlay(request: OverlayRequest):
    """Get performance overlay information."""
    overlays = []
    severity = "info"
    recommendations = []

    # Check generation time
    if request.stats.gen_ms > 100:
        overlays.append(f"⚠️ Slow generation: {request.stats.gen_ms:.1f}ms")
        severity = "warning"
        recommendations.append(
            "Consider reducing parallelization or using simpler transformations"
        )

    # Check fallbacks
    if request.stats.fallbacks:
        overlays.append(f"🔄 Fallbacks: {', '.join(request.stats.fallbacks)}")
        severity = "warning"
        recommendations.append("Review parallelization settings")

    # Check warnings
    if request.stats.warnings:
        overlays.append(f"⚠️ Warnings: {', '.join(request.stats.warnings)}")
        severity = "error"
        recommendations.append("Check code complexity and optimization settings")

    # Check memory usage
    if request.stats.memory_mb and request.stats.memory_mb > 100:
        overlays.append(f"💾 High memory: {request.stats.memory_mb:.1f}MB")
        severity = "warning"
        recommendations.append("Consider reducing data size or using streaming")

    return OverlayResponse(
        overlays=overlays, severity=severity, recommendations=recommendations
    )


# === UTILITY FUNCTIONS ===


def get_nested_value(obj: Dict[str, Any], path: str) -> Any:
    """Get nested value from dictionary using dot notation."""
    keys = path.split(".")
    current = obj
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return 0
    return current


def set_nested_value(obj: Dict[str, Any], path: str, value: Any) -> None:
    """Set nested value in dictionary using dot notation."""
    keys = path.split(".")
    current = obj
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def interpolate_states(
    state_a: Dict[str, Any], state_b: Dict[str, Any], t: float
) -> Dict[str, Any]:
    """Interpolate between two states."""
    result = {}
    for key in set(state_a.keys()) | set(state_b.keys()):
        val_a = state_a.get(key, 0)
        val_b = state_b.get(key, 0)
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            result[key] = val_a + (val_b - val_a) * t
        else:
            result[key] = val_b if t > 0.5 else val_a
    return result


def quantize_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """Quantize state values to grid."""
    result = {}
    for key, value in state.items():
        if isinstance(value, (int, float)):
            result[key] = round(value / 0.25) * 0.25
        else:
            result[key] = value
    return result


async def coalesce_requests(requests: List[RenderRequest]) -> List[RenderRequest]:
    """Coalesce similar requests to reduce processing."""
    # Simple coalescing: group by Python code
    groups = {}
    for req in requests:
        key = req.python
        if key not in groups:
            groups[key] = []
        groups[key].append(req)

    # Return one request per group (could be more sophisticated)
    return [group[0] for group in groups.values()]
