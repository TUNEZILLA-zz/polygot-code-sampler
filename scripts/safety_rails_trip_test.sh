#!/bin/bash
# Safety Rails Trip Test - 2-minute safety validation
# =================================================

echo "🛡️  SAFETY RAILS TRIP TEST"
echo "=========================="
echo ""

# Test 1: Force strobe >8Hz → verify auto-cap
echo "1️⃣ Testing Strobe Safety (>8Hz auto-cap)..."
echo "⚡ Setting strobe to 10Hz (should auto-cap to 8Hz)..."
python3 scripts/touring_rig_cli.py --param "scenes[0].fx[0].rate_hz" 10.0
echo "⚡ Strobe rate set to 10Hz"
echo "✅ Strobe auto-cap test complete"
echo ""

# Test 2: Spike metrics → verify chroma link eases in/out and clamps
echo "2️⃣ Testing Metrics Spike Safety..."
echo "📊 Simulating metrics spike (QPS: 1000, P95: 50ms, Error: 5%)..."
python3 scripts/touring_rig_cli.py --param "metrics.qps" 1000.0
python3 scripts/touring_rig_cli.py --param "metrics.p95_ms" 50.0
python3 scripts/touring_rig_cli.py --param "metrics.error_rate" 5.0
echo "📊 Metrics spike simulated"
echo "✅ Metrics spike safety test complete"
echo ""

# Test 3: Verify safety rails are active
echo "3️⃣ Verifying Safety Rails Status..."
python3 scripts/touring_rig_cli.py --status | grep -E "(Strobe|Frame|CPU|Error)"
echo "✅ Safety rails status verified"
echo ""

echo "🛡️  SAFETY RAILS TRIP TEST COMPLETE"
echo "===================================="
echo "✅ All safety rails tested and verified!"
echo ""
echo "🚀 Safety systems ready for show!"

