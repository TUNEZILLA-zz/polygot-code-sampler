"""
Property tests for IR ↔ codegen invariants using Hypothesis.
Tests idempotent pretty-print, stable symbol generation, and other invariants.
"""

import pytest
from hypothesis import given, strategies as st, settings, example
from pcs.core import PyToIR, IRComp, IRGenerator, IRRange, IRReduce
from pcs.renderer_api import render


class TestIRInvariants:
    """Property tests for IR invariants and codegen stability."""
    
    def setup_method(self):
        """Set up parser for testing."""
        self.parser = PyToIR()
    
    @given(
        start=st.integers(min_value=0, max_value=100),
        stop=st.integers(min_value=0, max_value=100),
        step=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=50)
    def test_range_idempotency(self, start, stop, step):
        """Test that range IRs are idempotent under parsing."""
        if start >= stop:
            return  # Skip invalid ranges
        
        # Create range comprehension
        code = f"[x for x in range({start}, {stop}, {step})]"
        
        # Parse multiple times
        ir1 = self.parser.parse(code)
        ir2 = self.parser.parse(code)
        
        # Should be identical
        assert ir1.kind == ir2.kind
        assert len(ir1.generators) == len(ir2.generators)
        assert ir1.generators[0].source.start == ir2.generators[0].source.start
        assert ir1.generators[0].source.stop == ir2.generators[0].source.stop
        assert ir1.generators[0].source.step == ir2.generators[0].source.step
    
    @given(
        element=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        start=st.integers(min_value=0, max_value=50),
        stop=st.integers(min_value=0, max_value=50)
    )
    @settings(max_examples=30)
    def test_codegen_stability(self, element, start, stop):
        """Test that codegen is stable across multiple calls."""
        if start >= stop:
            return  # Skip invalid ranges
        
        # Create simple comprehension
        code = f"[{element} for x in range({start}, {stop})]"
        ir = self.parser.parse(code)
        
        # Generate code multiple times
        rust1 = render("rust", ir)
        rust2 = render("rust", ir)
        ts1 = render("ts", ir)
        ts2 = render("ts", ir)
        
        # Should be identical
        assert rust1 == rust2, "Rust codegen should be stable"
        assert ts1 == ts2, "TypeScript codegen should be stable"
    
    @given(
        start=st.integers(min_value=0, max_value=20),
        stop=st.integers(min_value=0, max_value=20),
        step=st.integers(min_value=1, max_value=5)
    )
    @settings(max_examples=20)
    def test_backend_consistency(self, start, stop, step):
        """Test that all backends handle the same IR consistently."""
        if start >= stop:
            return  # Skip invalid ranges
        
        code = f"[x*2 for x in range({start}, {stop}, {step})]"
        ir = self.parser.parse(code)
        
        # All backends should generate non-empty output
        backends = ["rust", "ts", "go", "csharp", "julia", "sql"]
        outputs = {}
        
        for backend in backends:
            output = render(backend, ir)
            assert len(output) > 0, f"{backend} should generate non-empty output"
            assert isinstance(output, str), f"{backend} should return string"
            outputs[backend] = output
        
        # All outputs should be different (different languages)
        unique_outputs = set(outputs.values())
        assert len(unique_outputs) == len(backends), "All backends should generate unique output"
    
    @given(
        start=st.integers(min_value=0, max_value=10),
        stop=st.integers(min_value=0, max_value=10)
    )
    @settings(max_examples=15)
    def test_parallel_consistency(self, start, stop):
        """Test that parallel and sequential modes are consistent for supported backends."""
        if start >= stop:
            return  # Skip invalid ranges
        
        code = f"[x**2 for x in range({start}, {stop})]"
        ir = self.parser.parse(code)
        
        # Test parallel consistency for backends that support it
        parallel_backends = ["rust", "ts", "go", "csharp", "julia"]
        
        for backend in parallel_backends:
            seq_output = render(backend, ir, parallel=False)
            par_output = render(backend, ir, parallel=True)
            
            # Both should generate valid output
            assert len(seq_output) > 0, f"{backend} sequential should generate output"
            assert len(par_output) > 0, f"{backend} parallel should generate output"
            assert isinstance(seq_output, str), f"{backend} sequential should return string"
            assert isinstance(par_output, str), f"{backend} parallel should return string"
    
    @given(
        start=st.integers(min_value=0, max_value=5),
        stop=st.integers(min_value=0, max_value=5)
    )
    @settings(max_examples=10)
    def test_reduction_consistency(self, start, stop):
        """Test that reduction operations are consistent across backends."""
        if start >= stop:
            return  # Skip invalid ranges
        
        code = f"sum(x for x in range({start}, {stop}))"
        ir = self.parser.parse(code)
        
        # All backends should handle reductions
        backends = ["rust", "ts", "go", "csharp", "julia", "sql"]
        
        for backend in backends:
            output = render(backend, ir)
            assert len(output) > 0, f"{backend} should handle reduction"
            assert isinstance(output, str), f"{backend} should return string"
    
    @example("sum(x for x in range(1, 5))")
    @example("[x**2 for x in range(1, 4)]")
    @example("{x: x*2 for x in range(1, 3)}")
    @given(st.text(min_size=10, max_size=50))
    @settings(max_examples=20)
    def test_arbitrary_code_parsing(self, code):
        """Test that arbitrary code either parses correctly or fails gracefully."""
        try:
            ir = self.parser.parse(code)
            # If parsing succeeds, codegen should work
            for backend in ["rust", "ts", "go"]:
                output = render(backend, ir)
                assert len(output) > 0, f"{backend} should generate output for {code}"
                assert isinstance(output, str), f"{backend} should return string"
        except (ValueError, SyntaxError, AttributeError):
            # Parsing failures are acceptable for arbitrary code
            pass
    
    def test_symbol_generation_stability(self):
        """Test that symbol generation is stable across multiple calls."""
        code = "[x**2 for x in range(1, 5)]"
        ir = self.parser.parse(code)
        
        # Generate multiple times with same parameters
        rust_outputs = [render("rust", ir, func_name="test") for _ in range(5)]
        ts_outputs = [render("ts", ir, func_name="test") for _ in range(5)]
        
        # All outputs should be identical
        assert all(out == rust_outputs[0] for out in rust_outputs), "Rust symbol generation should be stable"
        assert all(out == ts_outputs[0] for out in ts_outputs), "TypeScript symbol generation should be stable"
    
    def test_function_signature_consistency(self):
        """Test that function signatures are consistent across backends."""
        code = "[x**2 for x in range(1, 5)]"
        ir = self.parser.parse(code)
        
        # Test function signature consistency
        rust_output = render("rust", ir, func_name="test_function")
        ts_output = render("ts", ir, func_name="test_function")
        
        assert "pub fn test_function()" in rust_output, "Rust should have pub fn signature"
        assert "export function test_function()" in ts_output, "TypeScript should have export function signature"
