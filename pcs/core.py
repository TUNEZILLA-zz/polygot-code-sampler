"""
Core functionality for Polyglot Code Sampler
"""

from __future__ import annotations

import ast
import json
from dataclasses import asdict, dataclass
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
class TypeInfo:
    element_type: str = "int"
    key_type: str = "int"
    value_type: str = "int"

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

class PyToIR:
    def parse(self, code: str) -> IRComp:
        tree = ast.parse(code)
        if len(tree.body) != 1:
            raise ValueError("Expected single expression")

        expr = tree.body[0]
        if isinstance(expr, ast.Expr):
            return self._parse_expr(expr.value)
        else:
            raise ValueError("Expected expression")

    def _parse_expr(self, node: ast.AST) -> IRComp:
        if isinstance(node, ast.ListComp):
            return self._parse_list_comp(node)
        elif isinstance(node, ast.DictComp):
            return self._parse_dict_comp(node)
        elif isinstance(node, ast.SetComp):
            return self._parse_set_comp(node)
        elif isinstance(node, ast.GeneratorExp):
            return self._parse_genexp(node)
        elif isinstance(node, ast.Call):
            return self._parse_call(node)
        else:
            raise ValueError(f"Unsupported expression type: {type(node)}")

    def _parse_list_comp(self, node: ast.ListComp) -> IRComp:
        generators = [self._parse_generator(gen) for gen in node.generators]
        element = ast.unparse(node.elt) if node.elt else None

        return IRComp(
            kind="list",
            generators=generators,
            element=element,
            provenance={"origin": "list_comp"}
        )

    def _parse_dict_comp(self, node: ast.DictComp) -> IRComp:
        generators = [self._parse_generator(gen) for gen in node.generators]
        key_expr = ast.unparse(node.key) if node.key else None
        val_expr = ast.unparse(node.value) if node.value else None

        return IRComp(
            kind="dict",
            generators=generators,
            key_expr=key_expr,
            val_expr=val_expr,
            provenance={"origin": "dict_comp"}
        )

    def _parse_set_comp(self, node: ast.SetComp) -> IRComp:
        generators = [self._parse_generator(gen) for gen in node.generators]
        element = ast.unparse(node.elt) if node.elt else None

        return IRComp(
            kind="set",
            generators=generators,
            element=element,
            provenance={"origin": "set_comp"}
        )

    def _parse_genexp(self, node: ast.GeneratorExp) -> IRComp:
        generators = [self._parse_generator(gen) for gen in node.generators]
        element = ast.unparse(node.elt) if node.elt else None

        return IRComp(
            kind="generator",
            generators=generators,
            element=element,
            provenance={"origin": "genexp"}
        )

    def _parse_call(self, node: ast.Call) -> IRComp:
        """Parse function calls like sum(), max(), min(), any(), all()"""
        if not isinstance(node.func, ast.Name):
            raise ValueError(f"Unsupported function call: {ast.unparse(node)}")

        func_name = node.func.id
        if func_name not in ('sum', 'max', 'min', 'any', 'all'):
            raise ValueError(f"Unsupported function: {func_name}")

        if len(node.args) != 1:
            raise ValueError(f"Function {func_name} expects exactly one argument")

        arg = node.args[0]
        if isinstance(arg, ast.GeneratorExp):
            # Parse the generator expression
            generators = [self._parse_generator(gen) for gen in arg.generators]
            element = ast.unparse(arg.elt) if arg.elt else None

            return IRComp(
                kind="generator",
                generators=generators,
                element=element,
                reduce=IRReduce(kind=func_name),
                provenance={"origin": f"call_{func_name}"}
            )
        else:
            raise ValueError(f"Function {func_name} expects a generator expression")

    def _parse_generator(self, node: ast.comprehension) -> IRGenerator:
        var = node.target.id if isinstance(node.target, ast.Name) else "x"
        source = self._parse_source(node.iter)
        filters = [ast.unparse(f) for f in node.ifs]

        return IRGenerator(var=var, source=source, filters=filters)

    def _parse_source(self, node: ast.AST) -> IRRange | str:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "range":
            args = node.args
            if len(args) == 1:
                return IRRange(0, self._eval_const(args[0]))
            elif len(args) == 2:
                return IRRange(self._eval_const(args[0]), self._eval_const(args[1]))
            elif len(args) == 3:
                return IRRange(
                    self._eval_const(args[0]),
                    self._eval_const(args[1]),
                    self._eval_const(args[2])
                )
        return ast.unparse(node)

    def _eval_const(self, node: ast.AST) -> int:
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        else:
            # For non-constant expressions, return a placeholder
            return 10
