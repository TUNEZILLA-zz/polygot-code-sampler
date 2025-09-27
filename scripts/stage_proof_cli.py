#!/usr/bin/env python3
"""
Stage-Proof CLI - Soundtoys-for-Text
====================================

Command-line interface for the stage-proof system.
"""

import argparse
import json
import sys
import os
import time
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the stage-proof engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.stage_proof import StageProofEngine, SceneConfig, RoutingType, CurveType


def main():
    parser = argparse.ArgumentParser(
        description="Stage-Proof System - Soundtoys-for-Text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load and process scene
  python3 scripts/stage_proof_cli.py --load presets/scenes/tour_opener.json --text "Code Live"

  # Run acceptance test
  python3 scripts/stage_proof_cli.py --acceptance-test

  # Set global intensity
  python3 scripts/stage_proof_cli.py --intensity 85.5

  # Toggle momentary buttons
  python3 scripts/stage_proof_cli.py --blackout true
  python3 scripts/stage_proof_cli.py --white-bloom true
  python3 scripts/stage_proof_cli.py --lightning-flash true

  # Show status
  python3 scripts/stage_proof_cli.py --status
        """,
    )

    parser.add_argument("--load", help="Load scene from JSON file")
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument(
        "--acceptance-test", action="store_true", help="Run acceptance test"
    )
    parser.add_argument("--intensity", type=float, help="Set global intensity (0-120%)")
    parser.add_argument("--blackout", type=bool, help="Toggle blackout")
    parser.add_argument("--white-bloom", type=bool, help="Toggle white bloom")
    parser.add_argument("--lightning-flash", type=bool, help="Toggle lightning flash")
    parser.add_argument("--status", action="store_true", help="Show engine status")

    args = parser.parse_args()

    # Create stage-proof engine
    engine = StageProofEngine()

    # Handle load scene
    if args.load:
        try:
            engine.load_scene_from_json(args.load)
            print(f"🎛️ Loaded scene from: {args.load}")
        except Exception as e:
            print(f"❌ Error loading scene: {e}")
            return
    else:
        # Create default scene
        default_scene = SceneConfig(
            id="default_scene",
            seed=4242,
            routing=RoutingType.SERIAL,
            macros={"color": 0.5, "space": 0.5, "motion": 0.5, "crunch": 0.5},
            fx=[
                {
                    "type": "distortion",
                    "drive": 0.7,
                    "tone": 0.6,
                    "mix": 0.5,
                    "bypass": False,
                },
                {
                    "type": "chorus",
                    "depth": 0.35,
                    "rate_hz": 0.2,
                    "width": 0.8,
                    "mix": 0.7,
                },
                {
                    "type": "echo",
                    "time_ms": 180,
                    "feedback": 0.35,
                    "color": 0.4,
                    "mix": 0.4,
                },
            ],
        )
        engine.load_scene(default_scene)
        print("🎛️ Using default scene")

    # Handle acceptance test
    if args.acceptance_test:
        try:
            print("🧪 Running 10-minute acceptance test...")
            results = engine.run_acceptance_test()

            print(f"\n📊 Acceptance Test Results:")
            for test_name, test_result in results.items():
                status = (
                    "✅ PASSED" if test_result.get("passed", False) else "❌ FAILED"
                )
                print(f"  {test_name}: {status}")

                if "param_jumps" in test_result:
                    print(f"    Param jumps: {test_result['param_jumps']}")
                if "frame_time_ms" in test_result:
                    print(f"    Frame time: {test_result['frame_time_ms']:.2f}ms")
                if "fade_time_ms" in test_result:
                    print(f"    Fade time: {test_result['fade_time_ms']:.2f}ms")

            # Overall result
            all_passed = all(result.get("passed", False) for result in results.values())
            print(
                f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}"
            )

        except Exception as e:
            print(f"❌ Error running acceptance test: {e}")
            return

    # Handle global intensity
    if args.intensity is not None:
        try:
            engine.set_global_intensity(args.intensity)
            print(f"🎛️ Global intensity set to: {args.intensity}%")
        except Exception as e:
            print(f"❌ Error setting intensity: {e}")
            return

    # Handle momentary buttons
    if args.blackout is not None:
        try:
            engine.toggle_momentary_button("blackout", args.blackout)
            print(f"🌑 Blackout: {'ON' if args.blackout else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling blackout: {e}")
            return

    if args.white_bloom is not None:
        try:
            engine.toggle_momentary_button("white_bloom", args.white_bloom)
            print(f"💡 White bloom: {'ON' if args.white_bloom else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling white bloom: {e}")
            return

    if args.lightning_flash is not None:
        try:
            engine.toggle_momentary_button("lightning_flash", args.lightning_flash)
            print(f"⚡ Lightning flash: {'ON' if args.lightning_flash else 'OFF'}")
        except Exception as e:
            print(f"❌ Error toggling lightning flash: {e}")
            return

    # Process text
    if args.text:
        try:
            result = engine.apply_rack(args.text, engine.current_scene)
            print(f"✨ Result: {result}")
        except Exception as e:
            print(f"❌ Error processing text: {e}")
            return

    # Show status
    if args.status or not any(
        [
            args.load,
            args.text,
            args.acceptance_test,
            args.intensity,
            args.blackout,
            args.white_bloom,
            args.lightning_flash,
        ]
    ):
        status = engine.get_engine_status()
        print(f"\n📊 Stage-Proof Engine Status:")
        print(f"🎛️ Global Intensity: {status.get('global_intensity', 0)}%")
        print(
            f"🌑 Blackout: {status.get('momentary_buttons', {}).get('blackout', False)}"
        )
        print(
            f"💡 White Bloom: {status.get('momentary_buttons', {}).get('white_bloom', False)}"
        )
        print(
            f"⚡ Lightning Flash: {status.get('momentary_buttons', {}).get('lightning_flash', False)}"
        )
        print(f"🔥 Frame Budget Active: {status.get('frame_budget_active', False)}")
        print(f"🎹 MIDI Binds: {status.get('midi_binds', 0)}")
        print(f"🌐 OSC Binds: {status.get('osc_binds', 0)}")
        print(f"🎬 Current Scene: {status.get('current_scene', 'None')}")
        print(f"🎭 Current Show: {status.get('current_show', 'None')}")

        # Show guardrails
        guardrails = status.get("guardrails", {})
        print(f"\n🛡️ Guardrails:")
        print(f"  Strobe Hz Max: {guardrails.get('strobe_hz_max', 0)}")
        print(f"  Strobe On Time Min: {guardrails.get('strobe_on_time_min_ms', 0)}ms")
        print(f"  Frame P95 Cap: {guardrails.get('frame_ms_p95_cap', 0)}ms")
        print(f"  Param Slew Max: {guardrails.get('param_slew_max', 0)}")
        print(f"  Motion Fade Time: {guardrails.get('motion_fade_time_ms', 0)}ms")


if __name__ == "__main__":
    main()
