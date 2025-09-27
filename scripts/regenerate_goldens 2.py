#!/usr/bin/env python3
"""
Regenerate golden files from IR fixture
"""

import json
import subprocess
import sys
from pathlib import Path


def load_fixture(fixture_path):
    """Load test fixture from JSON"""
    with open(fixture_path) as f:
        return json.load(f)


def generate_julia_code(python_code, flags):
    """Generate Julia code using PCS"""
    cmd = [sys.executable, "-m", "pcs", "--code", python_code, "--target", "julia"]

    if flags.get("mode"):
        cmd.extend(["--mode", flags["mode"]])
    if flags.get("parallel"):
        cmd.append("--parallel")
    if flags.get("unsafe"):
        cmd.append("--unsafe")

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate Julia code: {result.stderr}")

    return result.stdout


def regenerate_goldens():
    """Regenerate all golden files from fixture"""

    print("🔄 Regenerating Golden Files from IR Fixture")
    print("=" * 50)

    # Load fixture
    fixture_path = (
        Path(__file__).parent.parent / "tests" / "fixtures" / "sum_even_squares.json"
    )
    fixture = load_fixture(fixture_path)

    print(f"📝 Fixture: {fixture['description']}")
    print(f"🐍 Python Code: {fixture['python_code']}")
    print()

    for test_case in fixture["test_cases"]:
        print(f"🔄 Regenerating: {test_case['name']}")
        print(f"   Flags: {test_case['flags']}")

        try:
            # Use test-case specific Python code if available, otherwise use fixture default
            python_code = test_case.get("python_code", fixture["python_code"])
            generated = generate_julia_code(python_code, test_case["flags"])

            # Write to golden file
            golden_path = (
                Path(__file__).parent.parent
                / "tests"
                / "golden"
                / "julia"
                / test_case["golden_file"]
            )
            golden_path.parent.mkdir(parents=True, exist_ok=True)

            with open(golden_path, "w") as f:
                f.write(generated)

            print(f"   ✅ Written to: {golden_path}")

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            return False

        print()

    print("🎉 All golden files regenerated successfully!")
    return True


def main():
    """Main regeneration runner"""

    # Confirm regeneration
    print("⚠️  This will overwrite existing golden files!")
    confirm = input("Continue? (y/N): ").strip().lower()

    if confirm != "y":
        print("❌ Regeneration cancelled")
        sys.exit(1)

    success = regenerate_goldens()

    if success:
        print("\n✅ Golden files regeneration completed!")
        print("🧪 Run 'make test-fixtures' to validate the new golden files")
        sys.exit(0)
    else:
        print("\n💥 Golden files regeneration failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
