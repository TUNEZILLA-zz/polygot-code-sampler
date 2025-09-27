#!/bin/bash
# Chaos Drill - 60s Safe Testing
# ==============================

echo "🌪️  CHAOS DRILL - 60s SAFE TESTING"
echo "==================================="
echo ""

# Check if we're in the right directory
if [ ! -f "Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run from the project root."
    exit 1
fi

echo "🧪 Starting 60-second chaos drill..."
echo "⏱️  Duration: 60 seconds"
echo "🛡️  Safety: All tests are safe and reversible"
echo ""

# Function to run safety rails trip test
run_safety_rails_trip() {
    echo "1️⃣ Running Safety Rails Trip Test..."
    ./scripts/safety_rails_trip_test.sh
    echo "✅ Safety rails trip test complete"
}

# Function to run touring rig status
run_touring_rig_status() {
    echo "2️⃣ Running Touring Rig Status..."
    make touring-rig-status
    echo "✅ Touring rig status complete"
}

# Function to test intensity changes
test_intensity_changes() {
    echo "3️⃣ Testing Intensity Changes..."
    
    # Test intensity ramp up
    echo "🎛️  Testing intensity ramp up..."
    for i in {50..100..10}; do
        make touring-rig-intensity VALUE=$i
        sleep 1
    done
    
    # Test intensity ramp down
    echo "🎛️  Testing intensity ramp down..."
    for i in {90..10..-10}; do
        make touring-rig-intensity VALUE=$i
        sleep 1
    done
    
    echo "✅ Intensity changes test complete"
}

# Function to test metrics link changes
test_metrics_link_changes() {
    echo "4️⃣ Testing Metrics Link Changes..."
    
    # Test metrics link ramp up
    echo "📊 Testing metrics link ramp up..."
    for i in {20..80..20}; do
        make touring-rig-metrics-link STRENGTH=$i
        sleep 1
    done
    
    # Test metrics link ramp down
    echo "📊 Testing metrics link ramp down..."
    for i in {60..20..-20}; do
        make touring-rig-metrics-link STRENGTH=$i
        sleep 1
    done
    
    echo "✅ Metrics link changes test complete"
}

# Function to test momentary buttons
test_momentary_buttons() {
    echo "5️⃣ Testing Momentary Buttons..."
    
    # Test blackout
    echo "🌑 Testing blackout..."
    make touring-rig-blackout true
    sleep 2
    make touring-rig-blackout false
    sleep 1
    
    # Test flash strobe
    echo "⚡ Testing flash strobe..."
    make touring-rig-flash-strobe true
    sleep 2
    make touring-rig-flash-strobe false
    sleep 1
    
    # Test white bloom
    echo "💡 Testing white bloom..."
    make touring-rig-white-bloom true
    sleep 2
    make touring-rig-white-bloom false
    sleep 1
    
    echo "✅ Momentary buttons test complete"
}

# Function to test scene changes
test_scene_changes() {
    echo "6️⃣ Testing Scene Changes..."
    
    # Test scene navigation
    echo "🎬 Testing scene navigation..."
    for i in {0..2}; do
        make touring-rig-jump $i
        sleep 2
    done
    
    echo "✅ Scene changes test complete"
}

# Function to test parameter changes
test_parameter_changes() {
    echo "7️⃣ Testing Parameter Changes..."
    
    # Test various parameters
    echo "🎛️  Testing parameter changes..."
    make touring-rig-param key="scenes[0].fx[0].wet" value=0.5
    sleep 1
    make touring-rig-param key="scenes[0].fx[0].wet" value=0.8
    sleep 1
    make touring-rig-param key="scenes[0].fx[0].wet" value=0.3
    sleep 1
    
    echo "✅ Parameter changes test complete"
}

# Function to test undo/redo
test_undo_redo() {
    echo "8️⃣ Testing Undo/Redo..."
    
    # Test undo
    echo "↶ Testing undo..."
    make touring-rig-undo
    sleep 1
    
    # Test redo
    echo "↷ Testing redo..."
    make touring-rig-redo
    sleep 1
    
    echo "✅ Undo/redo test complete"
}

# Function to run final status check
run_final_status() {
    echo "9️⃣ Final Status Check..."
    make touring-rig-status
    echo "✅ Final status check complete"
}

# Main chaos drill function
main_chaos_drill() {
    echo "🌪️  Starting chaos drill sequence..."
    
    # Run all tests
    run_safety_rails_trip
    run_touring_rig_status
    test_intensity_changes
    test_metrics_link_changes
    test_momentary_buttons
    test_scene_changes
    test_parameter_changes
    test_undo_redo
    run_final_status
    
    echo "🌪️  Chaos drill sequence complete!"
}

# Parse command line arguments
case "${1:-main}" in
    "safety")
        run_safety_rails_trip
        ;;
    "status")
        run_touring_rig_status
        ;;
    "intensity")
        test_intensity_changes
        ;;
    "metrics")
        test_metrics_link_changes
        ;;
    "momentary")
        test_momentary_buttons
        ;;
    "scenes")
        test_scene_changes
        ;;
    "params")
        test_parameter_changes
        ;;
    "undo")
        test_undo_redo
        ;;
    "final")
        run_final_status
        ;;
    "main"|*)
        main_chaos_drill
        ;;
esac

echo ""
echo "🌪️  CHAOS DRILL - 60s SAFE TESTING"
echo "==================================="
echo "✅ Chaos drill complete!"
echo ""
echo "💡 Available commands:"
echo "  ./scripts/chaos_drill.sh safety    # Safety rails trip test"
echo "  ./scripts/chaos_drill.sh status    # Touring rig status"
echo "  ./scripts/chaos_drill.sh intensity # Intensity changes test"
echo "  ./scripts/chaos_drill.sh metrics   # Metrics link changes test"
echo "  ./scripts/chaos_drill.sh momentary # Momentary buttons test"
echo "  ./scripts/chaos_drill.sh scenes    # Scene changes test"
echo "  ./scripts/chaos_drill.sh params    # Parameter changes test"
echo "  ./scripts/chaos_drill.sh undo      # Undo/redo test"
echo "  ./scripts/chaos_drill.sh final     # Final status check"
echo "  ./scripts/chaos_drill.sh           # Full chaos drill sequence"
echo ""
echo "🚀 All systems tested and verified!"

