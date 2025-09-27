#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# ---------- Tiny IR (extended for nesting) ----------


@dataclass
class IRRange:
    start: int
    stop: int
    step: int = 1


@dataclass
class IRGenerator:
    var: str
    source: IRRange | str  # range(...) or variable name
    filters: list[str]  # list of predicate expressions as strings


@dataclass
class IRReduce:
    op: str  # '+', '*', etc.
    initial: str | None = None


@dataclass
class IRComp:
    generators: list[IRGenerator]
    element: str  # expression for the element (e.g., "i * j", "(i, j)")
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


# ---------- Python subset parser (nested comprehensions) ----------


class PyToIRNested(ast.NodeVisitor):
    """
    Supports patterns like:
      out = [ expr for i in range(...) if ... for j in range(...) if ... ]
      total = sum( expr for i in range(...) if ... for j in range(...) if ... )
    Assumptions:
      - Only 'range(...)' or simple variable names as sources.
      - Filters are side-effect-free expressions.
    """

    def __init__(self):
        self.comp: IRComp | None = None

    def parse(self, code: str) -> IRComp:
        tree = ast.parse(code)
        self.comp = None
        for node in tree.body:
            # Assignment to listcomp
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.ListComp):
                self.comp = self._comp_to_ir(node.value, reduce_=None)
                break
            # Assignment to sum(generator)
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Call)
                and getattr(node.value.func, "id", None) == "sum"
            ):
                gen = node.value.args[0]
                if not isinstance(gen, (ast.GeneratorExp, ast.ListComp)):
                    raise ValueError("sum() must wrap a generator or listcomp")
                self.comp = self._comp_to_ir(gen, reduce_=IRReduce(op="+", initial="0"))
                break
            # Expr: sum(...)
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Call)
                and getattr(node.value.func, "id", None) == "sum"
            ):
                gen = node.value.args[0]
                self.comp = self._comp_to_ir(gen, reduce_=IRReduce(op="+", initial="0"))
                break
        if not self.comp:
            raise ValueError("No supported comprehension/sum found")
        return self.comp

    def _parse_range(self, call: ast.Call) -> IRRange:
        if getattr(call.func, "id", None) != "range":
            raise ValueError("Only range(...) supported in this demo")
        args = [ast.literal_eval(a) for a in call.args]
        if len(args) == 1:
            start, stop, step = 0, args[0], 1
        elif len(args) == 2:
            start, stop, step = args[0], args[1], 1
        else:
            start, stop, step = args[0], args[1], args[2]
        return IRRange(start=start, stop=stop, step=step)

    def _comp_to_ir(
        self, comp: ast.ListComp | ast.GeneratorExp, reduce_: IRReduce | None
    ) -> IRComp:
        # Multiple generators allowed
        gens: list[IRGenerator] = []
        for gen in comp.generators:
            # Target var name
            if not isinstance(gen.target, ast.Name):
                raise ValueError("Only simple variable targets supported")
            var = gen.target.id
            # Source
            src = gen.iter
            if isinstance(src, ast.Call) and getattr(src.func, "id", None) == "range":
                source = self._parse_range(src)
            elif isinstance(src, ast.Name):
                source = src.id
            else:
                raise ValueError("Only range(...) or variable sources supported")
            # Filters (convert each 'if' to source string)
            filters = [ast.unparse(cond) for cond in gen.ifs] if gen.ifs else []
            gens.append(IRGenerator(var=var, source=source, filters=filters))

        element_src = ast.unparse(comp.elt)

        provenance = {
            "origin": "python",
            "pattern": "nested_comp" if len(gens) > 1 else "comp",
        }
        return IRComp(
            generators=gens, element=element_src, reduce=reduce_, provenance=provenance
        )


# ---------- Utilities: Python → Rust expr tweaks ----------

REPLACEMENTS = [
    (r"\\band\\b", "&&"),
    (r"\\bor\\b", "||"),
    (r"\\bnot\\b", "!"),
    (r"\\bTrue\\b", "true"),
    (r"\\bFalse\\b", "false"),
]


def py_expr_to_rust(expr: str) -> str:
    out = expr
    for pat, repl in REPLACEMENTS:
        out = re.sub(pat, repl, out)
    # Python uses '==' and '!=' same as Rust; '%' same; '//' not handled here.
    return out


def range_to_rust(r: IRRange) -> str:
    base = f"({r.start}..{r.stop})"
    if r.step != 1:
        # step_by requires usize
        return f"{base}.step_by({r.step}usize)"
    return base


