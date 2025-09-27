# 🎛️ Code Live - Production Lockdown + Creative Freedom Checklist

## 🔒 **Lock Down Main (and Develop)**

### **Branch Protection (GitHub CLI)**
```bash
# Protect main branch
gh api -X PUT repos/:owner/:repo/branches/main/protection \
  -f required_status_checks.strict=true \
  -F required_status_checks.contexts[]='ci: test' \
  -F required_status_checks.contexts[]='ci: lint' \
  -F required_status_checks.contexts[]='ci: pre-commit' \
  -F required_status_checks.contexts[]='ci: golden-stability' \
  -F required_status_checks.contexts[]='ci: matrix-smoke' \
  -F enforce_admins=true \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F restrictions=''

# Protect develop branch (optional staging)
gh api -X PUT repos/:owner/:repo/branches/develop/protection \
  -f required_status_checks.strict=true \
  -F required_status_checks.contexts[]='ci: test' \
  -F required_status_checks.contexts[]='ci: lint' \
  -F required_status_checks.contexts[]='ci: pre-commit' \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -F required_pull_request_reviews.dismiss_stale_reviews=true

# Additional protections
gh api -X PUT repos/:owner/:repo/branches/main/protection \
  -F required_linear_history=true \
  -F required_signatures=true
```

### **Nice-to-Haves**
- ✅ Require linear history on main
- ✅ Require signed commits and signed tags
- ✅ Dismiss stale approvals on new commits
- ✅ Require up-to-date branches before merging

---

## 🧰 **PR Hygiene + Releases**

### **CODEOWNERS for Safe Merges**
```bash
# .github/CODEOWNERS
*                   @TUNEZILLA-zz
/scripts/           @TUNEZILLA-zz @perf-teammate
/site/              @TUNEZILLA-zz @frontend-teammate
/server*.py         @TUNEZILLA-zz @backend-teammate
/grafana/           @TUNEZILLA-zz @ops-teammate
/alert_rules.yml    @TUNEZILLA-zz @ops-teammate
```

### **PR Template for Experiments**
```markdown
# .github/pull_request_template.md
## What
Brief description of changes

## Why
Why this change is needed

## Screens/Metrics
- [ ] Screenshots of UI changes
- [ ] Performance metrics before/after
- [ ] Test results

## Rollback Plan
How to rollback if this causes issues

## Risk Assessment
- [ ] Low Risk - No breaking changes
- [ ] Medium Risk - Some breaking changes with migration path
- [ ] High Risk - Major breaking changes

## Mitigations
What we're doing to reduce risk

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Golden tests pass
- [ ] Manual testing completed
```

### **Conventional Commits + Auto Releases**
```bash
# Use conventional commit format
feat: add synth modulation to physics FX
fix: resolve Julia rendering timeout issue
docs: update branching strategy guide
chore: update dependencies
perf: optimize particle rendering performance

# Auto-release with Release Drafter
# .github/release-drafter.yml already configured
```

---

## 🚦 **CI Gates That Keep Main Pristine**

### **Required CI Jobs on PRs**
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main, develop]

jobs:
  test:
    name: ci: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          python -m pytest tests/ -v
          python -m pytest tests/test_golden.py -v

  lint:
    name: ci: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linting
        run: |
          ruff check .
          black --check .
          mypy pcs/

  pre-commit:
    name: ci: pre-commit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run pre-commit
        run: pre-commit run --all-files

  golden-stability:
    name: ci: golden-stability
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check golden stability
        run: python scripts/regenerate_goldens.py --check-only

  matrix-smoke:
    name: ci: matrix-smoke
    runs-on: ubuntu-latest
    strategy:
      matrix:
        backend: [rust, ts, go, csharp, sql, julia]
    steps:
      - uses: actions/checkout@v4
      - name: Smoke test ${{ matrix.backend }}
        run: python -c "from pcs import render_generic; print(render_generic('${{ matrix.backend }}', 'test'))"
```

---

## 🧹 **Branch Hygiene (Stay Creative, Not Messy)**

### **Auto-Delete Branches on Merge**
```yaml
# .github/workflows/cleanup.yml
name: Cleanup
on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Delete merged branch
        run: |
          gh pr close ${{ github.event.pull_request.number }}
          gh branch delete ${{ github.event.pull_request.head.ref }} --remote
```

### **Weekly Cleanup Script**
```bash
#!/bin/bash
# scripts/weekly_cleanup.sh

# Delete merged branches
gh pr list --state merged -L 200 | awk '{print $1}' | xargs -n1 gh branch delete --remote

