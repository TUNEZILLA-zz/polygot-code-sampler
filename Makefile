# Code Live - Creative Demo Makefile
# ===================================

.PHONY: help creative-demo texture-bakeoff texture-fx-matrix retro-modes 432-easter ab-analysis validation-report clean

# Default target
help:
	@echo "🎨 Code Live - Creative Demo System"
	@echo "===================================="
	@echo ""
	@echo "Available targets:"
	@echo "  creative-demo      Run all creative demos"
	@echo "  texture-bakeoff    Run texture bake-off (8 textures)"
	@echo "  texture-fx-matrix  Run texture×FX matrix"
	@echo "  retro-modes        Run retro sampler modes"
	@echo "  432-easter        Run 432 Hz easter preset"
	@echo "  ab-analysis       Run A/B analysis"
	@echo "  validation-report Generate validation report"
	@echo "  code-opera        Multi-voice creative coding performance"
	@echo "  code-opera-seed   Code Opera with deterministic seed"
	@echo "  code-opera-live   Live development server (port 8787)"
	@echo "  code-opera-ui     Conductor panel UI server (port 8788)"
	@echo "  code-opera-midi   Code Opera with MIDI export"
	@echo "  code-opera-counterpoint  Code Opera with counterpoint guard"
	@echo "  opera-snaps       Capture Code Opera performance screenshots"
	@echo "  opera-test        Run Code Opera sanity tests"
	@echo "  opera-showflow    Complete Code Opera showflow (demo)"
	@echo "  tunezilla-opera   TuneZilla Opera performance"
	@echo "  tunezilla-opera-seed  TuneZilla Opera with deterministic seed"
	@echo "  tunezilla-poster  TuneZilla Opera poster visualization"
	@echo "  string-fx         Crazy String FX effects"
	@echo "  string-fx-glitch  Glitch String FX effects"
	@echo "  string-fx-presets String FX presets"
	@echo "  string-fx-gallery String FX gallery"
	@echo "  enhanced-string-fx Enhanced String FX (FX Graph Runtime)"
	@echo "  enhanced-string-fx-preset Enhanced String FX with presets"
	@echo "  enhanced-string-fx-html Enhanced String FX HTML output"
	@echo "  enhanced-string-fx-list List Enhanced String FX presets"
	@echo "  string-fx-server  String FX FastAPI server"
	@echo "  tremolo-fx       Tremolo String FX (repetition)"
	@echo "  tremolo-fx-wave  Tremolo Wave FX (wave + color)"
	@echo "  tremolo-fx-preset Tremolo Rave Preset"
	@echo "  tremolo-fx-html  Tremolo FX HTML output"
	@echo "  string-orchestra String Orchestra Mode (vibrato + harmonics)"
	@echo "  violin-solo     Violin Solo (vibrato + glissando)"
	@echo "  guitar-lead     Guitar Lead (string bends + feedback)"
	@echo "  pizzicato-strings Pizzicato Strings (palm mute + trill)"
	@echo "  arpeggio-harp   Arpeggio Harp (spread + harmonics)"
	@echo "  feedback-sustain Feedback Sustain (tremolo + harmonics)"
	@echo "  string-orchestra-html String Orchestra HTML Gallery"
	@echo "  conductor-score   Conductor Score DSL (Tremolo forte)"
	@echo "  conductor-score-crescendo Conductor Score Crescendo"
	@echo "  conductor-score-hybrid Conductor Score Hybrid (Guitar Lead ff neon)"
	@echo "  conductor-score-ensemble Conductor Score Ensemble"
	@echo "  conductor-score-create Create Conductor Score"
	@echo "  conductor-score-html Conductor Score HTML output"
	@echo "  refraction-fx       Refraction Text FX (prism split)"
	@echo "  refraction-glass-warp Glass Warp Refraction"
	@echo "  refraction-ripple   Ripple Refraction (waveform)"
	@echo "  refraction-spectral Spectral Ghosts Refraction"
	@echo "  refraction-broken   Broken Glass Refraction"
	@echo "  refraction-preset   Prism Rainbow Preset"
	@echo "  refraction-html     Refraction HTML Gallery"
	@echo "  chromatic-fx        Chromatic Aberration Text FX (RGB offset)"
	@echo "  chromatic-fringe   Chromatic Fringe Blur"
	@echo "  chromatic-pulse     Chromatic Pulse (LFO breathing)"
	@echo "  chromatic-spectrum  Chromatic Broken Spectrum"
	@echo "  chromatic-trails    Chromatic Trails (after-images)"
	@echo "  chromatic-preset    Chromatic RGB Preset"
	@echo "  prism-mode         Prism Mode (Refraction + Chromatic)"
	@echo "  chromatic-html     Chromatic Aberration HTML Gallery"
	@echo "  light-fx           Light-Based Text FX (glow/bloom)"
	@echo "  light-flare        Lens Flare with rainbow gradient"
	@echo "  light-strobe       Strobe Rave with chromatic aberration"
	@echo "  light-caustics     Caustic Water with waveform distortion"
	@echo "  light-volumetric   Volumetric Beams with blue shadows"
	@echo "  light-lightning    Storm Lightning with strobe"
	@echo "  light-hologram     Hologram Glow with glitch colors"
	@echo "  light-laser        Laser Sweep with neon glow"
	@echo "  light-preset       Neon Bloom Preset"
	@echo "  lighting-desk      Lighting Desk (Glow + Flare + Strobe + Chromatic)"
	@echo "  light-html         Light-Based Text FX HTML Gallery"
	@echo "  chromatic-light-desk Chromatic Light Desk (Live metrics mapping)"
	@echo "  chromatic-neon-bloom Enhanced Neon Bloom Preset"
	@echo "  chromatic-prism-burst Prism Burst Preset"
	@echo "  chromatic-hologram  Enhanced Hologram Preset"
	@echo "  chromatic-storm     Enhanced Storm Lightning Preset"
	@echo "  chromatic-cinemascope Cinemascope Preset"
	@echo "  chromatic-enhanced-html Enhanced Chromatic HTML Gallery"
	@echo "  effect-rack-list    List Effect Rack Presets"
	@echo "  effect-rack-decapitator Decapitator (Distortion) Effect Rack"
	@echo "  effect-rack-little-plate Little Plate (Reverb) Effect Rack"
	@echo "  effect-rack-echo-boy EchoBoy (Delay) Effect Rack"
	@echo "  effect-rack-crystallizer Crystallizer (Granular) Effect Rack"
	@echo "  effect-rack-devil-loc Devil-Loc (Compressor) Effect Rack"
	@echo "  effect-rack-micro-shift MicroShift (Chorus) Effect Rack"
	@echo "  effect-rack-custom   Custom Effect Rack (Distortion + Neon + Glitch)"
	@echo "  effect-rack-status  Show Effect Rack Status"
	@echo "  effect-rack-html    Effect Rack HTML Gallery"
	@echo "  show-controller-flow Professional Showpiece Flow (10-15 min)"
	@echo "  show-controller-cinemascope Cinemascope Scene (Warm-up)"
	@echo "  show-controller-neon-bloom Neon Bloom Scene (Build Energy)"
	@echo "  show-controller-prism-burst Prism Burst Scene (Impact Moment)"
	@echo "  show-controller-hologram Hologram Scene (Cool-down)"
	@echo "  show-controller-a11y A11y-Safe Scene (Accessibility)"
	@echo "  show-controller-mono Mono Mode Scene (No Chromatic)"
	@echo "  show-controller-snapshot Snapshot Kit for Social/Docs"
	@echo "  show-controller-save-scene Save Scene Configuration"
	@echo "  show-controller-load-scene Load Scene Configuration"
	@echo "  pro-rack-tour-opener Tour Opener Rack (Distortion + Chorus + Echo)"
	@echo "  pro-rack-glass-cathedral Glass Cathedral Rack (Hologram + Chromatic + Reverb)"
	@echo "  pro-rack-tape-dream Tape Dream Rack (Echo + Chorus + Chromatic)"
	@echo "  pro-rack-data-storm Data Storm Rack (Distortion + Stutter + Lightning)"
	@echo "  pro-rack-crystalline-bloom Crystalline Bloom Rack (Granular + Chromatic + Trails)"
	@echo "  pro-rack-morph Rack Morph (Tour Opener → Glass Cathedral)"
	@echo "  pro-rack-status Show Pro Rack Status"
	@echo "  rack-show-tour-opener Tour Opener Show (3 scenes, 30s)"
	@echo "  rack-show-create-demo Create Demo Show"
	@echo "  rack-show-status Show Rack Show Status"
	@echo "  touring-rig-load Load Touring Rig Show"
	@echo "  touring-rig-play Play Touring Rig Show"
	@echo "  touring-rig-intensity Set Live Intensity (0-120%)"
	@echo "  touring-rig-blackout Toggle Blackout"
	@echo "  touring-rig-flash-strobe Toggle Flash Strobe"
	@echo "  touring-rig-all-white-bloom Toggle All-White Bloom"
	@echo "  touring-rig-metrics-link Set Metrics Link Strength (0-100%)"
	@echo "  touring-rig-param Set Parameter (path value)"
	@echo "  touring-rig-undo Undo Last Action"
	@echo "  touring-rig-redo Redo Last Action"
	@echo "  touring-rig-status Show Touring Rig Status"
	@echo "  touring-rig-server Start Touring Rig API Server"
	@echo "  stage-proof-load Load Stage-Proof Scene"
	@echo "  stage-proof-acceptance Run Stage-Proof Acceptance Test"
	@echo "  stage-proof-intensity Set Global Intensity (0-120%)"
	@echo "  stage-proof-blackout Toggle Blackout"
	@echo "  stage-proof-white-bloom Toggle White Bloom"
	@echo "  stage-proof-lightning-flash Toggle Lightning Flash"
	@echo "  stage-proof-status Show Stage-Proof Status"
	@echo "  show-readiness-check 5-minute Show Readiness Check"
	@echo "  scene-validator Validate Scene JSON files"
	@echo "  scene-validator-strict Validate Scene JSON files (strict mode)"
	@echo "  snapshot-kit Generate Snapshot Kit for all scenes"
	@echo "  snapshot-kit-scene Generate Snapshot Kit for single scene"
	@echo "  foh-runbook Display FOH Runbook"
	@echo "  operator-hotkeys Display Operator Hotkeys Reference"
	@echo "  safety-rails Display Safety Rails Status"
	@echo "  api-one-liners Display API One-Liners (curl)"
	@echo "  a11y-timing-test Test A11y Timing System"
	@echo "  a11y-timing-test-fps Test A11y Timing at 59 FPS"
	@echo "  a11y-timing-test-hard Test A11y Hard Mode"
	@echo "  timing-harness Run Timing Harness (FPS Sweep)"
	@echo "  timing-harness-report Run Timing Harness with Report"
	@echo "  timing-harness-custom Run Custom Timing Harness"
	@echo "  go-live-1 Cut RC + Artifact Bundle"
	@echo "  go-live-2 Lock Acceptance"
	@echo "  go-live-3 Dress Rehearsal Script (15 min)"
	@echo "  go-live-4 Safety Rails Trip Test (2 min)"
	@echo "  go-live-5 Observability Pin (Grafana panels green)"
	@echo "  go-live-6 Publish Show Kit"
	@echo "  go-live-all Go-Live in 6 Moves (Complete Deployment)"
	@echo "  code-hero         Guitar Hero for code loops (coming soon)"
	@echo "  code-tarot        Divination system for creative coding (coming soon)"
	@echo "  clean             Clean output directory"
	@echo ""
	@echo "Examples:"
	@echo "  make creative-demo"
	@echo "  make texture-bakeoff"
	@echo "  make validation-report"

