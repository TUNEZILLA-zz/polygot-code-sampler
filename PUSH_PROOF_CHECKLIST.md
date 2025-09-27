# 🎛️ Code Live - Push-Proof Checklist

## 🚨 **Common Push Blockers (and Quick Fixes)**

### **1. Protected Branches / Required Checks**
```bash
# Symptom: ! [remote rejected] ... protected branch hook declined
# Fix: push a feature branch and open a PR, or update branch protection rules

# Check current branch protection
gh api repos/:owner/:repo/branches/main/protection --jq .

# Push to feature branch instead
git checkout -b feature/your-feature
git push origin feature/your-feature
gh pr create --title "Your Feature" --body "Description"
```

### **2. Large File Limit (100 MB) / Repo Bloat**
```bash
# Symptom: fatal: file ... is 123.45 MB; this exceeds GitHub's file size limit
# Fix: use Git LFS and rewrite history for any large files already committed

# Install and configure Git LFS
git lfs install
git lfs track "*.mp4" "*.mov" "*.zip" "*.pickle" "*.onnx" "*.bin" "*.model"
echo "*.mp4 filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.mov filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.zip filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.pickle filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.onnx filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.bin filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
echo "*.model filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
git add .gitattributes

# Rewrite history to move big files into LFS
git lfs migrate import --include="*.mp4,*.mov,*.zip,*.pickle,*.onnx,*.bin,*.model"
git push --force-with-lease
```

### **3. Secrets Detected by GitHub**
```bash
# Symptom: Push blocked or security alert for leaked keys/tokens
# Fix: rotate the credential, remove it from history

# Scan locally for secrets
npx git-secrets-scan || true
# or
pipx install trufflehog && trufflehog filesystem --directory .

# Purge a leaked file (BFG)
bfg --delete-files id_rsa --no-blob-protection
git push --force-with-lease

# Remove secrets from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret/file' \
  --prune-empty --tag-name-filter cat -- --all
```

### **4. Line Endings / Permission Churn**
```bash
# Symptom: "changed every line" diffs, or execute-bit toggles (chmod +x) on Windows
# Fix: normalize via .gitattributes

# Add to .gitattributes
* text=auto eol=lf
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
*.jpg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.tar.gz binary
```

### **5. Auth / Token Scope Issues**
```bash
# Symptom: 403, fatal: Authentication failed
# Fix: use SSH or a PAT with repo scope

# Switch to SSH
git remote set-url origin git@github.com:TUNEZILLA-zz/polygot-code-sampler.git
ssh -T git@github.com

# Or use PAT with repo scope
git remote set-url origin https://ghp_YOUR_TOKEN@github.com/TUNEZILLA-zz/polygot-code-sampler.git
```

---

## 🛡️ **Prevent Problems Before They Reach GitHub**

### **A. Add a Sane .gitignore**
```bash
# .gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
.venv/
.env
.dist/
build/
dist/
*.egg-info/
.ipynb_checkpoints/
*.ipynb

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editors/OS
.DS_Store
*.swp
*.swo
*~
.vscode/
.idea/
*.sublime-*

# Bench/data
bench/results/
site/benchmarks.json
performance_data/
*.json
*.ndjson

# Artifacts
coverage/
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Large files
*.mp4
*.mov
*.zip
*.tar.gz
*.bin
*.model
*.onnx
*.pickle

# Temporary files
*.tmp
*.temp
*.log
*.pid
*.seed
*.pid.lock

# OS generated files
Thumbs.db
ehthumbs.db
Desktop.ini
```

### **B. Pre-commit Hooks (Runs Locally on Commit/Push)**
```bash
# Install pre-commit
pipx install pre-commit || pip install pre-commit
pre-commit init-templatedir ~/.git-template
pre-commit install --hook-type pre-commit --hook-type pre-push
```

### **C. Pre-push Guard (Quick Sanity Checks)**
```bash
# .git/hooks/pre-push (make executable)
#!/usr/bin/env bash
set -euo pipefail

# Block accidental pushes of large blobs (fast scan of staged/HEAD diff)
max_kb=95000
over=$(git ls-files -s | awk '{print $4}' \
  | xargs -I{} git cat-file -s {} 2>/dev/null \
  | awk -v m=$max_kb '$1>m*1024{print $1; exit 0}')
if [ -n "${over:-}" ]; then
  echo "❌ A file exceeds ${max_kb}KB. Use Git LFS."
  exit 1
fi

# Optional: reject pushes to main without PR
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ]; then
  echo "🔒 Push to 'main' blocked. Open a PR instead."
  exit 1
fi

# Check for secrets
if command -v git-secrets >/dev/null 2>&1; then
  git-secrets --scan
fi

# Check for large files
if git ls-files | xargs -I{} sh -c 'test -f {} && test $(stat -c%s {}) -gt 95000000' 2>/dev/null; then
  echo "❌ Large files detected. Use Git LFS."
  exit 1
fi
```

