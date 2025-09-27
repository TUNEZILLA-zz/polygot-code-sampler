"""
Polyglot Code Sampler - Transform Python comprehensions across 5 ecosystems
"""

from .__version__ import __version__
from .cli import main
from .core import IRComp, IRGenerator, IRRange, IRReduce, PyToIR, TypeInfo
from .renderer_api import (
    render,
    render_csharp,
    render_go,
    render_julia,
    render_rust,
    render_sql,
    render_ts,
)

__all__ = [
    "__version__",
    "PyToIR",
    "IRComp",
    "IRRange",
    "IRGenerator",
    "IRReduce",
    "TypeInfo",
    "main",
    "render",
    "render_rust",
    "render_ts",
    "render_go",
    "render_csharp",
    "render_julia",
    "render_sql",
]
