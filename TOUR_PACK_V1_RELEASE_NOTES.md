# 🎼 Tour Pack v1 - Release Notes

## 🌙✨ **CODE SAMPLER + FX SYMPHONY** - Bulletproof Anywhere System

### **🚀 What's New**
- **3-Movement Performance Timeline** (90s total)
- **Polyglot Fugue** with Glass Cathedral shimmer
- **FX Rack Morph** from cathedral to storm  
- **Lunar Interlude** with LOLcat++ Cat-Walk
- **Tour Pack** for FOH on USB (works offline)
- **Creative Mini-Sets** for spontaneous performances
- **Safety Rails** for all audiences

---

## 🎭 **30-Second Show Start**

### **Quick Start**
```bash
# 1) Open the house (runs symphony, builds poster, gallery, bundle, stage page)
make code-sampler-fx-symphony-show

# 2) If venue Wi-Fi is flaky, go fully offline
make tour-pack
python -m http.server 8080 -d out   # share the stage page locally

# 3) Choose a room profile
make venue-small   # cozy room, fast tails
# or
make venue-large   # big room, longer bloom
```

### **FOH Micro-Cheat (Live Keys)**
- **1 / 2 / 3** = movements I / II / III
- **I / K** = intensity up/down (slew-limited)
- **M** = toggle metrics link (sweet spot ~0.6 in movement II)
- **W** = white bloom on the downbeat to III
- **B** = blackout for final button

---

## 🎼 **Creative Mini-Sets**

### **1. Polyglot Rondo (60s)**
```bash
make polyglot-rondo
```
**Python→Rust→Go→SQL with Glass Cathedral start, morph to Data Storm, resolve with Cinemascope.**

### **2. Lunar Catwalk (45s)**
```bash
make lunar-catwalk
```
**Clair de Lune shimmer → LOLcat++ Cat-Walk (Studio-Safe palette) → Stage-Punch hit for 2s.**

### **3. Opera Tag (30s)**
```bash
make opera-tag
```
**Bring in the Code Opera choir for a final cadence, then blackout.**

---

## 🎵 **"Wow" Encores**

### **Tape Dream Bridge (20s)**
```bash
make tape-dream-bridge-live
```
**Lo-fi palate cleanser before the storm**

### **Audience Palette Vote (5–8 keys)**
```bash
make audience-palette-neon      # Neon (cyberpunk)
make audience-palette-emerald   # Emerald (nature)
make audience-palette-copper    # Copper (warm)
make audience-palette-cyberpunk # Cyberpunk (futuristic)
```

---

## 📸 **Zero-Friction Capture**

```bash
make snapshot-kit      # low/mid/peak stills
make capture-30s       # highlight reel
make code-sampler-fx-symphony-poster
```

---

## 🛡️ **Quick Rescue / Safety**

```bash
make show-readiness-check     # sanity sweep
make stage-proof-acceptance   # ALL GREEN or fix before doors
make safety-rails             # strobe cap, motion watchdog
```

---

## 🎨 **Tiny Polish That Plays Huge**

### **Performance Flow**
- **Intro hush**: start intensity at 0.28, ramp to 0.45 over 10s
- **Storm crest**: 6–8s morph Glass Cathedral → Data Storm, sidechain ≤ 0.8
- **A11y flip**: use Studio-Safe palette in LOLcat++; fades ≤ 490ms
- **Seed stamp**: re-run the exact take later with SEED=<n>

### **Safety Features**
- **Strobe guard**: ≤ 8 Hz, duty ≤ 35%
- **Frame rate**: p95 ≤ 10-12 ms
- **Motion-reduced**: ≤ 490 ms fades
- **A11y compliance**: Full accessibility support
- **Mono fallback**: Safe for all audiences

---

## 📦 **Tour Pack Contents**

### **What's Included**
- **Venue Profiles**: Small, Medium, Large venue settings
- **Stage Page**: Clean stream page (dark UI, big text, no controls)
- **FOH Cheat Sheet**: Micro-cheat sheet for operators
- **30s Highlight Reel**: Script for social media captures
- **Concert Poster**: Professional promo materials
- **README**: Complete setup guide

### **Quick Start**
1. **Extract** tour pack zip to USB drive
2. **Run** appropriate venue profile:
   - `make venue-small` (intimate spaces)
   - `make venue-medium` (mid-size venues)  
   - `make venue-large` (arena spaces)
3. **Start** offline stage page: `make offline-stage-page`
4. **Open** http://localhost:8080 in browser

---

## 🎼 **Complete Command Reference**

### **Show Ready**
```bash
make code-sampler-fx-symphony-show      # Complete symphony + artifacts
make code-sampler-fx-symphony-double-bill # Epic double-bill
make tour-pack                          # Tour pack for FOH on USB
```

### **Creative Mini-Sets**
```bash
make polyglot-rondo    # Python→Rust→Go→SQL with Glass Cathedral
make lunar-catwalk     # Clair de Lune → LOLcat++ → Stage-Punch
make opera-tag         # Code Opera choir for final cadence
```

### **Encores & Extras**
```bash
make tape-dream-bridge-live     # Lo-fi palate cleanser
make audience-palette-neon      # Neon palette vote
make audience-palette-emerald   # Emerald palette vote
make audience-palette-copper    # Copper palette vote
make audience-palette-cyberpunk # Cyberpunk palette vote
```

### **Safety & Readiness**
```bash
make show-readiness-check     # Final readiness check
make stage-proof-acceptance   # All systems check
make safety-rails             # Safety rails active
```

### **Capture & Share**
```bash
make snapshot-kit           # Generate snapshots
make capture-30s            # 30s highlight reel
make stage-page             # Clean stream page
make artifact-bundle        # Create release bundle
```

---

## 🌙✨ **The Magic**

### **What You Get:**
- **3-Movement Performance Timeline** (90s total)
- **Polyglot Fugue** with Glass Cathedral shimmer
- **FX Rack Morph** from cathedral to storm
- **Lunar Interlude** with LOLcat++ Cat-Walk
- **Tour Pack** for FOH on USB
- **Creative Mini-Sets** for spontaneous performances
- **Safety Rails** for all audiences

### **The Result:**
- **Bach-like cathedral fugue** → **Modern glitch opera storm** → **Playful moonlit cats**
- **Code is both score and sound**
- **Creative instrument perfection**
- **Bulletproof anywhere in minutes**

---

## 🚀 **Ready for Showtime!**

### **30-Second Setup**
1. **Open the house**: `make code-sampler-fx-symphony-show`
2. **Choose venue**: `make venue-small/medium/large`
3. **Start performance**: Use FOH micro-cheat keys
4. **Capture & share**: `make snapshot-kit && make capture-30s`

### **Creative Freedom**
- **Mini-sets** for spontaneous performances
- **Encores** for audience interaction
- **Safety rails** for all audiences
- **Offline tour pack** for any venue

---

## 🎼 **CODE SAMPLER + FX SYMPHONY = BULLETPROOF ANYWHERE!**

**🌙✨ Ready to open the house and perform anywhere in minutes! 🚀**

**House is open, lights are warm - showtime! 🎭**

---

## 📋 **Safety Badge**

✅ **A11y Compliant** - Full accessibility support  
✅ **Motion Reduced** - ≤ 490 ms fades  
✅ **Strobe Guard** - ≤ 8 Hz, duty ≤ 35%  
✅ **Mono Fallback** - Safe for all audiences  
✅ **Frame Rate** - p95 ≤ 10-12 ms  
✅ **Offline Ready** - Works in venues with flaky Wi-Fi  

**🎼 Tour Pack v1 - Bulletproof Anywhere System Ready! ✨**


