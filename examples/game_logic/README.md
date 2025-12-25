# Game logic examples

## Loot filter
Python intent:
```python
[item for item in drops
 if item.rarity >= 4 and item.zone == "Neon Ruins"]
```

Try:
```bash
pcs "[item for item in drops if item.rarity >= 4 and item.zone == 'Neon Ruins']" --target ts
pcs "[item for item in drops if item.rarity >= 4 and item.zone == 'Neon Ruins']" --target rust
```

Use case: ECS-like pipelines, balancing sims, replay parsers.