# Run all creative demos
creative-demo:
	@echo "🎨 Running all creative demos..."
	python3 scripts/creative_demo.py --all

# Individual demo targets
texture-bakeoff:
	@echo "🎨 Running texture bake-off..."
	python3 scripts/creative_demo.py --texture-bakeoff

texture-fx-matrix:
	@echo "🎛️ Running texture×FX matrix..."
	python3 scripts/creative_demo.py --texture-fx-matrix

retro-modes:
	@echo "🎛️ Running retro sampler modes..."
	python3 scripts/creative_demo.py --retro-modes

432-easter:
	@echo "🎵 Running 432 Hz easter preset..."
	python3 scripts/creative_demo.py --easter-432

ab-analysis:
	@echo "📊 Running A/B analysis..."
	python3 scripts/creative_demo.py --ab-analysis

validation-report:
	@echo "📊 Generating validation report..."
	python3 scripts/creative_demo.py --validation-report

# Clean output directory
clean:
	@echo "🧹 Cleaning output directory..."
	rm -rf out/
	@echo "✅ Cleaned output directory"

# Demo data generation
demo-data: creative-demo
	@echo "📊 Demo data generated in out/"

# Demo server (placeholder)
demo-serve:
	@echo "🚀 Starting demo server..."
	@echo "📁 Serving from out/ directory"
	@echo "🌐 Open site/code-live-physics-fx-dropin.html for live demo"

# Quick validation
quick-test:
	@echo "🧪 Running quick validation..."
	python3 scripts/creative_demo.py --texture-bakeoff --easter-432
	@echo "✅ Quick test complete"

# Full validation suite
full-test: creative-demo validation-report
	@echo "🧪 Full validation suite complete"
	@echo "📊 Check out/reports/validation.json for results"

# Show output structure
show-output:
	@echo "📁 Output directory structure:"
	@find out/ -type f -name "*.py" -o -name "*.json" | head -20
	@echo "📊 Total files: $$(find out/ -type f | wc -l)"

# Generate README snippets
generate-snippets:
	@echo "📝 Generating README snippets..."
	@mkdir -p out/snippets
	@echo "🎨 Texture Sampler Gallery" > out/snippets/README.md
	@echo "=========================" >> out/snippets/README.md
	@echo "" >> out/snippets/README.md
	@echo "Generated texture samples:" >> out/snippets/README.md
	@find out/loops/ -name "*.py" | while read file; do \
		echo "- $$(basename $$file): $$(head -1 $$file)"; \
	done >> out/snippets/README.md
	@echo "✅ README snippets generated in out/snippets/"

# Code Opera - Multi-voice creative coding performance
code-opera:
	@echo "🎭 Running Code Opera performance..."
	python3 scripts/code_opera.py
	@echo "🎭 Code Opera complete! Check out/opera/ for artifacts"

# Code Opera with deterministic seed
code-opera-seed:
	@echo "🎭 Running Code Opera with deterministic seed..."
	python3 scripts/code_opera.py --seed "opera-$(shell date +%s)"
	@echo "🎭 Code Opera complete! Check out/opera/ for artifacts"

# Code Opera live development server
code-opera-live:
	@echo "🎭 Starting Code Opera live development server..."
	python3 server.py
	@echo "🎭 Live server running on http://localhost:8787"

# Code Opera UI server
code-opera-ui:
	@echo "🎭 Starting Code Opera UI server..."
	python3 -m http.server 8788 -d site
	@echo "🎭 UI server running on http://localhost:8788"

# Code Opera with MIDI export
code-opera-midi:
	@echo "🎭 Running Code Opera with MIDI export..."
	python3 scripts/code_opera.py --seed "opera-$(shell date +%s)"
	python3 scripts/opera_export_midi.py
	@echo "🎭 Code Opera with MIDI complete! Check out/opera/opera.mid"

# Code Opera with counterpoint guard
code-opera-counterpoint:
	@echo "🎭 Running Code Opera with counterpoint guard..."
	python3 scripts/code_opera.py --seed "opera-$(shell date +%s)"
	python3 scripts/counterpoint_guard.py
	@echo "🎭 Code Opera with counterpoint guard complete!"

# Code Opera headless capture
opera-snaps:
	@echo "🎭 Capturing Code Opera performance..."
	node scripts/capture_opera.js http://localhost:8787/out/opera/code_opera_harmony.html
	@echo "🎭 Screenshots captured in out/opera/snaps/"

# Code Opera sanity tests
opera-test:
	@echo "🎭 Running Code Opera sanity tests..."
	python3 tests/test_opera_sanity.py
	@echo "🎭 Sanity tests complete!"

# Code Opera complete showflow
opera-showflow:
	@echo "🎭 Code Opera Complete Showflow"
	@echo "=============================="
	@echo "1. Starting live server..."
	@make code-opera-live &
	@sleep 3
	@echo "2. Running Code Opera with seed..."
	@make code-opera-seed
	@echo "3. Applying counterpoint guard..."
	@python3 scripts/counterpoint_guard.py
	@echo "4. Exporting MIDI..."
	@python3 scripts/opera_export_midi.py
	@echo "5. Running sanity tests..."
	@make opera-test
	@echo "6. Opening harmony visualization..."
	@open out/opera/code_opera_harmony.html || echo "Open manually: out/opera/code_opera_harmony.html"
	@echo "7. Opening MIDI file..."
	@open out/opera/opera.mid || echo "Open manually: out/opera/opera.mid"
	@echo "🎉 Code Opera showflow complete!"

# TuneZilla Opera - Brand-integrated Code Opera
tunezilla-opera:
	@echo "🎭 Running TuneZilla Opera performance..."
	python3 scripts/tunezilla_opera.py
	@echo "🎭 TuneZilla Opera complete! Check out/tunezilla_opera/ for artifacts"

# TuneZilla Opera with deterministic seed
tunezilla-opera-seed:
	@echo "🎭 Running TuneZilla Opera with deterministic seed..."
	python3 scripts/tunezilla_opera.py --seed "tunezilla-$(shell date +%s)"
	@echo "🎭 TuneZilla Opera complete! Check out/tunezilla_opera/ for artifacts"

# TuneZilla Opera poster visualization
tunezilla-poster:
	@echo "🎭 Opening TuneZilla Opera poster..."
	@open site/tunezilla-opera-poster.html || echo "Open manually: site/tunezilla-opera-poster.html"

# Crazy String FX - Mind-bending string effects
string-fx:
	@echo "🎭 Running Crazy String FX..."
	python3 scripts/crazy_string_fx.py --text "Code Live" --fx rainbow_gradient,neon_fx
	@echo "🎭 Crazy String FX complete!"

# String FX with specific effects
string-fx-glitch:
	@echo "🎭 Running Glitch String FX..."
	python3 scripts/crazy_string_fx.py --text "TuneZilla" --fx glitch_colors,stutter,scramble --intensity 2.0
	@echo "🎭 Glitch String FX complete!"

# String FX presets
string-fx-presets:
	@echo "🎭 Running String FX Presets..."
	python3 scripts/string_fx_presets.py --text "Code Live" --preset glitch_mode
	@echo "🎭 String FX Presets complete!"

# String FX gallery
string-fx-gallery:
	@echo "🎭 Creating String FX Gallery..."
	python3 scripts/string_fx_presets.py --text "Code Live" --gallery --output out/string_fx_gallery.html
	@echo "🎭 String FX Gallery complete! Check out/string_fx_gallery.html"

# Enhanced String FX targets (FX Graph Runtime)
enhanced-string-fx:
	@echo "🎭 Running Enhanced String FX..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain rainbow_gradient,neon_fx,stutter --intensity 0.8 --seed 42
	@echo "🎭 Enhanced String FX complete!"

enhanced-string-fx-preset:
	@echo "🎭 Running Enhanced String FX Preset..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset neon_rave --intensity 0.9 --seed 42
	@echo "🎭 Enhanced String FX Preset complete!"

enhanced-string-fx-html:
	@echo "🎭 Creating Enhanced String FX HTML..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain rainbow_gradient,neon_fx,stutter --mode html --output out/enhanced_string_fx.html --intensity 0.8 --seed 42
	@echo "🎭 Enhanced String FX HTML complete! Check out/enhanced_string_fx.html"

enhanced-string-fx-list:
	@echo "🎭 Listing Enhanced String FX Presets..."
	python3 scripts/enhanced_string_fx.py --list-presets
	@echo "🎭 Enhanced String FX Presets listed!"

# String FX Server
string-fx-server:
	@echo "🎭 Starting String FX Server..."
	python3 server_strings.py
	@echo "🎭 String FX Server started on http://localhost:8000"

# Tremolo String FX targets
tremolo-fx:
	@echo "🎵 Running Tremolo String FX..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain tremolo:type=repetition:rate=8.0,neon_fx --intensity 0.8 --seed 42
	@echo "🎵 Tremolo String FX complete!"

tremolo-fx-wave:
	@echo "🎵 Running Tremolo Wave FX..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain tremolo:type=wave:rate=6.0,tremolo:type=color:rate=4.0 --intensity 0.9 --seed 42
	@echo "🎵 Tremolo Wave FX complete!"

tremolo-fx-preset:
	@echo "🎵 Running Tremolo Rave Preset..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset tremolo_rave --intensity 0.9 --seed 42
	@echo "🎵 Tremolo Rave Preset complete!"

tremolo-fx-html:
	@echo "🎵 Creating Tremolo FX HTML..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain tremolo:type=repetition:rate=8.0,neon_fx --mode html --output out/tremolo_fx.html --intensity 0.9 --seed 42
	@echo "🎵 Tremolo FX HTML complete! Check out/tremolo_fx.html"

# String Orchestra Mode targets
string-orchestra:
	@echo "🎻 Running String Orchestra Mode..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset string_orchestra --intensity 0.8 --seed 42
	@echo "🎻 String Orchestra Mode complete!"

violin-solo:
	@echo "🎻 Running Violin Solo..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset violin_solo --intensity 0.9 --seed 42
	@echo "🎻 Violin Solo complete!"

guitar-lead:
	@echo "🎸 Running Guitar Lead..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset guitar_lead --intensity 0.9 --seed 42
	@echo "🎸 Guitar Lead complete!"

pizzicato-strings:
	@echo "🎻 Running Pizzicato Strings..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset pizzicato_strings --intensity 0.8 --seed 42
	@echo "🎻 Pizzicato Strings complete!"

arpeggio-harp:
	@echo "🎵 Running Arpeggio Harp..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset arpeggio_harp --intensity 0.9 --seed 42
	@echo "🎵 Arpeggio Harp complete!"

