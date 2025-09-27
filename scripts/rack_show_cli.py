#!/usr/bin/env python3
"""
Rack Show CLI - One-Command Rack Shows
======================================

Command-line interface for the rack show system.
"""

import argparse
import json
import sys
import os
import time
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the rack show
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.rack_show import RackShowEngine, RackShow, ShowScene


def main():
    parser = argparse.ArgumentParser(
        description="Rack Show System - One-Command Rack Shows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Play a rack show
  python3 scripts/rack_show_cli.py --play presets/shows/tour_opener.show.json --text "Code Live"

  # Create a new show
  python3 scripts/rack_show_cli.py --create "My Show" --scenes tour_opener.rack.json,glass_cathedral.rack.json

  # Record show with HTML
  python3 scripts/rack_show_cli.py --play presets/shows/tour_opener.show.json --record-html --text "TuneZilla"
        """,
    )

    parser.add_argument("--play", help="Play a rack show from JSON file")
    parser.add_argument("--create", help="Create a new rack show")
    parser.add_argument(
        "--scenes", help="Comma-separated list of rack scenes for new show"
    )
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--record-html", action="store_true", help="Record HTML output")
    parser.add_argument(
        "--record-webm", action="store_true", help="Record animated WebM"
    )
    parser.add_argument(
        "--output-dir", default="out/rack_shows", help="Output directory"
    )
    parser.add_argument("--status", action="store_true", help="Show show status")

    args = parser.parse_args()

    # Create rack show engine
    engine = RackShowEngine()

    # Set recording options
    if args.record_html:
        engine.record_html = True
    if args.record_webm:
        engine.record_webm = True
    if args.output_dir:
        engine.output_dir = args.output_dir

    # Handle play show
    if args.play:
        try:
            engine.load_show_from_json(args.play)
            print(f"🎭 Loaded rack show from: {args.play}")

            # Play the show
            text = args.text or "Code Live"
            result = engine.play_show(text)

            print(f"🎭 Show complete!")
            print(f"📁 Show ID: {result['show_id']}")
            print(f"📁 Show Directory: {result['show_dir']}")
            print(f"⏱️  Total Duration: {result['total_duration']:.2f}s")
            print(f"🎬 Scenes: {len(result['scenes'])}")

            if engine.record_html:
                print(f"💾 HTML recorded to: {result['show_dir']}/show.html")
                print(
                    f"💾 Chromascene saved to: {result['show_dir']}/show.chromascene.json"
                )

        except Exception as e:
            print(f"❌ Error playing show: {e}")
            return

    # Handle create show
    if args.create:
        try:
            if not args.scenes:
                print("❌ Please specify scenes with --scenes")
                return

            # Parse scenes
            scene_files = [s.strip() for s in args.scenes.split(",")]
            scenes = []

            for i, scene_file in enumerate(scene_files):
                scene = ShowScene(
                    preset=scene_file,
                    duration=10.0 + i * 2.0,  # Vary duration
                    morph=2.0,
                    notes=f"Scene {i+1} from {scene_file}",
                )
                scenes.append(scene)

            # Create show
            show = RackShow(name=args.create, bpm=110.0, scenes=scenes)

            # Save show
            show_file = (
                f"presets/shows/{args.create.lower().replace(' ', '_')}.show.json"
            )
            os.makedirs("presets/shows", exist_ok=True)
            engine.save_show_to_json(show_file)

            print(f"🎭 Created rack show: {args.create}")
            print(f"💾 Saved to: {show_file}")
            print(f"🎬 Scenes: {len(scenes)}")
            print(f"⏱️  Total Duration: {show.total_duration}s")

        except Exception as e:
            print(f"❌ Error creating show: {e}")
            return

    # Show status
    if args.status or not args.play:
        status = engine.get_show_status()
        if status.get("status") == "no_show":
            print("📊 No show loaded")
        else:
            print(f"\n📊 Show Status:")
            print(f"🎭 Show: {status.get('show_name', 'None')}")
            print(f"🎵 BPM: {status.get('bpm', 0)}")
            print(f"⏱️  Duration: {status.get('total_duration', 0)}s")
            print(f"🎬 Scenes: {status.get('scenes', 0)}")
            print(f"🎬 Current Scene: {status.get('current_scene', 0)}")
            print(f"▶️  Playing: {status.get('is_playing', False)}")
            if status.get("is_playing"):
                print(f"⏱️  Elapsed: {status.get('elapsed_time', 0):.1f}s")


if __name__ == "__main__":
    main()
