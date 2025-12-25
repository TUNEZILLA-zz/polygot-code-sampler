# Data Analytics examples

## Moving average (intent-style)
Python intent:
```python
[(t, sum(vals[i-window:i])/window)
 for i,(t,_) in enumerate(vals)
 if i >= window]
```

Try targets:
```bash
pcs "[(t, sum(vals[i-window:i])/window) for i,(t,_) in enumerate(vals) if i >= window]" --target ts
pcs "[(t, sum(vals[i-window:i])/window) for i,(t,_) in enumerate(vals) if i >= window]" --target rust --parallel
```

Use case: smoothing metrics, sensor streams, game telemetry.
