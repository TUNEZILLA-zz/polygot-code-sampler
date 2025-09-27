#!/usr/bin/env python3
"""
🎨 Code Live - Texture Mode
==========================

Conceptual textures for code transformation aesthetics.
Like musical texture (dense vs sparse, smooth vs grainy) applied to code generation.
"""

import ast
import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class TextureType(Enum):
    """Code texture types inspired by music and design"""

    DENSE = "dense"  # Nested loops, comprehensions, stacked transformations
    SPARSE = "sparse"  # Minimalistic, flat iteration with only essentials
    SMOOTH = "smooth"  # Vectorized ops, batch processing, continuous interpolation
    GRAINY = "grainy"  # Stepwise, noisy iterations, explicit jitter
    POLYPHONIC = "polyphonic"  # Multiple concurrent code paths, like musical voices
    MINIMAL = "minimal"  # Very small, almost haiku-like loops
    MAXIMAL = "maximal"  # Overloaded with decorators, abstractions, parallelization
    FRACTAL = "fractal"  # Recursive texture, code "folds in on itself"


@dataclass
class TextureParams:
    """Parameters for texture transformations"""

    # Dense texture
    dense_nesting_level: int = 3  # How many levels of nesting
    dense_comprehensions: bool = True  # Use list comprehensions

    # Sparse texture
    sparse_minimal: bool = True  # Keep only essentials
    sparse_flat: bool = True  # Avoid nesting

    # Smooth texture
    smooth_vectorized: bool = True  # Use vectorized operations
    smooth_interpolation: bool = True  # Continuous interpolation

    # Grainy texture
    grainy_jitter: float = 0.1  # Amount of jitter
    grainy_stepwise: bool = True  # Stepwise processing

    # Polyphonic texture
    polyphonic_voices: int = 3  # Number of concurrent voices
    polyphonic_harmony: bool = True  # Add harmonic relationships

    # Minimal texture
    minimal_lines: int = 3  # Maximum lines per loop

    # Maximal texture
    maximal_decorators: bool = True  # Add decorators
    maximal_abstractions: bool = True  # Add abstractions
    maximal_parallel: bool = True  # Add parallelization

    # Fractal texture
    fractal_depth: int = 3  # Recursion depth
    fractal_branches: int = 2  # Number of branches per level


