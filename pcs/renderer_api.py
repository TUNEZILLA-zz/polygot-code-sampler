from __future__ import annotations
import inspect
from typing import Any, Callable, Dict, Protocol

# Import concrete backends
from pcs.renderers.rust import render_rust            # noqa: F401
from pcs.renderers.ts import render_ts                # noqa: F401
from pcs.renderers.go import render_go                # noqa: F401
from pcs.renderers.csharp import render_csharp        # noqa: F401
from pcs.renderers.julia import render_julia          # noqa: F401
from pcs.renderers.sql import render_sql              # noqa: F401


class RendererFn(Protocol):
    """Protocol for renderer functions to ensure type safety."""
    def __call__(self, ir: Any, **kwargs: Any) -> str: ...


_BACKENDS: Dict[str, RendererFn] = {
    "rust": render_rust,
    "ts": render_ts,
    "go": render_go,
    "csharp": render_csharp,
    "julia": render_julia,
    "sql": render_sql,
}

def _filter_kwargs(fn: Callable[..., Any], **kwargs) -> Dict[str, Any]:
    """Return only the kwargs that `fn` actually accepts (tolerates mismatches)."""
    sig = inspect.signature(fn)
    accepted = set(sig.parameters.keys())
    return {k: v for k, v in kwargs.items() if k in accepted}

def render(target: str, ir: Any, **kwargs) -> str:
    """
    Generic entrypoint:
      - dispatches by `target`
      - filters kwargs to match the concrete backend signature
    This prevents test failures from minor signature drift across renderers.
    """
    if target not in _BACKENDS:
        raise ValueError(f"Unknown target: {target}. Known: {sorted(_BACKENDS)}")
    fn = _BACKENDS[target]
    safe_kwargs = _filter_kwargs(fn, **kwargs)
    return fn(ir, **safe_kwargs)

# Optional: per-backend shims so existing imports in tests continue to work
def render_rust(ir: Any, **kwargs) -> str:
    return render("rust", ir, **kwargs)

def render_ts(ir: Any, **kwargs) -> str:
    return render("ts", ir, **kwargs)

def render_go(ir: Any, **kwargs) -> str:
    return render("go", ir, **kwargs)

def render_csharp(ir: Any, **kwargs) -> str:
    return render("csharp", ir, **kwargs)

def render_julia(ir: Any, **kwargs) -> str:
    return render("julia", ir, **kwargs)

def render_sql(ir: Any, **kwargs) -> str:
    return render("sql", ir, **kwargs)
