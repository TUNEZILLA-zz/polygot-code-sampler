#!/usr/bin/env python3
"""
Golden file tests for Polyglot Code Sampler

Tests Python → IR → Rust/TypeScript transformations against golden snapshots
"""

import json
from pathlib import Path

import pytest

from pcs_step3_ts import (
    PyToIR,
    infer_types,
    render_go,
    render_rust,
    render_sql,
    render_ts,
)

# Test cases: (python_code, case_name, description)
TEST_CASES = [
    (
        "m = { i: i*i for i in range(1,6) if i % 2 == 1 }",
        "dict_odds_squares",
        "Dict comprehension with filter",
    ),
    (
        "s = { (i, j) for i in range(0,3) for j in range(0,3) if i != j }",
        "set_nested_pairs",
        "Set comprehension with nested generators",
    ),
    (
        "result = [i*j for i in range(1,4) for j in range(1,4)]",
        "list_nested_products",
        "List comprehension with nested generators",
    ),
    (
        "total = sum(x for x in range(1,11) if x % 2 == 0)",
        "sum_even_numbers",
        "Sum reduction with filter",
    ),
    (
        "best = max(i*j for i in range(1,5) for j in range(1,4))",
        "max_nested_products",
        "Max reduction with nested generators",
    ),
    (
        "import math\np = math.prod(x for x in range(1,6) if x != 3)",
        "prod_filtered_range",
        "Product reduction with filter",
    ),
    (
        "ok = all(x % 2 == 0 for x in range(2,10))",
        "all_even_check",
        "All reduction with predicate",
    ),
    (
        "has_odd = any(x % 2 == 1 for x in range(1,10))",
        "any_odd_check",
        "Any reduction with predicate",
    ),
    (
        "min_val = min(x**2 for x in range(1,6))",
        "min_squares",
        "Min reduction with transformation",
    ),
    (
        "complex = {i: j for i in range(1,4) for j in range(1,4) if i != j}",
        "dict_nested_complex",
        "Complex nested dict comprehension",
    ),
]

# SQL test cases: (python_code, case_name, description)
SQL_TEST_CASES = [
    (
        "[i*2 for i in range(10) if i % 2 == 0]",
        "sql_simple_list",
        "Simple list comprehension to SQL",
    ),
    (
        "sum(i for i in range(10) if i % 2 == 0)",
        "sql_sum_reduction",
        "Sum reduction to SQL",
    ),
    (
        "[i*j for i in range(1,4) for j in range(1,4) if i != j]",
        "sql_nested_cross_join",
        "Nested comprehension with CROSS JOIN",
    ),
    (
        "{i: i*i for i in range(1,6) if i % 2 == 1}",
        "sql_dict_comprehension",
        "Dict comprehension to SQL SELECT key, value",
    ),
    (
        "max(i*j for i in range(1,5) for j in range(1,4))",
        "sql_max_reduction",
        "Max reduction to SQL",
    ),
    (
        "any(x % 2 == 1 for x in range(1,10))",
        "sql_any_reduction",
        "Any reduction to SQL EXISTS",
    ),
    (
        "[i for i in range(10, 5)]",
        "sql_empty_range",
        "Empty range optimization",
    ),
    (
        "[i*j for i in range(1,3) for j in range(1,3) if i != j]",
        "sql_nested_optimized",
        "Nested comprehension with predicate pushdown",
    ),
]

# Dialect-specific test cases
SQL_DIALECT_TEST_CASES = [
    (
        "[i*2 for i in range(10) if i % 2 == 0]",
        "sql_simple_list",
        "Simple list comprehension",
    ),
    (
        "[i*j for i in range(1,4) for j in range(1,4) if i != j]",
        "sql_nested_cross_join",
        "Nested comprehension with CROSS JOIN",
    ),
    (
        "sum(i for i in range(10) if i % 2 == 0)",
        "sql_sum_reduction",
        "Sum reduction",
    ),
    (
        "any(x % 2 == 1 for x in range(1,10))",
        "sql_any_exists",
        "Any reduction to EXISTS",
    ),
]

# Go test cases: (python_code, case_name, description)
GO_TEST_CASES = [
    (
        "[i*2 for i in range(10) if i % 2 == 0]",
        "go_simple_list",
        "Simple list comprehension to Go",
    ),
    (
        "sum(i for i in range(10) if i % 2 == 0)",
        "go_sum_reduction",
        "Sum reduction to Go",
    ),
    (
        "{i: i*i for i in range(1,6) if i % 2 == 1}",
        "go_dict_comprehension",
        "Dict comprehension to Go map",
    ),
    (
        "{(i, j) for i in range(1,3) for j in range(1,3) if i != j}",
        "go_set_tuple",
        "Set comprehension with tuples to Go struct",
    ),
    (
        "max(i*j for i in range(1,5) for j in range(1,4))",
        "go_max_reduction",
        "Max reduction to Go",
    ),
    (
        "any(x % 2 == 1 for x in range(1,10))",
        "go_any_reduction",
        "Any reduction to Go",
    ),
]

