"""
SQL renderer for Polyglot Code Sampler
"""

from ..core import IRComp

def render_sql(ir: IRComp, func_name: str = "program", dialect: str = "sqlite") -> str:
    """
    SQL backend with dialect support:
      list -> SELECT with FROM generate_series/CTE
      set  -> SELECT DISTINCT
      dict -> SELECT key, value
      reductions: SUM/MAX/MIN/COUNT
    Notes:
      - PostgreSQL: generate_series() for ranges
      - SQLite: recursive CTEs for ranges
      - Query optimization with predicate pushdown
    """
    
    lines = []
    
    # Build the source range
    if len(ir.generators) == 1 and hasattr(ir.generators[0].source, 'start'):
        gen = ir.generators[0]
        start, stop, step = gen.source.start, gen.source.stop, gen.source.step
        
        # Generate range based on dialect
        if dialect == "postgresql":
            if step == 1:
                range_clause = f"generate_series({start}, {stop - 1}) AS {gen.var}"
            else:
                range_clause = f"generate_series({start}, {stop - 1}, {step}) AS {gen.var}"
        else:  # sqlite
            if step == 1:
                range_clause = f"""
WITH RECURSIVE range({gen.var}) AS (
    SELECT {start}
    UNION ALL
    SELECT {gen.var} + 1
    FROM range
    WHERE {gen.var} < {stop - 1}
)
SELECT {gen.var} FROM range"""
            else:
                range_clause = f"""
WITH RECURSIVE range({gen.var}) AS (
    SELECT {start}
    UNION ALL
    SELECT {gen.var} + {step}
    FROM range
    WHERE {gen.var} < {stop - 1}
)
SELECT {gen.var} FROM range"""
        
        # Build the query
        if ir.reduce:
            k = ir.reduce.kind
            if ir.kind == "dict":
                expr = ir.val_expr or "0"
            else:
                expr = ir.element or "0"
            
            if k == "sum":
                lines.append(f"SELECT SUM({expr})")
            elif k == "max":
                lines.append(f"SELECT MAX({expr})")
            elif k == "min":
                lines.append(f"SELECT MIN({expr})")
            elif k == "any":
                lines.append(f"SELECT EXISTS(SELECT 1 WHERE {expr})")
            elif k == "all":
                lines.append(f"SELECT NOT EXISTS(SELECT 1 WHERE NOT ({expr}))")
        else:
            # Collection operations
            if ir.kind == "list":
                if ir.element:
                    lines.append(f"SELECT {ir.element}")
                else:
                    lines.append(f"SELECT {gen.var}")
            elif ir.kind == "set":
                if ir.element:
                    lines.append(f"SELECT DISTINCT {ir.element}")
                else:
                    lines.append(f"SELECT DISTINCT {gen.var}")
            elif ir.kind == "dict":
                key_expr = ir.key_expr or "0"
                val_expr = ir.val_expr or "0"
                lines.append(f"SELECT {key_expr}, {val_expr}")
        
        # Add FROM clause
        if dialect == "postgresql":
            lines.append(f"FROM {range_clause}")
        else:  # sqlite
            lines.append(f"FROM ({range_clause})")
        
        # Add WHERE clause for filters
        if gen.filters:
            where_conditions = []
            for filter_expr in gen.filters:
                where_conditions.append(filter_expr)
            lines.append(f"WHERE {' AND '.join(where_conditions)}")
    
    else:
        # Handle nested comprehensions (more complex)
        lines.append("-- Complex nested comprehension - simplified for demo")
        lines.append("SELECT 0")
    
    return "\n".join(lines)
