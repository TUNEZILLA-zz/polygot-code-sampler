"""
Rust renderer for Polyglot Code Sampler
"""

from ..core import IRComp

def render_rust(ir: IRComp, func_name: str = "program", parallel: bool = False, int_type: str = "i32") -> str:
    """
    Rust backend with Rayon parallel support:
      list -> Vec<i32>
      set  -> HashSet<i32>
      dict -> HashMap<i32, i32>
      reductions: sum/max/min -> i32, any/all -> bool
    Notes:
      - Uses Rayon for parallel processing
      - Type-safe with compile-time guarantees
      - Iterator chains for functional style
    """
    
    # Determine return type
    if ir.reduce:
        k = ir.reduce.kind
        if k in ("sum", "prod", "max", "min"):
            return_type = int_type
        elif k in ("any", "all"):
            return_type = "bool"
        else:
            return_type = int_type
    else:
        if ir.kind == "list":
            return_type = f"Vec<{int_type}>"
        elif ir.kind == "set":
            return_type = f"HashSet<{int_type}>"
        elif ir.kind == "dict":
            return_type = f"HashMap<{int_type}, {int_type}>"
        else:
            return_type = f"Vec<{int_type}>"
    
    # Build the iterator chain
    lines = []
    
    # Add imports
    lines.append("use std::collections::{HashMap, HashSet};")
    if parallel:
        lines.append("use rayon::prelude::*;")
    lines.append("")
    
    # Function signature
    lines.append(f"fn {func_name}() -> {return_type} {{")
    
    # Build the source range
    if len(ir.generators) == 1 and hasattr(ir.generators[0].source, 'start'):
        gen = ir.generators[0]
        start, stop, step = gen.source.start, gen.source.stop, gen.source.step
        
        if step == 1:
            source = f"({start}..{stop})"
        else:
            source = f"({start}..{stop}).step_by({step})"
        
        # Add parallel prefix if requested
        if parallel:
            source = f"{source}.into_par_iter()"
        
        # Build the iterator chain
        chain = source
        
        # Add filters
        for filter_expr in gen.filters:
            chain += f".filter(|&{gen.var}| {filter_expr})"
        
        # Add the final operation
        if ir.reduce:
            k = ir.reduce.kind
            if ir.kind == "dict":
                expr = ir.val_expr or "0"
            else:
                expr = ir.element or "0"
            
            if k == "sum":
                chain += f".map(|{gen.var}| {expr}).sum()"
            elif k == "max":
                chain += f".map(|{gen.var}| {expr}).max().unwrap_or(0)"
            elif k == "min":
                chain += f".map(|{gen.var}| {expr}).min().unwrap_or(0)"
            elif k == "any":
                chain += f".any(|{gen.var}| {expr})"
            elif k == "all":
                chain += f".all(|{gen.var}| {expr})"
        else:
            # Collection operations
            if ir.kind == "list":
                if ir.element:
                    chain += f".map(|{gen.var}| {ir.element})"
                chain += ".collect()"
            elif ir.kind == "set":
                if ir.element:
                    chain += f".map(|{gen.var}| {ir.element})"
                chain += ".collect()"
            elif ir.kind == "dict":
                key_expr = ir.key_expr or "0"
                val_expr = ir.val_expr or "0"
                chain += f".map(|{gen.var}| ({key_expr}, {val_expr})).collect()"
        
        lines.append(f"    {chain}")
    
    else:
        # Handle nested comprehensions (more complex)
        lines.append("    // Complex nested comprehension - simplified for demo")
        lines.append("    vec![]")
    
    lines.append("}")
    
    return "\n".join(lines)
