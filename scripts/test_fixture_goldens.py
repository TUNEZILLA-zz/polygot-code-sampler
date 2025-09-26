#!/usr/bin/env python3
"""
Test harness for IR fixture → 4 goldens regression safety net
"""

import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

def load_fixture(fixture_path):
    """Load test fixture from JSON"""
    with open(fixture_path, 'r') as f:
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
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to generate Julia code: {result.stderr}")
    
    return result.stdout

def load_golden(golden_path):
    """Load golden file content"""
    with open(golden_path, 'r') as f:
        return f.read()

def test_fixture_goldens():
    """Test all golden files against fixture"""
    
    print("🧪 Testing IR Fixture → 4 Goldens Regression Safety Net")
    print("=" * 60)
    
    # Load fixture
    fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "sum_even_squares.json"
    fixture = load_fixture(fixture_path)
    
    print(f"📝 Fixture: {fixture['description']}")
    print(f"🐍 Python Code: {fixture['python_code']}")
    print(f"🎯 Expected Result: {fixture['expected_result']}")
    print()
    
    all_passed = True
    
    for test_case in fixture["test_cases"]:
        print(f"🧪 Testing: {test_case['name']}")
        print(f"   Flags: {test_case['flags']}")
        print(f"   Description: {test_case['description']}")
        
        try:
            # Use test-case specific Python code if available, otherwise use fixture default
            python_code = test_case.get("python_code", fixture["python_code"])
            generated = generate_julia_code(python_code, test_case["flags"])
            
            # Load golden file
            golden_path = Path(__file__).parent.parent / "tests" / "golden" / "julia" / test_case["golden_file"]
            golden = load_golden(golden_path)
            
            # Compare (normalize whitespace and ignore module names)
            def normalize_code(code):
                lines = []
                for line in code.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("module PCS_Generated_"):
                        # Also ignore const PCS_Generated lines
                        if not line.startswith("const PCS_Generated ="):
                            lines.append(line)
                return "\n".join(lines)
            
            generated_norm = normalize_code(generated)
            golden_norm = normalize_code(golden)
            
            if generated_norm == golden_norm:
                print("   ✅ PASSED - Generated matches golden")
            else:
                print("   ❌ FAILED - Generated does not match golden")
                print("   📝 Generated:")
                print("   " + "\n   ".join(generated.split("\n")))
                print("   📝 Golden:")
                print("   " + "\n   ".join(golden.split("\n")))
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def validate_results():
    """Validate that generated code produces expected results"""
    
    print("🔍 Validating Generated Code Results")
    print("=" * 40)
    
    fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "sum_even_squares.json"
    fixture = load_fixture(fixture_path)
    
    # Test with different sizes
    test_sizes = [5, 10, 20]
    
    for size in test_sizes:
        print(f"📊 Testing with range(1, {size+1})")
        
        # Generate test code
        test_code = f"sum(i*i for i in range(1, {size+1}) if i%2==0)"
        
        # Calculate expected result
        expected = sum(i*i for i in range(1, size+1) if i%2==0)
        print(f"   Expected: {expected}")
        
        # Test different modes
        modes = [
            {"mode": "loops", "parallel": False},
            {"mode": "broadcast", "parallel": False},
            {"mode": "loops", "parallel": True}
        ]
        
        for mode in modes:
            try:
                generated = generate_julia_code(test_code, mode)
                
                # Write to temp file and run with Julia
                with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as f:
                    f.write(generated)
                    temp_file = f.name
                
                try:
                    # Run Julia code
                    result = subprocess.run([
                        "julia", "--project", "-e", 
                        f"include(\"{temp_file}\"); println(PCS_Generated.main())"
                    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
                    
                    if result.returncode == 0:
                        actual = int(result.stdout.strip())
                        if actual == expected:
                            print(f"   ✅ {mode} mode: {actual}")
                        else:
                            print(f"   ❌ {mode} mode: expected {expected}, got {actual}")
                    else:
                        print(f"   ❌ {mode} mode: Julia execution failed: {result.stderr}")
                        
                finally:
                    os.unlink(temp_file)
                    
            except Exception as e:
                print(f"   ❌ {mode} mode: {e}")

def main():
    """Main test runner"""
    
    # Test golden file matching
    golden_passed = test_fixture_goldens()
    
    # Validate results
    validate_results()
    
    if golden_passed:
        print("\n🎉 All fixture golden tests passed!")
        print("✅ Regression safety net is intact!")
        sys.exit(0)
    else:
        print("\n💥 Some fixture golden tests failed!")
        print("❌ Regression safety net compromised!")
        sys.exit(1)

if __name__ == "__main__":
    main()
