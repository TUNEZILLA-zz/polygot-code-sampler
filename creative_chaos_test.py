#!/usr/bin/env python3
"""
🎛️ Code Live - Creative Chaos Test
==================================

This script tests our push-proof system with creative chaos:
- Intentional formatting issues
- Mixed line endings
- Trailing whitespace
- YAML syntax errors
- Large file simulation
- Secret patterns (fake)
- Case conflicts
- Merge conflicts

Let's see if our push-proof system catches everything! 🚀
"""

import json
import os
import sys
from pathlib import Path

import yaml


def create_chaos_files():
    """Create various chaos files to test our push-proof system"""

    # 1. Python file with formatting issues
    chaos_py = """
# This file has intentional formatting issues
def bad_function(  ):
    x=1+2*3
    y = [1,2,3,4,5]
    z = {"key": "value", "another": "thing"}
    return x,y,z

class BadClass:
    def __init__(self):
        self.value=42
        self.name="test"

    def method(self):
        return self.value*2
"""

    # 2. YAML file with syntax errors
    chaos_yaml = """
# This YAML has intentional syntax errors
name: Creative Chaos Test
version: 1.0.0
description: Testing push-proof system

# Intentional syntax error - missing colon
bad_key value
# Another error - wrong indentation
  nested:
    value: 42
    another: "string"

# List with mixed types
items:
  - string
  - 42
  - true
  - null
"""

    # 3. JSON file with syntax errors
    chaos_json = """
{
  "name": "Creative Chaos Test",
  "version": "1.0.0",
  "description": "Testing push-proof system",
  "bad_key": "value",
  "nested": {
    "value": 42,
    "another": "string"
  },
  "items": ["string", 42, true, null],
  "bad_syntax": "missing comma"
  "another": "value"
}
"""

    # 4. File with trailing whitespace
    chaos_whitespace = """
# This file has trailing whitespace on purpose
def function_with_whitespace():
    x = 1
    y = 2
    z = 3
    return x + y + z

# More trailing whitespace
class ClassWithWhitespace:
    def __init__(self):
        self.value = 42
        self.name = "test"
"""

    # 5. File with mixed line endings (CRLF and LF)
    chaos_line_endings = """# This file has mixed line endings\r\n
def function_with_mixed_endings():\n
    x = 1\r\n
    y = 2\n
    z = 3\r\n
    return x + y + z\n
"""

    # 6. File with case conflicts
    chaos_case = """
# This file has case conflicts
def Function():
    return "uppercase"

def function():
    return "lowercase"

class Class:
    pass

class class:
    pass
"""

    # 7. File with potential secrets (fake)
    chaos_secrets = """
# This file has fake secrets to test secret detection
API_KEY = "sk-1234567890abcdef1234567890abcdef"
AWS_ACCESS_KEY = "AKIA1234567890ABCDEF"
PASSWORD = "super_secret_password_123"
DATABASE_URL = "postgresql://user:password@localhost:5432/db"
"""

    # 8. Large file simulation (create a file that's close to the limit)
    chaos_large = "# Large file simulation\n" + "x" * (50 * 1024 * 1024)  # 50MB

    # Create all the chaos files
    files_to_create = [
        ("chaos_formatting.py", chaos_py),
        ("chaos_syntax.yaml", chaos_yaml),
        ("chaos_syntax.json", chaos_json),
        ("chaos_whitespace.py", chaos_whitespace),
        ("chaos_line_endings.py", chaos_line_endings),
        ("chaos_case.py", chaos_case),
        ("chaos_secrets.py", chaos_secrets),
        ("chaos_large.txt", chaos_large),
    ]

    print("🎛️ Creating creative chaos files...")
    for filename, content in files_to_create:
        filepath = Path(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created {filename}")

    print("\n🎯 Chaos files created! Now let's test our push-proof system...")


def test_push_proof_system():
    """Test our push-proof system with the chaos files"""

    print("\n🧪 Testing Push-Proof System")
    print("=" * 40)

    # Test 1: Pre-commit hooks
    print("\n1️⃣ Testing pre-commit hooks...")
    os.system("pre-commit run --all-files")

    # Test 2: Git LFS check
    print("\n2️⃣ Testing Git LFS...")
    os.system("git lfs ls-files")

    # Test 3: Large file detection
    print("\n3️⃣ Testing large file detection...")
    os.system("find . -type f -size +50M -not -path './.git/*'")

    # Test 4: Secret detection
    print("\n4️⃣ Testing secret detection...")
    os.system("grep -r 'sk-' . --exclude-dir=.git || echo 'No secrets found'")

    # Test 5: YAML validation
    print("\n5️⃣ Testing YAML validation...")
    try:
        with open("chaos_syntax.yaml") as f:
            yaml.safe_load(f)
        print("✅ YAML is valid")
    except yaml.YAMLError as e:
        print(f"❌ YAML error: {e}")

    # Test 6: JSON validation
    print("\n6️⃣ Testing JSON validation...")
    try:
        with open("chaos_syntax.json") as f:
            json.load(f)
        print("✅ JSON is valid")
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")


def cleanup_chaos():
    """Clean up the chaos files"""
    print("\n🧹 Cleaning up chaos files...")
    chaos_files = [
        "chaos_formatting.py",
        "chaos_syntax.yaml",
        "chaos_syntax.json",
        "chaos_whitespace.py",
        "chaos_line_endings.py",
        "chaos_case.py",
        "chaos_secrets.py",
        "chaos_large.txt",
    ]

    for filename in chaos_files:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"🗑️ Removed {filename}")

    print("✅ Chaos cleanup complete!")


if __name__ == "__main__":
    print("🎛️ Code Live - Creative Chaos Test")
    print("===================================")
    print("Testing our push-proof system with intentional chaos!")
    print()

    try:
        # Create chaos files
        create_chaos_files()

        # Test the push-proof system
        test_push_proof_system()

        # Clean up
        cleanup_chaos()

        print("\n🎉 Creative Chaos Test Complete!")
        print("Our push-proof system should have caught all the issues!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        cleanup_chaos()
        sys.exit(1)
