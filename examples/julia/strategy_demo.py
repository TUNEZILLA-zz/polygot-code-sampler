#!/usr/bin/env python3
"""
Comprehensive demo of Julia backend strategy selector and new features
"""

import subprocess
import sys
from pathlib import Path


def run_demo():
    """Run comprehensive demo of Julia backend features"""

    print("🧪 Julia Backend Strategy Selector Demo")
    print("=" * 50)

    # Test cases demonstrating different strategies
    test_cases = [
        {
            "name": "Auto Mode - Small N (Broadcast)",
            "code": "sum(i*i for i in range(1, 10))",
            "args": ["--target", "julia", "--mode", "auto"],
            "expected": "broadcast mode",
        },
        {
            "name": "Auto Mode - Small N with Filter (Loops)",
            "code": "sum(i*i for i in range(1, 10) if i%2==0)",
            "args": ["--target", "julia", "--mode", "auto"],
            "expected": "loops mode",
        },
        {
            "name": "Auto Mode - Large N (Loops)",
            "code": "sum(i*i for i in range(1, 10000))",
            "args": ["--target", "julia", "--mode", "auto"],
            "expected": "loops mode",
        },
        {
            "name": "Explicit Broadcast Mode",
            "code": "sum(i*i for i in range(1, 100) if i%2==0)",
            "args": ["--target", "julia", "--mode", "broadcast"],
            "expected": "ifelse. dot-fusion",
        },
        {
            "name": "Parallel with Thread-Locals",
            "code": "sum(i*i for i in range(1, 100) if i%2==0)",
            "args": ["--target", "julia", "--mode", "auto", "--parallel"],
            "expected": "thread-local partials",
        },
        {
            "name": "Parallel Dict with Shards",
            "code": "{x: x*x for x in range(1, 10) if x%2==0}",
            "args": ["--target", "julia", "--mode", "auto", "--parallel"],
            "expected": "shard-merge pattern",
        },
        {
            "name": "Unsafe Optimizations",
            "code": "sum(i*i for i in range(1, 100) if i%2==0)",
            "args": ["--target", "julia", "--mode", "auto", "--parallel", "--unsafe"],
            "expected": "@inbounds",
        },
        {
            "name": "No Explain Mode",
            "code": "sum(i*i for i in range(1, 100) if i%2==0)",
            "args": [
                "--target",
                "julia",
                "--mode",
                "auto",
                "--parallel",
                "--no-explain",
            ],
            "expected": "clean output",
        },
        {
            "name": "Non-Associative Fallback",
            "code": "any(i > 50 for i in range(100))",
            "args": ["--target", "julia", "--mode", "auto", "--parallel"],
            "expected": "sequential fallback",
        },
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"Code: {test['code']}")
        print(f"Args: {' '.join(test['args'])}")
        print(f"Expected: {test['expected']}")
        print("-" * 30)

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pcs", "--code", test["code"]] + test["args"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent.parent,
            )

            if result.returncode == 0:
                print("✅ Generated successfully:")
                print(result.stdout)
            else:
                print(f"❌ Failed: {result.stderr}")

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n🎉 Demo completed! All {len(test_cases)} test cases processed.")
    print("\n📊 Strategy Selection Summary:")
    print("- Auto mode intelligently selects broadcast for small N without filters")
    print("- Auto mode selects loops for large N or operations with filters")
    print("- Parallel mode uses thread-locals for reductions and shards for dicts")
    print("- Unsafe mode adds @inbounds optimizations")
    print("- Explain mode provides clear decision explanations")
    print("- No-explain mode produces clean production code")


if __name__ == "__main__":
    run_demo()
