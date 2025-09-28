# 🎼 Code Sampler + FX Symphony - Bulletproof Anywhere

## 🌙✨ **HOUSE IS OPEN, LIGHTS ARE WARM!** Complete Show Readiness System

### **🚀 One-Liner Commands**
```bash
# Complete symphony + artifacts + stage page
make code-sampler-fx-symphony-show

# Epic double-bill: Lunar Recital + Code Symphony  
make code-sampler-fx-symphony-double-bill

# Tour pack for FOH on USB
make tour-pack
```

---

## 📦 Rapid Upgrades (5–10 min)

### **No-Internet "Tour Pack"**
```bash
make artifact-bundle            # zip out/ + poster + logs
python -m http.server 8080 -d out   # offline stage page
```
**Works in venues with flaky Wi-Fi.**

### **Venue Profiles (auto-scale)**
```bash
make venue-small     # dust/trails low, 60fps bias
make venue-medium    # balanced settings
make venue-large     # bigger particles, longer tails
```
**Maps intensity + particle density to room size.**

### **Operator Safety Snapshot**
```bash
make stage-proof-acceptance
make safety-rails
make show-readiness-check
```
**Paste the "ALL GREEN" line into the run log before doors.**

---

## 🎭 Killer Encores (drop-in scenes)

### **"Tape Dream" Bridge (20s)**
```bash
make tape-dream-bridge
```
**Insert between Movements II → III for a lo-fi palate cleanser.**

### **Audience Palette Vote (keys 5–8)**
- **5**: Neon (cyberpunk)
- **6**: Emerald (nature)  
- **7**: Copper (warm)
- **8**: Cyberpunk (futuristic)
**Add to your hotkeys overlay so the crowd sees the change.**

### **Code Opera Tag**
```bash
make code-opera-tag
```
**Bring in the choir for the final cadence, then blackout.**

---

## 📺 Stream/Record Ready

### **Clean Stream Page (dark UI, big text, no controls)**
```bash
make stage-page && open out/stage/index.html
```

### **30s Highlight & Grid**
```bash
make snapshot-kit && make capture-30s
```

---

## 🎛️ FOH Micro-Cheat (Print This)

### **Performance Flow**
- **Open**: intensity 0.28 → 0.45 over 10s
- **Crest**: morph Glass Cathedral → Data Storm, 6–8s, sidechain ≤0.8
- **Cat-Walk**: Studio-Safe palette, dust 0.18, trails 0.25
- **Encore**: Stage-Punch for ≤2s + White Bloom, then B (blackout)

### **Live Control**
- **1/2/3** — Jump to movements I/II/III
- **I / K** — Intensity up/down (slew-limited)
- **M** — Toggle metrics link (sweet spot ~0.6 in Movement II)
- **W** — White Bloom on the downbeat of Movement II → III
- **B** — Blackout on the final cadence

### **Sidechain Sweet Spots**
- **QPS ↑** → Gradient phase speed ↑ (cap 0.8/s)
- **Error rate ↑** → Chaos bump (≤ +0.1, guarded)
- **P95 ↑** → Emoji & trail × 0.75 (comfort + perf)

---

## 🚀 Release in One Shot

```bash
make code-sampler-fx-symphony-show   # run + poster + gallery + bundle
gh release create v0.5-show --notes "Code Sampler + FX Symphony"
```

---

## 📦 Tour Pack Contents

### **What's Included**
- **Venue Profiles**: Small, Medium, Large venue settings
- **Stage Page**: Clean stream page (dark UI, big text, no controls)
- **FOH Cheat Sheet**: Micro-cheat sheet for operators
- **30s Highlight Reel**: Script for social media captures
- **Concert Poster**: Professional promo materials

### **Quick Start**
1. **Extract** tour pack zip to USB drive
2. **Run** appropriate venue profile:
   - `make venue-small` (intimate spaces)
   - `make venue-medium` (mid-size venues)  
   - `make venue-large` (arena spaces)
3. **Start** offline stage page: `make offline-stage-page`
4. **Open** http://localhost:8080 in browser

### **FOH Control**
- **Movement Navigation**: 1/2/3 for movements I/II/III
- **Live Parameters**: I/K for intensity, M for metrics link
- **Effects**: W for White Bloom, B for blackout
- **Safety**: All rails active, A11y compliant

