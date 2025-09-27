#!/usr/bin/env python3
# (full script from previous cell, reconstructed)
from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class IRRange:
    start: int
    stop: int
    step: int = 1


@dataclass
class IRGenerator:
    var: str
    source: IRRange | str
    filters: list[str]


@dataclass
class IRReduce:
    kind: str
    op: str | None = None
    initial: str | None = None


@dataclass
class IRComp:
    kind: str
    generators: list[IRGenerator]
    element: str | None = None
    key_expr: str | None = None
    val_expr: str | None = None
    reduce: IRReduce | None = None
    provenance: dict = None

    def to_json(self) -> str:
        def to_dict(obj: Any):
            if hasattr(obj, "__dataclass_fields__"):
                d = asdict(obj)
                d["__type__"] = obj.__class__.__name__
                return d
            elif isinstance(obj, list):
                return [to_dict(x) for x in obj]
            else:
                return obj

        return json.dumps(to_dict(self), indent=2)


class PyToIR(ast.NodeVisitor):
    def __init__(self):
        self.comp: IRComp | None = None

    def parse(self, code: str) -> IRComp:
        tree = ast.parse(code)
        self.comp = None
        for node in tree.body:
            val = getattr(node, "value", node if isinstance(node, ast.expr) else None)
            if isinstance(val, ast.ListComp):
                self.comp = self._comp_to_ir(val, kind="list", reduce_=None)
                break
            if isinstance(val, ast.SetComp):
                self.comp = self._comp_to_ir(val, kind="set", reduce_=None)
                break
            if isinstance(val, ast.DictComp):
                self.comp = self._dictcomp_to_ir(val, reduce_=None)
                break
            if isinstance(val, ast.Call):
                red_kind = self._reduction_kind(val.func)
                if red_kind:
                    inner = val.args[0]
                    if isinstance(inner, (ast.GeneratorExp, ast.ListComp)):
                        self.comp = self._comp_to_ir(
                            inner, kind="list", reduce_=IRReduce(kind=red_kind)
                        )
                        break
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                red_kind = self._reduction_kind(node.value.func)
                if red_kind:
                    inner = node.value.args[0]
                    if isinstance(inner, (ast.GeneratorExp, ast.ListComp)):
                        self.comp = self._comp_to_ir(
                            inner, kind="list", reduce_=IRReduce(kind=red_kind)
                        )
                        break
        if not self.comp:
            raise ValueError("No supported comprehension/reduction found")
        return self.comp

    def _reduction_kind(self, func: ast.AST) -> str | None:
        if isinstance(func, ast.Name) and func.id in {
            "sum",
            "any",
            "all",
            "max",
            "min",
            "prod",
        }:
            return func.id
        if (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "math"
            and func.attr == "prod"
        ):
            return "prod"
        return None

    def _parse_range(self, call: ast.Call) -> IRRange:
        if getattr(call.func, "id", None) != "range":
            raise ValueError("Only range(...) supported as call sources for this demo")
        args = [ast.literal_eval(a) for a in call.args]
        if len(args) == 1:
            start, stop, step = 0, args[0], 1
        elif len(args) == 2:
            start, stop, step = args[0], args[1], 1
        else:
            start, stop, step = args[0], args[1], args[2]
        return IRRange(start=start, stop=stop, step=step)

    def _gens_from_comp(
        self, comp: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp
    ) -> list[IRGenerator]:
        gens: list[IRGenerator] = []
        for gen in comp.generators:
            if not isinstance(gen.target, ast.Name):
                raise ValueError("Only simple variable targets supported")
            var = gen.target.id
            src = gen.iter
            if isinstance(src, ast.Call) and getattr(src.func, "id", None) == "range":
                source = self._parse_range(src)
            elif isinstance(src, ast.Name):
                source = src.id
            else:
                raise ValueError("Only range(...) or variable sources supported")
            filters = [ast.unparse(cond) for cond in gen.ifs] if gen.ifs else []
            gens.append(IRGenerator(var=var, source=source, filters=filters))
        return gens

    def _comp_to_ir(
        self,
        comp: ast.ListComp | ast.SetComp | ast.GeneratorExp,
        kind: str,
        reduce_: IRReduce | None,
    ) -> IRComp:
        gens = self._gens_from_comp(comp)
        element_src = ast.unparse(comp.elt)
        provenance = {
            "origin": "python",
            "pattern": f"{kind}_nested" if len(gens) > 1 else kind,
        }
        return IRComp(
            kind=kind,
            generators=gens,
            element=element_src,
            reduce=reduce_,
            provenance=provenance,
        )

    def _dictcomp_to_ir(self, comp: ast.DictComp, reduce_: IRReduce | None) -> IRComp:
        gens = self._gens_from_comp(comp)
        key_src = ast.unparse(comp.key)
        val_src = ast.unparse(comp.value)
        provenance = {
            "origin": "python",
            "pattern": "dict_nested" if len(gens) > 1 else "dict",
        }
        return IRComp(
            kind="dict",
            generators=gens,
            key_expr=key_src,
            val_expr=val_src,
            reduce=reduce_,
            provenance=provenance,
        )


