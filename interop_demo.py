#!/usr/bin/env python3
"""
Interop Demo Generator
Shows the same IR rendered across all five backends for a single comprehension
"""

from pcs_step3_ts import (
    PyToIR,
    render_csharp,
    render_go,
    render_rust,
    render_sql,
    render_ts,
)


def generate_interop_demo():
    """Generate interop demo showing same IR across all backends"""

    # Choose a comprehensive example
    python_code = "sum(x * x for x in range(100) if x % 2 == 0)"

    print("🔄 **Interop Demo: Same IR → All Five Backends**")
    print("=" * 80)
    print(f"**Python Input:** {python_code}")
    print("=" * 80)

    # Parse to IR
    parser = PyToIR()
    ir = parser.parse(python_code)

    print("**IR (JSON):**")
    print(ir.to_json())
    print("=" * 80)

    # Generate all outputs from the same IR
    rust_output = render_rust(ir, func_name="sum_squares")
    ts_output = render_ts(ir, func_name="sumSquares")
    go_output = render_go(ir, func_name="SumSquares")
    csharp_output = render_csharp(ir, func_name="SumSquares")
    sql_output = render_sql(ir, func_name="sum_squares", dialect="postgresql")

    # Create the interop markdown
    interop_markdown = f"""
## 🔄 **Interop Demo: Same IR → All Five Backends**

*One Python comprehension, one IR, five different implementations:*

### 📝 **Input**
```python
{python_code}
```

### 🧠 **Intermediate Representation (IR)**
```json
{ir.to_json()}
```

---

## 🎯 **Same IR → Five Backends**

### 🦀 **Rust**
```rust
{rust_output}
```

### 🌐 **TypeScript**
```typescript
{ts_output}
```

### 🐹 **Go**
```go
{go_output}
```

### 🔷 **C#**
```csharp
{csharp_output}
```

### 🗄️ **SQL**
```sql
{sql_output}
```

---

## ⚡ **Parallel Versions**

### 🦀 **Rust (Rayon)**
```rust
{render_rust(ir, func_name="sum_squares_parallel", parallel=True)}
```

### 🌐 **TypeScript (Web Workers)**
```typescript
{render_ts(ir, func_name="sumSquaresParallel", parallel=True)}
```

### 🐹 **Go (Goroutines)**
```go
{render_go(ir, func_name="SumSquaresParallel", parallel=True)}
```

### 🔷 **C# (PLINQ)**
```csharp
{render_csharp(ir, func_name="SumSquaresParallel", parallel=True)}
```

---

## 🎯 **Key Benefits**

- **Single Source of Truth**: One Python comprehension
- **Consistent Logic**: Same IR ensures identical behavior
- **Language-Specific Optimization**: Each backend uses native patterns
- **Parallel Processing**: All backends support parallel execution
- **Type Safety**: Compile-time guarantees where available

## 🚀 **Try the Interop**

```bash
# Generate all five backends from the same input
python3 pcs_step3_ts.py --code "{python_code}" --target rust
python3 pcs_step3_ts.py --code "{python_code}" --target ts
python3 pcs_step3_ts.py --code "{python_code}" --target go
python3 pcs_step3_ts.py --code "{python_code}" --target csharp
python3 pcs_step3_ts.py --code "{python_code}" --target sql

# Generate parallel versions
python3 pcs_step3_ts.py --code "{python_code}" --target rust --parallel
python3 pcs_step3_ts.py --code "{python_code}" --target ts --parallel
python3 pcs_step3_ts.py --code "{python_code}" --target go --parallel
python3 pcs_step3_ts.py --code "{python_code}" --target csharp --parallel
```

**One comprehension, one IR, five production-ready implementations!** ✨
"""

    return interop_markdown

if __name__ == "__main__":
    demo = generate_interop_demo()
    print(demo)

    # Save to file
    with open("INTEROP_DEMO.md", "w") as f:
        f.write(demo)

    print("\n💾 Interop demo saved to: INTEROP_DEMO.md")