### **Capture & Share**
- **30s Highlight**: Run `./30s_highlight_reel.sh`
- **Snapshots**: Generated in out/touring/snapshots/
- **Gallery**: Chromatic enhanced HTML gallery
- **Poster**: Concert program poster

---

## 🛡️ Safety Features

### **Guardrails Active**
- **Strobe guard**: ≤ 8 Hz, duty ≤ 35%
- **Frame rate**: p95 ≤ 10-12 ms
- **Motion-reduced**: ≤ 490 ms fades
- **A11y compliance**: Full accessibility support
- **Mono fallback**: Safe for all audiences

### **Operator Safety**
- **Stage Proof Acceptance**: All systems green
- **Safety Rails**: Locked and loaded
- **Show Readiness**: Final systems check
- **FOH Cheat Sheet**: Print-ready operator guide

---

## 🎼 Complete Command Reference

### **Show Ready**
```bash
make code-sampler-fx-symphony-show      # Complete symphony + artifacts
make code-sampler-fx-symphony-double-bill # Epic double-bill
make tour-pack                          # Tour pack for FOH on USB
```

### **Individual Movements**
```bash
make code-sampler-fx-symphony-movement-I    # Polyglot Fugue
make code-sampler-fx-symphony-movement-II   # FX Rack Morph
make code-sampler-fx-symphony-movement-III  # Lunar Interlude
```

### **Venue Profiles**
```bash
make venue-small     # Intimate spaces
make venue-medium    # Mid-size venues
make venue-large     # Arena spaces
```

### **Safety & Readiness**
```bash
make stage-proof-acceptance  # All systems check
make safety-rails           # Safety rails active
make show-readiness-check   # Final readiness check
```

### **Capture & Share**
```bash
make snapshot-kit           # Generate snapshots
make capture-30s            # 30s highlight reel
make stage-page             # Clean stream page
make artifact-bundle        # Create release bundle
```

### **Encores & Extras**
```bash
make tape-dream-bridge       # Lo-fi palate cleanser
make audience-palette-vote  # Crowd palette voting
make code-opera-tag         # Choir for final cadence
```

---

## 🌙✨ The Result

### **What You Get:**
- **3-Movement Performance Timeline** (90s total)
- **Polyglot Fugue** with Glass Cathedral shimmer
- **FX Rack Morph** from cathedral to storm
- **Lunar Interlude** with LOLcat++ Cat-Walk
- **Tour Pack** for FOH on USB
- **Safety Rails** for all audiences
- **Stream/Record Ready** system

### **The Magic:**
- **Code Sampler** = Melody (polyglot transformations)
- **FX Engine** = Production Polish (racks, morphs, palettes, LOLcat++)
- **Together** = A polyglot code symphony with stage lighting & comic relief

### **Bulletproof Anywhere:**
- **No-Internet Tour Pack** for flaky Wi-Fi venues
- **Venue Profiles** that auto-scale to room size
- **Operator Safety** with stage-proof acceptance
- **FOH Micro-Cheat** for live control
- **Stream/Record Ready** for social media

---

## 🎼 **CODE SAMPLER + FX SYMPHONY = BULLETPROOF ANYWHERE!**

### **Complete System:**
- **3-Movement Performance Timeline** (90s total)
- **Rapid Upgrades** (5-10 min setup)
- **Killer Encores** (drop-in scenes)
- **Stream/Record Ready** (clean UI, 30s highlights)
- **FOH Micro-Cheat** (print-ready operator guide)
- **Tour Pack** (USB-ready for FOH)
- **Safety Features** (A11y compliant, guardrails active)

### **Ready Commands:**
- **Show Ready**: `make code-sampler-fx-symphony-show`
- **Double-Bill**: `make code-sampler-fx-symphony-double-bill`
- **Tour Pack**: `make tour-pack`
- **Individual**: `make code-sampler-fx-symphony-movement-I/II/III`
- **Venue Profiles**: `make venue-small/medium/large`
- **Safety**: `make show-readiness-check`

**🌙✨ CODE SAMPLER + FX SYMPHONY = BULLETPROOF ANYWHERE PERFECTION! 🐾✨**

**Ready to open the house and perform anywhere in minutes! 🚀**

**House is open, lights are warm - showtime! 🎭**


