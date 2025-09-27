#!/usr/bin/env python3
"""
Show Controller CLI - Chromatic Light Desk Show Controller
=========================================================

Command-line interface for the show controller system.
"""

import argparse
import json
import sys
import os
import time
from typing import Dict

# Add the parent directory to the path so we can import the show controller
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.show_controller import ShowController, SceneConfig, SceneType, ShowFlow


def main():
    parser = argparse.ArgumentParser(
        description="Chromatic Light Desk Show Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run showpiece flow
  python3 scripts/show_controller_cli.py --flow showpiece

  # Load specific scene
  python3 scripts/show_controller_cli.py --scene cinemascope --text "Code Live"

  # Save scene configuration
  python3 scripts/show_controller_cli.py --save-scene my_scene.json --scene neon_bloom

  # Load scene from file
  python3 scripts/show_controller_cli.py --load-scene my_scene.json --text "TuneZilla"

  # Create snapshot kit
  python3 scripts/show_controller_cli.py --snapshot-kit --scene prism_burst
        """
    )
    
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--flow", help="Run a show flow (showpiece)")
    parser.add_argument("--scene", help="Load a specific scene")
    parser.add_argument("--save-scene", help="Save current scene to file")
    parser.add_argument("--load-scene", help="Load scene from file")
    parser.add_argument("--snapshot-kit", action="store_true", help="Create snapshot kit")
    parser.add_argument("--a11y", action="store_true", help="Enable accessibility mode")
    parser.add_argument("--mono", action="store_true", help="Enable mono mode")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--output", "-o", help="Output file for HTML mode")
    
    args = parser.parse_args()
    
    # Create show controller
    controller = ShowController()
    
    # Set modes
    if args.a11y:
        controller.set_a11y_mode(True)
        print("♿ Accessibility mode enabled")
    
    if args.mono:
        controller.set_mono_mode(True)
        print("🎵 Mono mode enabled")
    
    # Handle show flow
    if args.flow == "showpiece":
        show_flow = controller.create_showpiece_flow()
        print(f"🎭 Running Showpiece Flow: {show_flow.name}")
        print(f"⏱️  Total Duration: {show_flow.total_duration}s")
        print(f"🎬 Scenes: {len(show_flow.scenes)}")
        
        # Run through scenes
        for i, scene in enumerate(show_flow.scenes):
            print(f"\n🎬 Scene {i+1}: {scene.name} ({scene.scene_type.value})")
            controller.load_scene(scene)
            
            # Simulate metrics for demo
            if scene.metrics_link:
                # Simulate different metrics for each scene type
                if scene.scene_type == SceneType.WARM_UP:
                    metrics = {"qps": 20, "p95": 30, "error_rate": 0.01, "bpm": 60}
                elif scene.scene_type == SceneType.BUILD_ENERGY:
                    metrics = {"qps": 50, "p95": 60, "error_rate": 0.03, "bpm": 90}
                elif scene.scene_type == SceneType.IMPACT_MOMENT:
                    metrics = {"qps": 100, "p95": 120, "error_rate": 0.08, "bpm": 120}
                else:  # COOL_DOWN
                    metrics = {"qps": 30, "p95": 40, "error_rate": 0.02, "bpm": 80}
                
                controller.update_metrics(metrics)
                print(f"📊 Metrics: QPS={metrics['qps']}, P95={metrics['p95']}ms, Error={metrics['error_rate']:.1%}, BPM={metrics['bpm']}")
            
            # Get current controls
            controls = controller.get_current_controls()
            print(f"🎛️  Controls: {controls}")
            
            # Process text if provided
            if args.text:
                # Simulate text processing with current controls
                result = simulate_text_processing(args.text, controls, scene.seed)
                print(f"✨ Result: {result}")
            
            # Wait for scene duration (in real implementation)
            print(f"⏱️  Scene duration: {scene.duration}s")
            time.sleep(0.5)  # Shortened for demo
        
        print(f"\n🎭 Showpiece Flow Complete!")
        return
    
    # Handle specific scene
    if args.scene:
        scene_config = create_scene_config(args.scene, args.seed)
        controller.load_scene(scene_config)
        print(f"🎬 Loaded Scene: {scene_config.name}")
        
        # Simulate metrics
        metrics = {"qps": 50, "p95": 60, "error_rate": 0.03, "bpm": 90}
        controller.update_metrics(metrics)
        
        # Get controls
        controls = controller.get_current_controls()
        print(f"🎛️  Controls: {controls}")
        
        # Process text if provided
        if args.text:
            result = simulate_text_processing(args.text, controls, scene_config.seed)
            print(f"✨ Result: {result}")
    
    # Handle save scene
    if args.save_scene and args.scene:
        scene_config = create_scene_config(args.scene, args.seed)
        controller.save_scene(args.save_scene, scene_config)
        print(f"💾 Scene saved to: {args.save_scene}")
    
    # Handle load scene
    if args.load_scene:
        try:
            scene_config = controller.load_scene_file(args.load_scene)
            controller.load_scene(scene_config)
            print(f"📁 Scene loaded from: {args.load_scene}")
            print(f"🎬 Scene: {scene_config.name}")
            
            # Process text if provided
            if args.text:
                controls = controller.get_current_controls()
                result = simulate_text_processing(args.text, controls, scene_config.seed)
                print(f"✨ Result: {result}")
        except Exception as e:
            print(f"❌ Error loading scene: {e}")
            return
    
    # Handle snapshot kit
    if args.snapshot_kit:
        if not args.scene:
            print("❌ Please specify a scene with --scene")
            return
        
        scene_config = create_scene_config(args.scene, args.seed)
        snapshot_kit = controller.create_snapshot_kit(scene_config)
        
        # Save snapshot kit
        output_file = f"out/snapshot_kit_{args.scene}.json"
        os.makedirs("out", exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(snapshot_kit, f, indent=2)
        
        print(f"📸 Snapshot kit created: {output_file}")
        print(f"🎬 Scene: {snapshot_kit['scene']}")
        print(f"🎲 Seed: {snapshot_kit['seed']}")
        print(f"📊 States: {list(snapshot_kit['states'].keys())}")
    
    # Show status
    status = controller.get_scene_status()
    if status.get("status") != "no_scene":
        print(f"\n📊 Scene Status:")
        print(f"🎬 Scene: {status['scene_name']}")
        print(f"⏱️  Duration: {status['duration']:.1f}s")
        print(f"🔗 Metrics Link: {status['metrics_link']}")
        print(f"♿ A11y Mode: {status['a11y_mode']}")
        print(f"🎵 Mono Mode: {status['mono_mode']}")
        print(f"🎛️  Controls: {status['controls']}")


def create_scene_config(scene_name: str, seed: int = None) -> SceneConfig:
    """Create a scene configuration based on name"""
    if seed is None:
        seed = 777
    
    scene_configs = {
        "cinemascope": SceneConfig(
            name="Cinemascope",
            scene_type=SceneType.WARM_UP,
            seed=seed,
            metrics_link=False,
            controls={"offset_px": 1.0, "fringe_px": 0.5, "trail_len": 2},
            mapping={},
            a11y_safe=True
        ),
        "neon_bloom": SceneConfig(
            name="Neon Bloom",
            scene_type=SceneType.BUILD_ENERGY,
            seed=seed,
            metrics_link=True,
            controls={"offset_px": 3.0, "fringe_px": 1.5, "trail_len": 6, "bpm": 90},
            mapping={
                "qps->offset_px": "0.06 * qps | clamp(0,8)",
                "p95->fringe_px": "(p95-20)/80 | clamp(0,3)"
            }
        ),
        "prism_burst": SceneConfig(
            name="Prism Burst",
            scene_type=SceneType.IMPACT_MOMENT,
            seed=seed,
            metrics_link=True,
            controls={"offset_px": 6.0, "fringe_px": 2.5, "trail_len": 10, "bpm": 120},
            mapping={
                "qps->offset_px": "0.08 * qps | clamp(0,8)",
                "p95->fringe_px": "(p95-20)/80 | clamp(0,3)",
                "error->broken_spectrum": "err>0.05 ? ease(2*t%1) : 0"
            },
            a11y_safe=False
        ),
        "hologram": SceneConfig(
            name="Hologram",
            scene_type=SceneType.COOL_DOWN,
            seed=seed,
            metrics_link=True,
            controls={"offset_px": 2.0, "fringe_px": 0.8, "trail_len": 4, "bpm": 80},
            mapping={
                "qps->offset_px": "0.04 * qps | clamp(0,8)",
                "p95->fringe_px": "(p95-20)/80 | clamp(0,3)"
            },
            a11y_safe=True
        )
    }
    
    return scene_configs.get(scene_name, scene_configs["cinemascope"])


def simulate_text_processing(text: str, controls: Dict[str, float], seed: int) -> str:
    """Simulate text processing with current controls"""
    import random
    random.seed(seed)
    
    # Simple simulation based on controls
    result = text
    
    # Apply offset effect
    offset = controls.get("offset_px", 0)
    if offset > 0:
        # Simulate RGB offset
        result = " ".join([f"{c} {c}" for c in result])
    
    # Apply fringe effect
    fringe = controls.get("fringe_px", 0)
    if fringe > 0:
        # Simulate fringe blur
        result = result.replace(" ", "~")
    
    # Apply trail effect
    trail_len = controls.get("trail_len", 0)
    if trail_len > 0:
        # Simulate trails
        result = result.replace("~", "~" * int(trail_len))
    
    return result


if __name__ == "__main__":
    main()
