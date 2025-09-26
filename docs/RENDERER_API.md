# Central Renderer API

The Polyglot Code Sampler provides a central renderer API that eliminates signature drift across backends and makes the codebase resilient to changes.

## Usage

### Recommended: Central API

```python
from pcs.core import PyToIR
from pcs.renderer_api import render

# Parse Python comprehension
parser = PyToIR()
ir = parser.parse("[x**2 for x in range(10) if x % 2 == 0]")

# Generate code for any backend
rust_code = render("rust", ir, parallel=True, int_type="i32")
ts_code = render("ts", ir, parallel=True)
go_code = render("go", ir, parallel=True)
csharp_code = render("csharp", ir, parallel=True)
julia_code = render("julia", ir, parallel=True, mode="broadcast")
sql_code = render("sql", ir, dialect="postgresql")
```

### Legacy: Direct Backend Imports (Supported)

```python
from pcs.renderers.rust import render_rust
from pcs.renderers.ts import render_ts

# Still works, but not recommended for new code
rust_code = render_rust(ir, parallel=True, int_type="i32")
ts_code = render_ts(ir, parallel=True)
```

## Benefits

### ✅ **Signature Drift Protection**
The central API automatically filters kwargs to match each backend's signature, preventing `TypeError` exceptions from signature mismatches.

### ✅ **Future-Proof**
Adding new backend flags won't break existing code - the adapter handles it automatically.

### ✅ **Type Safety**
All backends are typed with `RendererFn` protocol for compile-time safety.

### ✅ **Consistent Interface**
Single entry point for all backends with consistent parameter handling.

## Backend-Specific Parameters

| Backend | Supported Parameters |
|---------|-------------------|
| **Rust** | `parallel`, `int_type` |
| **TypeScript** | `parallel` |
| **Go** | `parallel` |
| **C#** | `parallel` |
| **Julia** | `parallel`, `mode`, `unsafe`, `explain`, `threads` |
| **SQL** | `dialect`, `explain` |

## Error Handling

```python
from pcs.renderer_api import render

try:
    output = render("rust", ir, parallel=True)
except ValueError as e:
    print(f"Unknown backend: {e}")
```

## Migration Guide

### From Direct Imports

**Before:**
```python
from pcs.renderers.rust import render_rust
from pcs.renderers.ts import render_ts

rust_code = render_rust(ir, parallel=True, int_type="i32")
ts_code = render_ts(ir, parallel=True)
```

**After:**
```python
from pcs.renderer_api import render

rust_code = render("rust", ir, parallel=True, int_type="i32")
ts_code = render("ts", ir, parallel=True)
```

### Benefits of Migration

1. **No Signature Errors**: Automatic kwargs filtering
2. **Future-Proof**: New backend flags won't break your code
3. **Consistent**: Same interface for all backends
4. **Type Safe**: Compile-time type checking

