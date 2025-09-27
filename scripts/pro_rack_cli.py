#!/usr/bin/env python3
"""
Pro Rack CLI - Professional Rack System
========================================

Command-line interface for the professional rack system.
"""

import argparse
import json
import sys
import os
import time
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the pro rack
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.pro_rack import (
    ProRack,
    RackScene,
    FXConfig,
    RoutingType,
    MacroKnobs,
    Metrics,
)


def main():
    parser = argparse.ArgumentParser(
        description="Professional Rack System - Soundtoys-for-Text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load and process with rack
  python3 scripts/pro_rack_cli.py --load presets/racks/tour_opener.rack.json --text "Code Live"

  # Apply macro knobs
  python3 scripts/pro_rack_cli.py --load presets/racks/glass_cathedral.rack.json --macros color=0.7,space=0.3

  # Sidechain from metrics
  python3 scripts/pro_rack_cli.py --load presets/racks/data_storm.rack.json --sidechain qps=50,p95=60,error_rate=0.05

  # Morph between scenes
  python3 scripts/pro_rack_cli.py --morph presets/racks/tour_opener.rack.json presets/racks/glass_cathedral.rack.json --morph-time 0.5
        """,
    )

    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--load", help="Load rack scene from JSON file")
    parser.add_argument("--save", help="Save current rack to JSON file")
    parser.add_argument(
        "--macros", help="Apply macro knobs (color=0.7,space=0.3,motion=0.5,crunch=0.8)"
    )
    parser.add_argument(
        "--sidechain",
        help="Apply sidechain from metrics (qps=50,p95=60,error_rate=0.05)",
    )
    parser.add_argument("--morph", nargs=2, help="Morph between two rack scenes")
    parser.add_argument(
        "--morph-time", type=float, default=0.5, help="Morph time (0.0-1.0)"
    )
    parser.add_argument(
        "--mode", default="raw", choices=["raw", "ansi", "html"], help="Output mode"
    )
    parser.add_argument("--output", "-o", help="Output file for HTML mode")
    parser.add_argument("--status", action="store_true", help="Show rack status")

    args = parser.parse_args()

    # Create pro rack
    rack = ProRack()

    # Handle load scene
    if args.load:
        try:
            rack.load_from_json(args.load)
            print(f"🎛️ Loaded rack scene from: {args.load}")
        except Exception as e:
            print(f"❌ Error loading rack scene: {e}")
            return
    else:
        # Create default scene
        default_scene = RackScene(
            sample="Code Live",
            fx=[
                FXConfig("distortion", 0.8, {"drive": 0.7}),
                FXConfig("neon_fx", 0.6, {"glow": 1.5}),
                FXConfig("echo", 0.4, {"delay": 0.5}),
            ],
        )
        rack.load_scene(default_scene)
        print("🎛️ Using default rack scene")

    # Handle macro knobs
    if args.macros:
        try:
            macro_dict = {}
            for macro in args.macros.split(","):
                key, value = macro.split("=")
                macro_dict[key.strip()] = float(value.strip())

            rack.apply_macros(macro_dict)
            print(f"🎛️ Applied macro knobs: {macro_dict}")
        except Exception as e:
            print(f"❌ Error applying macro knobs: {e}")
            return

    # Handle sidechain
    if args.sidechain:
        try:
            metrics_dict = {}
            for metric in args.sidechain.split(","):
                key, value = metric.split("=")
                metrics_dict[key.strip()] = float(value.strip())

            rack.sidechain(metrics_dict)
            print(f"📊 Applied sidechain: {metrics_dict}")
        except Exception as e:
            print(f"❌ Error applying sidechain: {e}")
            return

    # Handle morphing
    if args.morph:
        try:
            scene_a_path, scene_b_path = args.morph
            morph_time = args.morph_time

            # Load both scenes
            rack_a = ProRack()
            rack_a.load_from_json(scene_a_path)
            scene_a = rack_a.current_scene

            rack_b = ProRack()
            rack_b.load_from_json(scene_b_path)
            scene_b = rack_b.current_scene

            # Morph between scenes
            morphed_scene = rack.morph_to(scene_b, morph_time)
            rack.load_scene(morphed_scene)
            print(f"🎛️ Morphed between scenes (t={morph_time:.2f})")
        except Exception as e:
            print(f"❌ Error morphing scenes: {e}")
            return

    # Process text
    if args.text:
        result = rack.process(args.text, args.mode)
        print(f"✨ Result: {result}")

        # Save to file if HTML mode
        if args.mode == "html" and args.output:
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Pro Rack Result</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #0f0; }}
        .result {{ font-size: 24px; line-height: 1.5; }}
    </style>
</head>
<body>
    <div class="result">{result}</div>
</body>
</html>
            """
            with open(args.output, "w") as f:
                f.write(html_content)
            print(f"💾 HTML saved to: {args.output}")

    # Handle save
    if args.save:
        try:
            rack.save_to_json(args.save)
            print(f"💾 Rack scene saved to: {args.save}")
        except Exception as e:
            print(f"❌ Error saving rack scene: {e}")
            return

    # Show status
    if args.status or not args.text:
        status = rack.get_rack_status()
        print(f"\n📊 Rack Status:")
        print(f"🎬 Scene: {status.get('scene', 'None')}")
        print(f"🔀 Routing: {status.get('routing', 'None')}")
        print(f"🎛️ FX Count: {status.get('fx_count', 0)}")
        print(f"🎚️ Macros: {status.get('macros', {})}")
        print(f"📊 Metrics: {status.get('metrics', {})}")
        print(f"📝 Notes: {status.get('notes', 'None')}")


if __name__ == "__main__":
    main()