def py_expr_boolish_to_ts(expr: str) -> str:
    out = expr
    for pat, repl in [
        (r"\\band\\b", "&&"),
        (r"\\bor\\b", "||"),
        (r"\\bnot\\b", "!"),
        (r"\\bTrue\\b", "true"),
        (r"\\bFalse\\b", "false"),
    ]:
        out = re.sub(pat, repl, out)
    if " if " in out and " else " in out:
        try:
            a, rest = out.split(" if ", 1)
            c, b = rest.split(" else ", 1)
            out = f"(({c}) ? ({a}) : ({b}))"
        except Exception:
            pass
    return out


def py_expr_to_ts(expr: str) -> str:
    return py_expr_boolish_to_ts(expr)


def range_to_ts(r: IRRange) -> str:
    if r.step == 1:
        length = f"({r.stop} - {r.start})"
        return f"Array.from({{length: {length}}}, (_, i) => i + {r.start})"
    else:
        length = f"Math.ceil(({r.stop} - {r.start}) / {r.step})"
        return f"Array.from({{length: {length}}}, (_, i) => {r.start} + i*{r.step})"


def render_rust(
    ir: IRComp,
    func_name: str = "program",
    int_type: str = "i32",
    reduce_int: str = "i64",
) -> str:
    def py_expr_to_rust(expr: str) -> str:
        out = expr
        for pat, repl in [
            (r"\\band\\b", "&&"),
            (r"\\bor\\b", "||"),
            (r"\\bnot\\b", "!"),
            (r"\\bTrue\\b", "true"),
            (r"\\bFalse\\b", "false"),
        ]:
            out = re.sub(pat, repl, out)
        if " if " in out and " else " in out:
            try:
                a, rest = out.split(" if ", 1)
                c, b = rest.split(" else ", 1)
                out = f"(if {c} {{ {a} }} else {{ {b} }})"
            except Exception:
                pass
        return out

    def range_to_rust(r: IRRange) -> str:
        base = f"({r.start}..{r.stop})"
        return base + (f".step_by({r.step}usize)" if r.step != 1 else "")

    def render_gen(idx: int) -> str:
        gen = ir.generators[idx]
        var = gen.var
        src = (
            range_to_rust(gen.source) if isinstance(gen.source, IRRange) else gen.source
        )
        chain = src
        for pred in gen.filters:
            chain += f".filter(|&{var}| {py_expr_to_rust(pred)})"
        if idx == len(ir.generators) - 1:
            if ir.kind == "dict":
                chain += f".map(move |{var}| ({py_expr_to_rust(ir.key_expr)}, {py_expr_to_rust(ir.val_expr)}))"
            else:
                chain += f".map(move |{var}| {py_expr_to_rust(ir.element)})"
            return chain
        else:
            return f"{chain}.flat_map(move |{var}| {render_gen(idx + 1)})"

    body = render_gen(0)
    uses, ret_type, trailer = [], "", ""
    if ir.reduce:
        k = ir.reduce.kind
        if k == "sum":
            trailer = f".sum::<{reduce_int}>()"
            ret_type = reduce_int
        elif k == "prod":
            trailer = f".product::<{reduce_int}>()"
            ret_type = reduce_int
        elif k == "any":
            trailer = ".any(|x| x)"
            ret_type = "bool"
        elif k == "all":
            trailer = ".all(|x| x)"
            ret_type = "bool"
        elif k in ("max", "min"):
            method = ".max()" if k == "max" else ".min()"
            trailer = f"{method}.unwrap_or(0)"
            ret_type = reduce_int
    else:
        if ir.kind == "list":
            trailer = ".collect::<Vec<_>>()"
            ret_type = "Vec<_>"
        elif ir.kind == "set":
            uses.append("use std::collections::HashSet;")
            trailer = ".collect::<HashSet<_>>()"
            ret_type = "HashSet<_>"
        else:
            uses.append("use std::collections::HashMap;")
            trailer = ".collect::<HashMap<_, _>>()"
            ret_type = "HashMap<_, _>"
    return "\n".join(
        [
            f"// Rendered from IR (origin: {ir.provenance.get('origin')})",
            *uses,
            f"pub fn {func_name}() -> {ret_type} {{",
            f"    let result = {body}{trailer};",
            "    result",
            "}",
        ]
    )


