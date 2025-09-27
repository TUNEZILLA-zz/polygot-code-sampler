# Polyglot Code Sampler (PCS)

**Python → IR → Rust/TypeScript** transformer with nested comprehensions, dict/set support, and reductions — all covered by **pytest golden tests**.

## Features
- Nested list/set/dict comprehensions
- Reductions: `sum`, `prod`, `any`, `all`, `max`, `min`
- Backends: **Rust** (iterator chains) & **TypeScript** (Array/Set/Map)
- JSON IR for debugging
- CLI with `--target {rust,ts}` and `--emit-ir`
- Golden tests with `pytest`

## Quickstart
```bash
python pcs_step3_ts.py               # demo: prints Python → IR → Rust & TypeScript
python pcs_step3_ts.py --target ts --code "m = { i:i*i for i in range(1,6) if i%2 }"
python pcs_step3_ts.py --target rust --code "sum(i*i for i in range(10) if i%2==0)"
```

## Tests
```bash
pytest -q --update-golden   # refresh snapshots (first run)
pytest -q                   # regular run
```

## CI (GitHub Actions)
- Runs tests on **Linux/macOS/Windows** across **3.9–3.12**
- Release job on `v*.*.*` tags builds, runs tests, and publishes a GitHub Release with assets

### Badges
Add after your first run on GitHub:
```md
![CI](https://github.com/<you>/<repo>/actions/workflows/ci.yml/badge.svg)
```

## Releasing
Tag a version:
```bash
git tag v0.1.0 && git push origin v0.1.0
```
GitHub Actions will create a release and attach the main scripts.

## Project layout
```
pcs_step3_ts.py        # main transformer (Rust + TS)
pcs_step3.py           # Rust-only (dict/set + reductions)
pcs_step2.py           # Step 2 baseline
tests/
  conftest.py
  test_golden.py
  golden/              # snapshot files (*.ir.json, *.rust.txt, *.ts.txt)
.github/
  workflows/
    ci.yml
    release.yml
```
