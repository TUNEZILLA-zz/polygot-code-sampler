#!/usr/bin/env python3
"""
Touring Rig CLI - Professional Show Controller
==============================================

Command-line interface for the touring rig system.
"""

import argparse
import json
import sys
import os
import time
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the touring rig
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.touring_rig import TouringRig, ShowConfig, MorphCurve, MomentaryButton


def main():
    parser = argparse.ArgumentParser(
        description="Touring Rig System - Professional Show Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load and play show
  python3 scripts/touring_rig_cli.py --load presets/shows/tour_opener.show.json --play

  # Set live intensity
  python3 scripts/touring_rig_cli.py --intensity 85.5

  # Toggle momentary buttons
  python3 scripts/touring_rig_cli.py --blackout true
  python3 scripts/touring_rig_cli.py --flash-strobe true
  python3 scripts/touring_rig_cli.py --all-white-bloom true

  # Set parameters
  python3 scripts/touring_rig_cli.py --param "scenes[2].fx[1].wet" 0.42

  # Show status
  python3 scripts/touring_rig_cli.py --status
        """
    )
    
    parser.add_argument("--load", help="Load show from JSON file")
    parser.add_argument("--play", action="store_true", help="Start playing show")
    parser.add_argument("--next", action="store_true", help="Next scene")
    parser.add_argument("--jump", type=int, help="Jump to scene index")
    parser.add_argument("--intensity", type=float, help="Set live intensity (0-120%)")
    parser.add_argument("--metrics-link", type=float, help="Set metrics link strength (0-100%)")
    parser.add_argument("--blackout", type=bool, help="Toggle blackout")
    parser.add_argument("--flash-strobe", type=bool, help="Toggle flash strobe")
    parser.add_argument("--all-white-bloom", type=bool, help="Toggle all-white bloom")
    parser.add_argument("--param", nargs=2, help="Set parameter (path value)")
    parser.add_argument("--undo", action="store_true", help="Undo last action")
    parser.add_argument("--redo", action="store_true", help="Redo last action")
    parser.add_argument("--status", action="store_true", help="Show show status")
    
    args = parser.parse_args()
    
    # Create touring rig
    rig = TouringRig()
    
    # Handle load show
    if args.load:
        try:
            with open(args.load, 'r') as f:
                data = json.load(f)
            
            # Extract scene names from the show data
            scene_names = []
            for scene_data in data.get("scenes", []):
                if isinstance(scene_data, dict):
                    scene_names.append(scene_data.get("preset", "unknown"))
                else:
                    scene_names.append(str(scene_data))
            
            show = ShowConfig(
                name=data.get("name", "Untitled Show"),
                bpm=data.get("bpm", 110.0),
                scenes=scene_names,
                intensity=data.get("intensity", 100.0),
                metrics_link_strength=data.get("metrics_link_strength", 100.0)
            )
            
            rig.load_show(show)
            print(f"🎭 Loaded show: {show.name}")
            print(f"🎬 Scenes: {len(show.scenes)}")
            print(f"🎵 BPM: {show.bpm}")
            
        except Exception as e:
            print(f"❌ Error loading show: {e}")
            return
    else:
        # Create default show
        default_show = ShowConfig(
            name="Default Show",
            bpm=110.0,
            scenes=["scene1", "scene2", "scene3"],
            intensity=100.0,
            metrics_link_strength=100.0
        )
        rig.load_show(default_show)
        print("🎭 Using default show")
    
    # Handle play show
    if args.play:
        try:
            rig.play_show()
            print("▶️  Show started!")
        except Exception as e:
            print(f"❌ Error playing show: {e}")
            return
    
    # Handle next scene
    if args.next:
        try:
            rig.next_scene()
            print("⏭️  Advanced to next scene")
        except Exception as e:
            print(f"❌ Error advancing scene: {e}")
            return
    
    # Handle jump to scene
    if args.jump is not None:
        try:
            rig.jump_to_scene(args.jump)
            print(f"🎬 Jumped to scene: {args.jump}")
        except Exception as e:
            print(f"❌ Error jumping to scene: {e}")
            return
    
    # Handle live intensity
    if args.intensity is not None:
        try:
            rig.set_live_intensity(args.intensity)
            print(f"🎛️ Live intensity set to: {args.intensity}%")
        except Exception as e:
            print(f"❌ Error setting intensity: {e}")
            return
    
    # Handle metrics link strength
    if args.metrics_link is not None:
        try:
            rig.set_metrics_link_strength(args.metrics_link)
            print(f"📊 Metrics link strength set to: {args.metrics_link}%")
        except Exception as e:
            print(f"❌ Error setting metrics link: {e}")
            return
    
    # Handle momentary buttons
    if args.blackout is not None:
        try:
            rig.toggle_blackout(args.blackout)
            print(f"🌑 Blackout: {'ON' if args.blackout else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling blackout: {e}")
            return
    
    if args.flash_strobe is not None:
        try:
            rig.toggle_flash_strobe(args.flash_strobe)
            print(f"⚡ Flash strobe: {'ON' if args.flash_strobe else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling flash strobe: {e}")
            return
    
    if args.all_white_bloom is not None:
        try:
            rig.toggle_all_white_bloom(args.all_white_bloom)
            print(f"💡 All-white bloom: {'ON' if args.all_white_bloom else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling all-white bloom: {e}")
            return
    
    # Handle parameter setting
    if args.param:
        try:
            path, value = args.param
            rig.set_parameter(path, float(value))
            print(f"🎛️ Parameter set: {path} = {value}")
        except Exception as e:
            print(f"❌ Error setting parameter: {e}")
            return
    
    # Handle undo/redo
    if args.undo:
        try:
            if rig.undo():
                print("↶ Undo successful")
            else:
                print("❌ Nothing to undo")
        except Exception as e:
            print(f"❌ Error undoing: {e}")
            return
    
    if args.redo:
        try:
            if rig.redo():
                print("↷ Redo successful")
            else:
                print("❌ Nothing to redo")
        except Exception as e:
            print(f"❌ Error redoing: {e}")
            return
    
    # Show status
    if args.status or not any([args.play, args.next, args.jump, args.intensity, args.metrics_link, 
                              args.blackout, args.flash_strobe, args.all_white_bloom, args.param, 
                              args.undo, args.redo]):
        status = rig.get_show_status()
        if status.get("status") == "no_show":
            print("📊 No show loaded")
        else:
            print(f"\n📊 Touring Rig Status:")
            print(f"🎭 Show: {status.get('show_name', 'None')}")
            print(f"🎵 BPM: {status.get('bpm', 0)}")
            print(f"🎬 Scenes: {status.get('scenes', 0)}")
            print(f"🎬 Current Scene: {status.get('current_scene', 0)}")
            print(f"▶️  Playing: {status.get('is_playing', False)}")
            print(f"🎛️ Live Intensity: {status.get('live_intensity', 0)}%")
            print(f"📊 Metrics Link: {status.get('metrics_link_enabled', False)}")
            print(f"📊 Link Strength: {status.get('metrics_link_strength', 0)}%")
            print(f"♿ Motion Reduced: {status.get('motion_reduced', False)}")
            print(f"🔥 Heat Guard: {status.get('heat_guard_active', False)}")
            print(f"🎚️ Quality Level: {status.get('quality_level', 0)}")
            
            # Show clock
            clock = status.get('show_clock', {})
            print(f"⏱️  Show Elapsed: {clock.get('elapsed', 0):.1f}s")
            print(f"⏱️  Show Remaining: {clock.get('remaining', 0):.1f}s")
            print(f"⏱️  Scene Elapsed: {clock.get('scene_elapsed', 0):.1f}s")
            print(f"⏱️  Scene Remaining: {clock.get('scene_remaining', 0):.1f}s")
            
            # Momentary states
            momentary = status.get('momentary_states', {})
            print(f"🌑 Blackout: {momentary.get('blackout', False)}")
            print(f"⚡ Flash Strobe: {momentary.get('flash_strobe', False)}")
            print(f"💡 All-White Bloom: {momentary.get('all_white_bloom', False)}")
            
            # Strobe state
            strobe = status.get('strobe_state', {})
            print(f"⚡ Strobe Enabled: {strobe.get('enabled', False)}")
            print(f"⚡ Strobe On: {strobe.get('is_on', False)}")
            
            # Current metrics
            metrics = status.get('current_metrics', {})
            print(f"📊 QPS: {metrics.get('qps', 0)}")
            print(f"📊 P95: {metrics.get('p95', 0)}ms")
            print(f"📊 Error Rate: {metrics.get('error_rate', 0):.1%}")
            print(f"📊 CPU: {metrics.get('cpu_percent', 0)}%")
            print(f"📊 Frame Time: {metrics.get('frame_time_ms', 0)}ms")


if __name__ == "__main__":
    main()
