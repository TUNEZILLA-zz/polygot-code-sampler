#!/usr/bin/env python3
"""
Test script for Go typed output feature
"""

from pcs_step3_ts import PyToIR, infer_types, render_go

def test_go_typed():
    # Test case 1: Simple list comprehension
    code1 = "squares = [x**2 for x in range(10)]"
    print("Test 1: Simple list comprehension")
    print(f"Python: {code1}")
    
    parser = PyToIR()
    ir1 = parser.parse(code1)
    type_info1 = infer_types(ir1, int_type="i64")
    
    print("\nWithout type info:")
    go1_untyped = render_go(ir1, func_name="squares_untyped")
    print(go1_untyped)
    
    print("\nWith type info:")
    go1_typed = render_go(ir1, func_name="squares_typed", type_info=type_info1)
    print(go1_typed)
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Dict comprehension
    code2 = "odds = {i: i*i for i in range(1,6) if i % 2 == 1}"
    print("Test 2: Dict comprehension")
    print(f"Python: {code2}")
    
    ir2 = parser.parse(code2)
    type_info2 = infer_types(ir2, int_type="i64")
    
    print("\nWithout type info:")
    go2_untyped = render_go(ir2, func_name="odds_untyped")
    print(go2_untyped)
    
    print("\nWith type info:")
    go2_typed = render_go(ir2, func_name="odds_typed", type_info=type_info2)
    print(go2_typed)

if __name__ == "__main__":
    test_go_typed()