# ---------- Renderer: IR → Rust iterator chains ----------


def render_rust_iter_chain(ir: IRComp, func_name: str = "program") -> str:
    # Build nested iterator chain with flat_map for inner generators
    def render_gen(idx: int) -> str:
        gen = ir.generators[idx]
        var = gen.var
        # Source iterator
        if isinstance(gen.source, IRRange):
            src = range_to_rust(gen.source)
        elif isinstance(gen.source, str):
            src = gen.source  # assume it's an iterator-like in Rust context
        else:
            raise ValueError("Unsupported generator source")

        chain = src
        # Apply filters
        for pred in gen.filters:
            chain += f".filter(|&{var}| {py_expr_to_rust(pred)})"

        if idx == len(ir.generators) - 1:
            # Last generator → map to element
            chain += f".map(move |{var}| {py_expr_to_rust(ir.element)})"
            return chain
        else:
            # There are inner generators → flat_map into the next
            inner = render_gen(idx + 1)
            return f"{chain}.flat_map(move |{var}| {inner})"

    body_chain = render_gen(0)

    # Wrap with collect or reduce
    if ir.reduce:
        if ir.reduce.op == "+":
            trailer = ".sum::<i64>()"
        elif ir.reduce.op == "*":
            trailer = ".product::<i64>()"
        else:
            trailer = "/* unsupported reduce op */"
        ret_type = "i64"
    else:
        trailer = ".collect::<Vec<_>>()"
        ret_type = "Vec<_>"

    lines = []
    lines.append(f"// Rendered from IR (origin: {ir.provenance.get('origin')})")
    lines.append(f"pub fn {func_name}() -> {ret_type} {{")
    lines.append(f"    let result = {body_chain}{trailer};")
    lines.append("    result")
    lines.append("}")
    return "\n".join(lines)


# ---------- CLI + Demo ----------

DEMO_CASES = [
    (
        """
out = [ (i, j) for i in range(0, 3) for j in range(0, 2) ]
""",
        "pairs",
    ),
    (
        """
out = [ i * j for i in range(1, 5) if i % 2 == 0 for j in range(1, 4) if j > 1 ]
""",
        "even_times_gt1",
    ),
    (
        """
total = sum(i * j for i in range(1, 5) if i % 2 == 1 for j in range(1, 4) if j != 2)
""",
        "sum_odd_times_not2",
    ),
]


def run_demo():
    parser = PyToIRNested()
    outputs = []
    for code, name in DEMO_CASES:
        ir = parser.parse(code)
        rust_code = render_rust_iter_chain(ir, func_name=name)
        outputs.append(
            {
                "python": code.strip(),
                "ir_json": json.loads(ir.to_json()),
                "rust": rust_code,
            }
        )
    return outputs


def cli():
    ap = argparse.ArgumentParser(
        description="Polyglot Code Sampler - Step 2 (Nested comprehensions → Rust iterators)"
    )
    ap.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to a Python file containing a list/generator comprehension",
    )
    ap.add_argument("--code", "-c", type=str, help="Inline Python code snippet")
    ap.add_argument(
        "--name",
        "-n",
        type=str,
        default="program",
        help="Function name for the generated Rust code",
    )
    ap.add_argument("--demo", action="store_true", help="Run built-in demo cases")
    ap.add_argument("--emit-ir", action="store_true", help="Also print the JSON IR")
    ap.add_argument("--out", "-o", type=str, help="Write Rust output to this file")
    args = ap.parse_args()

    if args.demo:
        demos = run_demo()
        for i, d in enumerate(demos, 1):
            print("=" * 80)
            print(f"DEMO {i} — Python source:")
            print(d["python"])
            print("\nIR (JSON):")
            print(json.dumps(d["ir_json"], indent=2))
            print("\nRust render:")
            print(d["rust"])
        return

    src_code = None
    if args.code:
        src_code = args.code
    elif args.file:
        src_code = Path(args.file).read_text()
    else:
        print("Provide --demo, --code, or --file", file=sys.stderr)
        sys.exit(1)

    parser = PyToIRNested()
    ir = parser.parse(src_code)
    rust = render_rust_iter_chain(ir, func_name=args.name)

    if args.emit_ir:
        print("=== IR (JSON) ===")
        print(ir.to_json())
        print()

    print("=== Rust Output ===")
    print(rust)

    if args.out:
        Path(args.out).write_text(rust)
        print(f"\n[Saved Rust to] {args.out}")


if __name__ == "__main__":
    cli()