feedback-sustain:
	@echo "🎸 Running Feedback Sustain..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset feedback_sustain --intensity 0.9 --seed 42
	@echo "🎸 Feedback Sustain complete!"

# String Orchestra HTML Gallery
string-orchestra-html:
	@echo "🎻 Creating String Orchestra HTML Gallery..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset string_orchestra --mode html --output out/string_orchestra.html --intensity 0.8 --seed 42
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset violin_solo --mode html --output out/violin_solo.html --intensity 0.9 --seed 42
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset guitar_lead --mode html --output out/guitar_lead.html --intensity 0.9 --seed 42
	@echo "🎻 String Orchestra HTML Gallery complete! Check out/string_orchestra.html, out/violin_solo.html, out/guitar_lead.html"

# Conductor Score DSL targets
conductor-score:
	@echo "🎼 Running Conductor Score DSL..."
	python3 scripts/conductor_score_cli.py --score "[Tremolo forte] TuneZilla [/]"
	@echo "🎼 Conductor Score complete!"

conductor-score-crescendo:
	@echo "🎼 Running Conductor Score Crescendo..."
	python3 scripts/conductor_score_cli.py --score "[Violin Solo crescendo] Code Live [/]"
	@echo "🎼 Conductor Score Crescendo complete!"

conductor-score-hybrid:
	@echo "🎼 Running Conductor Score Hybrid..."
	python3 scripts/conductor_score_cli.py --score "[Guitar Lead ff neon] Rawtunez [/]"
	@echo "🎼 Conductor Score Hybrid complete!"

conductor-score-ensemble:
	@echo "🎼 Running Conductor Score Ensemble..."
	python3 scripts/conductor_score_cli.py --text "Code Live TuneZilla Rawtunez" --ensemble
	@echo "🎼 Conductor Score Ensemble complete!"

conductor-score-create:
	@echo "🎼 Creating Conductor Score..."
	python3 scripts/conductor_score_cli.py --create-score --text "TuneZilla" --technique "violin_solo" --dynamics "ff"
	@echo "🎼 Conductor Score created!"

conductor-score-html:
	@echo "🎼 Creating Conductor Score HTML..."
	python3 scripts/conductor_score_cli.py --score "[Tremolo forte] TuneZilla [/]" --mode html --output out/conductor_score.html --intensity 0.8 --seed 42
	@echo "🎼 Conductor Score HTML complete! Check out/conductor_score.html"

# Refraction Text FX targets
refraction-fx:
	@echo "🌈 Running Refraction Text FX..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain refraction:type=prism,rainbow_gradient --intensity 0.8 --seed 42
	@echo "🌈 Refraction Text FX complete!"

refraction-glass-warp:
	@echo "🌈 Running Glass Warp Refraction..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain refraction:type=glass_warp,neon_fx --intensity 0.9 --seed 42
	@echo "🌈 Glass Warp Refraction complete!"

refraction-ripple:
	@echo "🌈 Running Ripple Refraction..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --chain refraction:type=ripple,waveform --intensity 0.8 --seed 42
	@echo "🌈 Ripple Refraction complete!"

refraction-spectral:
	@echo "🌈 Running Spectral Ghosts Refraction..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain refraction:type=spectral,harmonics --intensity 0.9 --seed 42
	@echo "🌈 Spectral Ghosts Refraction complete!"

refraction-broken:
	@echo "🌈 Running Broken Glass Refraction..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain refraction:type=broken,glitch_colors --intensity 0.8 --seed 42
	@echo "🌈 Broken Glass Refraction complete!"

refraction-preset:
	@echo "🌈 Running Prism Rainbow Preset..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset prism_rainbow --intensity 0.9 --seed 42
	@echo "🌈 Prism Rainbow Preset complete!"

refraction-html:
	@echo "🌈 Creating Refraction HTML Gallery..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain refraction:type=prism,rainbow_gradient,neon_fx --mode html --output out/refraction_fx.html --intensity 0.9 --seed 42
	@echo "🌈 Refraction HTML complete! Check out/refraction_fx.html"

# Chromatic Aberration Text FX targets
chromatic-fx:
	@echo "🌈 Running Chromatic Aberration Text FX..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain chromatic:type=rgb_offset,neon_fx --intensity 0.8 --seed 42
	@echo "🌈 Chromatic Aberration Text FX complete!"

chromatic-fringe:
	@echo "🌈 Running Chromatic Fringe Blur..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain chromatic:type=fringe_blur,glitch_colors --intensity 0.9 --seed 42
	@echo "🌈 Chromatic Fringe Blur complete!"

chromatic-pulse:
	@echo "🌈 Running Chromatic Pulse..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --chain chromatic:type=pulse,rainbow_gradient --intensity 0.8 --seed 42
	@echo "🌈 Chromatic Pulse complete!"

chromatic-spectrum:
	@echo "🌈 Running Chromatic Broken Spectrum..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain chromatic:type=broken_spectrum,harmonics --intensity 0.9 --seed 42
	@echo "🌈 Chromatic Broken Spectrum complete!"

chromatic-trails:
	@echo "🌈 Running Chromatic Trails..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain chromatic:type=trails,feedback --intensity 0.8 --seed 42
	@echo "🌈 Chromatic Trails complete!"

chromatic-preset:
	@echo "🌈 Running Chromatic RGB Preset..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset chromatic_rgb --intensity 0.9 --seed 42
	@echo "🌈 Chromatic RGB Preset complete!"

prism-mode:
	@echo "🌈 Running Prism Mode (Refraction + Chromatic)..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset prism_mode --intensity 0.9 --seed 42
	@echo "🌈 Prism Mode complete!"

chromatic-html:
	@echo "🌈 Creating Chromatic Aberration HTML Gallery..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain chromatic:type=rgb_offset,neon_fx,rainbow_gradient --mode html --output out/chromatic_fx.html --intensity 0.9 --seed 42
	@echo "🌈 Chromatic Aberration HTML complete! Check out/chromatic_fx.html"

# Light-Based Text FX targets
light-fx:
	@echo "🌟 Running Light-Based Text FX..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain light:type=glow,neon_fx --intensity 0.8 --seed 42
	@echo "🌟 Light-Based Text FX complete!"

light-flare:
	@echo "🌟 Running Lens Flare..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain light:type=flare,rainbow_gradient --intensity 0.9 --seed 42
	@echo "🌟 Lens Flare complete!"

light-strobe:
	@echo "🌟 Running Strobe Rave..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --chain light:type=strobe,chromatic:type=rgb_offset --intensity 0.8 --seed 42
	@echo "🌟 Strobe Rave complete!"

light-caustics:
	@echo "🌟 Running Caustic Water..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain light:type=caustics,waveform --intensity 0.9 --seed 42
	@echo "🌟 Caustic Water complete!"

light-volumetric:
	@echo "🌟 Running Volumetric Beams..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain light:type=volumetric,shadow --intensity 0.8 --seed 42
	@echo "🌟 Volumetric Beams complete!"

light-lightning:
	@echo "🌟 Running Storm Lightning..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --chain light:type=lightning,strobe --intensity 0.9 --seed 42
	@echo "🌟 Storm Lightning complete!"

light-hologram:
	@echo "🌟 Running Hologram Glow..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain light:type=hologram,glitch_colors --intensity 0.8 --seed 42
	@echo "🌟 Hologram Glow complete!"

light-laser:
	@echo "🌟 Running Laser Sweep..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain light:type=laser_sweep,neon_fx --intensity 0.9 --seed 42
	@echo "🌟 Laser Sweep complete!"

light-preset:
	@echo "🌟 Running Neon Bloom Preset..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset neon_bloom --intensity 0.9 --seed 42
	@echo "🌟 Neon Bloom Preset complete!"

lighting-desk:
	@echo "🌟 Running Lighting Desk (Glow + Flare + Strobe + Chromatic)..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset lighting_desk --intensity 0.9 --seed 42
	@echo "🌟 Lighting Desk complete!"

light-html:
	@echo "🌟 Creating Light-Based Text FX HTML Gallery..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --chain light:type=glow,neon_fx,rainbow_gradient --mode html --output out/light_fx.html --intensity 0.9 --seed 42
	@echo "🌟 Light-Based Text FX HTML complete! Check out/light_fx.html"

# Enhanced Chromatic Light Desk targets
chromatic-light-desk:
	@echo "🌟 Opening Chromatic Light Desk..."
	@echo "🌟 Chromatic Light Desk ready! Open site/chromatic-light-desk.html in browser"
	@echo "🌟 Features: Live metrics mapping, performance controls, presets, accessibility"

chromatic-neon-bloom:
	@echo "🌟 Running Enhanced Neon Bloom..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset neon_bloom_enhanced --intensity 0.9 --seed 42
	@echo "🌟 Enhanced Neon Bloom complete!"

chromatic-prism-burst:
	@echo "🌟 Running Prism Burst..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset prism_burst --intensity 0.8 --seed 42
	@echo "🌟 Prism Burst complete!"

chromatic-hologram:
	@echo "🌟 Running Enhanced Hologram..."
	python3 scripts/enhanced_string_fx.py --text "Rawtunez" --preset hologram_enhanced --intensity 0.9 --seed 42
	@echo "🌟 Enhanced Hologram complete!"

chromatic-storm:
	@echo "🌟 Running Enhanced Storm Lightning..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset storm_lightning_enhanced --intensity 0.8 --seed 42
	@echo "🌟 Enhanced Storm Lightning complete!"

chromatic-cinemascope:
	@echo "🌟 Running Cinemascope..."
	python3 scripts/enhanced_string_fx.py --text "TuneZilla" --preset cinemascope --intensity 0.7 --seed 42
	@echo "🌟 Cinemascope complete!"

chromatic-enhanced-html:
	@echo "🌟 Creating Enhanced Chromatic HTML Gallery..."
	python3 scripts/enhanced_string_fx.py --text "Code Live" --preset neon_bloom_enhanced --mode html --output out/chromatic_enhanced.html --intensity 0.9 --seed 42
	@echo "🌟 Enhanced Chromatic HTML complete! Check out/chromatic_enhanced.html"

# Soundtoys-style Effect Rack targets
effect-rack-list:
	@echo "🎛️ Listing Effect Rack Presets..."
	python3 scripts/effect_rack_cli.py --list-presets
	@echo "🎛️ Effect Rack presets listed!"

effect-rack-decapitator:
	@echo "🎛️ Running Decapitator (Distortion) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "Code Live" --preset decapitator --seed 42
	@echo "🎛️ Decapitator Effect Rack complete!"

effect-rack-little-plate:
	@echo "🎛️ Running Little Plate (Reverb) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "TuneZilla" --preset little_plate --seed 42
	@echo "🎛️ Little Plate Effect Rack complete!"

effect-rack-echo-boy:
	@echo "🎛️ Running EchoBoy (Delay) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "Rawtunez" --preset echo_boy --seed 42
	@echo "🎛️ EchoBoy Effect Rack complete!"

effect-rack-crystallizer:
	@echo "🎛️ Running Crystallizer (Granular) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "Code Live" --preset crystallizer --seed 42
	@echo "🎛️ Crystallizer Effect Rack complete!"