# Go parallel test cases
GO_PARALLEL_TEST_CASES = [
    (
        "sum(i*i for i in range(100) if i % 2 == 0)",
        "go_parallel_sum",
        "Parallel sum reduction with goroutines",
    ),
    (
        "[i*i for i in range(20) if i % 2 == 0]",
        "go_parallel_list",
        "Parallel list comprehension with goroutines",
    ),
    (
        "max(i*j for i in range(1,10) for j in range(1,10))",
        "go_parallel_max",
        "Parallel max reduction with goroutines",
    ),
    (
        "any(x > 50 for x in range(100))",
        "go_parallel_any",
        "Parallel any reduction with goroutines",
    ),
]

# Type inference test cases: (python_code, case_name, description)
TYPE_TEST_CASES = [
    (
        "squares = [x**2 for x in range(10)]",
        "typed_list_squares",
        "Typed list comprehension - Vec<i64>",
    ),
    (
        "odds = {i: i*i for i in range(1,6) if i % 2 == 1}",
        "typed_dict_odds",
        "Typed dict comprehension - HashMap<i64, i64>",
    ),
    (
        "evens = {x for x in range(0,10) if x % 2 == 0}",
        "typed_set_evens",
        "Typed set comprehension - HashSet<i64>",
    ),
    (
        "total = sum(x for x in range(10) if x % 2 == 0)",
        "typed_sum_reduction",
        "Typed sum reduction - i64",
    ),
    (
        "has_odd = any(x % 2 == 1 for x in range(1,10))",
        "typed_any_reduction",
        "Typed any reduction - bool",
    ),
    (
        "max_val = max(i*j for i in range(1,5) for j in range(1,4))",
        "typed_max_reduction",
        "Typed max reduction - i64",
    ),
]

# Parallel test cases: (python_code, case_name, description)
PARALLEL_TEST_CASES = [
    (
        "squares = [x**2 for x in range(1, 1000)]",
        "par_squares",
        "Parallel list comprehension with large range",
    ),
    (
        "sum_evens = sum(x for x in range(1, 1000) if x % 2 == 0)",
        "par_sum_evens",
        "Parallel sum reduction with filter",
    ),
    (
        "data = {i: i*i for i in range(1, 100) if i % 2 == 1}",
        "par_dict_squares",
        "Parallel dict comprehension",
    ),
    (
        "evens = [x for x in range(0, 100, 2)]",
        "par_step_range",
        "Parallel range with step != 1 (filter emulation)",
    ),
]


def run_case(
    python_code: str,
    case_name: str,
    update_golden: bool,
    golden_dir: Path,
    parallel: bool = False,
    use_types: bool = False,
    use_sql: bool = False,
    sql_dialect: str = "postgresql",
    use_go: bool = False,
    use_go_parallel: bool = False,
):
    """Run a single test case and compare/update golden files"""
    # Parse Python code to IR
    parser = PyToIR()
    ir = parser.parse(python_code)

    # Generate outputs
    ir_json = ir.to_json()

    if use_sql:
        # SQL-only mode
        sql_output = render_sql(ir, func_name=case_name, dialect=sql_dialect)
        rust_output = ""
        ts_output = ""
        go_output = ""
    elif use_go:
        # Go-only mode
        go_output = render_go(ir, func_name=case_name, parallel=use_go_parallel)
        rust_output = ""
        ts_output = ""
        sql_output = ""
    elif use_types:
        # Use type inference
        type_info = infer_types(ir, int_type="i64")
        rust_output = render_rust(
            ir, func_name=case_name, parallel=parallel, type_info=type_info
        )
        ts_output = render_ts(ir, func_name=case_name, type_info=type_info)
        sql_output = ""
        go_output = ""
    else:
        # Legacy behavior
        rust_output = render_rust(ir, func_name=case_name, parallel=parallel)
        ts_output = render_ts(ir, func_name=case_name)
        sql_output = ""
        go_output = ""

    # Define golden file paths
    ir_file = golden_dir / f"{case_name}.ir.json"
    rust_file = golden_dir / f"{case_name}.rust.txt"
    ts_file = golden_dir / f"{case_name}.ts.txt"
    sql_file = golden_dir / f"{case_name}.sql.txt"
    go_file = golden_dir / f"{case_name}.go.txt"

    if update_golden:
        # Update golden files
        ir_file.write_text(ir_json)
        if use_sql:
            sql_file.write_text(sql_output)
        elif use_go:
            go_file.write_text(go_output)
        else:
            rust_file.write_text(rust_output)
            ts_file.write_text(ts_output)
        print(f"✅ Updated golden files for {case_name}")
        return True
    else:
        # Compare with golden files
        if not ir_file.exists():
            pytest.fail(f"Golden IR file missing: {ir_file}")
        if use_sql:
            if not sql_file.exists():
                pytest.fail(f"Golden SQL file missing: {sql_file}")
        elif use_go:
            if not go_file.exists():
                pytest.fail(f"Golden Go file missing: {go_file}")
        else:
            if not rust_file.exists():
                pytest.fail(f"Golden Rust file missing: {rust_file}")
            if not ts_file.exists():
                pytest.fail(f"Golden TypeScript file missing: {ts_file}")

        # Load golden files
        golden_ir = ir_file.read_text()
        if use_sql:
            golden_sql = sql_file.read_text()
        elif use_go:
            golden_go = go_file.read_text()
        else:
            golden_rust = rust_file.read_text()
            golden_ts = ts_file.read_text()

        # Compare IR (normalize JSON)
        try:
            current_ir_obj = json.loads(ir_json)
            golden_ir_obj = json.loads(golden_ir)
            assert current_ir_obj == golden_ir_obj, f"IR mismatch for {case_name}"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in IR for {case_name}: {e}")

        # Compare outputs
        if use_sql:
            assert sql_output == golden_sql, f"SQL output mismatch for {case_name}"
        elif use_go:
            assert go_output == golden_go, f"Go output mismatch for {case_name}"
        else:
            assert rust_output == golden_rust, f"Rust output mismatch for {case_name}"
            assert ts_output == golden_ts, f"TypeScript output mismatch for {case_name}"

        return True


