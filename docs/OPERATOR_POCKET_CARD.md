# Operator Pocket Card (FOH)
============================

## Quick Reference

### Scene Control
- **1-9**: Jump to scene
- **0**: Previous scene  
- **Space**: Pause/resume
- **G**: Goto time +10s

### Intensity Control
- **I**: Intensity up (+5% with acceleration)
- **K**: Intensity down (-5% with acceleration)

### Metrics Control
- **M**: Metrics link toggle
- **,**: Link strength decrease
- **.**: Link strength increase

### Momentary Buttons
- **B**: Blackout
- **F**: Flash
- **W**: White bloom

### Undo/Redo
- **U**: Undo
- **R**: Redo

### Special Functions
- **F**: Freeze/unfreeze
- **T**: Tap tempo

## Pre-Show 5-Minute Check

```bash
# Load show and verify status
make touring-rig-load touring-rig-status

# Run show readiness check
make show-readiness-check

# Run acceptance test
make stage-proof-acceptance

# Set intensity and metrics
make touring-rig-intensity VALUE=0.82
make touring-rig-metrics-link STRENGTH=0.75
```

## Safety Checklist

- ✅ Thumbs render
- ✅ Rails respond  
- ✅ A11y on
- ✅ Spectrum panels green

## Post-Show Capture

```bash
# Generate snapshots
make snapshot-kit

# Create tour opener
make rack-show-tour-opener
```

## Emergency Procedures

### Blackout
- **Action**: Press **B** (Blackout)
- **Effect**: Kill motion/brightness instantly
- **Recovery**: Press **B** again to resume

### Motion Watchdog Trip
- **Indicator**: Banner will appear
- **System Response**: Auto-throttles trails & strobe
- **Operator Action**: Keep intensity ≤0.7 for 20s

### Undo/Redo
- **Misfired Tweak**: Press **U** (Undo)
- **Redo**: Press **R** (Redo)
- **History**: 20-step undo/redo stack available

## API One-Liners (curl)

### Intensity Fader (0.0–1.2)
```bash
curl -X POST :8787/rig/intensity -d '{"value":0.82}' -H 'Content-Type: application/json'
```

### Momentary Buttons
```bash
# Blackout
curl -X POST :8787/rig/blackout -d '{"state":true}' -H 'Content-Type: application/json'

# Flash (with latch time)
curl -X POST :8787/rig/flash -d '{"latch_ms":800}' -H 'Content-Type: application/json'

# White Bloom (with latch time)
curl -X POST :8787/rig/bloom -d '{"latch_ms":1200}' -H 'Content-Type: application/json'
```

### Metrics Link (0–1)
```bash
curl -X POST :8787/rig/metrics-link -d '{"strength":0.75}' -H 'Content-Type: application/json'
```

### Morph Curve + Duration
```bash
curl -X POST :8787/rig/morph -d '{"curve":"EaseInOut","seconds":2.0}' -H 'Content-Type: application/json'
```

### Parameter Nudge
```bash
curl -X POST :8787/rig/param -d '{"key":"chromatic.offset","value":0.28}' -H 'Content-Type: application/json'
```

## Safety Rails

### Strobe Cap
- **Frequency**: ≤8 Hz
- **On-time**: ≥120 ms
- **Duty-cycle**: ≤35% over 10s

### Frame Budget Governor
- **Trigger**: 30-frame p95 > 12 ms
- **Response**: Auto-reduce trails, particle count, chroma offsets
- **Target**: p95 ≤ 10 ms

### Param Slew Limiter
- **Intensity**: ≤0.6/s
- **Chroma Offset**: ≤0.3/s
- **Purpose**: Prevent visual "zip" artifacts

### Reduced-Motion Compliance
- **Trigger**: System signal or user toggle
- **Response**: Instant mono fallback
- **Recovery**: 300ms crossfade back in

## Show Flow

### Scene 1: Warmup - Cinemascope
- **Duration**: 20-30s
- **Intensity**: 0.55 → 0.75 (gradual ramp)
- **Metrics Link**: 0.35 (subtle reactive motion)

### Scene 2: Build - Neon Bloom
- **Duration**: 30-45s
- **Intensity**: 0.75 → 0.85
- **Metrics Link**: 0.6 → 0.8 (increased reactive motion)

### Scene 3: Impact - Prism Burst
- **Duration**: 15-20s
- **Intensity**: 0.85 → 0.95
- **Metrics Link**: 0.8 (maximum reactive motion)
- **Momentary**: White Bloom (≤1.2s) on downbeat

### Scene 4: Texture - Hologram
- **Duration**: 25-35s
- **Intensity**: 0.95 → 0.45 (taper down)
- **Metrics Link**: 0.8 → 0.25 (reduce reactive motion)

## Troubleshooting

### Show Won't Start
1. Check if show is loaded: `make touring-rig-status`
2. Verify scenes are ready
3. Check intensity is set
4. Ensure metrics link is enabled

### Performance Issues
1. Check frame budget: p95 ≤ 12ms
2. Reduce intensity if needed
3. Disable heavy FX
4. Check system resources

### A11y Issues
1. Verify motion-reduced mode
2. Check mono fallback
3. Ensure fade times ≤ 500ms
4. Test with A11y hard mode

## Contact Information

### Technical Issues
- **Primary**: FOH Engineer
- **Secondary**: Tour Manager
- **Escalation**: Production Manager

### Safety Issues
- **Immediate**: Stop show, activate blackout
- **Contact**: Stage Manager
- **Escalation**: Venue Safety Officer

