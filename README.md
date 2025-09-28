# CodeSampler Live — Hybrid Performance Stack

🎭 **Complete performance system with BeatBridge + MIDI + OSC + TouchOSC + Ableton integration**

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Launch complete performance system
make performance-setup

# Open browser, allow Mic + MIDI permissions
# Your CodeSampler Live is now ready!
```

## 🎛️ OSC Controls

Send these OSC messages to `127.0.0.1:57120`:

- **`/fx/hue <0..1>`** → Hue control (0-360°)
- **`/fx/intensity <0..1>`** → FX intensity (0-1)
- **`/run`** → Trigger code execution
- **`/crowd/kick`** → Audience kick
- **`/gov/cap <0..1>`** → FPS governor cap

## 🎵 BeatBridge Integration

Your sandboxed code receives an **ENV object** with real-time audio data:

```javascript
// BeatBridge injected variables
const { beat, bpm, bands, t } = ENV;

// Beat-sync code example
let value = Math.sin(t * (bpm/60) * Math.PI);
if (beat) value *= 1.2; // kick on downbeat

return {
  time: new Date().toLocaleTimeString(),
  bpm: Math.round(bpm),
  bass: Number(bands.bass.toFixed(2)),
  value: Number(value.toFixed(4))
};
```

## 📱 Mobile Control (TouchOSC)

1. **Import template**: `scripts/touchosc-template.xml`
2. **Set host**: `127.0.0.1:57120`
3. **Control**: Hue, Intensity, Run, Kick from your phone

## 🎹 DAW Integration (Ableton Live)

1. **Setup guide**: `scripts/ableton-template.md`
2. **OSC device**: Add Max for Live OSC sender
3. **Map controls**: CC1→Hue, CC2→Intensity, C1→Run
4. **Automation**: Sync with your DAW timeline

## 👥 Crowd Control

- **WebSocket**: `ws://localhost:8765`
- **Audience participation**: Nudge hue/intensity from phones
- **Live interaction**: Real-time crowd feedback

## 🎬 Show Commands

```bash
# Complete performance setup
make performance-setup

# Individual components
make osc-bridge          # OSC → WebSocket bridge
make crowd-test          # Crowd control demo
make code-sampler-live   # Main application

# Templates
make touchosc-template   # TouchOSC setup
make ableton-template    # Ableton setup
```

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Start OSC bridge
npm run osc-bridge

# Start crowd control
npm run crowd-test

# Complete setup (all services)
npm run performance-setup
```

## 🎉 Ready for Showtime!

Your **CodeSampler Live** performance system is now **complete** with:
- ✅ **BeatBridge** for real-time audio sync
- ✅ **MIDI/OSC** for professional control
- ✅ **TouchOSC** for mobile control
- ✅ **Ableton** integration for DAW sync
- ✅ **Crowd Control** for audience participation
- ✅ **Safety Rails** for performance stability

**🌙✨ Let the creative coding begin! 🎭🚀**