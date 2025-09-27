# server/contracts.py - FastAPI contracts and models
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

# === ENUMS ===


class BackendType(str, Enum):
    RUST = "rust"
    JULIA = "julia"
    SQL = "sql"
    TYPESCRIPT = "ts"
    GO = "go"
    CSHARP = "csharp"


class ModeType(str, Enum):
    AUTO = "auto"
    LOOPS = "loops"
    BROADCAST = "broadcast"


class ComparisonOp(str, Enum):
    GT = ">"
    LT = "<"
    EQ = "=="
    GTE = ">="
    LTE = "<="


# === CORE MODELS ===


class Track(BaseModel):
    backend: BackendType
    level: float = Field(ge=0, le=1, description="Fader level 0-1")
    mode: ModeType = ModeType.AUTO
    parallel: bool = False
    unsafe: bool = False
    muted: bool = False
    soloed: bool = False
    pan: float = Field(ge=-1, le=1, description="Pan position -1 to 1")


class MacroKnob(BaseModel):
    performance: float = Field(ge=0, le=1, default=0.5)
    safety: float = Field(ge=0, le=1, default=0.5)
    chaos: float = Field(ge=0, le=1, default=0.0)
    energy: float = Field(ge=0, le=1, default=0.5)


class Effects(BaseModel):
    predicate_pushdown: bool = False
    constant_folding: bool = False
    type_inference: bool = False
    parallel_safety: bool = True


class Policy(BaseModel):
    grace_days: int = Field(ge=0, le=30, default=3)
    thresholds: dict[str, float] = Field(default_factory=dict)
    max_gen_time_ms: int = Field(ge=100, le=5000, default=1000)


# === REQUEST/RESPONSE MODELS ===


class RenderRequest(BaseModel):
    python: str = Field(..., min_length=1, max_length=10000)
    tracks: list[Track]
    effects: Effects = Field(default_factory=Effects)
    policy: Policy = Field(default_factory=Policy)
    quantize: bool = False
    quantize_grid: float = Field(ge=0.01, le=1.0, default=0.25)


class PerformanceStats(BaseModel):
    gen_ms: float
    loc: int
    fallbacks: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    memory_mb: Optional[float] = None


class RenderResult(BaseModel):
    backend: BackendType
    code: str
    stats: PerformanceStats
    success: bool = True
    error: Optional[str] = None


class RenderResponse(BaseModel):
    results: list[RenderResult]
    total_gen_ms: float
    quantized: bool = False


# === SIDECHAIN RULES ===


class Metric(BaseModel):
    path: str = Field(..., regex=r"^[a-zA-Z_][a-zA-Z0-9_.]*$")
    op: ComparisonOp
    value: float


class Action(BaseModel):
    target: str = Field(..., regex=r"^[a-zA-Z_][a-zA-Z0-9_.]*$")
    delta: float = Field(ge=-1, le=1)


class Rule(BaseModel):
    when: Metric
    then: Action
    enabled: bool = True


class SidechainRequest(BaseModel):
    rules: list[Rule]
    metrics: dict[str, Any]
    current_state: dict[str, Any]


class SidechainResponse(BaseModel):
    updated_state: dict[str, Any]
    triggered_rules: list[str]


# === KEYFRAME & TIMELINE ===


class Keyframe(BaseModel):
    t: float = Field(ge=0, le=100)
    state: dict[str, Any]
    easing: Literal["linear", "exp", "s"] = "linear"


class TimelineRequest(BaseModel):
    keyframes: list[Keyframe]
    current_time: float = Field(ge=0, le=100)
    quantize: bool = False


class TimelineResponse(BaseModel):
    interpolated_state: dict[str, Any]
    active_keyframes: list[str]


# === PRESET MANAGEMENT ===


class Preset(BaseModel):
    version: str = "1.0"
    name: str = Field(..., min_length=1, max_length=100)
    state: dict[str, Any]
    notes: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class PresetListResponse(BaseModel):
    presets: list[Preset]
    total: int