class TextureTransformer(ast.NodeTransformer):
    """AST transformer that applies texture transformations to code"""

    def __init__(self, texture_type: TextureType, params: TextureParams):
        self.texture_type = texture_type
        self.params = params

    def visit_For(self, node: ast.For) -> ast.For:
        """Transform for loops with texture effects"""
        # Visit children first
        node = self.generic_visit(node)

        # Apply texture-specific transformations
        if self.texture_type == TextureType.DENSE:
            return self._apply_dense_texture(node)
        elif self.texture_type == TextureType.SPARSE:
            return self._apply_sparse_texture(node)
        elif self.texture_type == TextureType.SMOOTH:
            return self._apply_smooth_texture(node)
        elif self.texture_type == TextureType.GRAINY:
            return self._apply_grainy_texture(node)
        elif self.texture_type == TextureType.POLYPHONIC:
            return self._apply_polyphonic_texture(node)
        elif self.texture_type == TextureType.MINIMAL:
            return self._apply_minimal_texture(node)
        elif self.texture_type == TextureType.MAXIMAL:
            return self._apply_maximal_texture(node)
        elif self.texture_type == TextureType.FRACTAL:
            return self._apply_fractal_texture(node)

        return node

    def _apply_dense_texture(self, node: ast.For) -> ast.For:
        """Apply dense texture - nested loops, comprehensions, stacked transformations"""
        if not self.params.dense_comprehensions:
            return node

        # Convert to list comprehension if possible
        if len(node.body) == 1 and isinstance(node.body[0], ast.Expr):
            # Simple case: single expression
            expr = node.body[0].value
            if isinstance(expr, ast.Call):
                # Convert to comprehension
                comp = ast.ListComp(
                    elt=expr,
                    generators=[
                        ast.comprehension(
                            target=node.target, iter=node.iter, ifs=[], is_async=0
                        )
                    ],
                )
                return ast.Expr(value=comp)

        # Add nested loops for dense texture
        new_body = []
        for level in range(self.params.dense_nesting_level):
            nested_loop = ast.For(
                target=ast.Name(id=f"level_{level}", ctx=ast.Store()),
                iter=ast.Call(
                    func=ast.Name(id="range", ctx=ast.Load()),
                    args=[ast.Constant(value=3)],
                    keywords=[],
                ),
                body=node.body.copy(),
                orelse=[],
            )
            new_body.append(nested_loop)

        node.body = new_body
        return node

    def _apply_sparse_texture(self, node: ast.For) -> ast.For:
        """Apply sparse texture - minimalistic, flat iteration with only essentials"""
        if not self.params.sparse_minimal:
            return node

        # Keep only essential operations
        essential_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # Keep only function calls
                essential_body.append(stmt)
            elif isinstance(stmt, ast.Assign):
                # Keep only simple assignments
                essential_body.append(stmt)

        node.body = essential_body
        return node

    def _apply_smooth_texture(self, node: ast.For) -> ast.For:
        """Apply smooth texture - vectorized ops, batch processing, continuous interpolation"""
        if not self.params.smooth_vectorized:
            return node

        # Add vectorized operations
        vectorized_body = []

        # Add numpy-style vectorization
        vectorized_call = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="np", ctx=ast.Load()),
                    attr="vectorize",
                    ctx=ast.Load(),
                ),
                args=[ast.Name(id="process", ctx=ast.Load())],
                keywords=[],
            )
        )
        vectorized_body.append(vectorized_call)

        # Add interpolation
        if self.params.smooth_interpolation:
            interp_call = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="np", ctx=ast.Load()),
                        attr="interp",
                        ctx=ast.Load(),
                    ),
                    args=[
                        node.target,
                        ast.Call(
                            func=ast.Name(id="np", ctx=ast.Load()),
                            attr="linspace",
                            ctx=ast.Load(),
                        ),
                        ast.Call(
                            func=ast.Name(id="np", ctx=ast.Load()),
                            attr="linspace",
                            ctx=ast.Load(),
                        ),
                    ],
                    keywords=[],
                )
            )
            vectorized_body.append(interp_call)

        vectorized_body.extend(node.body)
        node.body = vectorized_body
        return node

    def _apply_grainy_texture(self, node: ast.For) -> ast.For:
        """Apply grainy texture - stepwise, noisy iterations, explicit jitter"""
        if not self.params.grainy_stepwise:
            return node

        # Add jitter to loop variable
        jitter_body = []

        # Add random jitter
        jitter_assign = ast.Assign(
            targets=[ast.Name(id="_jitter", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="random", ctx=ast.Load()),
                    attr="uniform",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Constant(value=-self.params.grainy_jitter),
                    ast.Constant(value=self.params.grainy_jitter),
                ],
                keywords=[],
            ),
            lineno=0,
            col_offset=0,
        )
        jitter_body.append(jitter_assign)

        # Add jittered processing
        jittered_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="process", ctx=ast.Load()),
                args=[
                    ast.BinOp(
                        left=node.target,
                        op=ast.Add(),
                        right=ast.Name(id="_jitter", ctx=ast.Load()),
                    )
                ],
                keywords=[],
            )
        )
        jittered_body.append(jittered_call)

        jittered_body.extend(node.body)
        node.body = jittered_body
        return node

    def _apply_polyphonic_texture(self, node: ast.For) -> ast.For:
        """Apply polyphonic texture - multiple concurrent code paths, like musical voices"""
        if not self.params.polyphonic_harmony:
            return node

        # Create multiple voices
        voices = []
        for voice in range(self.params.polyphonic_voices):
            voice_loop = ast.For(
                target=ast.Name(id=f"voice_{voice}", ctx=ast.Store()),
                iter=ast.Call(
                    func=ast.Name(id="range", ctx=ast.Load()),
                    args=[ast.Constant(value=10)],
                    keywords=[],
                ),
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id="process", ctx=ast.Load()),
                            args=[
                                ast.Name(id=f"voice_{voice}", ctx=ast.Load()),
                                ast.Constant(value=voice),
                            ],
                            keywords=[],
                        )
                    )
                ],
                orelse=[],
            )
            voices.append(voice_loop)

        # Return the first voice (others are added as siblings)
        return voices[0] if voices else node

    def _apply_minimal_texture(self, node: ast.For) -> ast.For:
        """Apply minimal texture - very small, almost haiku-like loops"""
        if not self.params.sparse_minimal:
            return node

        # Keep only essential operations
        minimal_body = []
        for i, stmt in enumerate(node.body):
            if i >= self.params.minimal_lines:
                break
            minimal_body.append(stmt)

        node.body = minimal_body
        return node

    def _apply_maximal_texture(self, node: ast.For) -> ast.For:
        """Apply maximal texture - overloaded with decorators, abstractions, parallelization"""
        if not self.params.maximal_decorators:
            return node

        # Add decorators
        decorators = []
        if self.params.maximal_parallel:
            decorators.append(ast.Name(id="parallelize", ctx=ast.Load()))
        if self.params.maximal_abstractions:
            decorators.append(ast.Name(id="instrument", ctx=ast.Load()))

        # Add function wrapper
        func_def = ast.FunctionDef(
            name="textured_loop",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="n", annotation=None)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
                vararg=None,
                kwarg=None,
            ),
            body=node.body,
            decorator_list=decorators,
            returns=None,
            type_comment=None,
        )

        # Return function call
        return ast.Expr(
            value=ast.Call(
                func=ast.Name(id="textured_loop", ctx=ast.Load()),
                args=[ast.Constant(value=10)],
                keywords=[],
            )
        )

    def _apply_fractal_texture(self, node: ast.For) -> ast.For:
        """Apply fractal texture - recursive texture, code 'folds in on itself'"""
        if not self.params.fractal_branches:
            return node

        # Add recursive processing
        fractal_body = []

        # Add fractal depth calculation
        depth_assign = ast.Assign(
            targets=[ast.Name(id="_fractal_depth", ctx=ast.Store())],
            value=ast.Constant(value=self.params.fractal_depth),
            lineno=0,
            col_offset=0,
        )
        fractal_body.append(depth_assign)

        # Add recursive call
        recursive_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="fractal_process", ctx=ast.Load()),
                args=[node.target, ast.Name(id="_fractal_depth", ctx=ast.Load())],
                keywords=[],
            )
        )
        fractal_body.append(recursive_call)

        fractal_body.extend(node.body)
        node.body = fractal_body
        return node


