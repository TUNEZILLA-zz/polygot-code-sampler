# PCS Performance Monitoring Runbook

## 🚨 When Nightly Run Fails Due to Regression Gate

### 1. **Immediate Investigation**
```bash
# Download failing run artifacts
gh run download <run-id> --dir artifacts/
cd artifacts/bench/results/
```

### 2. **Compare to Historical Data**
```bash
# Check workload size, runner variance, toolchain versions
python3 -c "
import json, glob
from datetime import datetime, timedelta

# Load current results
current = []
for f in glob.glob('*.ndjson'):
    for line in open(f):
        if line.strip():
            current.append(json.loads(line))

# Check for infrastructure noise
print('🔍 Infrastructure Check:')
for r in current:
    print(f'  {r[\"backend\"]}: n={r[\"n\"]}, os={r[\"os\"]}, cpu={r[\"cpu\"]}')
"
```

### 3. **Decision Tree**

#### **If Infrastructure Noise (Runner Variance)**
- **Action**: Re-run once
- **Command**: `gh run rerun <run-id>`
- **Expected**: Should pass on second run

#### **If Real Performance Drop**
- **Action**: Find culprit commit via bisect
- **Command**: 
  ```bash
  # Test last good commit
  git checkout <last-good-commit>
  python3 scripts/bench_all.py
  git checkout main
  python3 scripts/bench_all.py
  ```

- **If Needed**: Temporarily raise threshold
  ```bash
  # Update workflow with higher threshold
  --per-backend-thresholds "+20%:rust"  # Temporary override
  ```

### 4. **Communication**
- **Automated**: Regression comment already posted
- **Manual**: File issue with label `perf-regression`
  - Include JSON snippet
  - Include performance charts
  - Link to failing run

## 🚀 **Unblock Deploy (Emergency Override)**

### **One-off Override**
```bash
# Trigger workflow with override
gh workflow run publish-dashboard.yml -f ALLOW_REGRESSION=true
```

### **Workflow Override Logic**
```yaml
- name: Check for performance regressions
  run: |
    if [[ "$ALLOW_REGRESSION" == "true" ]]; then 
      echo "⚠️  Override enabled - skipping regression check"
      exit 0
    fi
    python3 scripts/regression_check.py \
      --input site/benchmarks.json \
      --per-backend-thresholds "+12%:julia,+8%:rust,+15%:go,+10%:ts,+10%:csharp" \
      --grace-period 3 \
      --github-comment \
      --fail-on-regression
```

## 🔧 **Troubleshooting Commands**

### **Local Smoke Test**
```bash
make bench-refresh DRY_RUN=1 && python -m http.server --directory site 8080
# Open http://localhost:8080 and confirm Data Status + charts
```

### **Schema Validation**
```bash
python - <<'PY'
import json, sys, glob
rows=[]
for f in glob.glob("bench/results/*.ndjson"):
    for line in open(f):
        if line.strip(): rows.append(json.loads(line))
assert all(isinstance(r, dict) for r in rows)
print(f"rows={len(rows)} OK")
PY
```

### **Regression Check with Custom Thresholds**
```bash
python3 scripts/regression_check.py \
  --per-backend-thresholds "+12%:julia,+8%:rust,+15%:go,+10%:ts,+10%:csharp" \
  --grace-period 3 \
  --github-comment
```

## 📊 **Data Analysis**

### **Check Data Freshness**
```bash
python3 -c "
import json
from datetime import datetime

with open('site/benchmarks.json') as f:
    data = json.load(f)

latest = max(data, key=lambda x: x['timestamp'])
print(f'Latest: {latest[\"timestamp\"]}')
print(f'Age: {(datetime.now() - datetime.fromisoformat(latest[\"timestamp\"].replace(\"Z\", \"+00:00\"))).days} days')
"
```

### **Backend Performance Comparison**
```bash
python3 -c "
import json
from collections import defaultdict

with open('site/benchmarks.json') as f:
    data = json.load(f)

by_backend = defaultdict(list)
for r in data:
    by_backend[r['backend']].append(r['mean_ns'])

for backend, times in by_backend.items():
    print(f'{backend}: {min(times):,.0f}ns (best), {max(times):,.0f}ns (worst)')
"
```

## 🔔 **Slack Notifications Setup**

### **Configure Slack Webhook**
1. **Create Slack App**: Go to https://api.slack.com/apps
2. **Add Incoming Webhooks**: Enable the feature
3. **Create Webhook**: Choose your monitoring channel
4. **Copy URL**: Save the webhook URL

### **Add GitHub Secret**
1. **Repository Settings**: Go to Settings → Secrets and variables → Actions
2. **New Secret**: Click "New repository secret"
3. **Name**: `SLACK_WEBHOOK_URL`
4. **Value**: Paste your webhook URL

### **Test Notifications**
```bash
# Test with emergency override (safe)
gh workflow run publish-dashboard.yml -f ALLOW_REGRESSION=true

# Or temporarily lower threshold to trigger regression
# Update workflow with: --per-backend-thresholds "+1%:rust"
```

## 🛠️ **Maintenance Tasks**

### **Weekly Cache Bust**
```bash
# Clear CI caches to avoid bias
gh cache delete --all
```

### **Data Retention (180 days)**
```bash
# Archive old results
find bench/results/ -name "*.ndjson" -mtime +180 -exec mv {} archive/ \;
```

### **Toolchain Pinning Check**
```bash
# Verify pinned versions in CI
grep -r "toolchain\|version" .github/workflows/
```