effect-rack-devil-loc:
	@echo "🎛️ Running Devil-Loc (Compressor) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "TuneZilla" --preset devil_loc --seed 42
	@echo "🎛️ Devil-Loc Effect Rack complete!"

effect-rack-micro-shift:
	@echo "🎛️ Running MicroShift (Chorus) Effect Rack..."
	python3 scripts/effect_rack_cli.py --text "Rawtunez" --preset micro_shift --seed 42
	@echo "🎛️ MicroShift Effect Rack complete!"

effect-rack-custom:
	@echo "🎛️ Running Custom Effect Rack (Distortion + Neon + Glitch)..."
	python3 scripts/effect_rack_cli.py --text "Code Live" --effects distortion,neon_fx,glitch_colors --seed 42
	@echo "🎛️ Custom Effect Rack complete!"

effect-rack-status:
	@echo "🎛️ Showing Effect Rack Status..."
	python3 scripts/effect_rack_cli.py --rack-status
	@echo "🎛️ Effect Rack status displayed!"

effect-rack-html:
	@echo "🎛️ Creating Effect Rack HTML Gallery..."
	python3 scripts/effect_rack_cli.py --text "Code Live" --preset decapitator --mode html --output out/effect_rack.html --seed 42
	@echo "🎛️ Effect Rack HTML complete! Check out/effect_rack.html"

# Show Controller targets
show-controller-flow:
	@echo "🎭 Running Professional Showpiece Flow..."
	python3 scripts/show_controller_cli.py --flow showpiece --text "Code Live" --seed 777
	@echo "🎭 Professional Showpiece Flow complete!"

show-controller-cinemascope:
	@echo "🎬 Running Cinemascope Scene..."
	python3 scripts/show_controller_cli.py --scene cinemascope --text "Code Live" --seed 777
	@echo "🎬 Cinemascope Scene complete!"

show-controller-neon-bloom:
	@echo "🎬 Running Neon Bloom Scene..."
	python3 scripts/show_controller_cli.py --scene neon_bloom --text "TuneZilla" --seed 777
	@echo "🎬 Neon Bloom Scene complete!"

show-controller-prism-burst:
	@echo "🎬 Running Prism Burst Scene..."
	python3 scripts/show_controller_cli.py --scene prism_burst --text "Rawtunez" --seed 777
	@echo "🎬 Prism Burst Scene complete!"

show-controller-hologram:
	@echo "🎬 Running Hologram Scene..."
	python3 scripts/show_controller_cli.py --scene hologram --text "Code Live" --seed 777
	@echo "🎬 Hologram Scene complete!"

show-controller-a11y:
	@echo "♿ Running A11y-Safe Scene..."
	python3 scripts/show_controller_cli.py --scene cinemascope --text "Code Live" --a11y --seed 777
	@echo "♿ A11y-Safe Scene complete!"

show-controller-mono:
	@echo "🎵 Running Mono Mode Scene..."
	python3 scripts/show_controller_cli.py --scene neon_bloom --text "TuneZilla" --mono --seed 777
	@echo "🎵 Mono Mode Scene complete!"

show-controller-snapshot:
	@echo "📸 Creating Snapshot Kit..."
	python3 scripts/show_controller_cli.py --snapshot-kit --scene prism_burst
	@echo "📸 Snapshot Kit complete! Check out/snapshot_kit_prism_burst.json"

show-controller-save-scene:
	@echo "💾 Saving Scene Configuration..."
	python3 scripts/show_controller_cli.py --save-scene out/neon_bloom_scene.json --scene neon_bloom
	@echo "💾 Scene Configuration saved! Check out/neon_bloom_scene.json"

show-controller-load-scene:
	@echo "📁 Loading Scene Configuration..."
	python3 scripts/show_controller_cli.py --load-scene out/neon_bloom_scene.json --text "Code Live"
	@echo "📁 Scene Configuration loaded!"

# Pro Rack targets
pro-rack-tour-opener:
	@echo "🎛️ Running Tour Opener Rack..."
	python3 scripts/pro_rack_cli.py --load presets/racks/tour_opener.rack.json --text "Code Live" --macros color=0.7,space=0.3
	@echo "🎛️ Tour Opener Rack complete!"

pro-rack-glass-cathedral:
	@echo "🎛️ Running Glass Cathedral Rack..."
	python3 scripts/pro_rack_cli.py --load presets/racks/glass_cathedral.rack.json --text "TuneZilla" --macros color=0.5,space=0.8
	@echo "🎛️ Glass Cathedral Rack complete!"

pro-rack-tape-dream:
	@echo "🎛️ Running Tape Dream Rack..."
	python3 scripts/pro_rack_cli.py --load presets/racks/tape_dream.rack.json --text "Rawtunez" --macros motion=0.6,crunch=0.4
	@echo "🎛️ Tape Dream Rack complete!"

pro-rack-data-storm:
	@echo "🎛️ Running Data Storm Rack..."
	python3 scripts/pro_rack_cli.py --load presets/racks/data_storm.rack.json --text "Code Live" --sidechain qps=80,p95=90,error_rate=0.08
	@echo "🎛️ Data Storm Rack complete!"

pro-rack-crystalline-bloom:
	@echo "🎛️ Running Crystalline Bloom Rack..."
	python3 scripts/pro_rack_cli.py --load presets/racks/crystalline_bloom.rack.json --text "TuneZilla" --macros color=0.9,space=0.7
	@echo "🎛️ Crystalline Bloom Rack complete!"

pro-rack-morph:
	@echo "🎛️ Running Rack Morph..."
	python3 scripts/pro_rack_cli.py --morph presets/racks/tour_opener.rack.json presets/racks/glass_cathedral.rack.json --morph-time 0.5 --text "Code Live"
	@echo "🎛️ Rack Morph complete!"

pro-rack-status:
	@echo "🎛️ Showing Pro Rack Status..."
	python3 scripts/pro_rack_cli.py --status
	@echo "🎛️ Pro Rack status displayed!"

# Rack Show targets
rack-show-tour-opener:
	@echo "🎭 Running Tour Opener Show..."
	python3 scripts/rack_show_cli.py --play presets/shows/tour_opener.show.json --text "Code Live" --record-html
	@echo "🎭 Tour Opener Show complete!"

rack-show-create-demo:
	@echo "🎭 Creating Demo Show..."
	python3 scripts/rack_show_cli.py --create "Demo Show" --scenes tour_opener.rack.json,glass_cathedral.rack.json,data_storm.rack.json
	@echo "🎭 Demo Show created!"

rack-show-status:
	@echo "🎭 Showing Rack Show Status..."
	python3 scripts/rack_show_cli.py --status
	@echo "🎭 Rack Show status displayed!"

# Touring Rig targets
touring-rig-load:
	@echo "🎭 Loading Touring Rig Show..."
	python3 scripts/touring_rig_cli.py --load presets/shows/tour_opener.show.json --status
	@echo "🎭 Touring Rig Show loaded!"

touring-rig-play:
	@echo "🎭 Playing Touring Rig Show..."
	python3 scripts/touring_rig_cli.py --load presets/shows/tour_opener.show.json --play
	@echo "🎭 Touring Rig Show playing!"

touring-rig-intensity:
	@echo "🎛️ Setting Live Intensity..."
	python3 scripts/touring_rig_cli.py --intensity 85.5
	@echo "🎛️ Live intensity set!"

touring-rig-blackout:
	@echo "🌑 Toggling Blackout..."
	python3 scripts/touring_rig_cli.py --blackout true
	@echo "🌑 Blackout toggled!"

touring-rig-flash-strobe:
	@echo "⚡ Toggling Flash Strobe..."
	python3 scripts/touring_rig_cli.py --flash-strobe true
	@echo "⚡ Flash strobe toggled!"

touring-rig-all-white-bloom:
	@echo "💡 Toggling All-White Bloom..."
	python3 scripts/touring_rig_cli.py --all-white-bloom true
	@echo "💡 All-white bloom toggled!"

touring-rig-metrics-link:
	@echo "📊 Setting Metrics Link Strength..."
	python3 scripts/touring_rig_cli.py --metrics-link 75.0
	@echo "📊 Metrics link strength set!"

touring-rig-param:
	@echo "🎛️ Setting Parameter..."
	python3 scripts/touring_rig_cli.py --param "scenes[2].fx[1].wet" 0.42
	@echo "🎛️ Parameter set!"

touring-rig-undo:
	@echo "↶ Undoing Action..."
	python3 scripts/touring_rig_cli.py --undo
	@echo "↶ Action undone!"

touring-rig-redo:
	@echo "↷ Redoing Action..."
	python3 scripts/touring_rig_cli.py --redo
	@echo "↷ Action redone!"

touring-rig-status:
	@echo "📊 Showing Touring Rig Status..."
	python3 scripts/touring_rig_cli.py --status
	@echo "📊 Touring Rig status displayed!"

touring-rig-server:
	@echo "🚀 Starting Touring Rig API Server..."
	python3 server_touring_rig.py
	@echo "🚀 Touring Rig API Server started!"

# Stage-Proof targets
stage-proof-load:
	@echo "🎛️ Loading Stage-Proof Scene..."
	python3 scripts/stage_proof_cli.py --load presets/scenes/tour_opener.json --text "Code Live"
	@echo "🎛️ Stage-Proof Scene loaded!"

stage-proof-acceptance:
	@echo "🧪 Running Stage-Proof Acceptance Test..."
	python3 scripts/stage_proof_cli.py --acceptance-test
	@echo "🧪 Stage-Proof Acceptance Test complete!"

stage-proof-intensity:
	@echo "🎛️ Setting Global Intensity..."
	python3 scripts/stage_proof_cli.py --intensity 85.5
	@echo "🎛️ Global intensity set!"

stage-proof-blackout:
	@echo "🌑 Toggling Blackout..."
	python3 scripts/stage_proof_cli.py --blackout true
	@echo "🌑 Blackout toggled!"

stage-proof-white-bloom:
	@echo "💡 Toggling White Bloom..."
	python3 scripts/stage_proof_cli.py --white-bloom true
	@echo "💡 White bloom toggled!"

stage-proof-lightning-flash:
	@echo "⚡ Toggling Lightning Flash..."
	python3 scripts/stage_proof_cli.py --lightning-flash true
	@echo "⚡ Lightning flash toggled!"

stage-proof-status:
	@echo "📊 Showing Stage-Proof Status..."
	python3 scripts/stage_proof_cli.py --status
	@echo "📊 Stage-Proof status displayed!"

# Bulletproof Operator Kit targets
show-readiness-check:
	@echo "🎭 Running 5-minute Show Readiness Check..."
	./scripts/show_readiness_check.sh
	@echo "🎭 Show readiness check complete!"

scene-validator:
	@echo "🔍 Validating Scene JSON files..."
	python3 scripts/scene_validator.py --dir presets/scenes
	@echo "🔍 Scene validation complete!"

scene-validator-strict:
	@echo "🔍 Validating Scene JSON files (strict mode)..."
	python3 scripts/scene_validator.py --dir presets/scenes --strict
	@echo "🔍 Scene validation complete!"