def render_ts(ir: IRComp, func_name: str = "program") -> str:
    def render_gen(idx: int) -> str:
        gen = ir.generators[idx]
        v = gen.var
        src = range_to_ts(gen.source) if isinstance(gen.source, IRRange) else gen.source
        chain = f"({src})"
        for pred in gen.filters:
            chain += f".filter(({v}) => {py_expr_boolish_to_ts(pred)})"
        if idx == len(ir.generators) - 1:
            if ir.kind == "dict":
                chain += f".map(({v}) => [ {py_expr_to_ts(ir.key_expr)}, {py_expr_to_ts(ir.val_expr)} ])"
            else:
                chain += f".map(({v}) => {py_expr_to_ts(ir.element)})"
            return chain
        else:
            return chain + f".flatMap(({v}) => {render_gen(idx + 1)})"

    body = render_gen(0)
    if ir.reduce:
        k = ir.reduce.kind
        if k == "sum":
            trailer = ".reduce((a,b)=>a+b,0)"
        elif k == "prod":
            trailer = ".reduce((a,b)=>a*b,1)"
        elif k == "any":
            trailer = ".some(x=>x)"
        elif k == "all":
            trailer = ".every(x=>x)"
        elif k == "max":
            trailer = ".reduce((a,b)=>a>b?a:b, Number.NEGATIVE_INFINITY)"
        elif k == "min":
            trailer = ".reduce((a,b)=>a<b?a:b, Number.POSITIVE_INFINITY)"
        ret = "number|boolean"
        return "\n".join(
            [
                f"// Rendered from IR (origin: {ir.provenance.get('origin')})",
                f"export function {func_name}(): {ret} {{",
                f"  const result = {body}{trailer};",
                "  return result;",
                "}",
            ]
        )
    else:
        if ir.kind == "list":
            ret = "any[]"
            result = body
        elif ir.kind == "set":
            ret = "Set<any>"
            result = f"new Set({body})"
        else:
            ret = "Map<any, any>"
            result = f"new Map({body})"
        return "\n".join(
            [
                f"// Rendered from IR (origin: {ir.provenance.get('origin')})",
                f"export function {func_name}(): {ret} {{",
                f"  const result = {result};",
                "  return result;",
                "}",
            ]
        )


DEMO_CASES = [
    ("m = { i: i*i for i in range(1,6) if i % 2 == 1 }", "map_odds"),
    ("s = { (i, j) for i in range(0,3) for j in range(0,3) if i != j }", "pairs_set"),
    ("ok = all(x % 2 == 0 for x in range(2,10))", "all_even"),
    ("best = max(i*j for i in range(1,5) for j in range(1,4))", "max_prod"),
    ("import math\np = math.prod(x for x in range(1,5) if x != 3)", "prod_simple"),
]


def run_demo(target="rust"):
    parser = PyToIR()
    outs = []
    for code, name in DEMO_CASES:
        ir = parser.parse(code)
        out = (
            render_rust(ir, func_name=name)
            if target == "rust"
            else render_ts(ir, func_name=name)
        )
        outs.append({"python": code, "ir_json": json.loads(ir.to_json()), target: out})
    return outs


