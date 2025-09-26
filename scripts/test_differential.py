#!/usr/bin/env python3
"""
Differential test harness: IR → Julia vs hand-written reference
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_differential_test():
    """Run differential test comparing generated Julia to hand-written reference"""

    print("🧪 Running Differential Tests: IR → Julia vs Hand-written Reference")
    print("=" * 70)

    # Test case: sum of even squares
    python_code = "sum(i*i for i in range(1, 100) if i%2==0)"

    # Generate Julia code
    print(f"📝 Generating Julia code for: {python_code}")
    result = subprocess.run([
        sys.executable, "-m", "pcs",
        "--code", python_code,
        "--target", "julia",
        "--mode", "auto",
        "--parallel"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)

    if result.returncode != 0:
        print(f"❌ Failed to generate Julia code: {result.stderr}")
        return False

    # Write generated code to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as f:
        f.write(result.stdout)
        generated_file = f.name

    try:
        # Copy to tests directory for inclusion
        test_dir = Path(__file__).parent.parent / "tests"
        target_file = test_dir / "generated_map_filter_reduce.jl"

        with open(generated_file) as src, open(target_file, 'w') as dst:
            dst.write(src.read())

        print(f"✅ Generated Julia code written to {target_file}")

        # Run Julia differential test
        print("🚀 Running Julia differential test...")
        julia_result = subprocess.run([
            "julia", "--project", "-e",
            f"include(\"{test_dir}/diff_map_filter_reduce.jl\")"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)

        if julia_result.returncode == 0:
            print("✅ Differential test passed!")
            print(julia_result.stdout)
            return True
        else:
            print("❌ Differential test failed!")
            print("STDOUT:", julia_result.stdout)
            print("STDERR:", julia_result.stderr)
            return False

    finally:
        # Clean up temporary file
        os.unlink(generated_file)
        if target_file.exists():
            target_file.unlink()

def main():
    """Main test runner"""
    success = run_differential_test()

    if success:
        print("\n🎉 All differential tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Differential tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