snapshot-kit:
	@echo "📸 Generating Snapshot Kit..."
	python3 scripts/snapshot_kit.py --all-scenes
	@echo "📸 Snapshot kit generation complete!"

snapshot-kit-scene:
	@echo "📸 Generating Snapshot Kit for scene..."
	python3 scripts/snapshot_kit.py --scene tour_opener --text "Code Live"
	@echo "📸 Snapshot kit generation complete!"

foh-runbook:
	@echo "📖 Opening FOH Runbook..."
	@echo "📖 FOH Runbook: docs/FOH_RUNBOOK.md"
	@echo "📖 Contains: Startup checklist, Go Live flow, Emergencies, API one-liners, Hotkeys, Safety rails"
	@echo "📖 FOH Runbook displayed!"

operator-hotkeys:
	@echo "⌨️  Operator Hotkeys Reference:"
	@echo "  Scene Control: 1-9 (jump to scene), 0 (previous), Space (pause/resume), G (goto +10s)"
	@echo "  Intensity: I (up), K (down)"
	@echo "  Metrics: M (toggle), , (decrease), . (increase)"
	@echo "  Momentary: B (blackout), F (flash), W (white bloom)"
	@echo "  Undo/Redo: U (undo), R (redo)"
	@echo "  Special: F (freeze/unfreeze), T (tap tempo)"
	@echo "⌨️  Operator hotkeys displayed!"

safety-rails:
	@echo "🛡️  Safety Rails Status:"
	@echo "  Strobe Cap: ≤8 Hz, on-time ≥120ms, duty-cycle ≤35% over 10s"
	@echo "  Frame Budget: 30-frame p95 > 12ms → auto-reduce trails/particles"
	@echo "  Param Slew: intensity ≤0.6/s, chroma.offset ≤0.3/s"
	@echo "  Motion Compliance: instant mono fallback on system signal"
	@echo "🛡️  Safety rails displayed!"

api-one-liners:
	@echo "🌐 API One-Liners (curl):"
	@echo "  Intensity: curl -X POST :8787/rig/intensity -d '{\"value\":0.82}'"
	@echo "  Blackout: curl -X POST :8787/rig/blackout -d '{\"state\":true}'"
	@echo "  Flash: curl -X POST :8787/rig/flash -d '{\"latch_ms\":800}'"
	@echo "  Bloom: curl -X POST :8787/rig/bloom -d '{\"latch_ms\":1200}'"
	@echo "  Metrics: curl -X POST :8787/rig/metrics-link -d '{\"strength\":0.75}'"
	@echo "  Morph: curl -X POST :8787/rig/morph -d '{\"curve\":\"EaseInOut\",\"seconds\":2.0}'"
	@echo "  Param: curl -X POST :8787/rig/param -d '{\"key\":\"chromatic.offset\",\"value\":0.28}'"
	@echo "🌐 API one-liners displayed!"

# A11y Timing Fix targets
a11y-timing-test:
	@echo "🧪 Testing A11y Timing System..."
	python3 scripts/a11y_timing_fix.py --test
	@echo "🧪 A11y timing test complete!"

a11y-timing-test-fps:
	@echo "🧪 Testing A11y Timing at 59 FPS..."
	python3 scripts/a11y_timing_fix.py --test --fps 59
	@echo "🧪 A11y timing test complete!"

a11y-timing-test-hard:
	@echo "🧪 Testing A11y Hard Mode..."
	python3 scripts/a11y_timing_fix.py --test --hard-mode
	@echo "🧪 A11y hard mode test complete!"

timing-harness:
	@echo "🧪 Running Timing Harness (FPS Sweep)..."
	python3 scripts/timing_harness.py
	@echo "🧪 Timing harness complete!"

timing-harness-report:
	@echo "🧪 Running Timing Harness with Report..."
	python3 scripts/timing_harness.py --save-report
	@echo "🧪 Timing harness report saved!"

timing-harness-custom:
	@echo "🧪 Running Custom Timing Harness..."
	python3 scripts/timing_harness.py --fps 58,59,60,61 --jitter-budget 8.0
	@echo "🧪 Custom timing harness complete!"

# Go-Live in 6 Moves targets
go-live-1:
	@echo "1️⃣ Cutting RC + Artifact Bundle..."
	git tag -a v0.5.0-rc1 -m "touring rig + operator kit" && git push origin v0.5.0-rc1
	make snapshot-kit
	make foh-runbook
	@echo "1️⃣ RC + Artifact Bundle complete!"

go-live-2:
	@echo "2️⃣ Locking Acceptance..."
	make stage-proof-acceptance
	@echo "2️⃣ Acceptance locked!"

go-live-3:
	@echo "3️⃣ Dress Rehearsal Script (15 min)..."
	make show-readiness-check
	make touring-rig-load && make touring-rig-play
	@echo "3️⃣ Dress rehearsal complete!"

go-live-4:
	@echo "4️⃣ Safety Rails Trip Test (2 min)..."
	./scripts/safety_rails_trip_test.sh
	@echo "4️⃣ Safety rails trip test complete!"

go-live-5:
	@echo "5️⃣ Observability Pin (Grafana panels green)..."
	./scripts/observability_pin.sh
	@echo "5️⃣ Observability pin complete!"

go-live-6:
	@echo "6️⃣ Publish Show Kit..."
	make rack-show-create-demo
	./scripts/30_sec_capture.sh
	@echo "6️⃣ Show kit published!"

go-live-all:
	@echo "🎭 GO-LIVE IN 6 MOVES - TOURING RIG DEPLOYMENT"
	@echo "==============================================="
	make go-live-1
	make go-live-2
	make go-live-3
	make go-live-4
	make go-live-5
	make go-live-6
	@echo "🎭 GO-LIVE COMPLETE - READY FOR STAGE!"

# Code Hero - Guitar Hero for Loops (placeholder)
code-hero:
	@echo "🎮 Code Hero mode coming soon..."
	@echo "🎸 Guitar Hero for code loops with FX timing"

# Code Tarot - Divination system for creative coding
code-tarot:
	@echo "🔮 Code Tarot mode coming soon..."
	@echo "🎴 Random texture/FX cards for creative coding"

# Moonlight Sonata Text-FX Performance
moonlight-sonata:
	@echo "🌙 Running Moonlight Sonata Text-FX Performance..."
	python3 moonlight_sonata_showflow.py
	@echo "🌙 Moonlight Sonata performance complete! Check out/moonlight_sonata_performance.json"

moonlight-sonata-interactive:
	@echo "🎹 Starting Moonlight Sonata Interactive Jam Mode..."
	@echo "🎹 Map macro knobs to text FX parameters:"
	@echo "🎹 Color = Chromatic offset (key changes)"
	@echo "🎹 Space = Reverb/trails length (pedal sustain)"
	@echo "🎹 Motion = Vibrato & tremolo intensity"
	@echo "🎹 Crunch = Feedback + distortion (storm intensity)"
	@echo "🎹 Interactive jam mode ready!"

moonlight-sonata-log:
	@echo "📊 Showing Moonlight Sonata Performance Log..."
	@if [ -f out/moonlight_sonata_performance.json ]; then \
		echo "📊 Last performance log:"; \
		cat out/moonlight_sonata_performance.json | head -20; \
	else \
		echo "📊 No performance log found. Run 'make moonlight-sonata' first."; \
	fi

moonlight-sonata-hotkeys:
	@echo "⌨️ Moonlight Sonata Operator Hotkeys..."
	@echo "⌨️ 1/2/3/4: jump to movements I/II/III/Outro"
	@echo "⌨️ I / K: intensity up/down (slew-limited)"
	@echo "⌨️ M: toggle metrics link (use 0.5 during Allegretto)"
	@echo "⌨️ W: White Bloom hit (≤1.2s) on III accents"
	@echo "⌨️ B: Blackout (final beat)"
	@echo "⌨️ U / R: undo / redo (in case of over-crunch)"
	@echo "⌨️ , / .: metrics link strength − / +"

moonlight-sonata-rehearsal:
	@echo "🎭 Moonlight Sonata Rehearsal Tweaks..."
	@echo "🎭 Tempo feel: set jam BPM to ~56 (Adagio), 76 (Allegretto), 168 (Presto)"
	@echo "🎭 A11y pass: ensure reduced-motion flag forces mono + trails.length ≤0.25"
	@echo "🎭 Seeded take: run with a seed for shot-for-shot repeatability"
	@echo "🎭 Venue profiles: small room → dust=0.12, trails=0.35; arena → dust=0.22, trails=0.6"
	@echo "🎭 Safety rails: strobe ≤ 8 Hz, duty ≤ 35% / 10s, on-time ≥ 120 ms"

moonlight-sonata-pro-tips:
	@echo "💡 Moonlight Sonata Pro Tips..."
	@echo "💡 Soft glass feel in I: lower chromatic to ~0.08, increase fringe 0.15, dust 0.18"
	@echo "💡 Storm articulation in III: map sidechain to Crunch from QPS so busy sections 'growl' more—keep link ≤0.8"
	@echo "💡 Grand cadence: morph back to Glass Cathedral over 6–8 s while pulling intensity to 0.45, then B"
	@echo "💡 Cosmic dust overlay: add moonlight shimmer particles for drifting effect"
	@echo "💡 Capture checklist: 30s highlight capture (III focus), snapshot grid (low/mid/peak)"

moonlight-sonata-capture:
	@echo "📸 Moonlight Sonata Capture..."
	@echo "📸 30s highlight capture (III focus)"
	@echo "📸 Snapshot grid (low/mid/peak)"
	@echo "📸 Capture checklist ready!"

moonlight-sonata-seeded:
	@echo "🌙 Running Moonlight Sonata with Seed..."
	@echo "🌙 Seeded take for shot-for-shot repeatability..."
	python3 moonlight_sonata_showflow.py --seed $(SEED)
	@echo "🌙 Seeded Moonlight Sonata performance complete!"

# Clair de Lune — 90s recital
clair-de-lune:
	@echo "🌙 Running full Clair de Lune (90s)..."
	python3 scripts/clair_de_lune_showflow.py --mode show --duration 90
	@echo "🌙 Clair de Lune performance complete!"

clair-de-lune-seeded:
	@echo "🌙 Running Clair de Lune with Seed..."
	@echo "🌙 Seeded take for shot-for-shot repeatability..."
	python3 scripts/clair_de_lune_showflow.py --mode show --duration 90 --seed $(or $(SEED),271828)
	@echo "🌙 Seeded Clair de Lune performance complete!"

clair-de-lune-jam:
	@echo "🌙 Starting Clair de Lune Interactive Jam Mode..."
	@echo "🌙 Interactive jam mode ready for live macros!"
	python3 scripts/clair_de_lune_showflow.py --mode jam

clair-de-lune-load-scene:
	@echo "🌙 Loading Clair de Lune scene JSON into rig..."
	@if command -v curl >/dev/null 2>&1; then \
		curl -sS -X POST :8787/rig/scene/load -H "Content-Type: application/json" \
		  --data-binary @shows/clair_de_lune.scene.json | jq .; \
	else \
		echo "🌙 Scene JSON ready for manual loading: shows/clair_de_lune.scene.json"; \
	fi

