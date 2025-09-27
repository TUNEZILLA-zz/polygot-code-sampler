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
    ap.add_argument("--target", "-t", type=str, default="rust", choices=["rust", "ts"])
    ap.add_argument("--out", "-o", type=str)
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
    out = (
        render_rust(ir, func_name=args.name)
        if args.target == "rust"
        else render_ts(ir, func_name=args.name)
    )
    print(out)
    if args.out:
        Path(args.out).write_text(out)
        print(f"\\n[Saved to] {args.out}")


if __name__ == "__main__":
    cli()
