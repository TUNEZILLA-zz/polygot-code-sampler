"""
TypeScript renderer for Polyglot Code Sampler
"""

from ..core import IRComp

def render_ts(ir: IRComp, func_name: str = "program", parallel: bool = False) -> str:
    """
    TypeScript backend with Web Workers parallel support:
      list -> number[]
      set  -> Set<number>
      dict -> Map<number, number>
      reductions: sum/max/min -> number, any/all -> boolean
    Notes:
      - Uses Web Workers for parallel processing
      - Type-safe with TypeScript types
      - Functional array methods
    """
    
    # Determine return type
    if ir.reduce:
        k = ir.reduce.kind
        if k in ("sum", "prod", "max", "min"):
            return_type = "number"
        elif k in ("any", "all"):
            return_type = "boolean"
        else:
            return_type = "number"
    else:
        if ir.kind == "list":
            return_type = "number[]"
        elif ir.kind == "set":
            return_type = "Set<number>"
        elif ir.kind == "dict":
            return_type = "Map<number, number>"
        else:
            return_type = "number[]"
    
    if parallel:
        return _render_ts_parallel(ir, func_name, return_type)
    
    # Build the functional chain
    lines = []
    
    # Function signature
    lines.append(f"function {func_name}(): {return_type} {{")
    
    # Build the source range
    if len(ir.generators) == 1 and hasattr(ir.generators[0].source, 'start'):
        gen = ir.generators[0]
        start, stop, step = gen.source.start, gen.source.stop, gen.source.step
        
        if step == 1:
            source = f"Array.from({{length: {stop - start}}}, (_, i) => {start} + i)"
        else:
            source = f"Array.from({{length: Math.ceil(({stop} - {start}) / {step})}}, (_, i) => {start} + i * {step})"
        
        # Build the functional chain
        chain = source
        
        # Add filters
        for filter_expr in gen.filters:
            chain += f".filter({gen.var} => {filter_expr})"
        
        # Add the final operation
        if ir.reduce:
            k = ir.reduce.kind
            if ir.kind == "dict":
                expr = ir.val_expr or "0"
            else:
                expr = ir.element or "0"
            
            if k == "sum":
                chain += f".reduce((acc, {gen.var}) => acc + ({expr}), 0)"
            elif k == "max":
                chain += f".reduce((acc, {gen.var}) => Math.max(acc, {expr}), -Infinity)"
            elif k == "min":
                chain += f".reduce((acc, {gen.var}) => Math.min(acc, {expr}), Infinity)"
            elif k == "any":
                chain += f".some({gen.var} => {expr})"
            elif k == "all":
                chain += f".every({gen.var} => {expr})"
        else:
            # Collection operations
            if ir.kind == "list":
                if ir.element:
                    chain += f".map({gen.var} => {ir.element})"
                # Already an array
            elif ir.kind == "set":
                if ir.element:
                    chain += f".map({gen.var} => {ir.element})"
                chain += ".reduce((set, val) => set.add(val), new Set<number>())"
            elif ir.kind == "dict":
                key_expr = ir.key_expr or "0"
                val_expr = ir.val_expr or "0"
                chain += f".reduce((map, {gen.var}) => map.set({key_expr}, {val_expr}), new Map<number, number>())"
        
        lines.append(f"    return {chain};")
    
    else:
        # Handle nested comprehensions (more complex)
        lines.append("    // Complex nested comprehension - simplified for demo")
        lines.append("    return [];")
    
    lines.append("}")
    
    return "\n".join(lines)

def _render_ts_parallel(ir: IRComp, func_name: str, return_type: str) -> str:
    """TypeScript parallel renderer using Web Workers"""
    
    lines = []
    
    # Worker code
    worker_code = f"""
const workerCode = `
self.onmessage = function(e) {{
    const {{ start, end, step, filters, element, reduce }} = e.data;
    const results = [];
    
    for (let i = start; i < end; i += step) {{
        let {ir.generators[0].var if ir.generators else 'x'} = i;
        
        // Apply filters
        let passed = true;
        {chr(10).join([f'        if (!({f})) {{ passed = false; break; }}' for f in (ir.generators[0].filters if ir.generators else [])])}
        
        if (passed) {{
            {f'results.push({ir.element if ir.element else ir.generators[0].var if ir.generators else "i"});' if not ir.reduce else f'results.push({ir.element if ir.element else ir.generators[0].var if ir.generators else "i"});'}
        }}
    }}
    
    self.postMessage(results);
}};
`;
"""
    
    lines.append(worker_code)
    
    # Main function
    lines.append(f"function {func_name}(): Promise<{return_type}> {{")
    lines.append("    return new Promise((resolve) => {")
    lines.append("        const numWorkers = navigator.hardwareConcurrency || 4;")
    lines.append("        const chunkSize = Math.ceil(1000000 / numWorkers);")
    lines.append("        const workers: Worker[] = [];")
    lines.append("        const results: any[] = [];")
    lines.append("        let completed = 0;")
    lines.append("")
    lines.append("        for (let i = 0; i < numWorkers; i++) {")
    lines.append("            const worker = new Worker(URL.createObjectURL(new Blob([workerCode], {type: 'application/javascript'})));")
    lines.append("            const start = i * chunkSize;")
    lines.append("            const end = Math.min((i + 1) * chunkSize, 1000000);")
    lines.append("")
    lines.append("            worker.postMessage({")
    lines.append("                start,")
    lines.append("                end,")
    lines.append("                step: 1,")
    lines.append(f"                filters: {ir.generators[0].filters if ir.generators else []},")
    lines.append(f"                element: '{ir.element if ir.element else 'x'}',")
    lines.append(f"                reduce: '{ir.reduce.kind if ir.reduce else 'null'}'")
    lines.append("            });")
    lines.append("")
    lines.append("            worker.onmessage = (e) => {")
    lines.append("                results.push(...e.data);")
    lines.append("                completed++;")
    lines.append("                if (completed === numWorkers) {")
    lines.append("                    workers.forEach(w => w.terminate());")
    if ir.reduce and ir.reduce.kind == "sum":
        lines.append("                    resolve(results.reduce((a, b) => a + b, 0));")
    else:
        lines.append("                    resolve(results);")
    lines.append("                }")
    lines.append("            };")
    lines.append("            workers.push(worker);")
    lines.append("        }")
    lines.append("    });")
    lines.append("}")
    
    return "\n".join(lines)
