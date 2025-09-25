# 🚀 Polyglot Code Sampler

[![CI](https://github.com/TUNEZILLA-zz/polygot-code-sampler/workflows/CI/badge.svg)](https://github.com/TUNEZILLA-zz/polygot-code-sampler/actions)
[![codecov](https://codecov.io/gh/TUNEZILLA-zz/polygot-code-sampler/branch/main/graph/badge.svg)](https://codecov.io/gh/TUNEZILLA-zz/polygot-code-sampler)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transform Python comprehensions into Rust and TypeScript with a production-ready compiler pipeline!**

## ✨ Features

### 🎯 **Complete Language Support**
- **Python → Rust**: Iterator chains with `HashMap`, `HashSet`, `.filter()`, `.map()`, `.flat_map()`
- **Python → TypeScript**: Using `Map`, `Set`, `.filter()`, `.map()`, `.flatMap()`

### 🧩 **Comprehension Types**
- **List comprehensions**: `[x**2 for x in range(10) if x % 2 == 0]`
- **Dict comprehensions**: `{k: v for k, v in items if condition}`
- **Set comprehensions**: `{x for x in data if condition}`
- **Nested comprehensions**: `[i*j for i in range(3) for j in range(3)]`

### ⚡ **Advanced Reductions**
- `sum()`, `math.prod()`, `any()`, `all()`, `max()`, `min()`

### 🎯 **Type Inference & Annotations**
- **Smart type inference** from Python expressions
- **Rust**: `HashMap<i64, i64>`, `HashSet<i64>`, `Vec<i64>`, `i64`, `bool`
- **TypeScript**: `Map<number, number>`, `Set<number>`, `Array<number>`, `number`, `boolean`
- **CLI configuration**: `--int-type i32|i64`, `--strict-types`

### 🛡️ **Production Testing**
- **Golden file snapshots** for IR, Rust, and TypeScript outputs
- **Regression protection** with pytest
- **Multi-OS CI/CD** (Ubuntu, macOS, Windows)
- **Python 3.9-3.12** compatibility
- **Code coverage reporting** with Codecov integration

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/polyglot-code-sampler.git
cd polyglot-code-sampler

# Install dependencies
pip install pytest

# Run the demo
python pcs_step3_ts.py --demo

# Transform a Python comprehension to Rust
python pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --target rust

# Transform to TypeScript
python pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --target ts
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Generate golden files (first run)
python -m pytest tests/test_golden.py --update-golden -v

# Run tests with coverage
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# Generate HTML coverage report
make coverage-html

# Run specific test
python -m pytest tests/test_golden.py::test_golden_files -v
```

## 📊 Test Coverage

The test suite covers **10 comprehensive test cases**:

| Test Case | Python Input | Description |
|-----------|-------------|-------------|
| `dict_odds_squares` | `{ i: i*i for i in range(1,6) if i % 2 == 1 }` | Dict comprehension with filter |
| `set_nested_pairs` | `{ (i, j) for i in range(0,3) for j in range(0,3) if i != j }` | Set comprehension with nested generators |
| `list_nested_products` | `[i*j for i in range(1,4) for j in range(1,4)]` | List comprehension with nested generators |
| `sum_even_numbers` | `sum(x for x in range(1,11) if x % 2 == 0)` | Sum reduction with filter |
| `max_nested_products` | `max(i*j for i in range(1,5) for j in range(1,4))` | Max reduction with nested generators |
| `prod_filtered_range` | `math.prod(x for x in range(1,6) if x != 3)` | Product reduction with filter |
| `all_even_check` | `all(x % 2 == 0 for x in range(2,10))` | All reduction with predicate |
| `any_odd_check` | `any(x % 2 == 1 for x in range(1,10))` | Any reduction with predicate |
| `min_squares` | `min(x**2 for x in range(1,6))` | Min reduction with transformation |
| `dict_nested_complex` | `{i: j for i in range(1,4) for j in range(1,4) if i != j}` | Complex nested dict comprehension |

## 💡 Examples

### Dict Comprehension

**Python Input:**
```python
m = { i: i*i for i in range(1,6) if i % 2 == 1 }
```

**Rust Output:**
```rust
use std::collections::HashMap;
pub fn dict_odds_squares() -> HashMap<_, _> {
    let result = (1..6).filter(|&i| i % 2 == 1).map(move |i| (i, i * i)).collect::<HashMap<_, _>>();
    result
}
```

**TypeScript Output:**
```typescript
export function dict_odds_squares(): Map<any, any> {
  const result = new Map((Array.from({length: (6 - 1)}, (_, i) => i + 1)).filter((i) => i % 2 == 1).map((i) => [ i, i * i ]));
  return result;
}
```

### Nested Max Reduction

**Python Input:**
```python
best = max(i*j for i in range(1,5) for j in range(1,4))
```

**Rust Output:**
```rust
pub fn max_nested_products() -> i64 {
    let result = (1..5).flat_map(move |i| (1..4).map(move |j| i * j)).max().unwrap_or(0);
    result
}
```

**TypeScript Output:**
```typescript
export function max_nested_products(): number|boolean {
  const result = (Array.from({length: (5 - 1)}, (_, i) => i + 1)).flatMap((i) => (Array.from({length: (4 - 1)}, (_, i) => i + 1)).map((j) => i * j)).reduce((a,b)=>a>b?a:b, Number.NEGATIVE_INFINITY);
  return result;
}
```

## 🏗️ Project Structure

```
polyglot-code-sampler/
├── pcs_step3_ts.py              # Main transformer (Rust + TS parity)
├── pcs_step3.py                 # Step 3 implementation
├── pcs_step2.py                 # Step 2 implementation
├── tests/
│   ├── conftest.py              # Pytest configuration
│   ├── test_golden.py           # Golden file tests
│   └── golden/                  # Snapshot files
│       ├── *.ir.json            # IR representations
│       ├── *.rust.txt           # Rust outputs
│       └── *.ts.txt             # TypeScript outputs
├── .github/
│   └── workflows/
│       ├── ci.yml               # Continuous Integration
│       └── release.yml          # Release automation
├── requirements-test.txt        # Test dependencies
└── README.md                    # This file
```

## 🔧 CLI Usage

```bash
# Interactive demo
python pcs_step3_ts.py --demo

# Transform specific code
python pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --name "squares" --target rust

# Emit IR for debugging
python pcs_step3_ts.py --code "data = {x: x*2 for x in range(5)}" --emit-ir

# TypeScript output
python pcs_step3_ts.py --code "data = {x: x*2 for x in range(5)}" --target ts

# Type inference examples (default: i64)
python pcs_step3_ts.py --code "odds = {i: i*i for i in range(1,6) if i % 2 == 1}" --target rust
python pcs_step3_ts.py --code "evens = {x for x in range(0,10) if x % 2 == 0}" --target ts

# Use i32 types instead of i64
python pcs_step3_ts.py --code "squares = [x**2 for x in range(10)]" --target rust --int-type i32

# Parallel processing with types
python pcs_step3_ts.py --code "total = sum(x for x in range(1,1000) if x % 2 == 0)" --target rust --parallel
```

## 🚀 Roadmap

### ✅ **Completed**
- [x] Basic list comprehension → TypeScript
- [x] Nested comprehensions → Rust iterator chains
- [x] Dict/Set comprehensions support
- [x] Advanced reductions (sum, prod, any, all, max, min)
- [x] Production-ready pytest test suite
- [x] Golden file snapshots
- [x] Multi-OS CI/CD pipeline
- [x] Rayon parallel mode with `--parallel` flag
- [x] Code coverage reporting with Codecov integration
- [x] **Type inference & annotations** - Rust `HashMap<K,V>`/`HashSet<T>` and TypeScript `Map<number,number>`/`Set<number>`

### 🎯 **Next Targets**
- [ ] **Type Annotations** - Explicit Rust key/value types for HashMap, HashSet
- [ ] **TS Typing** - Narrower TypeScript generics (Map<number, number>)
- [ ] **Static Analysis** - Pre-commit hooks with ruff, black, mypy
- [ ] **Performance Benchmarks** - Compare generated code performance
- [ ] **Additional Languages** - Go, SQL, WASM backends
- [ ] **IDE Integration** - VS Code extension for inline transformations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for your changes
4. Run the test suite (`python -m pytest tests/ -v`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's `ast` module for robust parsing
- Inspired by functional programming patterns across languages
- Tested across multiple operating systems and Python versions

---

**Transform your Python comprehensions into production-ready Rust and TypeScript code!** 🎨✨
