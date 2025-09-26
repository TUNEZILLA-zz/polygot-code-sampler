"""
Julia renderer for Polyglot Code Sampler
"""

from ..core import IRComp
from ..backends.julia import lower_program

def render_julia(ir: IRComp, func_name: str = "program", parallel: bool = False, mode: str = "auto", explain: bool = True, unsafe: bool = False) -> str:
    """
    Julia backend with broadcast/vectorized support:
      list -> Vector{Int}
      set  -> Set{Int}
      dict -> Dict{Int, Int}
      reductions: sum/max/min -> Int, any/all -> Bool
    Notes:
      - Uses Julia's broadcast syntax (.+) for vectorized operations
      - Supports both loop-based and broadcast-based lowering
      - Threads.@threads for parallel processing
      - Leverages Julia's high-performance array operations
    """
    # Use the new comprehensive Julia backend
    return lower_program(ir, mode=mode, parallel=parallel, explain=explain, unsafe=unsafe)

def _should_use_broadcast(ir: IRComp, gen) -> bool:
    """Determine if broadcast syntax is appropriate"""
    # Use broadcast for simple element-wise operations
    if ir.element and not any(char in ir.element for char in ['if', 'else', 'and', 'or']):
        return True
    # Use loops for complex logic
    return False

def _render_julia_broadcast(ir: IRComp, gen, range_expr: str, parallel: bool) -> list:
    """Render using Julia's broadcast syntax"""
    lines = []
    
    if ir.reduce:
        k = ir.reduce.kind
        if ir.kind == "dict":
            expr = ir.val_expr or "0"
        else:
            expr = ir.element or "0"
        
        # Create the range
        lines.append(f"    {gen.var} = {range_expr}")
        
        # Apply filters using broadcast
        for filter_expr in gen.filters:
            lines.append(f"    mask = {filter_expr}")
            lines.append(f"    {gen.var} = {gen.var}[mask]")
        
        # Apply the reduction
        if k == "sum":
            lines.append(f"    return sum({expr})")
        elif k == "max":
            lines.append(f"    return maximum({expr})")
        elif k == "min":
            lines.append(f"    return minimum({expr})")
        elif k == "any":
            lines.append(f"    return any({expr})")
        elif k == "all":
            lines.append(f"    return all({expr})")
    else:
        # Collection operations
        lines.append(f"    {gen.var} = {range_expr}")
        
        # Apply filters
        for filter_expr in gen.filters:
            lines.append(f"    mask = {filter_expr}")
            lines.append(f"    {gen.var} = {gen.var}[mask]")
        
        # Apply element transformation
        if ir.kind == "list":
            if ir.element:
                lines.append(f"    return {ir.element}")
            else:
                lines.append(f"    return collect({gen.var})")
        elif ir.kind == "set":
            if ir.element:
                lines.append(f"    return Set({ir.element})")
            else:
                lines.append(f"    return Set({gen.var})")
        elif ir.kind == "dict":
            key_expr = ir.key_expr or "0"
            val_expr = ir.val_expr or "0"
            lines.append(f"    return Dict({key_expr} => {val_expr} for {gen.var} in {gen.var})")
    
    return lines

def _render_julia_loop(ir: IRComp, gen, range_expr: str, parallel: bool) -> list:
    """Render using explicit loops"""
    lines = []
    
    # Initialize result
    if ir.reduce:
        k = ir.reduce.kind
        if k == "sum":
            lines.append("    result = 0")
        elif k == "max":
            lines.append("    result = typemin(Int)")
        elif k == "min":
            lines.append("    result = typemax(Int)")
        elif k == "any":
            lines.append("    result = false")
        elif k == "all":
            lines.append("    result = true")
    else:
        if ir.kind == "list":
            lines.append("    result = Int[]")
        elif ir.kind == "set":
            lines.append("    result = Set{Int}()")
        elif ir.kind == "dict":
            lines.append("    result = Dict{Int, Int}()")
    
    # Add parallel prefix if requested
    loop_prefix = "    @threads " if parallel else "    "
    
    # Create the loop
    lines.append(f"{loop_prefix}for {gen.var} in {range_expr}")
    
    # Add filters as if statements
    for filter_expr in gen.filters:
        lines.append(f"        if !({filter_expr})")
        lines.append("            continue")
        lines.append("        end")
    
    # Add the body
    if ir.reduce:
        k = ir.reduce.kind
        if ir.kind == "dict":
            expr = ir.val_expr or "0"
        else:
            expr = ir.element or "0"
        
        if k == "sum":
            lines.append(f"        result += {expr}")
        elif k == "max":
            lines.append(f"        result = max(result, {expr})")
        elif k == "min":
            lines.append(f"        result = min(result, {expr})")
        elif k == "any":
            lines.append(f"        if {expr}")
            lines.append("            result = true")
            lines.append("        end")
        elif k == "all":
            lines.append(f"        if !({expr})")
            lines.append("            result = false")
            lines.append("        end")
    else:
        # Collection operations
        if ir.kind == "list":
            if ir.element:
                lines.append(f"        push!(result, {ir.element})")
            else:
                lines.append(f"        push!(result, {gen.var})")
        elif ir.kind == "set":
            if ir.element:
                lines.append(f"        push!(result, {ir.element})")
            else:
                lines.append(f"        push!(result, {gen.var})")
        elif ir.kind == "dict":
            key_expr = ir.key_expr or "0"
            val_expr = ir.val_expr or "0"
            lines.append(f"        result[{key_expr}] = {val_expr}")
    
    lines.append("    end")
    lines.append("    return result")
    
    return lines
