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

# Code Hero - Guitar Hero for Loops (placeholder)
code-hero:
	@echo "🎮 Code Hero mode coming soon..."
	@echo "🎸 Guitar Hero for code loops with FX timing"

# Code Tarot - Divination system for creative coding
code-tarot:
	@echo "🔮 Code Tarot mode coming soon..."
	@echo "🎴 Random texture/FX cards for creative coding"

# All-in-one demo
demo: clean creative-demo generate-snippets show-output
	@echo "🎉 Complete demo ready!"
	@echo "📁 Check out/ directory for all artifacts"
	@echo "📊 Ready for release or tweet thread!"