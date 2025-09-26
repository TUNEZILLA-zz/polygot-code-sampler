
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

# ---------- Tiny IR (extended) ----------

@dataclass
class IRRange:
    start: int
    stop: int
    step: int = 1

@dataclass
class IRGenerator:
    var: str
    source: IRRange | str  # range(...) or variable name
    filters: list[str]             # list of predicate expressions as strings

@dataclass
class IRReduce:
    kind: str            # 'sum'|'prod'|'any'|'all'|'max'|'min'
    op: str | None = None
    initial: str | None = None

@dataclass
class IRComp:
    kind: str                         # 'list'|'set'|'dict'
    generators: list[IRGenerator]
    element: str | None = None     # list/set element expr
    key_expr: str | None = None    # dict key
    val_expr: str | None = None    # dict value
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


# ---------- Python subset parser (nested comprehensions + kinds + reductions) ----------

class PyToIRStep3(ast.NodeVisitor):
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
                        self.comp = self._comp_to_ir(inner, kind="list", reduce_=IRReduce(kind=red_kind))
                        break

            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                red_kind = self._reduction_kind(node.value.func)
                if red_kind:
                    inner = node.value.args[0]
                    if isinstance(inner, (ast.GeneratorExp, ast.ListComp)):
                        self.comp = self._comp_to_ir(inner, kind="list", reduce_=IRReduce(kind=red_kind))
                        break

        if not self.comp:
            raise ValueError("No supported comprehension/reduction found")
        return self.comp

    def _reduction_kind(self, func: ast.AST) -> str | None:
        if isinstance(func, ast.Name) and func.id in {"sum", "any", "all", "max", "min", "prod"}:
            return func.id
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "math" and func.attr == "prod":
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

    def _gens_from_comp(self, comp: ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp) -> list[IRGenerator]:
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

    def _comp_to_ir(self, comp: ast.ListComp | ast.SetComp | ast.GeneratorExp, kind: str, reduce_: IRReduce | None) -> IRComp:
        gens = self._gens_from_comp(comp)
        element_src = ast.unparse(comp.elt)
        provenance = {"origin": "python", "pattern": f"{kind}_nested" if len(gens) > 1 else kind}
        return IRComp(kind=kind, generators=gens, element=element_src, reduce=reduce_, provenance=provenance)

    def _dictcomp_to_ir(self, comp: ast.DictComp, reduce_: IRReduce | None) -> IRComp:
        gens = self._gens_from_comp(comp)
        key_src = ast.unparse(comp.key)
        val_src = ast.unparse(comp.value)
        provenance = {"origin": "python", "pattern": "dict_nested" if len(gens) > 1 else "dict"}
        return IRComp(kind="dict", generators=gens, key_expr=key_src, val_expr=val_src, reduce=reduce_, provenance=provenance)


# ---------- Utilities: Python → Rust expr tweaks ----------

REPLACEMENTS = [
    (r"\band\b", "&&"),
    (r"\bor\b", "||"),
    (r"\bnot\b", "!"),
    (r"\bTrue\b", "true"),
    (r"\bFalse\b", "false"),
]

def py_expr_to_rust(expr: str) -> str:
    out = expr
    for pat, repl in REPLACEMENTS:
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
    if r.step != 1:
        return f"{base}.step_by({r.step}usize)"
    return base


# ---------- Renderer: IR → Rust iterator chains ----------

def render_rust(ir: IRComp, func_name: str = "program", int_type: str = "i32", reduce_int: str = "i64") -> str:
    def render_gen(idx: int) -> str:
        gen = ir.generators[idx]
        var = gen.var
        if isinstance(gen.source, IRRange):
            src = range_to_rust(gen.source)
        elif isinstance(gen.source, str):
            src = gen.source
        else:
            raise ValueError("Unsupported generator source")
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
            inner = render_gen(idx + 1)
            return f"{chain}.flat_map(move |{var}| {inner})"

    body_chain = render_gen(0)

    use_lines = []
    ret_type = ""
    trailer = ""

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
            # default 0 of chosen reduce_int
            default_zero = "0"
            trailer = f"{method}.unwrap_or({default_zero})"
            ret_type = reduce_int
        else:
            trailer = "/* unsupported reduction */"
            ret_type = "/* unknown */"
    else:
        if ir.kind == "list":
            trailer = ".collect::<Vec<_>>()"
            ret_type = "Vec<_>"
        elif ir.kind == "set":
            use_lines.append("use std::collections::HashSet;")
            trailer = ".collect::<HashSet<_>>()"
            ret_type = "HashSet<_>"
        elif ir.kind == "dict":
            use_lines.append("use std::collections::HashMap;")
            trailer = ".collect::<HashMap<_, _>>()"
            ret_type = "HashMap<_, _>"
        else:
            trailer = ".collect::<Vec<_>>()"
            ret_type = "Vec<_>"

    lines = []
    lines.append(f"// Rendered from IR (origin: {ir.provenance.get('origin')})")
    for u in use_lines:
        lines.append(u)
    lines.append(f"pub fn {func_name}() -> {ret_type} {{")
    lines.append(f"    let result = {body_chain}{trailer};")
    lines.append("    result")
    lines.append("}")
    return "\n".join(lines)


# ---------- CLI + Demo ----------

DEMO_CASES = [
    # Dict comp
    ('''
m = { i: i*i for i in range(1,6) if i % 2 == 1 }
''', "map_odds"),
    # Set comp with nesting
    ('''
s = { (i, j) for i in range(0,3) for j in range(0,3) if i != j }
''', "pairs_set"),
    # any/all on generator
    ('''
ok = all(x % 2 == 0 for x in range(2,10))
''', "all_even"),
    # max over nested
    ('''
best = max(i*j for i in range(1,5) for j in range(1,4))
''', "max_prod"),
    # prod
    ('''
import math
p = math.prod(x for x in range(1,5) if x != 3)
''', "prod_simple"),
]

def run_demo(int_type="i32", reduce_int="i64"):
    parser = PyToIRStep3()
    outputs = []
    for code, name in DEMO_CASES:
        ir = parser.parse(code)
        rust_code = render_rust(ir, func_name=name, int_type=int_type, reduce_int=reduce_int)
        outputs.append({
            "python": code.strip(),
            "ir_json": json.loads(ir.to_json()),
            "rust": rust_code
        })
    return outputs

def cli():
    ap = argparse.ArgumentParser(description="PCS Step 3 — Dict/Set comprehensions + reductions → Rust")
    ap.add_argument("--file", "-f", type=str, help="Path to a Python file containing a comprehension or reduction")
    ap.add_argument("--code", "-c", type=str, help="Inline Python code snippet")
    ap.add_argument("--name", "-n", type=str, default="program", help="Function name for the generated Rust code")
    ap.add_argument("--emit-ir", action="store_true", help="Also print the JSON IR")
    ap.add_argument("--demo", action="store_true", help="Run built-in demo cases")
    ap.add_argument("--int-type", type=str, default="i32", choices=["i32","i64"], help="Preferred integer type hint")
    ap.add_argument("--reduce-type", type=str, default="i64", choices=["i32","i64"], help="Type for sum/prod/max/min")
    ap.add_argument("--out", "-o", type=str, help="Write Rust output to this file")
    args = ap.parse_args()

    if args.demo:
        demos = run_demo(int_type=args.int_type, reduce_int=args.reduce_type)
        for i, d in enumerate(demos, 1):
            print("="*80)
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

    parser = PyToIRStep3()
    ir = parser.parse(src_code)
    rust = render_rust(ir, func_name=args.name, int_type=args.int_type, reduce_int=args.reduce_type)

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
