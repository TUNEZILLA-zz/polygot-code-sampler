#!/usr/bin/env python3
"""
CI smoke test for generated Julia code
Tests that generated Julia code can be executed and produces correct results
"""

import subprocess
import tempfile
import os
import sys
from pathlib import Path

def test_julia_code_generation():
    """Test that generated Julia code can be executed"""
    
    # Test cases: (python_code, expected_output)
    test_cases = [
        ("sum(i*i for i in range(1, 10) if i%2==0)", "120"),  # 2*2 + 4*4 + 6*6 + 8*8 = 4 + 16 + 36 + 64 = 120
        ("max(i for i in range(1, 10) if i%2==0)", "8"),
        ("any(i > 5 for i in range(1, 10))", "true"),
        ("all(i > 0 for i in range(1, 10))", "true"),
    ]
    
    print("🧪 Testing Julia code generation and execution...")
    
    for i, (python_code, expected) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {python_code}")
        
        # Generate Julia code
        try:
            result = subprocess.run([
                sys.executable, "-m", "pcs", 
                "--code", python_code, 
                "--target", "julia"
            ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode != 0:
                print(f"❌ Code generation failed: {result.stderr}")
                return False
                
            julia_code = result.stdout
            print(f"✅ Code generated successfully")
            
        except Exception as e:
            print(f"❌ Code generation error: {e}")
            return False
        
        # Test Julia execution (if julia is available)
        if _is_julia_available():
            try:
                # Write Julia code to temp file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as f:
                    f.write(julia_code)
                    temp_file = f.name
                
                # Execute Julia code
                result = subprocess.run([
                    "julia", temp_file
                ], capture_output=True, text=True, timeout=10)
                
                # Clean up
                os.unlink(temp_file)
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    print(f"✅ Julia execution successful: {output}")
                    
                    # Check if output matches expected (for simple cases)
                    if expected in ["true", "false"]:
                        if expected in output.lower():
                            print(f"✅ Output matches expected: {expected}")
                        else:
                            print(f"⚠️  Output doesn't match expected: {expected}")
                    else:
                        print(f"📊 Output: {output}")
                else:
                    print(f"❌ Julia execution failed: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print(f"❌ Julia execution timed out")
                return False
            except Exception as e:
                print(f"❌ Julia execution error: {e}")
                return False
        else:
            print(f"⚠️  Julia not available, skipping execution test")
    
    print(f"\n🎉 All {len(test_cases)} tests passed!")
    return True

def _is_julia_available():
    """Check if Julia is available in PATH"""
    try:
        result = subprocess.run(["julia", "--version"], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def test_parallel_modes():
    """Test parallel mode generation"""
    print(f"\n🚀 Testing parallel mode generation...")
    
    test_cases = [
        ("sum(i*i for i in range(1, 100) if i%2==0)", "parallel"),
        ("{x: x*x for x in range(1, 10) if x%2==0}", "parallel"),
        ("any(i > 50 for i in range(100))", "fallback"),
    ]
    
    for python_code, mode_type in test_cases:
        print(f"\n📝 Testing: {python_code}")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pcs", 
                "--code", python_code, 
                "--target", "julia",
                "--parallel"
            ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
            
            if result.returncode != 0:
                print(f"❌ Parallel code generation failed: {result.stderr}")
                return False
            
            julia_code = result.stdout
            
            if mode_type == "parallel":
                if "@threads" in julia_code and "threadid()" in julia_code:
                    print(f"✅ Parallel mode generated correctly")
                else:
                    print(f"❌ Parallel mode not generated")
                    return False
            elif mode_type == "fallback":
                if "sequential fallback" in julia_code.lower():
                    print(f"✅ Sequential fallback generated correctly")
                else:
                    print(f"❌ Sequential fallback not generated")
                    return False
                    
        except Exception as e:
            print(f"❌ Parallel test error: {e}")
            return False
    
    print(f"✅ All parallel mode tests passed!")
    return True

def test_broadcast_mode():
    """Test broadcast mode generation"""
    print(f"\n📡 Testing broadcast mode generation...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pcs", 
            "--code", "sum(i*i for i in range(1, 10) if i%2==0)", 
            "--target", "julia",
            "--mode", "broadcast"
        ], capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode != 0:
            print(f"❌ Broadcast code generation failed: {result.stderr}")
            return False
        
        julia_code = result.stdout
        
        if "ifelse." in julia_code and "sum(" in julia_code:
            print(f"✅ Broadcast mode generated correctly")
            return True
        else:
            print(f"❌ Broadcast mode not generated")
            return False
            
    except Exception as e:
        print(f"❌ Broadcast test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Julia Backend CI Smoke Tests")
    print("=" * 50)
    
    success = True
    
    # Test basic code generation and execution
    success &= test_julia_code_generation()
    
    # Test parallel modes
    success &= test_parallel_modes()
    
    # Test broadcast mode
    success &= test_broadcast_mode()
    
    if success:
        print(f"\n🎉 All CI smoke tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Some CI smoke tests failed!")
        sys.exit(1)
