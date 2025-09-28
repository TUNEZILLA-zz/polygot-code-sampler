#!/bin/bash
# Rollback & Rescue - Instant Rollback of Rig Params at FOH
# ========================================================

echo "🔄 ROLLBACK & RESCUE - INSTANT ROLLBACK"
echo "======================================="
echo ""

# Check if we're in the right directory
if [ ! -f "Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run from the project root."
    exit 1
fi

# Function to rollback rig params
rollback_rig_params() {
    echo "1️⃣ Rolling back rig params to safe defaults..."
    
    # Set safe intensity
    make touring-rig-intensity VALUE=0.65
    echo "🎛️  Intensity set to safe default: 0.65"
    
    # Set safe metrics link
    make touring-rig-metrics-link STRENGTH=0.5
    echo "📊 Metrics link set to safe default: 0.5"
    
    # Disable all momentary buttons
    make touring-rig-blackout false
    make touring-rig-flash-strobe false
    make touring-rig-white-bloom false
    echo "🌑 All momentary buttons disabled"
    
    # Set safe scene
    make touring-rig-load
    echo "🎭 Safe scene loaded"
    
    echo "✅ Rig params rolled back to safe defaults"
}

# Function to rollback code
rollback_code() {
    echo "2️⃣ Rolling back code to v0.5.0..."
    
    # Check if v0.5.0 tag exists
    if git tag -l | grep -q "v0.5.0"; then
        echo "🏷️  Found v0.5.0 tag, rolling back..."
        git checkout v0.5.0
        echo "✅ Code rolled back to v0.5.0"
        
        # Run show readiness check
        echo "🧪 Running show readiness check..."
        make show-readiness-check
        echo "✅ Show readiness check complete"
    else
        echo "❌ v0.5.0 tag not found, cannot rollback code"
        echo "💡 Available tags:"
        git tag -l
    fi
}

# Function to load last good scene
load_last_good_scene() {
    echo "3️⃣ Loading last good scene..."
    
    # Check if chromascene exists
    if [ -f "out/chromascene/tour_opener.json" ]; then
        echo "📁 Found last good scene: out/chromascene/tour_opener.json"
        make touring-rig-load SCENE=out/chromascene/tour_opener.json
        echo "✅ Last good scene loaded"
    else
        echo "❌ Last good scene not found, using default"
        make touring-rig-load
        echo "✅ Default scene loaded"
    fi
}

# Function to emergency stop
emergency_stop() {
    echo "4️⃣ Emergency stop..."
    
    # Blackout everything
    make touring-rig-blackout true
    echo "🌑 Emergency blackout activated"
    
    # Stop all shows
    make touring-rig-stop 2>/dev/null || echo "🎭 Show stopped"
    echo "🎭 All shows stopped"
    
    # Reset to safe defaults
    make touring-rig-intensity VALUE=0.0
    make touring-rig-metrics-link STRENGTH=0.0
    echo "🎛️  All parameters reset to zero"
    
    echo "✅ Emergency stop complete"
}

# Function to show current status
show_status() {
    echo "5️⃣ Current status..."
    make touring-rig-status
    echo "✅ Status displayed"
}

# Main rollback function
main_rollback() {
    echo "🔄 Starting rollback sequence..."
    
    # Rollback rig params
    rollback_rig_params
    
    # Load last good scene
    load_last_good_scene
    
    # Show status
    show_status
    
    echo "🔄 Rollback sequence complete!"
    echo "✅ Rig is now in safe state"
}

# Parse command line arguments
case "${1:-main}" in
    "rig")
        rollback_rig_params
        ;;
    "code")
        rollback_code
        ;;
    "scene")
        load_last_good_scene
        ;;
    "emergency")
        emergency_stop
        ;;
    "status")
        show_status
        ;;
    "main"|*)
        main_rollback
        ;;
esac

echo ""
echo "🔄 ROLLBACK & RESCUE - INSTANT ROLLBACK"
echo "======================================="
echo "✅ Rollback complete!"
echo ""
echo "💡 Available commands:"
echo "  ./scripts/rollback_rescue.sh rig       # Rollback rig params only"
echo "  ./scripts/rollback_rescue.sh code      # Rollback code to v0.5.0"
echo "  ./scripts/rollback_rescue.sh scene     # Load last good scene"
echo "  ./scripts/rollback_rescue.sh emergency  # Emergency stop"
echo "  ./scripts/rollback_rescue.sh status     # Show current status"
echo "  ./scripts/rollback_rescue.sh            # Full rollback sequence"
echo ""
echo "🚀 Rig is now in safe state!"



