#!/usr/bin/env python3
"""
🥧 Code Live - Pi Mode Audio Effects
====================================

Mathematical playground with π (pi) references, circular waveforms, and Pi Day easter eggs!
Turn code loops into mathematical art with π-based transformations.
"""

import ast
import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class PiModeType(Enum):
    """Pi mode transformation types"""
    PI_LOOP = "pi_loop"  # Loop lengths as π multiples
    WAVEFORM = "waveform"  # π-based sine/cosine modulation
    FRACTAL = "fractal"  # π-based fractal patterns
    CIRCULAR = "circular"  # Circular/spiral transformations
    CONSTANTS = "constants"  # Insert math constants (π, τ, e)
    EASTER_EGG = "easter_egg"  # Pi Day easter eggs


@dataclass
class PiModeParams:
    """Parameters for Pi mode transformations"""
    pi_multiplier: float = 100.0  # π * 100 = 314 iterations
    waveform_freq: float = 1.0  # Frequency for sine/cosine
    fractal_depth: int = 3  # Fractal recursion depth
    circular_radius: float = 1.0  # Circle radius
    constants_mode: bool = True  # Insert math constants
    easter_egg_mode: bool = True  # Enable Pi Day easter eggs


class PiModeTransformer(ast.NodeTransformer):
    """AST transformer that applies π-based transformations to code"""
    
    def __init__(self, pi_params: PiModeParams):
        self.pi_params = pi_params
        self.pi_value = math.pi
        self.tau_value = 2 * math.pi
        self.e_value = math.e
    
    def visit_For(self, node: ast.For) -> ast.For:
        """Transform for loops with π-based effects"""
        # Visit children first
        node = self.generic_visit(node)
        
        # Apply π-based transformations
        node = self._apply_pi_loop_length(node)
        node = self._apply_waveform_modulation(node)
        node = self._apply_fractal_patterns(node)
        node = self._apply_circular_transforms(node)
        node = self._insert_math_constants(node)
        node = self._add_pi_easter_eggs(node)
        
        return node
    
    def _apply_pi_loop_length(self, node: ast.For) -> ast.For:
        """Apply π-based loop length transformations"""
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            # Transform range(n) to range(int(π * multiplier))
            if len(node.iter.args) == 1:
                # range(n) -> range(int(π * multiplier))
                pi_multiplier = ast.Constant(value=self.pi_params.pi_multiplier)
                pi_call = ast.Call(
                    func=ast.Name(id="math.pi", ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
                pi_multiply = ast.BinOp(
                    left=pi_call,
                    op=ast.Mult(),
                    right=pi_multiplier
                )
                int_call = ast.Call(
                    func=ast.Name(id="int", ctx=ast.Load()),
                    args=[pi_multiply],
                    keywords=[]
                )
                node.iter.args[0] = int_call
            elif len(node.iter.args) == 2:
                # range(start, stop) -> range(start, int(π * multiplier))
                pi_multiplier = ast.Constant(value=self.pi_params.pi_multiplier)
                pi_call = ast.Call(
                    func=ast.Name(id="math.pi", ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
                pi_multiply = ast.BinOp(
                    left=pi_call,
                    op=ast.Mult(),
                    right=pi_multiplier
                )
                int_call = ast.Call(
                    func=ast.Name(id="int", ctx=ast.Load()),
                    args=[pi_multiply],
                    keywords=[]
                )
                node.iter.args[1] = int_call
        
        return node
    
    def _apply_waveform_modulation(self, node: ast.For) -> ast.For:
        """Apply π-based waveform modulation"""
        # Add sine wave modulation to loop body
        sine_modulation = ast.Assign(
            targets=[ast.Name(id="_pi_sine", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="math", ctx=ast.Load()),
                    attr="sin",
                    ctx=ast.Load()
                ),
                args=[
                    ast.BinOp(
                        left=ast.BinOp(
                            left=node.target,
                            op=ast.Mult(),
                            right=ast.Call(
                                func=ast.Name(id="math.pi", ctx=ast.Load()),
                                args=[],
                                keywords=[]
                            )
                        ),
                        op=ast.Div(),
                        right=ast.Constant(value=8.0)  # π/8 for nice phase
                    )
                ],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add cosine wave modulation
        cosine_modulation = ast.Assign(
            targets=[ast.Name(id="_pi_cosine", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="math", ctx=ast.Load()),
                    attr="cos",
                    ctx=ast.Load()
                ),
                args=[
                    ast.BinOp(
                        left=ast.BinOp(
                            left=node.target,
                            op=ast.Mult(),
                            right=ast.Call(
                                func=ast.Name(id="math.pi", ctx=ast.Load()),
                                args=[],
                                keywords=[]
                            )
                        ),
                        op=ast.Div(),
                        right=ast.Constant(value=8.0)
                    )
                ],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add waveform processing
        waveform_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="process_waveform", ctx=ast.Load()),
                args=[
                    node.target,
                    ast.Name(id="_pi_sine", ctx=ast.Load()),
                    ast.Name(id="_pi_cosine", ctx=ast.Load())
                ],
                keywords=[]
            )
        )
        
        # Insert at beginning of loop body
        new_body = [sine_modulation, cosine_modulation, waveform_call]
        new_body.extend(node.body)
        node.body = new_body
        
        return node
    
    def _apply_fractal_patterns(self, node: ast.For) -> ast.For:
        """Apply π-based fractal patterns"""
        # Add fractal depth calculation
        fractal_depth = ast.Assign(
            targets=[ast.Name(id="_pi_fractal_depth", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="int", ctx=ast.Load()),
                args=[
                    ast.BinOp(
                        left=ast.Call(
                            func=ast.Name(id="math.pi", ctx=ast.Load()),
                            args=[],
                            keywords=[]
                        ),
                        op=ast.Mult(),
                        right=ast.Constant(value=float(self.pi_params.fractal_depth))
                    )
                ],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add fractal processing
        fractal_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="process_fractal", ctx=ast.Load()),
                args=[
                    node.target,
                    ast.Name(id="_pi_fractal_depth", ctx=ast.Load())
                ],
                keywords=[]
            )
        )
        
        # Insert at beginning of loop body
        new_body = [fractal_depth, fractal_call]
        new_body.extend(node.body)
        node.body = new_body
        
        return node
    
    def _apply_circular_transforms(self, node: ast.For) -> ast.For:
        """Apply π-based circular transformations"""
        # Add circular coordinates
        radius = ast.Assign(
            targets=[ast.Name(id="_pi_radius", ctx=ast.Store())],
            value=ast.Constant(value=self.pi_params.circular_radius),
            lineno=0,
            col_offset=0
        )
        
        # Calculate angle (2π * i / n)
        angle = ast.Assign(
            targets=[ast.Name(id="_pi_angle", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.BinOp(
                    left=ast.BinOp(
                        left=ast.Constant(value=2.0),
                        op=ast.Mult(),
                        right=ast.Call(
                            func=ast.Name(id="math.pi", ctx=ast.Load()),
                            args=[],
                            keywords=[]
                        )
                    ),
                    op=ast.Mult(),
                    right=node.target
                ),
                op=ast.Div(),
                right=ast.Constant(value=100.0)  # Normalize
            ),
            lineno=0,
            col_offset=0
        )
        
        # Calculate x, y coordinates
        x_coord = ast.Assign(
            targets=[ast.Name(id="_pi_x", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Name(id="_pi_radius", ctx=ast.Load()),
                op=ast.Mult(),
                right=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="math", ctx=ast.Load()),
                        attr="cos",
                        ctx=ast.Load()
                    ),
                    args=[ast.Name(id="_pi_angle", ctx=ast.Load())],
                    keywords=[]
                )
            ),
            lineno=0,
            col_offset=0
        )
        
        y_coord = ast.Assign(
            targets=[ast.Name(id="_pi_y", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Name(id="_pi_radius", ctx=ast.Load()),
                op=ast.Mult(),
                right=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="math", ctx=ast.Load()),
                        attr="sin",
                        ctx=ast.Load()
                    ),
                    args=[ast.Name(id="_pi_angle", ctx=ast.Load())],
                    keywords=[]
                )
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add circular processing
        circular_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="process_circular", ctx=ast.Load()),
                args=[
                    node.target,
                    ast.Name(id="_pi_x", ctx=ast.Load()),
                    ast.Name(id="_pi_y", ctx=ast.Load())
                ],
                keywords=[]
            )
        )
        
        # Insert at beginning of loop body
        new_body = [radius, angle, x_coord, y_coord, circular_call]
        new_body.extend(node.body)
        node.body = new_body
        
        return node
    
    def _insert_math_constants(self, node: ast.For) -> ast.For:
        """Insert mathematical constants (π, τ, e) into loop body"""
        if not self.pi_params.constants_mode:
            return node
        
        # Add π constant
        pi_constant = ast.Assign(
            targets=[ast.Name(id="PI", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="math.pi", ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add τ (tau) constant
        tau_constant = ast.Assign(
            targets=[ast.Name(id="TAU", ctx=ast.Store())],
            value=ast.BinOp(
                left=ast.Constant(value=2.0),
                op=ast.Mult(),
                right=ast.Call(
                    func=ast.Name(id="math.pi", ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add e constant
        e_constant = ast.Assign(
            targets=[ast.Name(id="E", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="math", ctx=ast.Load()),
                    attr="e",
                    ctx=ast.Load()
                ),
                args=[],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Insert at beginning of loop body
        new_body = [pi_constant, tau_constant, e_constant]
        new_body.extend(node.body)
        node.body = new_body
        
        return node
    
    def _add_pi_easter_eggs(self, node: ast.For) -> ast.For:
        """Add Pi Day easter eggs"""
        if not self.pi_params.easter_egg_mode:
            return node
        
        # Add π day comment
        pi_comment = ast.Expr(
            value=ast.Constant(value="# 🥧 Happy Pi Day! π ≈ 3.14159...")
        )
        
        # Add π day processing
        pi_day_call = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="celebrate_pi_day", ctx=ast.Load()),
                args=[node.target],
                keywords=[]
            )
        )
        
        # Insert at beginning of loop body
        new_body = [pi_comment, pi_day_call]
        new_body.extend(node.body)
        node.body = new_body
        
        return node


class PiModeEngine:
    """Engine for applying π-based transformations to code"""
    
    def __init__(self):
        self.default_params = PiModeParams()
    
    def apply_pi_mode(self, code: str, params: Optional[PiModeParams] = None) -> str:
        """Apply π mode transformations to Python code"""
        if params is None:
            params = self.default_params
        
        try:
            tree = ast.parse(code)
            transformer = PiModeTransformer(params)
            transformed_tree = transformer.visit(tree)
            return ast.unparse(transformed_tree)
        except Exception as e:
            print(f"Error applying π mode: {e}")
            return code
    
    def get_pi_constants(self) -> Dict[str, float]:
        """Get mathematical constants for π mode"""
        return {
            "π": math.pi,
            "τ": 2 * math.pi,
            "e": math.e,
            "φ": (1 + math.sqrt(5)) / 2,  # Golden ratio
            "γ": 0.5772156649015329,  # Euler-Mascheroni constant
        }
    
    def generate_pi_art(self, params: PiModeParams) -> Dict[str, Any]:
        """Generate π-based art data"""
        return {
            "pi_mode": True,
            "constants": self.get_pi_constants(),
            "transformations": {
                "pi_loop": f"Loop length: π × {params.pi_multiplier} = {math.pi * params.pi_multiplier:.2f}",
                "waveform": f"Sine/cosine modulation at π/{8.0} phase",
                "fractal": f"Fractal depth: π × {params.fractal_depth} = {math.pi * params.fractal_depth:.2f}",
                "circular": f"Circular radius: {params.circular_radius}",
                "constants": "π, τ, e, φ, γ available",
                "easter_egg": "🥧 Pi Day celebration mode"
            },
            "mathematical_beauty": [
                "Circular harmonics with π-based coordinates",
                "Fractal patterns using π recursion depth",
                "Waveform modulation with π phase relationships",
                "Mathematical constants for precise calculations",
                "Pi Day easter eggs for mathematical fun"
            ]
        }


def main():
    """Test the π mode engine"""
    engine = PiModeEngine()
    
    print("🥧 Code Live - Pi Mode Engine")
    print("=" * 50)
    
    print("\n🥧 Mathematical Constants:")
    constants = engine.get_pi_constants()
    for name, value in constants.items():
        print(f"   {name} = {value:.10f}")
    
    print("\n🧪 Testing π Mode Transformations:")
    
    # Test code
    test_code = """
for i in range(10):
    process(i)
"""
    
    print(f"Original code:")
    print(test_code.strip())
    print()
    
    # Test π mode
    pi_params = PiModeParams(
        pi_multiplier=100.0,
        waveform_freq=1.0,
        fractal_depth=3,
        circular_radius=1.0,
        constants_mode=True,
        easter_egg_mode=True
    )
    
    pi_code = engine.apply_pi_mode(test_code, pi_params)
    print(f"π Mode code:")
    print(pi_code.strip())
    print()
    
    # Generate π art
    print("🎨 Generating π Art Data:")
    pi_art = engine.generate_pi_art(pi_params)
    for key, value in pi_art["transformations"].items():
        print(f"   {key}: {value}")
    
    print("\n🎉 Pi Mode Engine Ready!")
    print("🥧 Happy Pi Day! π ≈ 3.14159...")


if __name__ == "__main__":
    main()
