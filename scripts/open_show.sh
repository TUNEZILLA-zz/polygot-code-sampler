#!/bin/bash
# One-Key "Open Show" Script - Ops Friction → Zero
# ================================================

echo "🎭 CODE LIVE v0.5 - ONE-KEY OPEN SHOW"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run from the project root."
    exit 1
fi

echo "1️⃣ Starting Server..."
# Start server in background
python3 -m uvicorn server:app --port 8787 --host 0.0.0.0 &
SERVER_PID=$!
echo "🌐 Server started on port 8787 (PID: $SERVER_PID)"
echo ""

echo "2️⃣ Loading Show..."
make touring-rig-load
echo "🎭 Show loaded successfully"
echo ""

echo "3️⃣ Opening Dashboards..."
# Open FOH runbook
if [ -f "docs/FOH_RUNBOOK.md" ]; then
    echo "📖 Opening FOH Runbook..."
    open docs/FOH_RUNBOOK.md 2>/dev/null || echo "📖 FOH Runbook: docs/FOH_RUNBOOK.md"
fi

# Open operator pocket card
if [ -f "docs/OPERATOR_POCKET_CARD.md" ]; then
    echo "📋 Opening Operator Pocket Card..."
    open docs/OPERATOR_POCKET_CARD.md 2>/dev/null || echo "📋 Operator Pocket Card: docs/OPERATOR_POCKET_CARD.md"
fi

# Open show HTML
if [ -f "out/touring/snapshots/tour_opener-low.html" ]; then
    echo "📸 Opening Show HTML..."
    open out/touring/snapshots/tour_opener-low.html 2>/dev/null || echo "📸 Show HTML: out/touring/snapshots/tour_opener-low.html"
else
    echo "📸 Generating show HTML..."
    make snapshot-kit-scene
    if [ -f "out/touring/snapshots/tour_opener-low.html" ]; then
        open out/touring/snapshots/tour_opener-low.html 2>/dev/null || echo "📸 Show HTML: out/touring/snapshots/tour_opener-low.html"
    fi
fi
echo ""

echo "4️⃣ Displaying Quick Start..."
echo "🎛️  Quick Start Commands:"
echo "  make touring-rig-play          # Start show"
echo "  make touring-rig-status       # Show status"
echo "  make touring-rig-intensity VALUE=0.82  # Set intensity"
echo "  make touring-rig-metrics-link STRENGTH=0.75  # Set metrics"
echo "  make touring-rig-blackout     # Blackout"
echo "  make touring-rig-flash-strobe # Flash strobe"
echo "  make touring-rig-white-bloom   # White bloom"
echo ""

echo "5️⃣ Displaying Operator Hotkeys..."
echo "⌨️  Operator Hotkeys:"
echo "  Scenes: 1-9 (jump to scene), 0 (previous), Space (pause/resume)"
echo "  Intensity: I (up), K (down)"
echo "  Metrics: M (toggle), , (decrease), . (increase)"
echo "  Momentary: B (blackout), F (flash), W (white bloom)"
echo "  Undo/Redo: U (undo), R (redo)"
echo "  Special: F (freeze/unfreeze), T (tap tempo)"
echo ""

echo "6️⃣ Displaying Safety Rails..."
echo "🛡️  Safety Rails:"
echo "  Strobe Cap: ≤8 Hz, on-time ≥120ms, duty-cycle ≤35% over 10s"
echo "  Frame Budget: 30-frame p95 > 12ms → auto-reduce trails/particles"
echo "  Param Slew: intensity ≤0.6/s, chroma.offset ≤0.3/s"
echo "  Motion Compliance: instant mono fallback on system signal"
echo ""

echo "🎭 CODE LIVE v0.5 - ONE-KEY OPEN SHOW"
echo "======================================"
echo "✅ Show ready to go live!"
echo ""
echo "🌐 Server running on: http://localhost:8787"
echo "📖 FOH Runbook: docs/FOH_RUNBOOK.md"
echo "📋 Operator Pocket Card: docs/OPERATOR_POCKET_CARD.md"
echo "📸 Show HTML: out/touring/snapshots/tour_opener-low.html"
echo ""
echo "🚀 Ready for stage!"
echo ""
echo "💡 To stop the server: kill $SERVER_PID"
echo "💡 To run show readiness check: make show-readiness-check"
echo "💡 To run acceptance test: make stage-proof-acceptance"

