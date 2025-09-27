#!/usr/bin/env python3
"""
🎛️ Code Live - Audio Effects for Code Loops
============================================

Like a digital audio workstation (DAW) for code generation!
Apply reverb, delay, reverse, chorus, distortion, and LFO modulation to for loops.
"""

import ast
import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class FxType(Enum):
    """Audio effect types for code loops"""
    REVERB = "reverb"
    DELAY = "delay"
    REVERSE = "reverse"
    CHORUS = "chorus"
    DISTORTION = "distortion"
    LFO = "lfo"
    SWING = "swing"
    GATE = "gate"


@dataclass
class FxSpec:
    """Audio effect specification"""
    chain: List[str]
    params: Dict[str, Any]
    safety: Dict[str, Any]


@dataclass
class FxParams:
    """Parameters for specific audio effects"""
    # Reverb
    reverb_taps: int = 3
    reverb_decay: float = 0.6
    
    # Delay
    delay_steps: int = 3
    delay_extend_loop: bool = True
    
    # Chorus
    chorus_voices: int = 3
    chorus_jitter: float = 0.05
    
    # Distortion
    distortion_gain: float = 2.5
    distortion_clip: float = 1.0
    
    # LFO
    lfo_target: str = "param:alpha"
    lfo_freq: float = 0.5
    lfo_depth: float = 0.3
    
    # Swing
    swing_ratio: float = 0.6  # 60/40 swing
    
    # Gate
    gate_threshold: float = 0.1


