# Security logs examples

## Flag suspicious auth bursts
Python intent:
```python
[e for e in events
 if e.action == "login"
 and e.success == False
 and e.ip in watchlist]
```

Try:
```bash
pcs "[e for e in events if e.action == 'login' and e.success == False and e.ip in watchlist]" --target sql --dialect postgresql
```

Use case: quick "rules → query" conversion for triage.
