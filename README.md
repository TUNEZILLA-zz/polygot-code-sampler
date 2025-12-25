# 🚀 Polyglot Code Sampler

[![CI](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/workflows/CI/badge.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/actions) [![Coverage](https://codecov.io/gh/TUNEZILLA-zz/polyglot-code-sampler/branch/main/graph/badge.svg)](https://codecov.io/gh/TUNEZILLA-zz/polyglot-code-sampler) [![Performance](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/workflows/Performance%20Benchmarks/badge.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/actions) [![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

[![Tests](https://img.shields.io/badge/tests-59%20passing-brightgreen.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/actions) [![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-green.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler) [![Benchmarks](https://img.shields.io/badge/benchmarks-⚡%20active-orange.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/actions) [![Type Safety](https://img.shields.io/badge/type%20safety-mypy%20strict-blue.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler) [![Code Quality](https://img.shields.io/badge/code%20quality-ruff%20%2B%20black-black.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler) [![Renderer API](https://img.shields.io/badge/renderer%20API-centralized-purple.svg)](https://github.com/TUNEZILLA-zz/polyglot-code-sampler)

**Dashboards:** [Production](https://tunezilla-zz.github.io/polyglot-code-sampler/) · [Demo](https://tunezilla-zz.github.io/polyglot-code-sampler/?demo=1)

> **Write once (Python intent) → compile into many (runtime-specific implementations)**

Polyglot Code Sampler turns compact Python "intent" (comprehensions + common patterns) into readable equivalents across multiple targets. Teams rarely share one language—data work, backend services, analytics, and tooling split across stacks. This project is a **translation layer**.

## 🎯 What is Polyglot Code Sampler?

Transform Python comprehensions into optimized, parallel code across **6 different ecosystems**:

- **🦀 Rust** - Rayon parallel iterators with type safety
- **📱 TypeScript** - Web Workers for browser-based parallelism
- **🗄️ SQL** - Optimized queries with predicate pushdown
- **🔬 Julia** - High-performance scientific computing
- **⚡ Go** - Goroutines and channels for concurrency
- **💎 C#** - PLINQ for enterprise applications

## 🚀 Quick Start

```bash
# Install
pip install polyglot-code-sampler

# Transform Python to Rust
pcs "[x*x for x in range(100) if x%2==0]" --target rust --parallel

# Generate SQL with optimizations
pcs "sum(i*i for i in range(1,100) if i%3==0)" --target sql --dialect postgresql

# Parallel Julia with broadcast mode
pcs "[x+y for x in range(10) for y in range(5)]" --target julia --mode broadcast --parallel
```

## 📁 Examples

See `examples/` for real-world domains:

- **[Data Analytics](examples/data_analytics/)** - Time series, aggregations, anomaly detection
- **[Security Logs](examples/security_logs/)** - Threat detection, authentication analysis, network filtering
- **[Game Logic](examples/game_logic/)** - Entity systems, scoring, inventory management
- **[Music Theory](examples/music_theory/)** - Chord analysis, frequency processing, beat patterns

Each domain shows Python intent → multi-language output for practical use cases.

## 🎛️ Live Code Mixer

Experience code generation like a music producer mixing tracks:

- **🎚️ Track Faders** - Adjust parallelization levels per backend
- **🔧 Effects Rack** - Toggle optimizations (predicate pushdown, constant folding)
- **📈 Automation Lane** - Policy-driven governance and regression detection
- **🎧 Live Output** - Real-time code generation with performance metrics

[**Try the Live Mixer**](https://tunezilla-zz.github.io/polyglot-code-sampler/code-mixer-prod.html)

## 📊 Performance Results

| Backend | Sequential | Parallel | Speedup | Use Case |
|---------|------------|----------|---------|----------|
| **Rust** | 2.1ms | 0.6ms | **3.5x** | High-performance computing |
| **Julia** | 1.8ms | 0.5ms | **3.6x** | Scientific computing |
| **Go** | 2.3ms | 0.7ms | **3.3x** | Concurrent systems |
| **TypeScript** | 3.2ms | 0.9ms | **3.6x** | Web applications |
| **C#** | 2.5ms | 0.8ms | **3.1x** | Enterprise applications |
| **SQL** | 15.2ms | 4.1ms | **3.7x** | Database queries |

## 🏗️ Architecture

```
Python Comprehension
        ↓
    AST Parser
        ↓
  Intermediate Representation (IR)
        ↓
    ┌─────────────────────────────────────┐
    │        Renderer API                │
    └─────────────────────────────────────┘
        ↓
┌─────┬─────┬─────┬─────┬─────┬─────┐
│Rust │ TS  │ SQL │Julia│ Go  │ C#  │
└─────┴─────┴─────┴─────┴─────┴─────┘
```

## 🎯 Real-World Examples

### Data Processing Pipeline
```python
# Python: Process customer orders
orders = [order for order in orders
          if order.status == 'completed'
          and order.total > 100]
```

**Generated Rust:**
```rust
use rayon::prelude::*;

pub fn process_orders() -> Vec<Order> {
    orders.into_par_iter()
        .filter(|order| order.status == "completed")
        .filter(|order| order.total > 100)
        .collect()
}
```

**Generated SQL:**
```sql
SELECT * FROM orders
WHERE status = 'completed'
  AND total > 100;
```

### Machine Learning Preprocessing
```python
# Python: Normalize features
normalized = [(x - mean) / std for x in features]
```

**Generated Julia:**
```julia
function normalize_features(features)
    mean_val = sum(features) / length(features)
    std_val = sqrt(sum((x - mean_val)^2 for x in features) / length(features))
    return [(x - mean_val) / std_val for x in features]
end
```

## 📚 Documentation

- **[BENCHMARKS.md](BENCHMARKS.md)** - Performance testing and regression detection
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development setup and contribution guidelines
- **[API.md](docs/API.md)** - Complete API reference
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Real-world use cases and patterns
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Technical deep dive

## 🛠️ Development

```bash
# Clone and setup
git clone https://github.com/TUNEZILLA-zz/polyglot-code-sampler.git
cd polyglot-code-sampler
pip install -e .

# Run tests
python -m pytest tests/ -v

# Run benchmarks
make bench-all

# Start development server
python server_prod.py
```

## 🎛️ Enterprise Features

- **Performance Monitoring** - Real-time benchmarking with regression detection
- **Policy-Driven Governance** - Configurable thresholds and safety guards
- **Multi-OS CI/CD** - Automated testing across platforms
- **Code Coverage** - Comprehensive test coverage reporting
- **Security Scanning** - SBOM generation and vulnerability detection

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Python AST** - For robust code parsing
- **Rayon** - Rust parallel iterators
- **Julia Threads** - High-performance computing
- **Web Workers** - Browser parallelism
- **PLINQ** - .NET parallel processing

---

**Ready to transform your Python comprehensions?** [Get started now →](https://github.com/TUNEZILLA-zz/polyglot-code-sampler#-quick-start)
