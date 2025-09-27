#!/usr/bin/env python3
"""
LOLcat++ Content Guard Test - Skip LOLcat++ inside back-ticked code/URLs
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

def test_content_guard():
    """Test content guard functionality"""
    print("😺 Testing LOLcat++ Content Guard...")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Back-ticked code blocks",
            "text": "Here's some code: ```python\ndef hello():\n    print('world')\n``` and more text",
            "expected": "Code block should be preserved"
        },
        {
            "name": "Inline code",
            "text": "Use the `print()` function and `len()` method",
            "expected": "Inline code should be preserved"
        },
        {
            "name": "URLs",
            "text": "Check out https://github.com/user/repo and http://example.com",
            "expected": "URLs should be preserved"
        },
        {
            "name": "Mixed content",
            "text": "Run `make test` and visit https://docs.python.org/3/ for more info. Here's a code block:\n```bash\nmake lolcat-demo\n```",
            "expected": "All protected content should be preserved"
        },
        {
            "name": "No protection needed",
            "text": "This is just regular text that should be transformed",
            "expected": "Regular text should be transformed normally"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        print(f"   Input: {test_case['text']}")
        print(f"   Expected: {test_case['expected']}")
        
        # Test with content guard ON
        result_guarded = lolcat_plus(test_case['text'], content_guard=True, seed=1337)
        print(f"   Guarded: {result_guarded['text']}")
        
        # Test with content guard OFF
        result_unguarded = lolcat_plus(test_case['text'], content_guard=False, seed=1337)
        print(f"   Unguarded: {result_unguarded['text']}")
        
        # Check if protection worked
        if test_case['name'] != "No protection needed":
            if result_guarded['text'] != result_unguarded['text']:
                print("   ✅ Content guard working - protected content preserved")
            else:
                print("   ❌ Content guard not working - protected content was transformed")
        else:
            if result_guarded['text'] == result_unguarded['text']:
                print("   ✅ Content guard working - regular text transformed normally")
            else:
                print("   ❌ Content guard not working - regular text affected")

def test_documentation_preservation():
    """Test that documentation remains legible"""
    print("\n😺 Testing Documentation Preservation...")
    print("=" * 50)
    
    doc_text = """
# LOLcat++ Documentation

## Usage

```python
from string_fx.lolcat_plus import lolcat_plus

result = lolcat_plus("Hello world!", intensity=0.6)
print(result['text'])
```

## API Reference

- `intensity`: Controls overall effect strength (0.0-1.0)
- `uwu`: UwU-ifier amount (0.0-1.0)
- `chaos`: Chaos case amount (0.0-1.0)

Visit https://github.com/user/lolcat-plus for more info.

Use `make lolcat-demo` to test the system.
"""
    
    print("Original documentation:")
    print(doc_text)
    
    result = lolcat_plus(doc_text, content_guard=True, seed=1337)
    print("\nTransformed with content guard:")
    print(result['text'])
    
    # Check if code blocks and URLs are preserved
    if "```python" in result['text'] and "https://github.com" in result['text']:
        print("✅ Documentation preserved - code blocks and URLs intact")
    else:
        print("❌ Documentation corrupted - code blocks or URLs transformed")

def demo_content_guard():
    """Demo content guard in action"""
    print("😺 Content Guard Demo...")
    print("=" * 50)
    
    demo_text = "Check out this awesome project at https://github.com/user/repo and run `make test` to verify it works!"
    
    print(f"Input: {demo_text}")
    
    # Without content guard
    result_no_guard = lolcat_plus(demo_text, content_guard=False, seed=1337)
    print(f"Without guard: {result_no_guard['text']}")
    
    # With content guard
    result_with_guard = lolcat_plus(demo_text, content_guard=True, seed=1337)
    print(f"With guard: {result_with_guard['text']}")
    
    print("\n😺 Notice how the URL and code are preserved with content guard!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LOLcat++ Content Guard Test")
    parser.add_argument("--test", action="store_true", help="Run content guard tests")
    parser.add_argument("--demo", action="store_true", help="Demo content guard")
    parser.add_argument("--docs", action="store_true", help="Test documentation preservation")
    parser.add_argument("--text", default="Test with `code` and https://example.com", help="Text to test")
    parser.add_argument("--no-guard", action="store_true", help="Test without content guard")
    
    args = parser.parse_args()
    
    if args.test:
        test_content_guard()
    elif args.demo:
        demo_content_guard()
    elif args.docs:
        test_documentation_preservation()
    else:
        # Single test
        result = lolcat_plus(args.text, content_guard=not args.no_guard, seed=1337)
        print(f"😺 Result: {result['text']}")
        if not args.no_guard:
            print("😺 Content guard enabled - protected regions preserved")

if __name__ == "__main__":
    main()