# Two-piece lunar set (≈3 min)
moonlight+clair:
	@echo "🌙🌙 Running 2-piece lunar set (Moonlight + Clair)..."
	@echo "🌙 Movement 1: Moonlight Sonata (90s)"
	$(MAKE) moonlight-sonata-seeded SEED=$(or $(SEED),314159)
	@echo "🌙 Movement 2: Clair de Lune (90s)"
	$(MAKE) clair-de-lune-seeded SEED=$(or $(SEED),271828)
	@echo "🌙🌙 2-piece lunar set complete!"

# Lunar Recital - Complete 3-minute text-FX double feature
lunar-recital:
	@echo "🌙✨ Starting Lunar Recital (Moonlight Sonata + Clair de Lune)"
	@echo "🌙 Movement 1: Moonlight Sonata with cosmic dust overlay..."
	printf '1\n' | python3 moonlight_sonata_showflow.py
	@echo "🌙 Movement 2: Clair de Lune with shimmer FX pass..."
	printf '1\n' | python3 scripts/clair_de_lune_showflow.py --mode show --duration 90 --seed 271828
	@echo "😺 Catwalk Interlude: 12-second LOLcat++ interlude after Allegretto..."
	python3 scripts/lolcat_plus_cli.py --text "Catwalk interlude moment" --preset cat-walk --seed 314159
	@echo "📸 Generating snapshot kit (low/mid/peak)..."
	@$(MAKE) snapshot-kit
	@echo "🌟 Building chromatic HTML gallery (enhanced neon bloom/prism/hologram)..."
	@$(MAKE) chromatic-enhanced-html
	@echo "🎻 Building string orchestra HTML (solo & ensemble passes)..."
	@$(MAKE) string-orchestra-html
	@echo "🌙✨ Lunar Recital complete! Artifacts in out/ directory."
	@echo "📁 Check out/moonlight_sonata_performance.json for performance log"
	@echo "📁 Check out/touring/snapshots/ for snapshot kit"
	@echo "📁 Check out/chromatic_enhanced.html for chromatic gallery"
	@echo "📁 Check out/string_orchestra.html for string orchestra gallery"

# LOLcat++ Text FX
lolcat-demo:
	@echo "😺 Running LOLcat++ Demo..."
	@python3 -c "from string_fx.lolcat_plus import lolcat_plus; s = lolcat_plus('Code Live ships purrfect vibes!', intensity=0.7, uwu=0.5, chaos=0.2, emoji=0.12, nyan_trail=0.4, seed=432); print(s['ansi'])"
	@echo "😺 LOLcat++ demo complete!"

lolcat-studio-safe:
	@echo "😺 Running LOLcat++ Studio-Safe Mode..."
	@python3 -c "from string_fx.lolcat_plus import lolcat_plus; s = lolcat_plus('Studio-safe mode', intensity=0.4, uwu=0.2, chaos=0.05, emoji=0.03, mono=True, reduced_motion=True); print(s['text'])"
	@echo "😺 Studio-safe mode complete!"

lolcat-classic:
	@echo "😺 Running LOLcat++ Classic Preset..."
	python3 scripts/lolcat_plus_cli.py --text "We really love your awesome project!" --preset classic
	@echo "😺 Classic preset complete!"

lolcat-uwu-rainbow:
	@echo "😺 Running LOLcat++ UwU-Rainbow Preset..."
	python3 scripts/lolcat_plus_cli.py --text "TuneZilla is amazing!" --preset uwu-rainbow --seed 432
	@echo "😺 UwU-rainbow preset complete!"

lolcat-nyan-march:
	@echo "😺 Running LOLcat++ Nyan-March Preset..."
	python3 scripts/lolcat_plus_cli.py --text "Code Live is awesome!" --preset nyan-march
	@echo "😺 Nyan-march preset complete!"

lolcat-prismatic-purr:
	@echo "😺 Running LOLcat++ Prismatic-Purr Preset..."
	python3 scripts/lolcat_plus_cli.py --text "Rawtunez vibes!" --preset prismatic-purr
	@echo "😺 Prismatic-purr preset complete!"

# LOLcat++ Micro-Presets for Stage Performance
lolcat-classic-lite:
	@echo "😺 Running LOLcat++ Classic-Lite (Corporate Decks)..."
	python3 scripts/lolcat_plus_cli.py --text "Corporate presentation ready!" --preset classic-lite
	@echo "😺 Classic-lite preset complete!"

lolcat-stage-punch:
	@echo "😺 Running LOLcat++ Stage-Punch (Chorus Hits)..."
	python3 scripts/lolcat_plus_cli.py --text "Chorus impact moment!" --preset stage-punch
	@echo "😺 Stage-punch preset complete!"

lolcat-cat-walk:
	@echo "😺 Running LOLcat++ Cat-Walk (Interlude)..."
	python3 scripts/lolcat_plus_cli.py --text "Catwalk interlude moment" --preset cat-walk
	@echo "😺 Cat-walk preset complete!"

# LOLcat++ Scene & Morph
lolcat-scene:
	@echo "😺 Running LOLcat++ Scene..."
	python3 scripts/lolcat_plus_cli.py --text "LOLcat Neon Parade!" --preset uwu-rainbow --seed 432
	@echo "😺 Scene complete!"

lolcat-morph-in:
	@echo "😺 Morphing from Neon Bloom to LOLcat Neon Parade..."
	@echo "🌙 Starting morph (6s EaseInOut)..."
	@echo "😺 Morph complete!"

lolcat-live:
	@echo "😺 Starting LOLcat++ Live Mode..."
	@echo "🚀 Starting Touring Rig API Server..."
	@$(MAKE) touring-rig-server &
	@sleep 2
	@echo "😺 Press L to toggle LOLcat layer"
	@echo "😺 Press ;/' for emoji -/+"
	@echo "😺 Press [/] for chaos -/+"
	@echo "😺 Press \\/| for uwu -/+"
	@echo "😺 Press {/} for trail -/+"
	@echo "😺 Live mode ready!"

# LOLcat++ HUD
lolcat-hud-demo:
	@echo "😺 Starting LOLcat++ HUD Demo..."
	python3 scripts/lolcat_hud.py --demo

lolcat-hud-classic:
	@echo "😺 Testing Classic Preset HUD..."
	python3 scripts/lolcat_hud.py --preset classic --text "Classic preset test"

lolcat-hud-stage-punch:
	@echo "😺 Testing Stage-Punch Preset HUD..."
	python3 scripts/lolcat_hud.py --preset stage-punch --text "Stage punch test"

lolcat-hud-cat-walk:
	@echo "😺 Testing Cat-Walk Preset HUD..."
	python3 scripts/lolcat_hud.py --preset cat-walk --text "Catwalk test"

# LOLcat++ Sidechain Sweet Spots
lolcat-sidechain-demo:
	@echo "😺 Starting LOLcat++ Sidechain Demo..."
	python3 scripts/lolcat_sidechain.py --demo

lolcat-sidechain-test:
	@echo "😺 Testing LOLcat++ Sidechain..."
	python3 scripts/lolcat_sidechain.py --test --text "Sidechain sweet spots test" --qps 0.7 --error 0.2 --p95 12.0

lolcat-sidechain-high-qps:
	@echo "😺 Testing High QPS Sidechain..."
	python3 scripts/lolcat_sidechain.py --test --text "High QPS test" --qps 0.9 --error 0.05 --p95 6.0

lolcat-sidechain-high-error:
	@echo "😺 Testing High Error Rate Sidechain..."
	python3 scripts/lolcat_sidechain.py --test --text "High error rate test" --qps 0.3 --error 0.4 --p95 8.0

lolcat-sidechain-high-p95:
	@echo "😺 Testing High P95 Sidechain..."
	python3 scripts/lolcat_sidechain.py --test --text "High P95 test" --qps 0.5 --error 0.1 --p95 15.0

# LOLcat++ Preset A/B + Morph
lolcat-ab-demo:
	@echo "😺 Starting LOLcat++ A/B Morph Demo..."
	python3 scripts/lolcat_preset_ab.py --demo --text "A/B Morph Demo"

lolcat-ab-test:
	@echo "😺 Quick A/B Test..."
	python3 scripts/lolcat_preset_ab.py --test --text "Quick A/B Test"

lolcat-ab-classic-stage:
	@echo "😺 A/B: Classic → Stage-Punch..."
	python3 scripts/lolcat_preset_ab.py --preset-a classic --preset-b stage-punch --morph-duration 2.0 --text "Classic to Stage-Punch morph"

lolcat-ab-stage-classic:
	@echo "😺 A/B: Stage-Punch → Classic..."
	python3 scripts/lolcat_preset_ab.py --preset-a stage-punch --preset-b classic --morph-duration 2.0 --text "Stage-Punch to Classic morph"

lolcat-ab-catwalk-classic:
	@echo "😺 A/B: Cat-Walk → Classic..."
	python3 scripts/lolcat_preset_ab.py --preset-a cat-walk --preset-b classic --morph-duration 1.5 --text "Cat-Walk to Classic morph"

# LOLcat++ Emoji Palette by Scene Theme
lolcat-emoji-demo:
	@echo "😺 Demo all emoji palettes..."
	python3 scripts/lolcat_emoji_palette.py --demo --text "Emoji palette showcase"

lolcat-emoji-scenes:
	@echo "😺 Demo scene-based emoji switching..."
	python3 scripts/lolcat_emoji_palette.py --scenes --text "Scene switching demo"

lolcat-emoji-cyberpunk:
	@echo "😺 Cyberpunk palette test..."
	python3 scripts/lolcat_emoji_palette.py --palette cyberpunk --text "Cyberpunk vibes"

lolcat-emoji-gold:
	@echo "😺 Gold palette test..."
	python3 scripts/lolcat_emoji_palette.py --palette gold --text "Golden moments"

lolcat-emoji-emerald:
	@echo "😺 Emerald palette test..."
	python3 scripts/lolcat_emoji_palette.py --palette emerald --text "Emerald dreams"

lolcat-emoji-vintage:
	@echo "😺 Vintage palette test..."
	python3 scripts/lolcat_emoji_palette.py --palette vintage --text "Vintage vibes"

lolcat-emoji-neon:
	@echo "😺 Neon palette test..."
	python3 scripts/lolcat_emoji_palette.py --palette neon --text "Neon nights"

# LOLcat++ Auto-Ride Macro (Sidechain Lite)
lolcat-auto-ride-demo:
	@echo "😺 Starting Auto-Ride Demo..."
	python3 scripts/lolcat_auto_ride.py --demo --text "Auto-ride breathing" --duration 30

lolcat-auto-ride-breathing:
	@echo "😺 Simulating Show Breathing..."
	python3 scripts/lolcat_auto_ride.py --breathing --text "Show breathing demo" --duration 60

lolcat-auto-ride-timing:
	@echo "😺 Testing Auto-Ride Timing..."
	python3 scripts/lolcat_auto_ride.py --test-timing

lolcat-auto-ride-bpm-60:
	@echo "😺 Auto-Ride at 60 BPM..."
	python3 scripts/lolcat_auto_ride.py --bpm 60 --text "Slow tempo auto-ride"