@pytest.mark.parametrize("python_code,case_name,description", TEST_CASES)
def test_golden_files(python_code, case_name, description, update_golden, golden_dir):
    """Test each case against golden files"""
    print(f"\n🧪 Testing {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(python_code, case_name, update_golden, golden_dir)
    assert success, f"Test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", PARALLEL_TEST_CASES)
def test_parallel_rust_golden(
    python_code, case_name, description, update_golden, golden_dir
):
    """Test parallel Rust cases against golden files"""
    print(f"\n⚡️ Testing parallel {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(python_code, case_name, update_golden, golden_dir, parallel=True)
    assert success, f"Parallel test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", TYPE_TEST_CASES)
def test_type_inference_golden(
    python_code, case_name, description, update_golden, golden_dir
):
    """Test type inference cases against golden files"""
    print(f"\n🎯 Testing typed {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(
        python_code, case_name, update_golden, golden_dir, use_types=True
    )
    assert success, f"Type inference test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", SQL_TEST_CASES)
def test_sql_golden(python_code, case_name, description, update_golden, golden_dir):
    """Test SQL cases against golden files"""
    print(f"\n🗄️ Testing SQL {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(python_code, case_name, update_golden, golden_dir, use_sql=True)
    assert success, f"SQL test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", SQL_DIALECT_TEST_CASES)
def test_sql_postgresql_golden(
    python_code, case_name, description, update_golden, golden_dir
):
    """Test SQL PostgreSQL dialect cases against golden files"""
    print(f"\n🐘 Testing SQL PostgreSQL {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(
        python_code,
        f"{case_name}.pg",
        update_golden,
        golden_dir,
        use_sql=True,
        sql_dialect="postgresql",
    )
    assert success, f"SQL PostgreSQL test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", SQL_DIALECT_TEST_CASES)
def test_sql_sqlite_golden(
    python_code, case_name, description, update_golden, golden_dir
):
    """Test SQL SQLite dialect cases against golden files"""
    print(f"\n🗃️ Testing SQL SQLite {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(
        python_code,
        f"{case_name}.sqlite",
        update_golden,
        golden_dir,
        use_sql=True,
        sql_dialect="sqlite",
    )
    assert success, f"SQL SQLite test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", GO_TEST_CASES)
def test_go_golden(python_code, case_name, description, update_golden, golden_dir):
    """Test Go cases against golden files"""
    print(f"\n🐹 Testing Go {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(python_code, case_name, update_golden, golden_dir, use_go=True)
    assert success, f"Go test case {case_name} failed"


@pytest.mark.parametrize("python_code,case_name,description", GO_PARALLEL_TEST_CASES)
def test_go_parallel_golden(
    python_code, case_name, description, update_golden, golden_dir
):
    """Test Go parallel cases against golden files"""
    print(f"\n🚀 Testing Go Parallel {case_name}: {description}")
    print(f"   Python: {python_code.strip()}")

    success = run_case(
        python_code,
        case_name,
        update_golden,
        golden_dir,
        use_go=True,
        use_go_parallel=True,
    )
    assert success, f"Go parallel test case {case_name} failed"


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
        pytest.fail(
            f"Missing golden files: {missing_files}\nRun with --update-golden to generate them"
        )


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
    assert (
        "x ** 2" in rust_output or "x * x" in rust_output
    ), "Rust should contain squaring operation"
    assert "x ** 2" in ts_output, "TypeScript should contain squaring operation"

    # Both should have proper function structure
    assert "pub fn test()" in rust_output, "Rust should have proper function signature"
    assert (
        "export function test()" in ts_output
    ), "TypeScript should have proper function signature"
