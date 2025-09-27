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