class TextureEngine:
    """Engine for applying texture transformations to code"""

    def __init__(self):
        self.default_params = TextureParams()

    def apply_texture(
        self,
        code: str,
        texture_type: TextureType,
        params: Optional[TextureParams] = None,
    ) -> str:
        """Apply texture transformation to Python code"""
        if params is None:
            params = self.default_params

        try:
            tree = ast.parse(code)
            transformer = TextureTransformer(texture_type, params)
            transformed_tree = transformer.visit(tree)
            return ast.unparse(transformed_tree)
        except Exception as e:
            print(f"Error applying texture: {e}")
            return code

    def get_texture_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all texture types"""
        return {
            "dense": "Nested loops, comprehensions, stacked transformations",
            "sparse": "Minimalistic, flat iteration with only essentials",
            "smooth": "Vectorized ops, batch processing, continuous interpolation",
            "grainy": "Stepwise, noisy iterations, explicit jitter",
            "polyphonic": "Multiple concurrent code paths, like musical voices",
            "minimal": "Very small, almost haiku-like loops",
            "maximal": "Overloaded with decorators, abstractions, parallelization",
            "fractal": "Recursive texture, code 'folds in on itself'",
        }

    def get_texture_visual_effects(self, texture_type: TextureType) -> Dict[str, Any]:
        """Get visual effects for texture type"""
        effects = {
            TextureType.DENSE: {
                "particle_behavior": "cluster_clouds",
                "movement": "convergent",
                "density": "high",
                "color": "#4b6cff",  # Indigo
            },
            TextureType.SPARSE: {
                "particle_behavior": "isolated_points",
                "movement": "minimal",
                "density": "low",
                "color": "#2dd4bf",  # Teal
            },
            TextureType.SMOOTH: {
                "particle_behavior": "flowing_arcs",
                "movement": "continuous",
                "density": "medium",
                "color": "#8b5cf6",  # Purple
            },
            TextureType.GRAINY: {
                "particle_behavior": "jittery_scatter",
                "movement": "random",
                "density": "medium",
                "color": "#f59e0b",  # Amber
            },
            TextureType.POLYPHONIC: {
                "particle_behavior": "harmonic_waves",
                "movement": "oscillating",
                "density": "high",
                "color": "#ec4899",  # Pink
            },
            TextureType.MINIMAL: {
                "particle_behavior": "single_points",
                "movement": "static",
                "density": "very_low",
                "color": "#6b7280",  # Gray
            },
            TextureType.MAXIMAL: {
                "particle_behavior": "layered_clouds",
                "movement": "complex",
                "density": "very_high",
                "color": "#dc2626",  # Red
            },
            TextureType.FRACTAL: {
                "particle_behavior": "recursive_patterns",
                "movement": "self_similar",
                "density": "variable",
                "color": "#059669",  # Emerald
            },
        }
        return effects.get(texture_type, {})


def main():
    """Test the texture engine"""
    engine = TextureEngine()

    print("🎨 Code Live - Texture Mode Engine")
    print("=" * 50)

    print("\n🎨 Available Textures:")
    descriptions = engine.get_texture_descriptions()
    for texture, description in descriptions.items():
        print(f"  {texture}: {description}")

    print("\n🧪 Testing Texture Transformations:")

    # Test code
    test_code = """
for i in range(10):
    process(i)
"""

    print(f"Original code:")
    print(test_code.strip())
    print()

    # Test different textures
    for texture_type in TextureType:
        print(f"\n🎨 {texture_type.value.upper()} Texture:")
        print("-" * 30)

        textured_code = engine.apply_texture(test_code, texture_type)
        print(f"Original: {test_code.strip()}")
        print(f"Textured: {textured_code.strip()}")

        # Show visual effects
        visual_effects = engine.get_texture_visual_effects(texture_type)
        print(
            f"Visual: {visual_effects.get('particle_behavior', 'unknown')} ({visual_effects.get('color', 'unknown')})"
        )

    print("\n🎉 Texture Mode Engine Ready!")


if __name__ == "__main__":
    main()
