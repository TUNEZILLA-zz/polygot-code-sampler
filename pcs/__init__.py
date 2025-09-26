"""
Polyglot Code Sampler - Transform Python comprehensions across 5 ecosystems
"""

from .__version__ import __version__
from .core import PyToIR, IRComp, IRRange, IRGenerator, IRReduce, TypeInfo
from .cli import main
from .renderers.rust import render_rust
from .renderers.ts import render_ts
from .renderers.csharp import render_csharp
from .renderers.sql import render_sql
from .renderers.julia import render_julia

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
