"""
Centralized strategy selection for Julia code generation
"""

from typing import Tuple, Optional
from ...core import IRComp, IRGenerator
from .associativity import is_associative, get_parallel_note, get_associativity_explanation

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
    
    # 1) Mode selection
    if user_mode in ("loops", "broadcast"):
        mode = user_mode
        mode_explanation = ""
    else:
        # Auto mode heuristics
        small = (elem_count_hint or 0) <= 10_000
        no_filters = not any(gen.filters for gen in node.generators)
        
        if small and no_filters and (node.kind in {"list", "set"} or node.reduce):
            mode = "broadcast"
            mode_explanation = f"# NOTE: auto-selected broadcast mode for small N={elem_count_hint}"
        else:
            mode = "loops"
            mode_explanation = f"# NOTE: auto-selected loops mode for {node.kind} operation"
    
    # 2) Parallelization gate
    assoc_ok = is_associative(op_kind, elem_type) if op_kind else False
    # Dict/group operations are always parallelizable if requested (no associativity needed)
    dict_ok = node.kind in {"dict", "group_by"}
    can_parallel = bool(parallel_requested and (assoc_ok or dict_ok) and _has_no_cross_iteration_deps(node))
    
    # 3) Parallel flavor selection
    if node.kind in {"dict", "group_by"}:
        parallel_flavor = "sharded" if can_parallel else "sequential"
        mode = "loops"  # force loops for dict/group operations
        if can_parallel:
            parallel_explanation = "# NOTE: parallelized with shard-merge pattern (thread-local writes)"
        else:
            parallel_explanation = ""
    else:
        parallel_flavor = "threadlocals" if can_parallel else "sequential"
        if can_parallel:
            parallel_explanation = "# NOTE: parallelized with thread-local partials"
        else:
            parallel_explanation = ""
    
    # 4) Fallback explanations
    if parallel_requested and not can_parallel:
        if not assoc_ok and not dict_ok:
            parallel_explanation = get_parallel_note(op_kind, elem_type)
        elif not _has_no_cross_iteration_deps(node):
            parallel_explanation = "# NOTE: parallel fallback → sequential: cross-iteration dependencies detected"
    
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
    """Estimate element count for strategy selection with cost model"""
    if not node.generators:
        return None
    
    gen = node.generators[0]
    
    # Try to get size hint from node attributes first
    if hasattr(node, 'range_len'):
        return node.range_len
    
    # Simple range estimation
    if hasattr(gen.source, 'start') and hasattr(gen.source, 'stop'):
        return gen.source.stop - gen.source.start
    
    return None

def size_hint(node: IRComp) -> Optional[int]:
    """Cost model hook for size estimation"""
    # Try to propagate |range|, filter selectivity, etc.
    if hasattr(node, "range_len"): 
        return node.range_len
    
    # Estimate from generators
    if node.generators:
        gen = node.generators[0]
        if hasattr(gen.source, 'start') and hasattr(gen.source, 'stop'):
            base_size = gen.source.stop - gen.source.start
            
            # Apply filter selectivity estimate
            if gen.filters:
                # Conservative estimate: filters reduce size by ~50%
                return int(base_size * 0.5)
            return base_size
    
    return None  # unknown

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
