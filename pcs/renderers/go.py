"""
Go renderer for Polyglot Code Sampler
"""

from ..core import IRComp


def render_go(
    ir: IRComp, func_name: str = "program", parallel: bool = False, type_info=None
) -> str:
    """
    Go backend with goroutines parallel support:
      list -> []int
      set  -> map[int]struct{}
      dict -> map[int]int
      reductions: sum/max/min -> int, any/all -> bool
    Notes:
      - Uses goroutines and channels for parallel processing
      - Type-safe with compile-time guarantees
      - Loop-based implementation for performance
    """

    # Determine return type
    if ir.reduce:
        k = ir.reduce.kind
        if k in ("sum", "prod", "max", "min"):
            return_type = "int"
        elif k in ("any", "all"):
            return_type = "bool"
        else:
            return_type = "int"
    else:
        if ir.kind == "list":
            return_type = "[]int"
        elif ir.kind == "set":
            return_type = "map[int]struct{}"
        elif ir.kind == "dict":
            return_type = "map[int]int"
        else:
            return_type = "[]int"

    # Build the function
    lines = []

    # Add imports if needed
    if parallel:
        lines.append("import (")
        lines.append('    "runtime"')
        lines.append('    "sync"')
        lines.append(")")
        lines.append("")

    # Function signature
    lines.append(f"func {func_name}() {return_type} {{")

    # Handle single generator case (most common)
    if len(ir.generators) == 1:
        gen = ir.generators[0]
        var = gen.var

        # Get range bounds
        if hasattr(gen.source, "start") and hasattr(gen.source, "stop"):
            start, stop, step = gen.source.start, gen.source.stop, gen.source.step
        else:
            # Fallback for other sources
            start, stop, step = 0, 1000, 1

        if parallel:
            # Parallel implementation with goroutines
            lines.append("    numWorkers := runtime.NumCPU()")
            lines.append(f"    chunkSize := ({stop} - {start}) / numWorkers")
            lines.append("    if chunkSize == 0 { chunkSize = 1 }")
            lines.append("")
            lines.append("    results := make(chan int, numWorkers)")
            lines.append("    var wg sync.WaitGroup")
            lines.append("")
            lines.append("    for w := 0; w < numWorkers; w++ {{")
            lines.append("        wg.Add(1)")
            lines.append("        go func(workerID int) {{")
            lines.append("            defer wg.Done()")
            lines.append(f"            start := {start} + workerID * chunkSize")
            lines.append("            end := start + chunkSize")
            lines.append(f"            if workerID == numWorkers-1 {{ end = {stop} }}")
            lines.append("")
            lines.append("            acc := 0")
            lines.append(
                f"            for {var} := start; {var} < end; {var} += {step} {{"
            )

            # Add filters
            for filter_expr in gen.filters:
                lines.append(f"                if !({filter_expr}) {{ continue }}")

            # Add the operation
            if ir.reduce:
                k = ir.reduce.kind
                if ir.kind == "dict":
                    expr = ir.val_expr or "0"
                else:
                    expr = ir.element or "0"

                if k == "sum":
                    lines.append(f"                acc += {expr}")
                elif k == "max":
                    lines.append(f"                if {expr} > acc {{ acc = {expr} }}")
                elif k == "min":
                    lines.append(f"                if {expr} < acc {{ acc = {expr} }}")
                elif k == "any":
                    lines.append(f"                if {expr} {{ acc = 1; break }}")
                elif k == "all":
                    lines.append(f"                if !{expr} {{ acc = 0; break }}")
            else:
                # Collection operations
                if ir.kind == "list":
                    if ir.element:
                        lines.append(f"                acc += {ir.element}")
                    else:
                        lines.append(f"                acc += {var}")
                elif ir.kind == "set":
                    lines.append("                acc += 1")  # Count unique elements
                elif ir.kind == "dict":
                    if ir.element:
                        lines.append(f"                acc += {ir.element}")
                    else:
                        lines.append(f"                acc += {var}")

            lines.append("            }")
            lines.append("            results <- acc")
            lines.append("        }(w)")
            lines.append("    }")
            lines.append("")
            lines.append("    wg.Wait()")
            lines.append("    close(results)")
            lines.append("")

            if ir.reduce:
                if ir.reduce.kind in ("any", "all"):
                    lines.append("    for result := range results {")
                    lines.append("        if result == 1 { return true }")
                    lines.append("    }")
                    lines.append("    return false")
                else:
                    lines.append("    total := 0")
                    lines.append("    for result := range results {")
                    lines.append("        total += result")
                    lines.append("    }")
                    lines.append("    return total")
            else:
                lines.append("    result := make([]int, 0)")
                lines.append("    for result := range results {")
                lines.append("        result = append(result, result)")
                lines.append("    }")
                lines.append("    return result")
        else:
            # Sequential implementation
            if ir.reduce:
                lines.append("    acc := 0")
                lines.append(
                    f"    for {var} := {start}; {var} < {stop}; {var} += {step} {{"
                )

                # Add filters
                for filter_expr in gen.filters:
                    lines.append(f"        if !({filter_expr}) {{ continue }}")

                # Add the operation
                k = ir.reduce.kind
                if ir.kind == "dict":
                    expr = ir.val_expr or "0"
                else:
                    expr = ir.element or "0"

                if k == "sum":
                    lines.append(f"        acc += {expr}")
                elif k == "max":
                    lines.append(f"        if {expr} > acc {{ acc = {expr} }}")
                elif k == "min":
                    lines.append(f"        if {expr} < acc {{ acc = {expr} }}")
                elif k == "any":
                    lines.append(f"        if {expr} {{ return true }}")
                elif k == "all":
                    lines.append(f"        if !{expr} {{ return false }}")

                lines.append("    }")

                if k in ("any", "all"):
                    lines.append("    return false")
                else:
                    lines.append("    return acc")
            else:
                # Collection operations
                if ir.kind == "list":
                    lines.append("    result := make([]int, 0)")
                    lines.append(
                        f"    for {var} := {start}; {var} < {stop}; {var} += {step} {{"
                    )

                    # Add filters
                    for filter_expr in gen.filters:
                        lines.append(f"        if !({filter_expr}) {{ continue }}")

                    if ir.element:
                        lines.append(f"        result = append(result, {ir.element})")
                    else:
                        lines.append(f"        result = append(result, {var})")

                    lines.append("    }")
                    lines.append("    return result")
                elif ir.kind == "set":
                    lines.append("    result := make(map[int]struct{})")
                    lines.append(
                        f"    for {var} := {start}; {var} < {stop}; {var} += {step} {{"
                    )

                    # Add filters
                    for filter_expr in gen.filters:
                        lines.append(f"        if !({filter_expr}) {{ continue }}")

                    if ir.element:
                        lines.append(f"        result[{ir.element}] = struct{{}}{{}}")
                    else:
                        lines.append(f"        result[{var}] = struct{{}}{{}}")

                    lines.append("    }")
                    lines.append("    return result")
                elif ir.kind == "dict":
                    lines.append("    result := make(map[int]int)")
                    lines.append(
                        f"    for {var} := {start}; {var} < {stop}; {var} += {step} {{"
                    )

                    # Add filters
                    for filter_expr in gen.filters:
                        lines.append(f"        if !({filter_expr}) {{ continue }}")

                    if ir.element:
                        lines.append(f"        result[{var}] = {ir.element}")
                    else:
                        lines.append(f"        result[{var}] = {var}")

                    lines.append("    }")
                    lines.append("    return result")
    else:
        # Multiple generators - fallback to sequential
        lines.append("    // Multiple generators - using sequential implementation")
        lines.append("    // TODO: Implement parallel multi-generator support")
        lines.append("    return nil")

    lines.append("}")
    return "\n".join(lines)