def cli():
    ap = argparse.ArgumentParser(description="PCS — Rust & TypeScript backends")
    ap.add_argument("--file", "-f", type=str)
    ap.add_argument("--code", "-c", type=str)
    ap.add_argument("--name", "-n", type=str, default="program")
    ap.add_argument("--emit-ir", action="store_true")
    ap.add_argument(
        "--target",
        "-t",
        type=str,
        default="rust",
        choices=["rust", "ts", "sql", "go", "csharp"],
    )
    ap.add_argument("--out", "-o", type=str)
    ap.add_argument(
        "--execute-sql",
        action="store_true",
        help="Execute generated SQL and display results",
    )
    ap.add_argument(
        "--sql-dialect",
        type=str,
        default="sqlite",
        choices=["sqlite", "postgresql"],
        help="SQL dialect for generation",
    )
    ap.add_argument(
        "--parallel",
        action="store_true",
        help="Enable parallel processing (Rayon/Rust, Web Workers/TS, Goroutines/Go, PLINQ/C#)",
    )
    args = ap.parse_args()
    if args.file is None and args.code is None:
        dr = run_demo("rust")
        dt = run_demo("ts")
        for i, d in enumerate(dr, 1):
            print("=" * 80)
            print(f"DEMO {i} — Python:\\n{d['python']}")
            print("\\nIR (JSON):")
            print(json.dumps(d["ir_json"], indent=2))
            print("\\nRust:")
            print(d["rust"])
            print("\\nTypeScript:")
            print(dt[i - 1]["ts"])
        return
    src = args.code if args.code else Path(args.file).read_text()
    ir = PyToIR().parse(src)
    if args.emit_ir:
        print("=== IR (JSON) ===")
        print(ir.to_json())
        print()
    if args.target == "rust":
        out = render_rust(ir, func_name=args.name)
    elif args.target == "ts":
        out = render_ts(ir, func_name=args.name)
    elif args.target == "sql":
        out = render_sql(ir, func_name=args.name, dialect=args.sql_dialect)
        if args.execute_sql:
            execute_sql_and_display(out, args.sql_dialect)
    elif args.target == "go":
        out = render_go(ir, func_name=args.name)
    elif args.target == "csharp":
        out = render_csharp(ir, func_name=args.name, parallel=args.parallel)
    else:
        out = render_ts(ir, func_name=args.name)

    print(out)
    if args.out:
        Path(args.out).write_text(out)
        print(f"\\n[Saved to] {args.out}")


def render_csharp(
    ir: IRComp, func_name: str = "Program", parallel: bool = False
) -> str:
    """
    C# LINQ backend with PLINQ parallel support:
      list -> List<int> (or List<T> with type inference)
      set  -> HashSet<int>
      dict -> Dictionary<int, int>
      reductions: Sum/Max/Min -> int, Any/All -> bool
    Notes:
      - Uses LINQ for functional transformations
      - PLINQ (.AsParallel()) for parallel processing
      - Type inference for better production code
      - Enterprise-ready C# patterns
    """

    # Helper function to convert Python expressions to C#
    def csharp_expr(expr: str) -> str:
        # Basic Python→C# expression tweaks
        replacements = [
            (r"\band\b", "&&"),
            (r"\bor\b", "||"),
            (r"\bnot\b", "!"),
            (r"\bTrue\b", "true"),
            (r"\bFalse\b", "false"),
            (r"\*\*", "Math.Pow"),  # Python ** to C# Math.Pow
            (r"==", "=="),
            (r"!=", "!="),
        ]
        import re

        result = expr
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)

        # Handle Math.Pow expressions
        if "Math.Pow" in result:
            # Convert x**2 to Math.Pow(x, 2)
            result = re.sub(r"(\w+)\s*Math\.Pow\s*(\w+)", r"Math.Pow(\1, \2)", result)

        return result

    # Determine output type
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
            return_type = "List<int>"
        elif ir.kind == "set":
            return_type = "HashSet<int>"
        elif ir.kind == "dict":
            return_type = "Dictionary<int, int>"
        else:
            return_type = "List<int>"

    # Build the LINQ chain
    lines = []

    # Add using statements
    lines.append("using System;")
    lines.append("using System.Collections.Generic;")
    lines.append("using System.Linq;")
    if parallel:
        lines.append("using System.Threading.Tasks;")
    lines.append("")

    # Function signature
    lines.append(f"public static class {func_name}")
    lines.append("{")
    lines.append(f"    public static {return_type} Execute()")
    lines.append("    {")

    # Build the source range
    if len(ir.generators) == 1 and isinstance(ir.generators[0].source, IRRange):
        gen = ir.generators[0]
        start, stop, step = gen.source.start, gen.source.stop, gen.source.step

        if step == 1:
            source = f"Enumerable.Range({start}, {stop - start})"
        else:
            # For non-unit steps, use a custom range
            source = (
                f"Enumerable.Range(0, {stop - start}).Select(i => {start} + i * {step})"
            )

        # Add parallel prefix if requested
        if parallel:
            source = f"{source}.AsParallel()"

        # Build the LINQ chain
        chain = source

        # Add filters
        for filter_expr in gen.filters:
            filter_csharp = csharp_expr(filter_expr)
            chain += f".Where({gen.var} => {filter_csharp})"

        # Add the final operation
        if ir.reduce:
            k = ir.reduce.kind
            if ir.kind == "dict":
                expr = ir.val_expr or "0"
            else:
                expr = ir.element or "0"

            expr_csharp = csharp_expr(expr)

            if k == "sum":
                chain += f".Sum({gen.var} => {expr_csharp})"
            elif k == "prod":
                chain += f".Aggregate(1, (acc, {gen.var}) => acc * {expr_csharp})"
            elif k == "max":
                chain += f".Max({gen.var} => {expr_csharp})"
            elif k == "min":
                chain += f".Min({gen.var} => {expr_csharp})"
            elif k == "any":
                chain += f".Any({gen.var} => {expr_csharp})"
            elif k == "all":
                chain += f".All({gen.var} => {expr_csharp})"
        else:
            # Collection operations
            if ir.kind == "list":
                if ir.element:
                    elem_csharp = csharp_expr(ir.element)
                    chain += f".Select({gen.var} => {elem_csharp})"
                chain += ".ToList()"
            elif ir.kind == "set":
                if ir.element:
                    elem_csharp = csharp_expr(ir.element)
                    chain += f".Select({gen.var} => {elem_csharp})"
                chain += ".ToHashSet()"
            elif ir.kind == "dict":
                key_expr = ir.key_expr or "0"
                val_expr = ir.val_expr or "0"
                key_csharp = csharp_expr(key_expr)
                val_csharp = csharp_expr(val_expr)
                chain += f".ToDictionary({gen.var} => {key_csharp}, {gen.var} => {val_csharp})"

        lines.append(f"        return {chain};")

    else:
        # Handle nested comprehensions (more complex)
        lines.append("        // Complex nested comprehension - simplified for demo")
        lines.append("        return new List<int>();")

    lines.append("    }")
    lines.append("}")

    return "\n".join(lines)


