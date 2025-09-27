# 🎭 Code Opera - Complete Showflow

## One-Liner Showflow

```bash
make opera-showflow
```

This single command runs the complete Code Opera showflow:

1. **Start live server** (port 8787)
2. **Run Code Opera with seed** (deterministic)
3. **Apply counterpoint guard** (fix parallel fifths)
4. **Export MIDI** (one track per voice)
5. **Run sanity tests** (verify everything)
6. **Open harmony visualization** (HTML)
7. **Open MIDI file** (for DAW)

## Individual Commands

### 🎭 Basic Code Opera
```bash
make code-opera              # Basic performance
make code-opera-seed         # With deterministic seed
```

### 🎛️ Conductor Panel
```bash
make code-opera-live         # Live server (port 8787)
make code-opera-ui           # Conductor UI (port 8788)
```

### 🎵 MIDI Export
```bash
make code-opera-midi         # With MIDI export
```

### 🎼 Counterpoint Guard
```bash
make code-opera-counterpoint # With counterpoint rules
```

### 📸 Headless Capture
```bash
make opera-snaps             # Capture screenshots
```

### 🧪 Sanity Tests
```bash
make opera-test              # Run all tests
```

## 🎭 What You Get

### **Artifacts Generated:**
- `out/opera/code_opera_harmony.html` - Harmony visualization
- `out/opera/opera.mid` - MIDI file (one track per voice)
- `out/opera/manifest.json` - Performance manifest with content hash
- `out/opera/SEED.txt` - Deterministic seed for reproducibility
- `out/opera/counterpoint.log` - Counterpoint guard log
- `out/opera/snaps/` - Screenshot frames for video creation

### **Voice Files (3 Acts Each):**
- `out/voices/rust_act_1.py` - Rust voice, Act I (C major)
- `out/voices/rust_act_2.py` - Rust voice, Act II (G major)
- `out/voices/rust_act_3.py` - Rust voice, Act III (C major)
- ... (same for python, julia, typescript, go, csharp, sql)

### **MIDI Tracks:**
- **Track 1**: Rust (Bass voice)
- **Track 2**: Python (Tenor voice)
- **Track 3**: Julia (Soprano voice)
- **Track 4**: TypeScript (Alto voice)
- **Track 5**: Go (Bass voice)
- **Track 6**: C# (Bass voice)
- **Track 7**: SQL (Bass voice)

## 🎵 Musical Structure

### **Act I - Introduction (C Major)**
- All voices in C major
- Basic texture and FX patterns
- Introduction of themes

### **Act II - Development (G Major)**
- Key modulation to G major
- Enhanced complexity patterns
- Development of themes

### **Act III - Grand Cadence (C Major)**
- Return to C major
- Resolution patterns
- Grand cadence

## 🎛️ Conductor Panel Features

### **Global Controls:**
- **BPM**: 60-160 (real-time tempo)
- **Key**: C, G, F, D, A, E major
- **Seed**: Deterministic seed for reproducibility

### **Per-Voice Controls:**
- **Gain**: 0-100% volume
- **Mute/Solo**: Voice isolation
- **FX**: Reverb, chorus, distortion, delay, LFO

### **Performance Metrics:**
- **P95 Latency**: Maps to dynamics (forte)
- **Error Rate**: Maps to staccato (shorter motifs)
- **QPS**: Maps to tempo bump

## 🧪 Sanity Tests

### **Determinism Tests:**
- ✅ Same seed → identical content hash
- ✅ Manifest structure validation
- ✅ Content hash verification

### **Musical Tests:**
- ✅ Each voice emits ≥1 phrase per act
- ✅ Act II uses target key (G)
- ✅ Act III returns to tonic (C)
- ✅ No consecutive parallel 5ths/8ves

### **Performance Tests:**
- ✅ File size within budget
- ✅ Counterpoint guard applied
- ✅ Voice output validation

## 🎬 Video Creation

After running `make opera-snaps`:

```bash
cd out/opera/snaps
./create_video.sh
```

This creates:
- `opera_performance.mp4` - High-quality video
- `opera_performance.gif` - Animated GIF

## 🎭 API Endpoints

### **State Management:**
- `GET /opera/state` - Get current conductor state
- `POST /opera/state` - Update conductor state
- `GET /opera/seed` - Get current seed
- `POST /opera/seed` - Set deterministic seed

### **Performance Control:**
- `POST /opera/advance` - Advance to next act
- `POST /opera/reset` - Reset to Act I
- `POST /opera/metrics` - Update performance metrics

### **Voice Management:**
- `GET /opera/voices` - Get all voice configurations
- `GET /opera/performance` - Get performance data

## 🎵 MIDI Integration

### **DAW Import:**
1. Open `out/opera/opera.mid` in your DAW
2. Each track represents a voice
3. Apply your own FX and mixing
4. Export your interpretation

### **Track Mapping:**
- **Track 1**: Rust (Bass) - Acoustic Grand Piano
- **Track 2**: Python (Tenor) - Bright Acoustic Piano
- **Track 3**: Julia (Soprano) - Electric Grand Piano
- **Track 4**: TypeScript (Alto) - Honky-tonk Piano
- **Track 5**: Go (Bass) - Electric Piano 1
- **Track 6**: C# (Bass) - Electric Piano 2
- **Track 7**: SQL (Bass) - Harpsichord

## 🎭 Creative Extensions

### **Custom Seeds:**
```bash
python3 scripts/code_opera.py --seed "my-custom-seed"
```

### **Custom BPM:**
```bash
python3 scripts/opera_export_midi.py --bpm 120
```

### **Custom Key:**
```bash
python3 scripts/opera_export_midi.py --key G
```

## 🎉 Ready for Showtime!

**Code Opera** is now a complete creative coding orchestra with:**
- 🎛️ **Conductor Panel** - Real-time controls
- 🎵 **MIDI Export** - DAW integration
- 🎼 **Counterpoint Guard** - Musical rules
- 📸 **Headless Capture** - Video creation
- 🧪 **Sanity Tests** - Quality assurance
- 🎭 **3-Act Structure** - Musical form

**This is a complete creative coding performance system!** 🚀🎨✨