# Label experiments
gh pr list --label "type:experiment" --json number,title --jq '.[] | "\(.number): \(.title)"'

# Check for stale experiments
gh pr list --label "area:fx" --state open --json number,title,createdAt --jq '.[] | select(.createdAt < "2024-01-01T00:00:00Z") | "\(.number): \(.title) - STALE"'
```

---

## 🚀 **Kickoff Checklists for Experiment Branches**

### **fx-synth-modulation**
```bash
# Branch setup
git checkout fx-synth-modulation

# Add LFO/Envelope modules with tempo sync
mkdir -p scripts/synth/
touch scripts/synth/lfo.js
touch scripts/synth/envelope.js
touch scripts/synth/tempo-sync.js

# Map LFO → mixer params
touch scripts/synth/parameter-mapping.js

# MIDI CC learn
touch scripts/synth/midi-cc.js

# Safety rails
touch scripts/synth/safety-rails.js

# Demo preset bank
mkdir -p presets/synth/
touch presets/synth/basic.json
touch presets/synth/advanced.json
touch presets/synth/chaos.json
```

### **fx-lolcat-visuals**
```bash
# Branch setup
git checkout fx-lolcat-visuals

# Text stylizer
mkdir -p scripts/lolcat/
touch scripts/lolcat/text-stylizer.js
touch scripts/lolcat/rainbow-ansi.js
touch scripts/lolcat/echo-effects.js

# Color frequency mapper
touch scripts/lolcat/color-mapper.js

# Accessibility toggle
touch scripts/lolcat/accessibility.js

# Demo presets
mkdir -p presets/lolcat/
touch presets/lolcat/party.json
touch presets/lolcat/glitch.json
touch presets/lolcat/classic.json
```

### **fx-audio-reactive**
```bash
# Branch setup
git checkout fx-audio-reactive

# WebAudio FFT
mkdir -p scripts/audio/
touch scripts/audio/fft.js
touch scripts/audio/band-mapper.js

# Map bands → backends
touch scripts/audio/backend-mapping.js

# Sidechain compression
touch scripts/audio/sidechain.js

# Record/replay modulation
touch scripts/audio/recorder.js
touch scripts/audio/playback.js

# Demo presets
mkdir -p presets/audio/
touch presets/audio/techno.json
touch scripts/audio/ambient.json
touch scripts/audio/chaos.json
```

---

## 📈 **Ops Niceties**

### **Nightly Validation Workflow**
```yaml
# .github/workflows/nightly-validation.yml
name: Nightly Validation
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily

jobs:
  regression-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run regression tests
        run: python scripts/regression_smoke.sh
      - name: Check for anomalies
        run: python scripts/trend_alerts.py --anomaly-check
      - name: Comment on failures
        if: failure()
        run: |
          gh pr comment ${{ github.event.pull_request.number }} \
            --body "🚨 Nightly validation failed. Check logs for details."
```

### **Dashboard Data Health Badge**
```yaml
# .github/workflows/data-health.yml
name: Data Health Badge
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  data-health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check data health
        run: |
          python scripts/check_data_health.py
          echo "📊 Data Health: $(cat data_health_status.txt)" >> $GITHUB_STEP_SUMMARY
```

### **Dependabot Configuration**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## ⚡ **Handy Git Aliases**

```bash
# Sync with main
git config alias.sync '!git fetch -p && git rebase origin/main'

# Squash merge
git config alias.squash '!f(){ git checkout main && git merge --squash "$1" && git commit -m "feat: merge $1"; }; f'

# Cleanup merged branches
git config alias.cleanup '!git branch --merged | egrep -v "main|develop" | xargs -n1 git branch -d'

# Quick experiment start
git config alias.experiment '!f(){ git checkout main && git pull && git checkout -b "fx-$1"; }; f'

# Quick experiment merge
git config alias.merge-experiment '!f(){ git checkout main && git merge --squash "fx-$1" && git commit -m "feat: add $1 experiment"; }; f'
```

---

## 🎯 **Usage Examples**

### **Start New Experiment**
```bash
git experiment synth-modulation
# Creates: fx-synth-modulation branch
```

### **Merge Successful Experiment**
```bash
git merge-experiment synth-modulation
# Merges: fx-synth-modulation → main
```

### **Weekly Cleanup**
```bash
git cleanup
# Deletes: all merged branches except main/develop
```

---

*The Code Live Production Lockdown + Creative Freedom Checklist - where enterprise-grade stability meets wild creative experimentation!* 🎛️🔒🎨