class LoopFxRewriter(ast.NodeTransformer):
    """AST transformer that applies audio effects to for loops"""
    
    def __init__(self, fx_spec: FxSpec):
        self.fx_spec = fx_spec
        self.fx_params = FxParams(**fx_spec.params)
        self.safety = fx_spec.safety
    
    def visit_For(self, node: ast.For) -> ast.For:
        """Transform for loops with audio effects"""
        # Visit children first
        node = self.generic_visit(node)
        
        # Only transform if body is effect-safe (no break/continue/yield)
        if self._has_control_flow(node):
            return node
        
        # Apply effects in chain order
        for fx_kind in self.fx_spec.chain:
            node = self._apply_fx(node, fx_kind)
        
        return node
    
    def _has_control_flow(self, node: ast.For) -> bool:
        """Check if loop has control flow that makes effects unsafe"""
        for child in ast.walk(node):
            if isinstance(child, (ast.Break, ast.Continue, ast.Yield, ast.Return)):
                return True
        return False
    
    def _apply_fx(self, node: ast.For, fx_kind: str) -> ast.For:
        """Apply a specific audio effect to a for loop"""
        if fx_kind == "reverse":
            return self._apply_reverse(node)
        elif fx_kind == "delay":
            return self._apply_delay(node)
        elif fx_kind == "reverb":
            return self._apply_reverb(node)
        elif fx_kind == "chorus":
            return self._apply_chorus(node)
        elif fx_kind == "distortion":
            return self._apply_distortion(node)
        elif fx_kind == "lfo":
            return self._apply_lfo(node)
        elif fx_kind == "swing":
            return self._apply_swing(node)
        elif fx_kind == "gate":
            return self._apply_gate(node)
        else:
            return node
    
    def _apply_reverse(self, node: ast.For) -> ast.For:
        """Apply reverse effect - iterate in reverse order"""
        # Create reversed iteration
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            # Handle range() calls
            if len(node.iter.args) == 1:
                # range(n) -> reversed(range(n))
                node.iter = ast.Call(
                    func=ast.Name(id="reversed", ctx=ast.Load()),
                    args=[node.iter],
                    keywords=[]
                )
            elif len(node.iter.args) == 2:
                # range(start, stop) -> reversed(range(start, stop))
                node.iter = ast.Call(
                    func=ast.Name(id="reversed", ctx=ast.Load()),
                    args=[node.iter],
                    keywords=[]
                )
            elif len(node.iter.args) == 3:
                # range(start, stop, step) -> reversed(range(start, stop, step))
                node.iter = ast.Call(
                    func=ast.Name(id="reversed", ctx=ast.Load()),
                    args=[node.iter],
                    keywords=[]
                )
        return node
    
    def _apply_delay(self, node: ast.For) -> ast.For:
        """Apply delay effect - offset processing by N steps"""
        steps = min(self.fx_params.delay_steps, self.safety.get("max_expand", 8))
        if steps <= 0:
            return node
        
        # Create delay buffer and extend loop if needed
        delay_buffer_name = f"_delay_buffer_{id(node)}"
        
        # Add delay buffer initialization before loop
        delay_init = ast.Assign(
            targets=[ast.Name(id=delay_buffer_name, ctx=ast.Store())],
            value=ast.List(elts=[], ctx=ast.Load())
        )
        
        # Modify loop body to include delay processing
        new_body = []
        
        # Add current item to delay buffer
        append_call = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=delay_buffer_name, ctx=ast.Load()),
                    attr="append",
                    ctx=ast.Load()
                ),
                args=[node.target],
                keywords=[]
            )
        )
        new_body.append(append_call)
        
        # Add original body
        new_body.extend(node.body)
        
        # Add delayed processing
        if self.fx_params.delay_extend_loop:
            delay_condition = ast.If(
                test=ast.Compare(
                    left=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id=delay_buffer_name, ctx=ast.Load()),
                            attr="__len__",
                            ctx=ast.Load()
                        ),
                        args=[],
                        keywords=[]
                    ),
                    ops=[ast.Gt()],
                    comparators=[ast.Constant(value=steps)]
                ),
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id="process_delayed", ctx=ast.Load()),
                            args=[
                                ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Name(id=delay_buffer_name, ctx=ast.Load()),
                                        attr="pop",
                                        ctx=ast.Load()
                                    ),
                                    args=[ast.Constant(value=0)],
                                    keywords=[]
                                )
                            ],
                            keywords=[]
                        )
                    )
                ],
                orelse=[]
            )
            new_body.append(delay_condition)
        
        node.body = new_body
        return node
    
    def _apply_reverb(self, node: ast.For) -> ast.For:
        """Apply reverb effect - add decaying echoes of previous iterations"""
        taps = min(self.fx_params.reverb_taps, self.safety.get("max_expand", 8))
        decay = self.fx_params.reverb_decay
        
        if taps <= 0:
            return node
        
        new_body = []
        
        # Add original processing
        new_body.extend(node.body)
        
        # Add reverb taps
        for tap in range(1, taps + 1):
            tap_condition = ast.If(
                test=ast.Compare(
                    left=node.target,
                    ops=[ast.GtE()],
                    comparators=[ast.Constant(value=tap)]
                ),
                body=[
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id="process", ctx=ast.Load()),
                            args=[
                                ast.BinOp(
                                    left=node.target,
                                    op=ast.Sub(),
                                    right=ast.Constant(value=tap)
                                ),
                                ast.Constant(value=decay ** tap)
                            ],
                            keywords=[]
                        )
                    )
                ],
                orelse=[]
            )
            new_body.append(tap_condition)
        
        node.body = new_body
        return node
    
    def _apply_chorus(self, node: ast.For) -> ast.For:
        """Apply chorus effect - add multiple voices with slight variations"""
        voices = min(self.fx_params.chorus_voices, self.safety.get("max_expand", 8))
        jitter = self.fx_params.chorus_jitter
        
        if voices <= 0:
            return node
        
        new_body = []
        
        # Add original processing
        new_body.extend(node.body)
        
        # Add chorus voices
        for voice in range(1, voices + 1):
            # Create jittered index
            jittered_index = ast.BinOp(
                left=node.target,
                op=ast.Add(),
                right=ast.Constant(value=voice * jitter)
            )
            
            # Add chorus voice processing
            chorus_call = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id="process_chorus", ctx=ast.Load()),
                    args=[jittered_index, ast.Constant(value=voice)],
                    keywords=[]
                )
            )
            new_body.append(chorus_call)
        
        node.body = new_body
        return node
    
    def _apply_distortion(self, node: ast.For) -> ast.For:
        """Apply distortion effect - saturate/clip values"""
        gain = self.fx_params.distortion_gain
        clip = self.fx_params.distortion_clip
        
        new_body = []
        
        # Wrap original body with distortion
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # Apply distortion to function calls
                distorted_call = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="apply_distortion", ctx=ast.Load()),
                        args=[stmt.value, ast.Constant(value=gain), ast.Constant(value=clip)],
                        keywords=[]
                    )
                )
                new_body.append(distorted_call)
            else:
                new_body.append(stmt)
        
        node.body = new_body
        return node
    
    def _apply_lfo(self, node: ast.For) -> ast.For:
        """Apply LFO modulation - modulate parameters with sine wave"""
        target = self.fx_params.lfo_target
        freq = self.fx_params.lfo_freq
        depth = self.fx_params.lfo_depth
        
        # Add LFO calculation
        lfo_calc = ast.Assign(
            targets=[ast.Name(id="_lfo_value", ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="math", ctx=ast.Load()),
                    attr="sin",
                    ctx=ast.Load()
                ),
                args=[
                    ast.BinOp(
                        left=ast.BinOp(
                            left=ast.Constant(value=2 * math.pi),
                            op=ast.Mult(),
                            right=ast.BinOp(
                                left=ast.Constant(value=freq),
                                op=ast.Mult(),
                                right=node.target
                            )
                        ),
                        op=ast.Div(),
                        right=ast.Constant(value=100)  # Normalize
                    )
                ],
                keywords=[]
            ),
            lineno=0,
            col_offset=0
        )
        
        # Add LFO modulation to body
        new_body = [lfo_calc]
        new_body.extend(node.body)
        
        node.body = new_body
        return node
    
    def _apply_swing(self, node: ast.For) -> ast.For:
        """Apply swing effect - alternate timing patterns"""
        ratio = self.fx_params.swing_ratio
        
        # Create swing condition
        swing_condition = ast.If(
            test=ast.Compare(
                left=ast.BinOp(
                    left=node.target,
                    op=ast.Mod(),
                    right=ast.Constant(value=2)
                ),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=0)]
            ),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="process_heavy", ctx=ast.Load()),
                        args=[node.target],
                        keywords=[]
                    )
                )
            ],
            orelse=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="process_light", ctx=ast.Load()),
                        args=[node.target],
                        keywords=[]
                    )
                )
            ]
        )
        
        node.body = [swing_condition]
        return node
    
    def _apply_gate(self, node: ast.For) -> ast.For:
        """Apply gate effect - skip iterations under threshold"""
        threshold = self.fx_params.gate_threshold
        
        # Create gate condition
        gate_condition = ast.If(
            test=ast.Compare(
                left=ast.Call(
                    func=ast.Name(id="get_value", ctx=ast.Load()),
                    args=[node.target],
                    keywords=[]
                ),
                ops=[ast.Gt()],
                comparators=[ast.Constant(value=threshold)]
            ),
            body=node.body,
            orelse=[]
        )
        
        node.body = [gate_condition]
        return node


