"""
Exhaustive associativity gate - central mapping for operations
"""

# Central mapping for operations → associativity & identity
ASSOC_TABLE = {
    "+": {"types": {"Int", "Float64"}, "identity": "0"},
    "*": {"types": {"Int", "Float64"}, "identity": "1"},
    "sum": {"types": {"Int", "Float64"}, "identity": "0"},
    "prod": {"types": {"Int", "Float64"}, "identity": "1"},
    "max": {"types": {"Int", "Float64"}, "identity": "-Inf"},
    "min": {"types": {"Int", "Float64"}, "identity": "Inf"},
    "|": {"types": {"Int"}, "identity": "0"},
    "&": {"types": {"Int"}, "identity": "-1"},
    "^": {"types": {"Int"}, "identity": "0"},
}

def is_associative(op: str, elem_type: str) -> bool:
    """Check if operation is associative for given type"""
    if op not in ASSOC_TABLE:
        return False
    return elem_type in ASSOC_TABLE[op]["types"]

def get_associative_ops() -> set:
    """Get all associative operations"""
    return set(ASSOC_TABLE.keys())

def get_supported_types(op: str) -> set:
    """Get supported types for an operation"""
    if op not in ASSOC_TABLE:
        return set()
    return ASSOC_TABLE[op]["types"]

def assoc_identity(op: str, elem_type: str) -> str:
    """Get identity element for associative operation"""
    if op not in ASSOC_TABLE:
        return "0"

    ident = ASSOC_TABLE[op]["identity"]

    # Handle special cases for Inf/-Inf
    if ident == "Inf":
        return "Inf32" if elem_type == "Int" else "Inf"
    elif ident == "-Inf":
        return "-Inf32" if elem_type == "Int" else "-Inf"

    return ident

def get_parallel_note(op: str, elem_type: str) -> str:
    """Generate NOTE comment for parallelization"""
    if not is_associative(op, elem_type):
        return f"# NOTE: parallel fallback → sequential: non-associative op '{op}' or unsupported type '{elem_type}'"

    identity = assoc_identity(op, elem_type)
    return f"# NOTE: parallelized with thread-local partials (op '{op}', identity {identity}, type {elem_type})"

def get_associativity_explanation(op: str, elem_type: str) -> str:
    """Get detailed explanation of associativity decision"""
    if op not in ASSOC_TABLE:
        return f"Operation '{op}' not in associativity table"

    supported_types = get_supported_types(op)
    if elem_type not in supported_types:
        return f"Type '{elem_type}' not supported for '{op}' (supported: {supported_types})"

    return f"Operation '{op}' is associative for type '{elem_type}'"

