# FOH Runbook - Touring Rig Operator Flow
==========================================

## Startup (T-15 min)

### System Check
```bash
# Start API server (if driving via API)
make touring-rig-server

# Load show and verify status
make touring-rig-load && make touring-rig-status

# Set safe cold open settings
make touring-rig-intensity value=0.65
make touring-rig-metrics-link value=0.35

# Confirm A11y compliance
make touring-rig-param key=preview.variant value=motion-safe
make touring-rig-param key=preview.variant value=mono
```

### Pre-Show Checklist
- [ ] Show loaded and scenes verified
- [ ] Intensity set to 0.65 (safe cold open)
- [ ] Metrics link set to 0.35 (tasteful reactive motion)
- [ ] A11y: motion-safe variant thumbnail renders
- [ ] Mono mode available
- [ ] All momentary buttons tested
- [ ] Safety rails confirmed

## Go Live

### Scene 1: Warmup - Cinemascope
- **Duration**: 20-30s
- **Intensity**: 0.55 → 0.75 (gradual ramp)
- **Metrics Link**: 0.35 (subtle reactive motion)
- **Notes**: Safe cold open, gentle introduction

### Scene 2: Build - Neon Bloom
- **Duration**: 30-45s
- **Intensity**: 0.75 → 0.85
- **Metrics Link**: 0.6 → 0.8 (increased reactive motion)
- **Notes**: Energy building, audience engagement

### Scene 3: Impact - Prism Burst
- **Duration**: 15-20s
- **Intensity**: 0.85 → 0.95
- **Metrics Link**: 0.8 (maximum reactive motion)
- **Momentary**: White Bloom (≤1.2s) on downbeat
- **Notes**: Peak energy, dramatic impact

### Scene 4: Texture - Hologram
- **Duration**: 25-35s
- **Intensity**: 0.95 → 0.45 (taper down)
- **Metrics Link**: 0.8 → 0.25 (reduce reactive motion)
- **Notes**: Cool down, texture focus

## Emergencies

### Blackout
- **Action**: `make touring-rig-blackout`
- **Effect**: Kill motion/brightness instantly (one tap)
- **Recovery**: Toggle off when ready to resume

### Motion Watchdog Trip
- **Indicator**: Banner will appear
- **System Response**: Auto-throttles trails & strobe
- **Operator Action**: Keep intensity ≤0.7 for 20s
- **Recovery**: System auto-recovers after 20s

### Undo/Redo
- **Misfired Tweak**: `make touring-rig-undo`
- **Redo**: `make touring-rig-redo`
- **History**: 20-step undo/redo stack available

## Quick API One-Liners (curl)

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

## Operator Hotkeys

### Scene Control
- **1-9**: Jump to scene
- **0**: Previous scene
- **Space**: Pause/resume show clock
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
- **W**: White bloom (momentary)

### Undo/Redo
- **U**: Undo
- **R**: Redo

## Safety & Performance Rails

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

## Scene JSON Lint (Pre-flight)

### Duration Limits
- **Morph durations**: 0.3–6.0s
- **Scene durations**: 5–60s

### Intensity Limits
- **Normal scenes**: ≤1.0
- **Boost scenes**: Must declare `allow_boost: true`

### Strobe Safety
- **Any scene with strobe.enabled: true**
- **Must declare strobe.hz ≤ 8**

### A11y Compliance
- **Required**: {mono, motion_safe} thumbnails per scene
- **Format**: scene_id-mono.png, scene_id-motion-safe.png

## Snapshot Kit (Socials/Docs)

### Export Settings
- **Low**: Intensity 0.4, metrics 0.2
- **Mid**: Intensity 0.7, metrics 0.5
- **Peak**: Intensity 0.95, metrics 0.8 (bloom off)

### Export Path
```
/out/touring/snapshots/{scene}-{low|mid|peak}.html
```

### Footer Requirements
- **Seed**: For reproducibility
- **Metrics Window**: 30s average
- **Timestamp**: Export time

## Two Tiny Upgrades (High Impact)

### Global Freeze
- **Function**: Latch current rendered state (no FX updates)
- **UI**: Keep responsive during freeze
- **Recovery**: Unfreeze crossfades back in 300ms
- **Hotkey**: F (Freeze/Unfreeze)

### Tap-Tempo
- **Function**: Average last 4 taps → map to LFO rate & morph clock
- **Range**: 40–180 BPM
- **Hotkey**: T (Tap tempo)
- **Display**: BPM indicator in UI

## Emergency Contacts

### Technical Issues
- **Primary**: FOH Engineer
- **Secondary**: Tour Manager
- **Escalation**: Production Manager

### Safety Issues
- **Immediate**: Stop show, activate blackout
- **Contact**: Stage Manager
- **Escalation**: Venue Safety Officer

## Post-Show

### Cleanup
- [ ] Stop all shows
- [ ] Reset intensity to 0.0
- [ ] Disable all momentary buttons
- [ ] Save show state
- [ ] Export snapshots
- [ ] Clear undo/redo history

### Documentation
- [ ] Note any issues
- [ ] Record performance metrics
- [ ] Update show notes
- [ ] Backup show files



