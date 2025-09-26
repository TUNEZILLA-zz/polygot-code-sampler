"""
Polyglot Code Sampler - Transform Python comprehensions across 5 ecosystems
"""

from .__version__ import __version__
from .cli import main
from .core import IRComp, IRGenerator, IRRange, IRReduce, PyToIR, TypeInfo
from .renderers.csharp import render_csharp
from .renderers.julia import render_julia
from .renderers.rust import render_rust
from .renderers.sql import render_sql
from .renderers.ts import render_ts

__all__ = [
    "__version__",
    "PyToIR",
    "IRComp",
    "IRRange",
    "IRGenerator",
    "IRReduce",
    "TypeInfo",
    "main",
    "render_rust",
    "render_ts",
    "render_csharp",
    "render_sql",
    "render_julia"
]
