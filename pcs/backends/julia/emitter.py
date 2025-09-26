"""
Julia AST/strings builder with block context manager
"""

from dataclasses import dataclass
from typing import List, Any
import re

@dataclass
class JL:
    """Julia code emitter with indentation and block management"""
    code: List[str]
    indent: int = 0

    def w(self, s: str = ""):
        """Write a line with proper indentation"""
        self.code.append("    " * self.indent + s)

    def block(self, header: str, footer: str = "end"):
        """Create a block context manager"""
        self.w(header)
        self.indent += 1
        return _Block(self, footer)

    def render(self) -> str:
        """Render the complete Julia code"""
        return "\n".join(self.code)

class _Block:
    """Context manager for Julia code blocks"""
    def __init__(self, jl: JL, footer: str):
        self.jl = jl
        self.footer = footer
    
    def __enter__(self):
        return self
    
    def __exit__(self, *exc):
        self.jl.indent -= 1
        self.jl.w(self.footer)

def jl_var(name: str) -> str:
    """Sanitize Julia identifiers"""
    # Replace hyphens with underscores, ensure valid Julia identifier
    sanitized = name.replace("-", "_")
    # Ensure it starts with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', sanitized):
        sanitized = f"_{sanitized}"
    return sanitized

def literal(v: Any) -> str:
    """Convert Python literals to Julia literals"""
    if isinstance(v, bool):
        return "true" if v else "false"
    elif isinstance(v, str):
        return f'"{v}"'
    elif isinstance(v, float):
        return repr(v)
    elif isinstance(v, int):
        return str(v)
    elif isinstance(v, (list, tuple)):
        # Handle simple lists/tuples
        if isinstance(v, tuple):
            return f"({', '.join(literal(x) for x in v)})"
        else:
            return f"[{', '.join(literal(x) for x in v)}]"
    else:
        raise NotImplementedError(f"Unsupported literal type: {type(v)}")

def gensym(prefix: str = "var") -> str:
    """Generate unique Julia symbols"""
    if not hasattr(gensym, "_counter"):
        gensym._counter = 0
    gensym._counter += 1
    return f"{prefix}{gensym._counter}"

def reset_gensym():
    """Reset gensym counter for deterministic output"""
    gensym._counter = 0

def julia_operator(op: str) -> str:
    """Map Python operators to Julia operators"""
    operator_map = {
        "+": "+",
        "-": "-", 
        "*": "*",
        "/": "/",
        "%": "%",
        "**": "^",
        "==": "==",
        "!=": "!=",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "and": "&&",
        "or": "||",
        "not": "!",
    }
    return operator_map.get(op, op)