class PresetRequest(BaseModel):
    name: str
    state: dict[str, Any]
    notes: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


# === MIDI MAPPING ===


class MidiMap(BaseModel):
    cc: int = Field(ge=0, le=127)
    target: str = Field(..., regex=r"^[a-zA-Z_][a-zA-Z0-9_.]*$")
    enabled: bool = True


class MidiRequest(BaseModel):
    cc: int = Field(ge=0, le=127)
    value: int = Field(ge=0, le=127)
    mappings: list[MidiMap]


class MidiResponse(BaseModel):
    updated_state: dict[str, Any]
    triggered_mappings: list[str]


# === PROJECT MANAGEMENT ===


class Project(BaseModel):
    project_version: str = "1.0"
    python_source: str
    clips: list[dict[str, Any]] = Field(default_factory=list)
    keyframes: list[Keyframe] = Field(default_factory=list)
    rules: list[Rule] = Field(default_factory=list)
    midi_map: list[MidiMap] = Field(default_factory=list)
    history: list[dict[str, Any]] = Field(default_factory=list)


class ProjectRequest(BaseModel):
    python_source: str
    name: Optional[str] = None


class ProjectResponse(BaseModel):
    project: Project
    success: bool = True
    error: Optional[str] = None


# === GLITCH MODE ===


class GlitchRequest(BaseModel):
    intensity: float = Field(ge=0, le=1, default=0.5)
    seed: Optional[int] = None
    safe_mode: bool = True


class GlitchResponse(BaseModel):
    glitched_state: dict[str, Any]
    seed_used: int
    safe_applied: bool


# === A/B COMPARE ===


class ABCompareRequest(BaseModel):
    state_a: dict[str, Any]
    state_b: dict[str, Any]
    active: Literal["a", "b"] = "a"


class ABCompareResponse(BaseModel):
    active_state: dict[str, Any]
    diff_summary: dict[str, Any]


# === PERFORMANCE OVERLAYS ===


class OverlayRequest(BaseModel):
    backend: BackendType
    stats: PerformanceStats


class OverlayResponse(BaseModel):
    overlays: list[str]
    severity: Literal["info", "warning", "error"]
    recommendations: list[str] = Field(default_factory=list)


# === BATCH OPERATIONS ===


class BatchRenderRequest(BaseModel):
    requests: list[RenderRequest]
    coalesce: bool = True
    max_wait_ms: int = Field(ge=100, le=2000, default=500)


class BatchRenderResponse(BaseModel):
    results: list[RenderResponse]
    total_time_ms: float
    coalesced: bool


# === TELEMETRY ===


class TelemetryEvent(BaseModel):
    event_type: str
    timestamp: float
    data: dict[str, Any]
    session_id: Optional[str] = None


class TelemetryRequest(BaseModel):
    events: list[TelemetryEvent]
    opt_in: bool = True


# === VALIDATION HELPERS ===


def validate_python_syntax(code: str) -> bool:
    """Validate Python syntax for the input code."""
    try:
        compile(code, "<string>", "eval")
        return True
    except SyntaxError:
        return False


def validate_backend_support(backend: BackendType) -> bool:
    """Check if backend is supported."""
    return backend in [
        BackendType.RUST,
        BackendType.JULIA,
        BackendType.SQL,
        BackendType.TYPESCRIPT,
    ]


def validate_sidechain_rule(rule: Rule) -> bool:
    """Validate sidechain rule logic."""
    # Check if target path is valid
    if "." not in rule.then.target:
        return False

    # Check if metric path is valid
    if "." not in rule.when.path:
        return False

    return True


# === ERROR MODELS ===


class APIError(BaseModel):
    error: str
    code: str
    details: Optional[dict[str, Any]] = None


class ValidationError(APIError):
    error: str = "Validation Error"
    code: str = "VALIDATION_ERROR"


class RenderError(APIError):
    error: str = "Render Error"
    code: str = "RENDER_ERROR"


class BackendError(APIError):
    error: str = "Backend Error"
    code: str = "BACKEND_ERROR"
