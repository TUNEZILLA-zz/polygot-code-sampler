"""
Unit tests for the central renderer API to guard against future signature drift.
"""

import pytest
from pcs.core import PyToIR
from pcs.renderer_api import render


class TestRendererAPI:
    """Test the central renderer API with over-full kwargs to ensure no signature drift."""
    
    def setup_method(self):
        """Set up a simple IR for testing."""
        parser = PyToIR()
        self.ir = parser.parse("[x**2 for x in range(5)]")
    
    def test_adapter_handles_over_full_kwargs(self):
        """Test that the adapter filters kwargs correctly for all backends."""
        backends = ["rust", "ts", "go", "csharp", "julia", "sql"]
        
        # Intentionally over-full kwargs that no single backend accepts
        over_full_kwargs = {
            "parallel": True,
            "mode": "broadcast", 
            "unsafe": True,
            "explain": False,
            "dialect": "postgresql",
            "int_type": "i64",
            "strict_types": True,
            "threads": 8,
            "no_explain": True,
            "sql_dialect": "sqlite",
            "execute_sql": True,
            "some_random_param": "should_be_ignored",
            "another_unused_flag": 42
        }
        
        for backend in backends:
            # This should not raise TypeError due to signature mismatch
            output = render(backend, self.ir, **over_full_kwargs)
            
            # Basic sanity checks
            assert len(output) > 0, f"{backend} should generate non-empty output"
            assert isinstance(output, str), f"{backend} should return string"
    
    def test_adapter_handles_minimal_kwargs(self):
        """Test that the adapter works with minimal kwargs."""
        backends = ["rust", "ts", "go", "csharp", "julia", "sql"]
        
        for backend in backends:
            # Minimal kwargs
            output = render(backend, self.ir)
            
            assert len(output) > 0, f"{backend} should generate non-empty output"
            assert isinstance(output, str), f"{backend} should return string"
    
    def test_adapter_handles_empty_kwargs(self):
        """Test that the adapter works with empty kwargs."""
        backends = ["rust", "ts", "go", "csharp", "julia", "sql"]
        
        for backend in backends:
            # Empty kwargs
            output = render(backend, self.ir, **{})
            
            assert len(output) > 0, f"{backend} should generate non-empty output"
            assert isinstance(output, str), f"{backend} should return string"
    
    def test_adapter_handles_unknown_backend(self):
        """Test that the adapter raises ValueError for unknown backends."""
        with pytest.raises(ValueError, match="Unknown target"):
            render("unknown_backend", self.ir)
    
    def test_rust_ts_header_assertions(self):
        """Test that Rust and TypeScript generate proper function headers."""
        # Test Rust
        rust_output = render("rust", self.ir, func_name="test_function")
        assert "pub fn test_function()" in rust_output, "Rust should have pub fn header"
        
        # Test TypeScript  
        ts_output = render("ts", self.ir, func_name="test_function")
        assert "export function test_function()" in ts_output, "TypeScript should have export function header"
    
    def test_param_passthrough_safety(self):
        """Test that unused parameters are safely ignored by backends."""
        # Test that SQL backend ignores parallel/mode/unsafe
        sql_output = render("sql", self.ir, parallel=True, mode="broadcast", unsafe=True)
        assert "SELECT" in sql_output, "SQL should generate SELECT statement"
        
        # Test that Rust backend ignores dialect
        rust_output = render("rust", self.ir, dialect="postgresql")
        assert "pub fn" in rust_output, "Rust should generate pub fn"
        
        # Test that Julia backend ignores int_type
        julia_output = render("julia", self.ir, int_type="i64")
        assert "function" in julia_output, "Julia should generate function"
    
    def test_edge_cases(self):
        """Test adapter with edge case IRs."""
        parser = PyToIR()
        
        # Simple list comprehension
        simple_ir = parser.parse("[x for x in range(1)]")
        for backend in ["rust", "ts", "go"]:
            output = render(backend, simple_ir)
            assert len(output) > 0, f"{backend} should handle simple IR"
        
        # Simple reduction
        sum_ir = parser.parse("sum(x for x in range(3))")
        for backend in ["rust", "ts", "go"]:
            output = render(backend, sum_ir)
            assert len(output) > 0, f"{backend} should handle reduction IR"
