"""
Centralized strategy selection for Julia code generation
"""

from typing import Tuple, Optional
from ...core import IRComp, IRGenerator

# Associativity whitelist for safe parallelization
ASSOCIATIVE_OPS = {
    "sum": ("Int", "Float64"),  # sum reduction
    "prod": ("Int", "Float64"),  # product reduction
    "max": ("Int", "Float64"),
    "min": ("Int", "Float64"),
    "+": ("Int", "Float64"),  # addition operator
    "*": ("Int", "Float64"),  # multiplication operator
    "|": ("Int",),  # bitwise OR
    "&": ("Int",),  # bitwise AND
    "^": ("Int",),  # bitwise XOR
}

def choose_strategy(
    node: IRComp, 
    *,
    user_mode: str,
    elem_count_hint: Optional[int],
    op_kind: Optional[str],
    elem_type: str = "Int",
    parallel_requested: bool,
    explain: bool = True
) -> Tuple[str, str, str]:
    """
    Centralized strategy selection for Julia code generation
    
    Returns:
        (mode, parallel_flavor, explanation)
        - mode: "loops" or "broadcast"
        - parallel_flavor: "sequential", "threadlocals", or "sharded"
        - explanation: NOTE comment explaining the decision
    """
    
    # 1) Respect explicit user mode
    if user_mode in ("loops", "broadcast"):
        mode = user_mode
        mode_explanation = ""
    else:
        # Heuristics when auto:
        # - small vectors → broadcast for clarity
        # - filters + large N → loops to avoid allocations
        # - dict/group/join → loops (broadcast rarely helps)
        if (elem_count_hint and elem_count_hint <= 10_000 and 
            (node.kind in ("list", "set") or node.reduce) and 
            not any(gen.filters for gen in node.generators)):
            mode = "broadcast"
            mode_explanation = f"# NOTE: auto-selected broadcast mode for small N={elem_count_hint}"
        else:
            mode = "loops"
            mode_explanation = f"# NOTE: auto-selected loops mode for {node.kind} operation"
    
    # 2) Parallelization gate
    can_parallel = (
        parallel_requested
        and op_kind in ASSOCIATIVE_OPS
        and elem_type in ASSOCIATIVE_OPS[op_kind]
        and _has_no_cross_iteration_deps(node)
    )
    
    # 3) Dict/group safety
    if node.kind in {"dict", "group_by"} and can_parallel:
        parallel_flavor = "sharded"  # per-thread shards + merge
        parallel_explanation = "# NOTE: dict/group parallelized with shard-merge pattern (thread-local writes)"
    elif can_parallel:
        parallel_flavor = "threadlocals"  # parts[threadid()] pattern
        parallel_explanation = "# NOTE: parallelized with thread-local partials"
    else:
        parallel_flavor = "sequential"
        if parallel_requested and op_kind and op_kind not in ASSOCIATIVE_OPS:
            parallel_explanation = f"# NOTE: parallel fallback → sequential: non-associative op '{op_kind}'"
        elif parallel_requested and elem_type not in ASSOCIATIVE_OPS.get(op_kind, ()):
            parallel_explanation = f"# NOTE: parallel fallback → sequential: type '{elem_type}' not supported for '{op_kind}'"
        elif parallel_requested and not _has_no_cross_iteration_deps(node):
            parallel_explanation = "# NOTE: parallel fallback → sequential: cross-iteration dependencies detected"
        else:
            parallel_explanation = ""
    
    # Combine explanations
    explanations = [e for e in [mode_explanation, parallel_explanation] if e]
    explanation = "\n".join(explanations) if explanations and explain else ""
    
    return mode, parallel_flavor, explanation

def _has_no_cross_iteration_deps(node: IRComp) -> bool:
    """Check if the node has no cross-iteration dependencies"""
    # For now, assume simple cases are safe
    # TODO: More sophisticated analysis for complex nested operations
    if not node.generators:
        return True
    
    gen = node.generators[0]
    
    # Check for complex expressions that might have dependencies
    if node.element and any(char in node.element for char in ['if', 'else', 'and', 'or']):
        return False
    
    # Check for complex filters
    for filter_expr in gen.filters:
        if any(char in filter_expr for char in ['if', 'else', 'and', 'or']):
            return False
    
    return True

def get_elem_count_hint(node: IRComp) -> Optional[int]:
    """Estimate element count for strategy selection"""
    if not node.generators:
        return None
    
    gen = node.generators[0]
    
    # Simple range estimation
    if hasattr(gen.source, 'start') and hasattr(gen.source, 'stop'):
        return gen.source.stop - gen.source.start
    
    return None

def get_op_kind(node: IRComp) -> Optional[str]:
    """Get the operation kind for strategy selection"""
    if node.reduce:
        return node.reduce.kind
    return None

def get_elem_type(node: IRComp) -> str:
    """Get the element type for strategy selection"""
    # For now, default to Int
    # TODO: More sophisticated type inference
    return "Int"
