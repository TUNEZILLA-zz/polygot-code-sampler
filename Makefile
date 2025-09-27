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