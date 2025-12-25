# Music theory examples

## Frequency band selection
Python intent:
```python
[f for f in freqs if 20 <= f and f <= 200]
```

Try:
```bash
pcs "[f for f in freqs if 20 <= f and f <= 200]" --target rust
pcs "[f for f in freqs if 20 <= f and f <= 200]" --target ts
```

Use case: sub-bass analysis, EQ visualization, spectral rules.
