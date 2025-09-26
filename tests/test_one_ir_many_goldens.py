#!/usr/bin/env python3
"""
One IR → Many Goldens Integration Test
Ensures selector chooses the right strategy vs. flags
"""

import subprocess
import sys
from pathlib import Path


def test_strategy_selection():
    """Test that strategy selector chooses correct mode for different flags"""

    # Test case: sum of even squares
    python_code = "sum(i*i for i in range(1, 10) if i%2==0)"

    test_cases = [
        {
            "flags": {"mode": "auto", "parallel": False},
            "expected_patterns": ["# NOTE: auto-selected loops mode", "acc1 = 0", "for i in"]
        },
        {
            "flags": {"mode": "broadcast", "parallel": False},
            "expected_patterns": ["ifelse.", "sum("]
        },
        {
            "flags": {"mode": "auto", "parallel": True},
            "expected_patterns": ["# NOTE: parallelized with thread-local partials", "@threads", "parts1"]
        },
        {
            "flags": {"mode": "loops", "parallel": True, "unsafe": True},
            "expected_patterns": ["@threads", "@inbounds", "parts1"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['flags']}")

        # Build command
        cmd = [sys.executable, "-m", "pcs", "--code", python_code, "--target", "julia"]

        if test_case["flags"].get("mode"):
            cmd.extend(["--mode", test_case["flags"]["mode"]])
        if test_case["flags"].get("parallel"):
            cmd.append("--parallel")
        if test_case["flags"].get("unsafe"):
            cmd.append("--unsafe")

        # Run command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        output = result.stdout

        # Check expected patterns
        for pattern in test_case["expected_patterns"]:
            assert pattern in output, f"Pattern '{pattern}' not found in output for {test_case['flags']}"

        print(f"✅ Test {i} passed - all patterns found")

def test_dict_comprehension_strategies():
    """Test dict comprehension strategy selection"""

    python_code = "{x: x*x for x in range(1, 10) if x%2==0}"

    test_cases = [
        {
            "flags": {"mode": "auto", "parallel": False},
            "expected_patterns": ["# NOTE: auto-selected loops mode for dict operation", "Dict{Int, Int}()", "for x in"]
        },
        {
            "flags": {"mode": "auto", "parallel": True},
            "expected_patterns": ["# NOTE: parallelized with shard-merge pattern", "dict_comp_parallel"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Dict Test {i}: {test_case['flags']}")

        # Build command
        cmd = [sys.executable, "-m", "pcs", "--code", python_code, "--target", "julia"]

        if test_case["flags"].get("mode"):
            cmd.extend(["--mode", test_case["flags"]["mode"]])
        if test_case["flags"].get("parallel"):
            cmd.append("--parallel")

        # Run command
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        output = result.stdout

        # Check expected patterns
        for pattern in test_case["expected_patterns"]:
            assert pattern in output, f"Pattern '{pattern}' not found in output for {test_case['flags']}"

        print(f"✅ Dict Test {i} passed - all patterns found")

def test_fallback_behavior():
    """Test fallback behavior for non-associative operations"""

    python_code = "any(i > 50 for i in range(100))"

    result = subprocess.run([
        sys.executable, "-m", "pcs", "--code", python_code, "--target", "julia", "--parallel"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)

    assert result.returncode == 0, f"Command failed: {result.stderr}"

    output = result.stdout

    # Should fall back to sequential for non-associative 'any'
    assert "# NOTE: parallel fallback → sequential" in output
    assert "non-associative op 'any'" in output
    assert "@threads" not in output  # Should not use parallel

    print("✅ Fallback test passed - non-associative operation correctly falls back to sequential")

if __name__ == "__main__":
    test_strategy_selection()
    test_dict_comprehension_strategies()
    test_fallback_behavior()
    print("\n🎉 All one IR → many goldens tests passed!")