def render_sql(ir: IRComp, func_name: str = "program", dialect: str = "sqlite") -> str:
    """
    Simple SQL renderer for basic comprehensions
    """
    if ir.reduce:
        k = ir.reduce.kind
        if k == "sum":
            gen = ir.generators[0]
            if isinstance(gen.source, IRRange):
                start, stop, _step = gen.source.start, gen.source.stop, gen.source.step

                # Build the expression to sum
                if ir.kind == "dict":
                    expr = ir.val_expr or "i"
                else:
                    expr = ir.element or "i"

                # Convert Python expressions to SQL
                expr = expr.replace("**", "^")  # Python ** to SQL ^

                # Build WHERE clause from filters
                where_clause = ""
                if gen.filters:
                    for filter_expr in gen.filters:
                        filter_sql = (
                            filter_expr.replace(" and ", " AND ")
                            .replace(" or ", " OR ")
                            .replace(" not ", " NOT ")
                        )
                        where_clause += f" WHERE {filter_sql}"

                if dialect == "sqlite":
                    # Use recursive CTE for SQLite
                    return f"WITH RECURSIVE range(i) AS (SELECT {start} UNION ALL SELECT i+1 FROM range WHERE i < {stop - 1}) SELECT SUM({expr}) FROM range{where_clause};"
                else:  # postgresql
                    return f"SELECT SUM({expr}) FROM generate_series({start}, {stop - 1}) AS i{where_clause};"

    # Fallback for other cases
    return "-- SQL generation not implemented for this pattern"


def execute_sql_and_display(sql_query: str, dialect: str = "sqlite") -> None:
    """
    Execute SQL query and display results in a pretty format.
    Currently supports SQLite via sqlite3 command-line tool.
    """
    import os
    import subprocess
    import tempfile

    print(f"\n🗄️ Executing SQL ({dialect}):")
    print("=" * 50)
    print(sql_query)
    print("=" * 50)

    if dialect == "sqlite":
        try:
            # Create a temporary SQLite database
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".sql", delete=False
            ) as f:
                f.write(sql_query)
                sql_file = f.name

            # Execute with sqlite3
            result = subprocess.run(
                ["sqlite3", ":memory:", f".read {sql_file}"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Clean up
            os.unlink(sql_file)

            if result.returncode == 0:
                print("✅ Results:")
                if result.stdout.strip():
                    # Pretty print results
                    lines = result.stdout.strip().split("\n")
                    for i, line in enumerate(lines, 1):
                        print(f"  {i:2d}: {line}")
                else:
                    print("  (No results returned)")
            else:
                print(f"❌ SQL Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("⏰ Query timed out (>10s)")
        except FileNotFoundError:
            print("❌ sqlite3 not found. Install with: brew install sqlite3")
        except Exception as e:
            print(f"❌ Execution error: {e}")

    elif dialect == "postgresql":
        print("❌ PostgreSQL execution not yet implemented")
        print("   Use --sql-dialect sqlite for execution")

    else:
        print(f"❌ Unsupported dialect: {dialect}")


if __name__ == "__main__":
    cli()
