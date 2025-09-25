#!/usr/bin/env python3
"""
Golden file tests for Polyglot Code Sampler

Tests Python → IR → Rust/TypeScript transformations against golden snapshots
"""

import pytest
import json
from pathlib import Path
from pcs_step3_ts import PyToIR, render_rust, render_ts

# Test cases: (python_code, case_name, description)
TEST_CASES = [
    (
        "m = { i: i*i for i in range(1,6) if i % 2 == 1 }",
        "dict_odds_squares",
        "Dict comprehension with filter"
    ),
    (
        "s = { (i, j) for i in range(0,3) for j in range(0,3) if i != j }",
        "set_nested_pairs",
        "Set comprehension with nested generators"
    ),
    (
        "result = [i*j for i in range(1,4) for j in range(1,4)]",
        "list_nested_products",
        "List comprehension with nested generators"
    ),
    (
        "total = sum(x for x in range(1,11) if x % 2 == 0)",
        "sum_even_numbers",
        "Sum reduction with filter"
    ),
    (
        "best = max(i*j for i in range(1,5) for j in range(1,4))",
        "max_nested_products",
        "Max reduction with nested generators"
    ),
    (
        "import math\np = math.prod(x for x in range(1,6) if x != 3)",
        "prod_filtered_range",
        "Product reduction with filter"
    ),
    (
        "ok = all(x % 2 == 0 for x in range(2,10))",
        "all_even_check",
        "All reduction with predicate"
    ),
    (
        "has_odd = any(x % 2 == 1 for x in range(1,10))",
        "any_odd_check",
        "Any reduction with predicate"
    ),
    (
        "min_val = min(x**2 for x in range(1,6))",
        "min_squares",
        "Min reduction with transformation"
    ),
    (
        "complex = {i: j for i in range(1,4) for j in range(1,4) if i != j}",
        "dict_nested_complex",
        "Complex nested dict comprehension"
    )
]

def run_case(python_code: str, case_name: str, update_golden: bool, golden_dir: Path):
    """Run a single test case and compare/update golden files"""
    # Parse Python code to IR
    parser = PyToIR()
    ir = parser.parse(python_code)
    
    # Generate outputs
    ir_json = ir.to_json()
    rust_output = render_rust(ir, func_name=case_name)
    ts_output = render_ts(ir, func_name=case_name)
    
    # Define golden file paths
    ir_file = golden_dir / f"{case_name}.ir.json"
    rust_file = golden_dir / f"{case_name}.rust.txt"
    ts_file = golden_dir / f"{case_name}.ts.txt"
    
    if update_golden:
        # Update golden files
        ir_file.write_text(ir_json)
        rust_file.write_text(rust_output)
        ts_file.write_text(ts_output)
        print(f"✅ Updated golden files for {case_name}")
        return True
    else:
        # Compare with golden files
        if not ir_file.exists():
            pytest.fail(f"Golden IR file missing: {ir_file}")
        if not rust_file.exists():
            pytest.fail(f"Golden Rust file missing: {rust_file}")
        if not ts_file.exists():
            pytest.fail(f"Golden TypeScript file missing: {ts_file}")
        
        # Load golden files
        golden_ir = ir_file.read_text()
        golden_rust = rust_file.read_text()
        golden_ts = ts_file.read_text()
        
        # Compare IR (normalize JSON)
        try:
            current_ir_obj = json.loads(ir_json)
            golden_ir_obj = json.loads(golden_ir)
            assert current_ir_obj == golden_ir_obj, f"IR mismatch for {case_name}"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in IR for {case_name}: {e}")
        
        # Compare Rust output
        assert rust_output == golden_rust, f"Rust output mismatch for {case_name}"
        
        # Compare TypeScript output
        assert ts_output == golden_ts, f"TypeScript output mismatch for {case_name}"
        
        return True

@pytest.mark.parametrize("python_code,case_name,description", TEST_CASES)
def test_golden_files(python_code, case_name, description, update_golden, golden_dir):
    """Test each case against golden files"""
    print(f"\n🧪 Testing {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")
    
    success = run_case(python_code, case_name, update_golden, golden_dir)
    assert success, f"Test case {case_name} failed"

def test_all_golden_files_exist(update_golden, golden_dir):
    """Ensure all golden files exist (run after --update-golden)"""
    if update_golden:
        pytest.skip("Skipping existence check when updating golden files")
    
    missing_files = []
    for _, case_name, _ in TEST_CASES:
        ir_file = golden_dir / f"{case_name}.ir.json"
        rust_file = golden_dir / f"{case_name}.rust.txt"
        ts_file = golden_dir / f"{case_name}.ts.txt"
        
        if not ir_file.exists():
            missing_files.append(str(ir_file))
        if not rust_file.exists():
            missing_files.append(str(rust_file))
        if not ts_file.exists():
            missing_files.append(str(ts_file))
    
    if missing_files:
        pytest.fail(f"Missing golden files: {missing_files}\nRun with --update-golden to generate them")

def test_ir_consistency():
    """Test that IR is consistent across multiple parses"""
    parser = PyToIR()
    test_code = "result = [x**2 for x in range(1,6) if x % 2 == 0]"
    
    # Parse multiple times
    ir1 = parser.parse(test_code)
    ir2 = parser.parse(test_code)
    
    # Should be identical
    assert ir1.to_json() == ir2.to_json(), "IR should be consistent across parses"

def test_rust_ts_parity():
    """Test that Rust and TypeScript outputs are functionally equivalent"""
    parser = PyToIR()
    test_code = "squares = [x**2 for x in range(1,6)]"
    
    ir = parser.parse(test_code)
    rust_output = render_rust(ir, func_name="test")
    ts_output = render_ts(ir, func_name="test")
    
    # Both should contain the same mathematical operations
    assert "x ** 2" in rust_output or "x * x" in rust_output, "Rust should contain squaring operation"
    assert "x ** 2" in ts_output, "TypeScript should contain squaring operation"
    
    # Both should have proper function structure
    assert "pub fn test()" in rust_output, "Rust should have proper function signature"
    assert "export function test()" in ts_output, "TypeScript should have proper function signature"
