# 🤝 Contributing to Polyglot Code Sampler

Thank you for your interest in contributing! This guide will help you get started with development, understand our processes, and make meaningful contributions.

## 🚀 Quick Start

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/polyglot-code-sampler.git
cd polyglot-code-sampler

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-test.txt

# Run tests to verify setup
python -m pytest tests/ -v
```

## 🏗️ Development Setup

### Prerequisites

- **Python 3.9+** - Core language support
- **Rust** - For Rust backend testing
- **Node.js 16+** - For TypeScript backend testing
- **Go 1.19+** - For Go backend testing
- **.NET 6+** - For C# backend testing
- **Julia 1.8+** - For Julia backend testing
- **SQLite/PostgreSQL** - For SQL backend testing

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements-test.txt

# Install pre-commit hooks
pre-commit install

# Verify installation
python -c "import pcs; print('✅ Installation successful')"

## 🚀 First Commit? Quick Setup

```bash
# Install pre-commit (if not already installed)
pipx install pre-commit

# Install hooks
pre-commit install --hook-type pre-commit --hook-type pre-push

# Run on all files to fix any issues
pre-commit run --all-files
```

### Backend Setup

#### Rust
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup component add clippy rustfmt

# Install Rayon for parallel testing
cargo install rayon
```

#### TypeScript
```bash
# Install Node.js dependencies
npm install -g typescript ts-node

# Install Web Workers polyfill for testing
npm install -g worker_threads
```

#### Go
```bash
# Install Go
# Follow instructions at https://golang.org/doc/install

# Verify installation
go version
```

#### C#
```bash
# Install .NET SDK
# Follow instructions at https://dotnet.microsoft.com/download

# Verify installation
dotnet --version
```

#### Julia
```bash
# Install Julia
# Follow instructions at https://julialang.org/downloads/

# Install required packages
julia -e "using Pkg; Pkg.add([\"Threads\", \"BenchmarkTools\"])"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_golden.py -v
python -m pytest tests/test_renderer_api.py -v
python -m pytest tests/test_property_invariants.py -v

# Run with coverage
python -m pytest tests/ --cov=pcs --cov-report=html
```

### Test Categories

1. **Golden Tests** (`test_golden.py`) - Snapshot testing for code generation
2. **Renderer API Tests** (`test_renderer_api.py`) - Central API functionality
3. **Property Tests** (`test_property_invariants.py`) - Hypothesis-based testing
4. **Integration Tests** - End-to-end workflow testing

### Adding New Tests

```python
# Example: Adding a new golden test
def test_new_backend_feature():
    """Test new backend feature with golden file comparison."""
    parser = PyToIR()
    ir = parser.parse("[x*x for x in range(10)]")

    # Generate code
    code = render("rust", ir, parallel=True, new_feature=True)

    # Compare with golden file
    assert code == load_golden("rust_new_feature.golden")
```

## 🎯 Code Style

### Python Style

We use **Black** for formatting and **Ruff** for linting:

```bash
# Format code
black pcs/ tests/

# Lint code
ruff pcs/ tests/

# Type checking
mypy pcs/
```

### Style Guidelines

1. **Black Formatting** - Automatic code formatting
2. **Ruff Linting** - Fast Python linter
3. **Type Hints** - Use type annotations throughout
4. **Docstrings** - Google-style docstrings
5. **Naming** - snake_case for functions, PascalCase for classes

### Example Code Style

```python
from typing import List, Dict, Optional
from pcs.core import IRComp, PyToIR

def render_backend(
    target: str,
    ir: IRComp,
    parallel: bool = False,
    **kwargs: Dict[str, Any]
) -> str:
    """
    Render intermediate representation to target backend.

    Args:
        target: Target backend (rust, ts, go, etc.)
        ir: Intermediate representation
        parallel: Enable parallel processing
        **kwargs: Additional backend-specific options

    Returns:
        Generated code string

    Raises:
        ValueError: If target is not supported
    """
    if target not in SUPPORTED_BACKENDS:
        raise ValueError(f"Unsupported target: {target}")

    # Implementation here
    return generated_code
```

## 🔧 Adding New Backends

### 1. Create Renderer Module

```python
# pcs/renderers/new_backend.py
from typing import Dict, Any
from pcs.core import IRComp

def render_new_backend(ir: IRComp, **kwargs: Dict[str, Any]) -> str:
    """Render IR to new backend language."""
    # Implementation here
    return generated_code
```

### 2. Add to Renderer API