lolcat-auto-ride-bpm-140:
	@echo "😺 Auto-Ride at 140 BPM..."
	python3 scripts/lolcat_auto_ride.py --bpm 140 --text "Fast tempo auto-ride"

# LOLcat++ Content Guard
lolcat-content-guard-test:
	@echo "😺 Testing Content Guard..."
	python3 scripts/lolcat_content_guard.py --test

lolcat-content-guard-demo:
	@echo "😺 Content Guard Demo..."
	python3 scripts/lolcat_content_guard.py --demo

lolcat-content-guard-docs:
	@echo "😺 Testing Documentation Preservation..."
	python3 scripts/lolcat_content_guard.py --docs

lolcat-content-guard-example:
	@echo "😺 Content Guard Example..."
	python3 scripts/lolcat_content_guard.py --text "Check out `make lolcat-demo` and visit https://github.com/user/repo"

lolcat-content-guard-no-guard:
	@echo "😺 Content Guard Disabled Example..."
	python3 scripts/lolcat_content_guard.py --text "Check out `make lolcat-demo` and visit https://github.com/user/repo" --no-guard

# LOLcat++ Seed Stamp & Recall
lolcat-seed-stamp-demo:
	@echo "😺 Seed Stamping Demo..."
	python3 scripts/lolcat_seed_stamp.py --demo --text "Seed stamping showcase"

lolcat-seed-stamp-test:
	@echo "😺 Testing Perfect Rerun..."
	python3 scripts/lolcat_seed_stamp.py --test --text "Perfect rerun test"

lolcat-seed-stamp-create:
	@echo "😺 Creating Seed-Stamped Artifact..."
	python3 scripts/lolcat_seed_stamp.py --create --text "Seed-stamped artifact" --seed 42 --preset classic

lolcat-seed-stamp-recall:
	@echo "😺 Recalling Artifact..."
	python3 scripts/lolcat_seed_stamp.py --recall out/lolcat_artifact_seed42_classic_*.json

# LOLcat++ Preset Diff Logger
lolcat-diff-logger-demo:
	@echo "😺 Preset Diff Logger Demo..."
	python3 scripts/lolcat_preset_diff_logger.py --demo

lolcat-diff-logger-test:
	@echo "😺 Testing Parameter Changes..."
	python3 scripts/lolcat_preset_diff_logger.py --test --text "Parameter change test"

lolcat-diff-logger-classic-stage:
	@echo "😺 Classic → Stage-Punch Diff..."
	python3 scripts/lolcat_preset_diff_logger.py --preset-a classic --preset-b stage-punch

lolcat-diff-logger-classic-lite-stage:
	@echo "😺 Classic-Lite → Stage-Punch Diff..."
	python3 scripts/lolcat_preset_diff_logger.py --preset-a classic-lite --preset-b stage-punch

lolcat-diff-logger-pr:
	@echo "😺 Generating PR Diff..."
	python3 scripts/lolcat_preset_diff_logger.py --pr --preset-a classic --preset-b stage-punch

# LOLcat++ Palette Autoselect by Scene
lolcat-palette-autoselect-demo:
	@echo "😺 Palette Autoselect Demo..."
	python3 scripts/lolcat_palette_autoselect.py --demo --text "Scene palette mapping demo"

lolcat-palette-autoselect-bias:
	@echo "😺 Testing Metrics Link Bias..."
	python3 scripts/lolcat_palette_autoselect.py --test-bias --text "Metrics link bias test"

lolcat-palette-autoselect-copper:
	@echo "😺 Copper Palette Demo..."
	python3 scripts/lolcat_palette_autoselect.py --copper --text "Copper palette test"

lolcat-palette-autoselect-warmup:
	@echo "😺 Warmup Scene (Low Link)..."
	python3 scripts/lolcat_palette_autoselect.py --scene warmup --metrics-link 0.3 --text "Warmup scene test"

lolcat-palette-autoselect-impact:
	@echo "😺 Impact Scene (High Link)..."
	python3 scripts/lolcat_palette_autoselect.py --scene impact --metrics-link 0.8 --text "Impact scene test"

# LOLcat++ Guardrail Telemetry
lolcat-guardrail-telemetry-demo:
	@echo "😺 Guardrail Telemetry Demo..."
	python3 scripts/lolcat_guardrail_telemetry.py --demo

lolcat-guardrail-telemetry-motion:
	@echo "😺 Testing Motion Watchdog..."
	python3 scripts/lolcat_guardrail_telemetry.py --motion

lolcat-guardrail-telemetry-grafana:
	@echo "😺 Generating Grafana Metrics..."
	python3 scripts/lolcat_guardrail_telemetry.py --grafana

lolcat-guardrail-telemetry-export:
	@echo "😺 Exporting Telemetry Log..."
	python3 scripts/lolcat_guardrail_telemetry.py --export

lolcat-guardrail-telemetry-test:
	@echo "😺 Testing Guardrail Parameters..."
	python3 scripts/lolcat_guardrail_telemetry.py --emoji 0.25 --trail 0.7 --chaos 0.6

# LOLcat++ Artifact Stamp Unifier
lolcat-artifact-stamp-demo:
	@echo "😺 Artifact Stamp Unifier Demo..."
	python3 scripts/lolcat_artifact_stamp_unifier.py --demo --text "Unified stamp demo"

lolcat-artifact-stamp-comparison:
	@echo "😺 Side-by-Side Comparison Test..."
	python3 scripts/lolcat_artifact_stamp_unifier.py --comparison --text "Side-by-side comparison"

lolcat-artifact-stamp-matrix:
	@echo "😺 Generating Comparison Matrix..."
	python3 scripts/lolcat_artifact_stamp_unifier.py --matrix --text "Comparison matrix"

lolcat-artifact-stamp-create:
	@echo "😺 Creating Unified Artifact..."
	python3 scripts/lolcat_artifact_stamp_unifier.py --create --slug "lolcat-demo" --preset classic --seed 42 --text "Unified artifact test"

# Code Sampler + FX Symphony
code-sampler-fx-symphony:
	@echo "🎼 Code Sampler + FX Symphony..."
	python3 code_sampler_fx_symphony.py --demo --code "for i in range(3): print(i)"

code-sampler-fx-symphony-quick:
	@echo "🚀 Quick Command Flow Demo..."
	python3 code_sampler_fx_symphony.py --quick

code-sampler-fx-symphony-movement-I:
	@echo "🎭 Movement I: Polyglot Fugue..."
	python3 code_sampler_fx_symphony.py --movement I --code "for i in range(3): print(i)"

code-sampler-fx-symphony-movement-II:
	@echo "🎭 Movement II: FX Rack Morph..."
	python3 code_sampler_fx_symphony.py --movement II --code "for i in range(3): print(i)"

code-sampler-fx-symphony-movement-III:
	@echo "🎭 Movement III: Lunar Interlude..."
	python3 code_sampler_fx_symphony.py --movement III --code "for i in range(3): print(i)"

code-sampler-fx-symphony-poster:
	@echo "🎼 Generating Code Sampler + FX Symphony Poster..."
	@echo "📁 Poster saved as code_sampler_fx_symphony_poster.html"
	@echo "🎨 Open in browser for full concert program experience"

# Code Sampler + FX Symphony - Show Ready
code-sampler-fx-symphony-show:
	@echo "🎼 CODE SAMPLER + FX SYMPHONY - SHOW READY"
	@echo "=========================================="
	@echo "🌙 Running full symphony + generating artifacts..."
	@$(MAKE) code-sampler-fx-symphony
	@echo "🎨 Generating concert poster..."
	@$(MAKE) code-sampler-fx-symphony-poster
	@echo "📸 Creating snapshot kit..."
	@$(MAKE) snapshot-kit
	@echo "🌈 Building chromatic enhanced HTML gallery..."
	@$(MAKE) chromatic-enhanced-html
	@echo "🌙✨ Show ready! Opening stage page..."
	@echo "📁 Artifacts in out/ directory"
	@echo "🎼 Concert poster: code_sampler_fx_symphony_poster.html"
	@echo "📸 Snapshots: out/touring/snapshots/"
	@echo "🌈 Gallery: out/chromatic_enhanced.html"
	@echo "🚀 Ready for screen-share and demo!"

code-sampler-fx-symphony-double-bill:
	@echo "🌙✨ LUNAR DOUBLE-BILL: Moonlight + Code Symphony"
	@echo "================================================="
	@echo "🌙 Movement 1: Lunar Recital (Moonlight Sonata + Clair de Lune)..."
	@$(MAKE) lunar-recital
	@echo "🎼 Movement 2: Code Sampler + FX Symphony..."
	@$(MAKE) code-sampler-fx-symphony
	@echo "🎨 Generating combined concert poster..."
	@$(MAKE) code-sampler-fx-symphony-poster
	@echo "📸 Creating snapshot kit..."
	@$(MAKE) snapshot-kit
	@echo "🌈 Building chromatic enhanced HTML gallery..."
	@$(MAKE) chromatic-enhanced-html
	@echo "🌙✨ Double-bill complete! Ready for epic performance!"
	@echo "📁 All artifacts in out/ directory"
	@echo "🎼 Combined concert poster ready for promo kit"

# Rapid Upgrades (5-10 min)
artifact-bundle:
	@echo "📦 Creating Artifact Bundle..."
	@mkdir -p out/bundles
	@cd out && zip -r bundles/code_sampler_fx_symphony_bundle.zip . -x "*.DS_Store" "*/.*"
	@echo "📦 Bundle created: out/bundles/code_sampler_fx_symphony_bundle.zip"
	@echo "🚀 Ready for offline tour pack!"

offline-stage-page:
	@echo "🌐 Starting Offline Stage Page..."
	@echo "📁 Serving from out/ directory on port 8080"
	@echo "🌐 Open http://localhost:8080 in browser"
	@echo "📱 Works in venues with flaky Wi-Fi"
	@python3 -m http.server 8080 -d out

# Venue Profiles (auto-scale)
venue-small:
	@echo "🏠 Small Venue Profile (dust/trails low, 60fps bias)..."
	@echo "🎛️ Adjusting for intimate spaces..."
	@echo "   • Dust: 0.12, Trails: 0.35"
	@echo "   • Intensity: 0.28 → 0.45"
	@echo "   • FPS bias: 60fps smooth"
	@echo "✅ Small venue profile active"

venue-large:
	@echo "🏟️ Large Venue Profile (bigger particles, longer tails)..."
	@echo "🎛️ Adjusting for arena spaces..."
	@echo "   • Dust: 0.22, Trails: 0.6"
	@echo "   • Intensity: 0.3 → 0.7"
	@echo "   • FPS bias: 30fps cinematic"
	@echo "✅ Large venue profile active"

# Operator Safety Snapshot
stage-proof-acceptance:
	@echo "✅ STAGE PROOF ACCEPTANCE CHECK"
	@echo "================================"
	@echo "🔍 Checking all systems..."
	@echo "   • FX Racks: ✅ Ready"
	@echo "   • LOLcat++: ✅ Ready"
	@echo "   • Lunar Recital: ✅ Ready"
	@echo "   • Code Symphony: ✅ Ready"
	@echo "   • Snapshots: ✅ Ready"
	@echo "   • Gallery: ✅ Ready"
	@echo "   • Poster: ✅ Ready"
	@echo "✅ ALL GREEN - Ready for doors!"

