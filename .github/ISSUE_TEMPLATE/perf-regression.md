---
name: Performance Regression
about: Report performance regressions or benchmark issues
title: "[PERF] "
labels: ["performance", "regression"]
assignees: []
---

## ⚡ **Performance Regression Report**

### **Regression Type**
- [ ] Benchmark regression (slower than baseline)
- [ ] Memory usage increase
- [ ] Compilation time increase
- [ ] Runtime performance degradation
- [ ] Other: [describe]

### **Affected Backend**
- [ ] Rust
- [ ] TypeScript
- [ ] Go
- [ ] C#
- [ ] Julia
- [ ] SQL
- [ ] All backends

### **Test Case**
```python
# Python comprehension that shows regression
[your test case here]
```

### **Performance Metrics**
**Before:**
- Time: [e.g., 0.123s]
- Memory: [e.g., 45MB]
- Other: [specify]

**After:**
- Time: [e.g., 0.156s]
- Memory: [e.g., 52MB]
- Other: [specify]

### **Regression Details**
- **Percentage change**: [e.g., +26.8%]
- **When noticed**: [e.g., after commit abc123]
- **Environment**: [OS, Python version, etc.]

### **Steps to Reproduce**
1. Run benchmark: `make canary`
2. Compare with baseline
3. Observe regression

### **Additional Context**
<!-- Any other relevant information about the performance regression -->

### **Possible Causes**
<!-- Any ideas about what might be causing the regression -->