```python
# pcs/renderer_api.py
from pcs.renderers.new_backend import render_new_backend

_BACKENDS: Dict[str, RendererFn] = {
    "rust": render_rust,
    "ts": render_ts,
    "go": render_go,
    "csharp": render_csharp,
    "julia": render_julia,
    "sql": render_sql,
    "new_backend": render_new_backend,  # Add here
}
```

### 3. Add CLI Support

```python
# pcs/cli.py
def main():
    parser.add_argument(
        "--target",
        choices=["rust", "ts", "go", "csharp", "julia", "sql", "new_backend"],
        help="Target backend"
    )
```

### 4. Add Tests

```python
# tests/test_new_backend.py
def test_new_backend_basic():
    """Test basic new backend functionality."""
    parser = PyToIR()
    ir = parser.parse("[x for x in range(5)]")

    code = render("new_backend", ir)
    assert isinstance(code, str)
    assert len(code) > 0
```

### 5. Add Golden Tests

```python
# tests/test_golden.py
@pytest.mark.parametrize("backend", ["rust", "ts", "go", "csharp", "julia", "sql", "new_backend"])
def test_backend_golden(backend):
    """Test backend golden file generation."""
    # Test implementation
```

## 📝 Documentation

### Adding Documentation

1. **API Documentation** - Update `docs/API.md`
2. **Examples** - Add to `docs/EXAMPLES.md`
3. **Architecture** - Update `docs/ARCHITECTURE.md`
4. **README** - Keep main README focused and clean

### Documentation Style

- **Markdown** - Use standard Markdown formatting
- **Code Blocks** - Use syntax highlighting
- **Examples** - Include working code examples
- **Links** - Use relative links for internal documentation

## 🚀 Performance Considerations

### Benchmarking

```bash
# Run performance tests
make bench-all

# Run specific backend benchmarks
make bench-rust
make bench-julia

# Check for regressions
make regress
```

### Performance Guidelines

1. **Measure First** - Profile before optimizing
2. **Regression Testing** - Ensure changes don't degrade performance
3. **Documentation** - Record performance characteristics
4. **Monitoring** - Use our benchmarking system

## 🐛 Bug Reports

### Before Reporting

1. **Check Issues** - Search existing issues
2. **Reproduce** - Create minimal reproduction case
3. **Test Latest** - Ensure issue exists in latest version
4. **Document** - Include environment details

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue.

## Steps to Reproduce
1. Run command: `pcs "..." --target rust`
2. Expected: Generated Rust code
3. Actual: Error message

## Environment
- OS: macOS 13.0
- Python: 3.9.7
- Version: 0.3.1

## Additional Context
Any other relevant information.
```

## 💡 Feature Requests

### Before Requesting

1. **Check Roadmap** - Review planned features
2. **Search Issues** - Look for similar requests
3. **Use Cases** - Provide concrete examples
4. **Implementation** - Consider complexity

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature.

## Use Case
Why is this feature needed? Provide examples.

## Proposed Implementation
How should this feature work?

## Alternatives
What alternatives have you considered?
```

## 🔄 Pull Request Process

### Before Submitting

1. **Fork Repository** - Create your own fork
2. **Create Branch** - Use descriptive branch names
3. **Write Tests** - Add tests for new functionality
4. **Update Documentation** - Update relevant docs
5. **Run Tests** - Ensure all tests pass

### PR Guidelines

1. **Small Changes** - Keep PRs focused and small
2. **Clear Description** - Explain what and why
3. **Tests** - Include tests for new functionality
4. **Documentation** - Update docs if needed
5. **Performance** - Consider performance impact

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Performance tested

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🎯 Development Workflow

### Daily Development

```bash
# Start development
git checkout -b feature/new-backend
# Make changes
python -m pytest tests/ -v
black pcs/ tests/
ruff pcs/ tests/
git add .
git commit -m "feat: add new backend support"
git push origin feature/new-backend
```

### Release Process

1. **Version Bump** - Update version in `pyproject.toml`
2. **Changelog** - Update `CHANGELOG.md`
3. **Tests** - Run full test suite
4. **Benchmarks** - Run performance tests
5. **Documentation** - Update docs
6. **Release** - Create GitHub release

## 🆘 Getting Help

### Resources

- **Documentation** - Check `docs/` directory
- **Issues** - Search existing issues
- **Discussions** - Use GitHub Discussions
- **Code Review** - Ask for review on PRs

### Community

- **GitHub Discussions** - General questions and ideas
- **Issues** - Bug reports and feature requests
- **Pull Requests** - Code contributions
- **Code Review** - Help review others' contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Ready to contribute?** Start with a [good first issue](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/labels/good%20first%20issue) or open a [discussion](https://github.com/TUNEZILLA-zz/polyglot-code-sampler/discussions)!