class AudioFxEngine:
    """Engine for applying audio effects to code loops"""
    
    def __init__(self):
        self.default_safety = {
            "max_expand": 8,
            "max_cost_multiplier": 3.0
        }
    
    def apply_fx_to_code(self, code: str, fx_spec: FxSpec) -> str:
        """Apply audio effects to Python code"""
        try:
            tree = ast.parse(code)
            rewriter = LoopFxRewriter(fx_spec)
            transformed_tree = rewriter.visit(tree)
            return ast.unparse(transformed_tree)
        except Exception as e:
            print(f"Error applying audio effects: {e}")
            return code
    
    def create_fx_spec(self, fx_chain: List[str], params: Dict[str, Any], safety: Optional[Dict[str, Any]] = None) -> FxSpec:
        """Create an audio effects specification"""
        if safety is None:
            safety = self.default_safety.copy()
        
        return FxSpec(
            chain=fx_chain,
            params=params,
            safety=safety
        )
    
    def get_supported_effects(self) -> List[str]:
        """Get list of supported audio effects"""
        return [fx.value for fx in FxType]
    
    def validate_fx_spec(self, fx_spec: FxSpec) -> Tuple[bool, List[str]]:
        """Validate an audio effects specification"""
        issues = []
        
        # Check if all effects in chain are supported
        for fx in fx_spec.chain:
            if fx not in [fx_type.value for fx_type in FxType]:
                issues.append(f"Unsupported effect: {fx}")
        
        # Check safety limits
        max_expand = fx_spec.safety.get("max_expand", 8)
        total_expand = 0
        
        for fx in fx_spec.chain:
            if fx == "reverb":
                total_expand += fx_spec.params.get("reverb_taps", 3)
            elif fx == "chorus":
                total_expand += fx_spec.params.get("chorus_voices", 3)
            elif fx == "delay":
                total_expand += 1  # Delay adds buffer overhead
        
        if total_expand > max_expand:
            issues.append(f"Total expansion ({total_expand}) exceeds max_expand ({max_expand})")
        
        return len(issues) == 0, issues


