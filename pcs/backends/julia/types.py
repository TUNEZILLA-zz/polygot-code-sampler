"""
Julia type mapping and type inference
"""

from typing import Optional

# Type mapping from Python/IR types to Julia types
type_mapping = {
    "int": "Int",
    "float": "Float64",
    "bool": "Bool",
    "str": "String",
    "list": "Vector",
    "dict": "Dict",
    "tuple": "Tuple",
    "set": "Set",
}

def julia_type(ir_type: str, element_type: Optional[str] = None, key_type: Optional[str] = None, value_type: Optional[str] = None) -> str:
    """Convert IR type to Julia type annotation"""
    base_type = type_mapping.get(ir_type, ir_type)

    if ir_type == "list" and element_type:
        element_julia = type_mapping.get(element_type, element_type)
        return f"Vector{{{element_julia}}}"
    elif ir_type == "dict" and key_type and value_type:
        key_julia = type_mapping.get(key_type, key_type)
        value_julia = type_mapping.get(value_type, value_type)
        return f"Dict{{{key_julia}, {value_julia}}}"
    elif ir_type == "tuple" and element_type:
        # Handle simple tuples
        return f"Tuple{{{element_type}}}"
    else:
        return base_type

def infer_type_from_expression(expr: str) -> str:
    """Infer Julia type from expression"""
    # Simple type inference based on expression patterns
    if "**" in expr or "^" in expr:
        return "Float64"  # Exponentiation often results in floats
    elif "*" in expr or "/" in expr:
        return "Float64"  # Multiplication/division can produce floats
    elif "+" in expr or "-" in expr:
        return "Int"  # Addition/subtraction of integers
    else:
        return "Int"  # Default to Int

def get_collection_type(kind: str, element_type: str = "Int") -> str:
    """Get Julia collection type for IR comprehension kind"""
    if kind == "list":
        return f"Vector{{{element_type}}}"
    elif kind == "set":
        return f"Set{{{element_type}}}"
    elif kind == "dict":
        return f"Dict{{{element_type}, {element_type}}}"
    elif kind == "group_by":
        return f"Dict{{{element_type}, Vector{{{element_type}}}}}"
    else:
        return f"Vector{{{element_type}}}"

def get_reduction_type(reduce_kind: str) -> str:
    """Get Julia type for reduction operations"""
    if reduce_kind in ("sum", "prod", "max", "min"):
        return "Int"
    elif reduce_kind in ("any", "all"):
        return "Bool"
    else:
        return "Int"