---

## 📄 **Pre-commit Configuration**

### **.pre-commit-config.yaml**
```yaml
repos:
  # Basic hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=95000"]   # warn before GitHub's 100MB hard limit
      - id: check-case-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-xml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=95000"]
      - id: check-case-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-xml

  # GitHub Workflows
  - repo: https://github.com/sirosen/check-jsonschema
    rev: 0.28.4
    hooks:
      - id: check-github-workflows

  # Git secrets
  - repo: https://github.com/awslabs/git-secrets
    rev: 1.3.0
    hooks:
      - id: git-secrets

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3

  # Python linting
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
        args: [--ignore-missing-imports]

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.(js|ts|jsx|tsx)$
        types: [file]

  # Go
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: go-imports

  # Rust
  - repo: https://github.com/rust-lang/rustfmt
    rev: v1.6.0
    hooks:
      - id: rustfmt

  # Julia
  - repo: https://github.com/julia-actions/julia-format
    rev: v0.1.0
    hooks:
      - id: julia-format
```

---

## 🧹 **Keep Pages & Artifacts Out of Main**

### **GitHub Pages Workflow**
```yaml
# .github/workflows/publish-dashboard.yml
name: Publish Dashboard
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Build dashboard
        run: npm run build
      - name: Publish dashboard
        uses: peaceiris/actions-gh-pages@v3
        with:
          publish_dir: site
          publish_branch: gh-pages
          force_orphan: true
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### **Artifacts Instead of Commits**
```yaml
# .github/workflows/benchmark.yml
name: Benchmark
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run benchmarks
        run: python scripts/bench_all.py
      - name: Upload benchmark results
        uses: actions/upload-artifact@v4
        with:
          name: benchmark-results
          path: benchmark_results.json
          retention-days: 30
```

---

## 🔧 **One-time Repo Hygiene (If History Already Heavy)**

### **Identify Largest Blobs + Paths**
```bash
# Find the largest files in your repo
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
| awk '$1=="blob"{print $3 "\t" $4}' | sort -nr | head -50

# Check repo size
du -sh .git
```

### **Rewrite: Move Patterns to LFS and Clean Old Blobs**
```bash
# Move large files to LFS
git lfs migrate import --include="*.mp4,*.mov,*.zip,*.bin,*.onnx,*.model,*.pickle"

# Clean up old blobs
git gc --prune=now --aggressive

# Force push (be careful!)
git push --force-with-lease
```

---

## 🚀 **If a Push Still Fails, Diagnose Fast**

### **Diagnostic Commands**
```bash
# Check remote configuration
git remote -v
git status
git config --get remote.origin.url

# Verbose push to see server messages
git push -v

# Check branch protection (needs admin token)
gh api repos/TUNEZILLA-zz/polygot-code-sampler/branches/main/protection --jq .

# Check for large files
git ls-files | xargs -I{} sh -c 'test -f {} && echo $(stat -c%s {}) {}' | sort -nr | head -10

# Check for secrets
git-secrets --scan
```

---

## 🎯 **Quick Setup Commands**

### **1. Install Pre-commit Hooks**
```bash
# Install pre-commit
pipx install pre-commit || pip install pre-commit

# Initialize pre-commit
pre-commit init-templatedir ~/.git-template
pre-commit install --hook-type pre-commit --hook-type pre-push

# Run on all files
pre-commit run --all-files
```

### **2. Setup Git LFS**
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.mp4" "*.mov" "*.zip" "*.pickle" "*.onnx" "*.bin" "*.model"
git add .gitattributes
git commit -m "Add Git LFS tracking for large files"
```

### **3. Setup Pre-push Hook**
```bash
# Make pre-push hook executable
chmod +x .git/hooks/pre-push

# Test the hook
git push --dry-run
```

---

## 🎉 **Benefits of This Setup**

### **✅ Prevents Push Failures**
- **Large Files**: Caught locally before reaching GitHub
- **Secrets**: Scanned and blocked automatically
- **Protected Branches**: Clear error messages and guidance
- **Line Endings**: Normalized automatically

### **✅ Maintains Clean History**
- **LFS**: Large files stored efficiently
- **Artifacts**: Generated files not committed
- **Hooks**: Consistent formatting and linting

### **✅ Fast Development**
- **Local Checks**: Catch issues before push
- **Clear Errors**: Specific guidance for fixes
- **Automated**: No manual intervention needed

---

*The Code Live Push-Proof Checklist - where every push is clean, fast, and reliable!* 🎛️🚀✨
