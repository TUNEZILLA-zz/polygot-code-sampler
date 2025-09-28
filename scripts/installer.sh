#!/bin/bash
# Code Live v0.5 - Touring Rig + Operator Kit Installer
# =====================================================

echo "🎭 CODE LIVE v0.5 - TOURING RIG + OPERATOR KIT"
echo "==============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run from the project root."
    exit 1
fi

echo "1️⃣ Running Show Readiness Check..."
make show-readiness-check
echo ""

echo "2️⃣ Opening Show HTML..."
# Check if we have a show HTML file
if [ -f "out/touring/snapshots/tour_opener-low.html" ]; then
    echo "📸 Opening Tour Opener Show (Low Intensity)..."
    open out/touring/snapshots/tour_opener-low.html 2>/dev/null || echo "📸 Show HTML ready: out/touring/snapshots/tour_opener-low.html"
else
    echo "📸 Generating show HTML..."
    make snapshot-kit-scene
    if [ -f "out/touring/snapshots/tour_opener-low.html" ]; then
        open out/touring/snapshots/tour_opener-low.html 2>/dev/null || echo "📸 Show HTML ready: out/touring/snapshots/tour_opener-low.html"
    fi
fi
echo ""

echo "3️⃣ Displaying Operator Kit..."
echo "📖 FOH Runbook: docs/FOH_RUNBOOK.md"
echo "⌨️  Operator Hotkeys: make operator-hotkeys"
echo "🛡️  Safety Rails: make safety-rails"
echo "🌐 API One-Liners: make api-one-liners"
echo ""

echo "4️⃣ Quick Start Commands..."
echo "🎭 Load Show: make touring-rig-load"
echo "🎬 Play Show: make touring-rig-play"
echo "📊 Show Status: make touring-rig-status"
echo "🎛️  Set Intensity: make touring-rig-intensity VALUE=0.82"
echo "📊 Set Metrics: make touring-rig-metrics-link STRENGTH=0.75"
echo ""

echo "🎭 CODE LIVE v0.5 - TOURING RIG + OPERATOR KIT"
echo "==============================================="
echo "✅ Installation complete!"
echo ""
echo "🚀 Ready to go live!"
echo ""
echo "📖 See docs/FOH_RUNBOOK.md for complete operator guide"
echo "⌨️  See docs/OPERATOR_POCKET_CARD.md for quick reference"
echo ""
echo "🎭 Code Live v0.5 — Touring Rig + Operator Kit"
echo "Ready for Stage! ✨"



