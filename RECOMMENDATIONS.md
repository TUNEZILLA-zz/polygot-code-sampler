# Repository Review & Recommendations

Review date: February 2025

**Status:** All critical, high, and medium priority items have been addressed (February 2025).

## Critical (Fix Soon) — FIXED

### 1. Broken `pcs-gui` Entry Point
**Location:** `pyproject.toml` line 77

```toml
[project.gui-scripts]
pcs-gui = "pcs.gui:main"
```

**Issue:** No `pcs/gui.py` or `pcs/gui/` module exists. `pip install -e .` will succeed, but running `pcs-gui` will fail with `ModuleNotFoundError`.

**Fix:** Either create `pcs/gui.py` with a `main()` function, or remove the `[project.gui-scripts]` section.

---

### 2. Missing `py.typed` Marker
**Location:** `pyproject.toml` line 84

```toml
[tool.setuptools.package-data]
pcs = ["py.typed"]
```

**Issue:** Declares PEP 561 type marker, but `pcs/py.typed` does not exist. Type checkers expect this for proper stub resolution.

**Fix:** Create empty file: `touch pcs/py.typed` (or add to `.gitignore` if not committing).

---

### 3. Invalid Benchmark Dependency
**Location:** `pyproject.toml` line 56

```toml
benchmark = [
    "criterion>=0.1.0",  # ← This is a Rust crate, not a Python package
    ...
]
```

**Issue:** `criterion` is a Rust benchmarking crate. There is no `criterion` on PyPI. `pip install .[benchmark]` will fail.

**Fix:** Remove `criterion` or replace with a Python benchmark lib (e.g. `py-criterion` if it exists, or `pytest-benchmark`, `locust`, etc.).

---

### 4. CONTRIBUTING.md Syntax Error
**Location:** `CONTRIBUTING.md` lines 51–62

**Issue:** Nested code blocks with stray ` ``` ` — the outer block from "## 🚀 First Commit?" is closed incorrectly, leaving a lone ` ``` `.

**Fix:** Remove the extra ` ``` ` at line 62.

---

## High Priority

### 5. Duplicate Files
**Issue:** Many accidental duplicates with ` 2` or ` 3` suffixes:

- `tests/test_golden 2.py`, `tests/test_one_ir_many_goldens 2.py`, `tests/conftest 2.py`
- `pcs_step3_ts 2.py`, `pcs_step2 2.py`, `pcs_step3 2.py`, `pcs_step3_ts_backup 2.py`
- `pcs/__init__ 2.py`, `pcs/cli 2.py`, `pcs/__main__ 2.py`, `pcs/core 2.py`, `pcs/__version__ 2.py`
- `pyproject 2.toml`, `pyproject 3.toml`
- `Makefile 2`
- `requirements-test 2.txt`
- `docs/EXAMPLES 2.md`, `docs/FAILURE_CASES 2.md`, `docs/slack-setup 2.md`
- `scripts/* 2.py` (many)
- `.github/CODEOWNERS 2`

**Fix:** Delete duplicates after confirming the canonical version. Add to `.gitignore` or use a pre-commit hook to block ` 2` / ` 3` suffixes.

---

### 6. Missing docs/API.md
**Location:** `README.md` line 134

```markdown
- **[API.md](docs/API.md)** - Complete API reference
```

**Issue:** `docs/API.md` does not exist. You have `docs/RENDERER_API.md`, `docs/EXAMPLES.md`, etc.

**Fix:** Create `docs/API.md` or update the README link to point to `docs/RENDERER_API.md` (or another existing doc).

---

### 7. Makefile vs Documentation
**Issue:** README and CONTRIBUTING say `make bench-all`, but the main `Makefile` has no `bench-all` target. It focuses on Docker (`docker-compose exec code-live ...`). `Makefile 2` has `bench` and related targets.

**Fix:** Add `bench-all` (and related targets) to the main Makefile, e.g.:

```makefile
bench-all:
	python3 scripts/bench_all.py
```

Or consolidate Makefiles and update docs to match.

---

### 8. pyproject Description Mismatch
**Location:** `pyproject.toml` line 8

```toml
description = "Transform Python comprehensions across 5 ecosystems with parallel processing"
```

**Issue:** README and code support 6 targets: Rust, TypeScript, SQL, Julia, Go, C#.

**Fix:** Update to "6 ecosystems".

---

## Medium Priority

### 9. CI Uses Legacy Entry Point
**Location:** `.github/workflows/ci.yml` lines 49–51

```yaml
- name: Test CLI functionality
  run: |
    python pcs_step3_ts.py --demo
    python pcs_step3_ts.py --code "..." --target rust
```

**Issue:** CI tests `pcs_step3_ts.py` instead of the installed `pcs` CLI. The canonical entry point is `pcs` from `pcs.cli`.

**Fix:** Use `pcs` (or `python -m pcs`) in CI:

```yaml
pip install -e .
pcs --code "test = [x**2 for x in range(5)]" --target rust
pcs --code "test = [x**2 for x in range(5)]" --target ts
```

---

### 10. CI Lint Scope
**Location:** `.github/workflows/ci.yml` lines 110–122

**Issue:** Lint runs only on `pcs_step3_ts.py` and `tests/`, not on `pcs/`.

**Fix:** Broaden scope, e.g.:

```yaml
ruff check pcs/ pcs_step3_ts.py tests/
black --check pcs/ pcs_step3_ts.py tests/
```

---

### 11. Repository URL Consistency
**Location:** `pyproject.toml` project.urls

**Issue:** URLs use `polygot-code-sampler` (typo). Project name is `polyglot-code-sampler`. If the real repo is `polyglot-code-sampler`, URLs should match.

**Fix:** Confirm actual GitHub repo name and align all URLs.

---

## Low Priority / Nice to Have

### 12. Add New Scripts to README
**Location:** `README.md` Development section

**Suggestion:** Mention the new scripts:

```bash
# Valentine's terminal animation
python3 scripts/valentines_terminal.py 10

# Emoji art gallery
python3 scripts/emoji_art.py --cycle
```

---

### 13. Add `scripts/` to Ruff Config
**Location:** `pyproject.toml` ruff per-file-ignores

**Current:** `"scripts/**"` has broad ignores. Consider narrowing over time and adding `scripts/valentines_terminal.py` and `scripts/emoji_art.py` to the main check once they’re stable.

---

### 14. Pre-commit Config
**Suggestion:** Add `.pre-commit-config.yaml` if not present, with hooks for black, ruff, mypy, and trailing-whitespace to match CONTRIBUTING.

---

### 15. Python 3.8 Support
**Location:** `pyproject.toml` requires-python, classifiers

**Note:** `requires-python = ">=3.8"` but some code uses `list[X]` (3.9+). Ruff `target-version = "py311"` suggests 3.11+. Consider aligning `requires-python` with actual support (e.g. `>=3.9` or `>=3.11`).

---

## Summary Checklist

| Priority   | Item                    | Effort |
|-----------|--------------------------|--------|
| Critical  | Fix/remove pcs-gui       | Low    |
| Critical  | Add py.typed             | Low    |
| Critical  | Fix criterion dep        | Low    |
| Critical  | Fix CONTRIBUTING.md      | Low    |
| High      | Remove duplicate files   | Medium |
| High      | Fix docs/API.md link     | Low    |
| High      | Add bench-all to Makefile| Low    |
| High      | Update pyproject desc    | Low    |
| Medium    | CI: use pcs CLI          | Low    |
| Medium    | CI: lint pcs/            | Low    |
| Medium    | Verify repo URLs         | Low    |
