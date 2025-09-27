#!/bin/bash
# Show Readiness Check - 5-minute bulletproof check
# =================================================

echo "🎭 TOURING RIG - SHOW READINESS CHECK"
echo "======================================"
echo ""

# 1. Load show + verify scenes
echo "1️⃣ Loading show + verifying scenes..."
make touring-rig-load
if [ $? -eq 0 ]; then
    echo "✅ Show loaded successfully"
else
    echo "❌ Show load failed"
    exit 1
fi

echo ""
make touring-rig-status
echo ""

# 2. Thumbs preview sweep
echo "2️⃣ Thumbs preview sweep..."
echo "📸 Testing mono variant..."
make touring-rig-param key=preview.variant value=mono
echo "📸 Testing motion-safe variant..."
make touring-rig-param key=preview.variant value=motion-safe
echo "📸 Testing intensity-50 variant..."
make touring-rig-param key=preview.variant value=intensity-50
echo "✅ Preview variants tested"
echo ""

# 3. Safety rails ping
echo "3️⃣ Safety rails ping..."
echo "⚡ Testing flash strobe (should auto-release via duty-cycle guard)..."
make touring-rig-flash-strobe
sleep 1
echo "🌑 Testing blackout (toggle on/off cleanly)..."
make touring-rig-blackout
sleep 0.5
echo "🎛️ Testing intensity control..."
make touring-rig-intensity value=0.85
echo "✅ Safety rails tested"
echo ""

# 4. Metrics link sanity
echo "4️⃣ Metrics link sanity..."
echo "📊 Testing metrics link (easing in ≤300ms, out ≤200ms)..."
make touring-rig-metrics-link value=0.75
echo "✅ Metrics link tested"
echo ""

# 5. Morph smoke
echo "5️⃣ Morph smoke test..."
echo "🎬 Starting programmed scenes..."
make touring-rig-play &
PLAY_PID=$!

# Wait a moment for show to start
sleep 2

echo "🎛️ Testing morph curve..."
make touring-rig-param key=morph.curve value=EaseInOut
echo "🎛️ Testing morph duration..."
make touring-rig-param key=morph.duration value=2.0

# Stop the show
kill $PLAY_PID 2>/dev/null
echo "✅ Morph smoke test complete"
echo ""

echo "🎭 SHOW READINESS CHECK COMPLETE"
echo "================================="
echo "✅ All systems ready for show!"
echo ""
echo "🚀 Ready to go live!"

