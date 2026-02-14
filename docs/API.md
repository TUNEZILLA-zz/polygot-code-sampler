# API Reference

Polyglot Code Sampler provides a Python API for transforming comprehensions across 6 target languages.

## Quick Start

```python
from pcs import PyToIR, render

parser = PyToIR()
ir = parser.parse("[x*x for x in range(10) if x%2==0]")

# Generate for any target
rust_code = render("rust", ir, parallel=True)
ts_code = render("ts", ir, parallel=True)
sql_code = render("sql", ir, dialect="postgresql")
```

## Core API

### PyToIR

Parses Python comprehension strings into an intermediate representation (IR).

```python
from pcs.core import PyToIR

parser = PyToIR()
ir = parser.parse("[x**2 for x in range(100) if x % 2 == 0]")
```

### render

Central API for code generation. See [RENDERER_API.md](RENDERER_API.md) for full details.

```python
from pcs.renderer_api import render

# Targets: rust, ts, go, csharp, julia, sql
output = render(target, ir, **kwargs)
```

### Direct Backend Imports

```python
from pcs import render_rust, render_ts, render_go, render_csharp, render_julia, render_sql
```

## Documentation

- **[RENDERER_API.md](RENDERER_API.md)** - Renderer API, backend parameters, migration guide
- **[EXAMPLES.md](EXAMPLES.md)** - Real-world use cases and patterns
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive (if present)