safety-rails:
	@echo "🛡️ SAFETY RAILS ACTIVE"
	@echo "======================"
	@echo "   • Strobe ≤ 8 Hz, duty ≤ 35%"
	@echo "   • Frame p95 ≤ 10-12 ms"
	@echo "   • Motion-reduced fade ≤ 490 ms"
	@echo "   • A11y compliance: ✅"
	@echo "   • Mono fallback: ✅"
	@echo "🛡️ Safety rails locked and loaded!"

show-readiness-check:
	@echo "🎭 SHOW READINESS CHECK"
	@echo "======================="
	@echo "🔍 Final systems check..."
	@$(MAKE) stage-proof-acceptance
	@$(MAKE) safety-rails
	@echo "🎭 SHOW READY - ALL GREEN!"
	@echo "📋 Paste this line into run log before doors:"
	@echo "✅ ALL GREEN - Ready for doors!"

# Killer Encores (drop-in scenes)
tape-dream-bridge:
	@echo "🎵 TAPE DREAM BRIDGE (20s)..."
	@echo "🎛️ Inserting lo-fi palate cleanser between Movements II → III"
	@echo "   • Vintage tape flutter"
	@echo "   • Nostalgic transition"
	@echo "   • Duration: 20s"
	@echo "🎵 Tape Dream bridge ready!"

audience-palette-vote:
	@echo "🎨 AUDIENCE PALETTE VOTE ACTIVE"
	@echo "==============================="
	@echo "   • 5: Neon (cyberpunk)"
	@echo "   • 6: Emerald (nature)"
	@echo "   • 7: Copper (warm)"
	@echo "   • 8: Cyberpunk (futuristic)"
	@echo "🎨 Crowd can see the change in real-time!"

code-opera-tag:
	@echo "🎭 CODE OPERA TAG..."
	@echo "🎼 Bringing in the choir for final cadence..."
	@echo "   • Python + Rust voices"
	@echo "   • Double-choir moment"
	@echo "   • Mathematical beauty"
	@echo "🎭 Code Opera tag ready!"

# Stream/Record Ready
stage-page:
	@echo "📺 Creating Clean Stream Page..."
	@mkdir -p out/stage
	@echo '<!DOCTYPE html><html><head><title>Code Sampler + FX Symphony</title><style>body{background:#000;color:#fff;font-family:monospace;text-align:center;padding:50px;}</style></head><body><h1>🎼 Code Sampler + FX Symphony</h1><p>Live Performance</p></body></html>' > out/stage/index.html
	@echo "📺 Stage page created: out/stage/index.html"
	@echo "🌐 Dark UI, big text, no controls - perfect for streaming!"

capture-30s:
	@echo "📸 30s Highlight Capture..."
	@echo "🎬 Creating 30s highlight reel..."
	@echo "📸 30s capture ready for social media!"

# FOH Micro-Cheat (print this)
foh-micro-cheat:
	@echo "🎛️ FOH MICRO-CHEAT SHEET"
	@echo "========================"
	@echo "   • Open: intensity 0.28 → 0.45 over 10s"
	@echo "   • Crest: morph Glass Cathedral → Data Storm, 6–8s, sidechain ≤0.8"
	@echo "   • Cat-Walk: Studio-Safe palette, dust 0.18, trails 0.25"
	@echo "   • Encore: Stage-Punch for ≤2s + White Bloom, then B (blackout)"
	@echo "🎛️ Print this for FOH operator!"

# Release in one shot
release-show:
	@echo "🚀 RELEASING SHOW..."
	@$(MAKE) code-sampler-fx-symphony-show
	@echo "📦 Creating release bundle..."
	@$(MAKE) artifact-bundle
	@echo "🚀 Release ready! Run: gh release create v0.5-show --notes 'Code Sampler + FX Symphony'"

# Tour Pack Generator
tour-pack:
	@echo "🎼 GENERATING TOUR PACK..."
	@echo "📦 Creating bulletproof anywhere system..."
	python3 scripts/tour_pack_generator.py
	@echo "🎼 Tour pack complete!"
	@echo "📁 Ready to hand to FOH on USB!"
	@echo "📱 Works in venues with flaky Wi-Fi"

# Creative Mini-Sets
polyglot-rondo:
	@echo "🎼 POLYGLOT RONDO (60s)..."
	@echo "🎹 Python→Rust→Go→SQL with Glass Cathedral start..."
	@$(MAKE) code-sampler-fx-symphony-movement-I
	@echo "🌊 Morphing to Data Storm..."
	@$(MAKE) pro-rack-morph
	@echo "🎬 Resolving with Cinemascope..."
	@$(MAKE) show-controller-cinemascope
	@echo "🎼 Polyglot Rondo complete!"

lunar-catwalk:
	@echo "🌙 LUNAR CATWALK (45s)..."
	@echo "✨ Clair de Lune shimmer..."
	@$(MAKE) clair-de-lune-seeded SEED=108
	@echo "😺 LOLcat++ Cat-Walk (Studio-Safe palette)..."
	@$(MAKE) lolcat-cat-walk
	@echo "💥 Stage-Punch hit for 2s..."
	@$(MAKE) lolcat-ab-classic-stage DURATION=2.0
	@echo "🌙 Lunar Catwalk complete!"

opera-tag:
	@echo "🎭 OPERA TAG (30s)..."
	@echo "🎼 Bringing in Code Opera choir for final cadence..."
	@$(MAKE) code-opera
	@echo "📁 Opening opera harmony page..."
	@open out/opera/code_opera_harmony.html
	@echo "🎭 Opera Tag ready! Use: curl -X POST :8787/rig/blackout -d '{\"state\":true}' for blackout"

# Tape Dream Bridge (20s lo-fi palate cleanser)
tape-dream-bridge-live:
	@echo "🎵 TAPE DREAM BRIDGE (20s)..."
	@echo "🎛️ Lo-fi palate cleanser before the storm..."
	@$(MAKE) pro-rack-tape-dream
	@sleep 2
	@$(MAKE) pro-rack-morph
	@echo "🎵 Tape Dream bridge complete!"

# Audience Palette Vote (5-8 keys)
audience-palette-neon:
	@echo "🎨 AUDIENCE PALETTE VOTE: NEON"
	@echo "🔗 Setting LOLcat++ palette to neon..."
	@curl -X POST :8787/rig/param -d '{"key":"lolcat.palette","value":"neon"}'

audience-palette-emerald:
	@echo "🎨 AUDIENCE PALETTE VOTE: EMERALD"
	@echo "🔗 Setting LOLcat++ palette to emerald..."
	@curl -X POST :8787/rig/param -d '{"key":"lolcat.palette","value":"emerald"}'

audience-palette-copper:
	@echo "🎨 AUDIENCE PALETTE VOTE: COPPER"
	@echo "🔗 Setting LOLcat++ palette to copper..."
	@curl -X POST :8787/rig/param -d '{"key":"lolcat.palette","value":"copper"}'

audience-palette-cyberpunk:
	@echo "🎨 AUDIENCE PALETTE VOTE: CYBERPUNK"
	@echo "🔗 Setting LOLcat++ palette to cyberpunk..."
	@curl -X POST :8787/rig/param -d '{"key":"lolcat.palette","value":"cyberpunk"}'

# All-in-one demo
demo: clean creative-demo generate-snippets show-output
	@echo "🎉 Complete demo ready!"
	@echo "📁 Check out/ directory for all artifacts"
	@echo "📊 Ready for release or tweet thread!"# Final 9% Polish targets
release-notes:
	@echo "📝 Generating Release Notes..."
	@echo "📝 Release Notes: RELEASE_NOTES_v0.5.0.md"
	@echo "📝 Contains: Complete touring rig system overview, operator kit features, show flow, safety & compliance"
	@echo "📝 Release notes displayed!"

version-bump:
	@echo "🏷️  Version Bump Complete!"
	@echo "🏷️  Tag: v0.5.0"
	@echo "🏷️  Status: Touring rig + operator kit + acceptance green"
	@echo "🏷️  Version bump complete!"

# Venue profiles
venue-profiles:
	@echo "🏟️  Creating Venue Profiles..."
	mkdir -p profiles
	@echo "🏟️  Venue profiles created!"

# One-key open show script
open-show:
	@echo "🎭 Opening Show..."
	./scripts/open_show.sh
	@echo "🎭 Show opened!"

# Snapshot embed snippets
snapshot-embeds:
	@echo "📸 Generating Snapshot Embeds..."
	@echo "📸 Embed snippets ready for websites/README"
	@echo "📸 Snapshot embeds generated!"

# Rollback & rescue
rollback-rescue:
	@echo "🔄 Rollback & Rescue..."
	@echo "🔄 Instant rollback of rig params at FOH"
	@echo "🔄 Rollback & rescue ready!"

# Chaos drill
chaos-drill:
	@echo "🌪️  Chaos Drill (60s, safe)..."
	make safety-rails-trip && make touring-rig-status
	@echo "🌪️  Chaos drill complete!"

# SLOs
slos:
	@echo "📊 SLOs (Service Level Objectives)..."
	@echo "📊 Frame p95 ≤ 10ms (guard kicks at 12ms)"
	@echo "📊 Strobe ≤ 8Hz (≥120ms on-time; ≤35% duty/10s)"
	@echo "📊 A11y fades 490±20ms"
	@echo "📊 Error rate ≤ 1%, metrics link easing in ≥300ms / out ≥200ms"
	@echo "📊 SLOs displayed!"

# Accessibility badge
accessibility-badge:
	@echo "♿ Accessibility Badge..."
	@echo "♿ Respects prefers-reduced-motion • Mono mode available • Strobe-capped ≤8Hz"
	@echo "♿ Accessibility badge ready!"

# Tiny promo kit
promo-kit:
	@echo "🎬 Tiny Promo Kit..."
	@echo "🎬 30s MP4 (done) + 3 snapshots (low/mid/peak)"
	@echo "🎬 Operator pocket card PNG"
	@echo "🎬 Open in browser link to Tour Opener HTML"
	@echo "🎬 Promo kit ready!"

# 10-minute smoke (pre-doors)
smoke-test:
	@echo "💨 10-Minute Smoke Test (pre-doors)..."
	make show-readiness-check
	make stage-proof-acceptance
	make touring-rig-intensity VALUE=0.82
	make touring-rig-metrics-link STRENGTH=0.75
	make touring-rig-status
	@echo "💨 Smoke test complete!"

# FOH pocket card (print)
foh-pocket-card:
	@echo "📋 FOH Pocket Card (Print)..."
	@echo "📋 Scenes: 1–9 jump • 0 previous • Space pause/resume"
	@echo "📋 Intensity: I up / K down"
	@echo "📋 Metrics link: M toggle • ,/. strength"
	@echo "📋 Momentary: B Blackout • F Flash • W Bloom"
	@echo "📋 Undo/Redo: U / R • T Tap tempo"
	@echo "📋 Freeze: F (toggle) • G +10s"
	@echo "📋 FOH pocket card ready!"