def main():
    """Test the audio effects engine"""
    engine = AudioFxEngine()
    
    print("🎛️ Code Live - Audio Effects Engine")
    print("=" * 50)
    
    print("\n🎵 Supported Effects:")
    for fx in engine.get_supported_effects():
        print(f"  - {fx}")
    
    print("\n🧪 Testing Audio Effects:")
    
    # Test code
    test_code = """
for i in range(10):
    process(i)
"""
    
    # Test reverb effect
    print("\n1️⃣ Testing Reverb Effect:")
    reverb_spec = engine.create_fx_spec(
        fx_chain=["reverb"],
        params={"reverb_taps": 3, "reverb_decay": 0.6}
    )
    reverb_code = engine.apply_fx_to_code(test_code, reverb_spec)
    print(f"Original: {test_code.strip()}")
    print(f"Reverb:   {reverb_code.strip()}")
    
    # Test delay effect
    print("\n2️⃣ Testing Delay Effect:")
    delay_spec = engine.create_fx_spec(
        fx_chain=["delay"],
        params={"delay_steps": 3, "delay_extend_loop": True}
    )
    delay_code = engine.apply_fx_to_code(test_code, delay_spec)
    print(f"Original: {test_code.strip()}")
    print(f"Delay:    {delay_code.strip()}")
    
    # Test reverse effect
    print("\n3️⃣ Testing Reverse Effect:")
    reverse_spec = engine.create_fx_spec(
        fx_chain=["reverse"],
        params={}
    )
    reverse_code = engine.apply_fx_to_code(test_code, reverse_spec)
    print(f"Original: {test_code.strip()}")
    print(f"Reverse:  {reverse_code.strip()}")
    
    # Test chorus effect
    print("\n4️⃣ Testing Chorus Effect:")
    chorus_spec = engine.create_fx_spec(
        fx_chain=["chorus"],
        params={"chorus_voices": 3, "chorus_jitter": 0.05}
    )
    chorus_code = engine.apply_fx_to_code(test_code, chorus_spec)
    print(f"Original: {test_code.strip()}")
    print(f"Chorus:   {chorus_code.strip()}")
    
    # Test effect chain
    print("\n5️⃣ Testing Effect Chain (Reverse + Reverb):")
    chain_spec = engine.create_fx_spec(
        fx_chain=["reverse", "reverb"],
        params={"reverb_taps": 2, "reverb_decay": 0.5}
    )
    chain_code = engine.apply_fx_to_code(test_code, chain_spec)
    print(f"Original: {test_code.strip()}")
    print(f"Chain:    {chain_code.strip()}")
    
    # Validate effects
    print("\n6️⃣ Validating Effects:")
    is_valid, issues = engine.validate_fx_spec(chain_spec)
    if is_valid:
        print("✅ Effects validation: PASSED")
    else:
        print("❌ Effects validation: FAILED")
        for issue in issues:
            print(f"   - {issue}")
    
    print("\n🎉 Audio Effects Engine Ready!")


if __name__ == "__main__":
    main()
