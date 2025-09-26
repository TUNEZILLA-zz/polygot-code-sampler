# PCS Performance Monitoring SLOs

## 📊 **Service Level Objectives**

### **Data Freshness**
- **Target**: Latest `benchmarks.json` ≤ 24 hours old
- **Measurement**: Time since last successful benchmark run
- **Alert**: Dashboard shows "⚠️ Stale Data" if > 7 days
- **Recovery**: Re-run nightly benchmark workflow

### **Regression Gate Noise**
- **Target**: < 2% false-positive rate per month
- **Measurement**: Manual review of regression alerts
- **Tuning**: Adjust per-backend thresholds based on historical data
- **Grace Period**: 3 days for new tests to prevent false alarms

### **Dashboard Availability**
- **Target**: > 99.9% uptime (GitHub Pages)
- **Measurement**: External monitoring of https://tunezilla-zz.github.io/polygot-code-sampler/
- **Recovery**: Re-run publish-dashboard workflow
- **Backup**: Weekly mirror to `pages-backup` branch

### **Performance Drift Budget**
- **Target**: ≤ +10% rolling 7-day median per backend
- **Measurement**: Automated regression detection
- **Exceptions**: Approved performance changes with documentation
- **Thresholds**:
  - Julia: 12% (higher variance)
  - Rust: 8% (stable)
  - Go: 15% (GC variance)
  - TypeScript: 10% (default)
  - C#: 10% (default)

## 🔧 **Guardrails**

### **Toolchain Pinning**
```yaml
# Rust
- uses: dtolnay/rust-toolchain@stable
  with:
    toolchain: 1.75.0

# Go  
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'

# Node
- uses: actions/setup-node@v4
  with:
    node-version: '20'
```

### **Cache Strategy**
- **Build Artifacts**: Cache for speed
- **Weekly Bust**: Clear caches to avoid bias
- **Cache Keys**: Include toolchain versions

### **Data Retention**
- **Active**: 180 days of `bench/results/*.ndjson`
- **Archive**: Older data moved to `archive/`
- **Schema**: Versioned in `bench/schema.json`

## 📈 **Monitoring Metrics**

### **Key Performance Indicators**
- **Benchmark Success Rate**: > 95%
- **Regression Detection Accuracy**: > 98%
- **Dashboard Load Time**: < 2 seconds
- **Data Processing Time**: < 30 seconds

### **Alert Conditions**
- **Critical**: Dashboard unavailable > 1 hour
- **Warning**: Data stale > 24 hours
- **Info**: Performance regression detected
- **Debug**: Schema validation warnings

## 🎯 **Threshold Configuration**

### **Per-Backend Thresholds**
```
+12%:julia    # Higher variance, JIT compilation
+8%:rust      # Stable, predictable performance  
+15%:go       # GC variance, runtime differences
+10%:ts       # Default threshold
+10%:csharp   # Default threshold
```

### **Grace Period Rules**
- **New Tests**: 3 days minimum history
- **New Backends**: 7 days minimum history
- **Infrastructure Changes**: 1 day grace period

## 🔍 **Quality Gates**

### **Pre-Deploy Checks**
- [ ] Regression check passes
- [ ] Schema validation clean
- [ ] Data freshness < 24h
- [ ] Dashboard loads correctly

### **Post-Deploy Verification**
- [ ] Dashboard accessible
- [ ] Charts render correctly
- [ ] Data health badge shows "✅ Healthy"
- [ ] All backends represented

## 📋 **Maintenance Schedule**

### **Daily**
- Monitor regression alerts
- Check dashboard health
- Review performance trends

### **Weekly**
- Clear CI caches
- Archive old data
- Review threshold effectiveness

### **Monthly**
- Analyze false-positive rate
- Adjust thresholds if needed
- Update documentation
- Performance trend analysis
