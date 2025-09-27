#!/usr/bin/env python3
"""
🎛️ Code Live - Audio Effects CLI
================================

Command-line interface for applying audio effects to code loops.
Like a digital audio workstation (DAW) for code generation!
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from pcs.audio_fx import AudioFxEngine


class AudioFxCLI:
    """CLI interface for audio effects"""

    def __init__(self):
        self.engine = AudioFxEngine()

    def list_effects(self):
        """List all available audio effects"""
        print("🎛️ Code Live - Audio Effects")
        print("=" * 50)
        print("Available audio effects:")
        print()

        effects_info = {
            "reverb": {
                "description": "Add decaying echoes of previous iterations",
                "params": ["reverb_taps", "reverb_decay"],
                "example": "--fx reverb --reverb-taps 3 --reverb-decay 0.6",
            },
            "delay": {
                "description": "Offset processing by N steps",
                "params": ["delay_steps", "delay_extend_loop"],
                "example": "--fx delay --delay-steps 3",
            },
            "reverse": {
                "description": "Iterate in reverse order",
                "params": [],
                "example": "--fx reverse",
            },
            "chorus": {
                "description": "Add multiple voices with slight variations",
                "params": ["chorus_voices", "chorus_jitter"],
                "example": "--fx chorus --chorus-voices 3 --chorus-jitter 0.05",
            },
            "distortion": {
                "description": "Saturate/clip values for overdrive effect",
                "params": ["distortion_gain", "distortion_clip"],
                "example": "--fx distortion --distortion-gain 2.5 --distortion-clip 1.0",
            },
            "lfo": {
                "description": "Modulate parameters with sine wave",
                "params": ["lfo_target", "lfo_freq", "lfo_depth"],
                "example": "--fx lfo --lfo-freq 0.5 --lfo-depth 0.3",
            },
            "swing": {
                "description": "Alternate timing patterns (60/40 swing)",
                "params": ["swing_ratio"],
                "example": "--fx swing --swing-ratio 0.6",
            },
            "gate": {
                "description": "Skip iterations under threshold",
                "params": ["gate_threshold"],
                "example": "--fx gate --gate-threshold 0.1",
            },
        }

        for fx, info in effects_info.items():
            print(f"🎵 {fx.upper()}")
            print(f"   {info['description']}")
            if info["params"]:
                print(f"   Parameters: {', '.join(info['params'])}")
            print(f"   Example: {info['example']}")
            print()

    def apply_effects(
        self,
        code: str,
        fx_chain: List[str],
        params: Dict[str, Any],
        output_file: Optional[str] = None,
    ):
        """Apply audio effects to code"""
        print(f"🎛️ Applying Audio Effects: {', '.join(fx_chain)}")
        print("=" * 50)

        # Create FX specification
        fx_spec = self.engine.create_fx_spec(fx_chain, params)

        # Validate effects
        is_valid, issues = self.engine.validate_fx_spec(fx_spec)
        if not is_valid:
            print("❌ Effects validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            return

        print("✅ Effects validation passed")

        # Apply effects
        try:
            result_code = self.engine.apply_fx_to_code(code, fx_spec)

            print("\nOriginal code:")
            print("-" * 30)
            print(code)

            print("\nProcessed code:")
            print("-" * 30)
            print(result_code)

            # Save to file if specified
            if output_file:
                with open(output_file, "w") as f:
                    f.write(result_code)
                print(f"\n💾 Saved to {output_file}")

            # Show effect details
            print("\n🎚️ Effect Details:")
            for fx in fx_chain:
                print(f"   - {fx}: {self._get_fx_description(fx)}")

        except Exception as e:
            print(f"❌ Error applying effects: {e}")

    def demo_effects(self):
        """Demonstrate audio effects on sample code"""
        print("🎛️ Code Live - Audio Effects Demo")
        print("=" * 50)

        # Sample code
        sample_code = """
for i in range(8):
    process(i)
"""

        print("Sample code:")
        print(sample_code.strip())
        print()

        # Demo individual effects
        demos = [
            {
                "name": "Reverb Effect",
                "fx": ["reverb"],
                "params": {"reverb_taps": 3, "reverb_decay": 0.6},
            },
            {
                "name": "Delay Effect",
                "fx": ["delay"],
                "params": {"delay_steps": 3, "delay_extend_loop": True},
            },
            {"name": "Reverse Effect", "fx": ["reverse"], "params": {}},
            {
                "name": "Chorus Effect",
                "fx": ["chorus"],
                "params": {"chorus_voices": 3, "chorus_jitter": 0.05},
            },
            {
                "name": "Distortion Effect",
                "fx": ["distortion"],
                "params": {"distortion_gain": 2.5, "distortion_clip": 1.0},
            },
            {
                "name": "LFO Modulation",
                "fx": ["lfo"],
                "params": {
                    "lfo_target": "param:alpha",
                    "lfo_freq": 0.5,
                    "lfo_depth": 0.3,
                },
            },
            {"name": "Swing Groove", "fx": ["swing"], "params": {"swing_ratio": 0.6}},
            {"name": "Gate Filter", "fx": ["gate"], "params": {"gate_threshold": 0.1}},
        ]

        for demo in demos:
            print(f"\n🎵 {demo['name']}")
            print("-" * 30)
            self.apply_effects(sample_code, demo["fx"], demo["params"])
            print()

        # Demo effect chains
        print("\n🎵 Effect Chains")
        print("-" * 30)

        chains = [
            {
                "name": "Reverse + Reverb",
                "fx": ["reverse", "reverb"],
                "params": {"reverb_taps": 2, "reverb_decay": 0.5},
            },
            {
                "name": "Delay + Chorus",
                "fx": ["delay", "chorus"],
                "params": {"delay_steps": 2, "chorus_voices": 2, "chorus_jitter": 0.03},
            },
            {
                "name": "Distortion + LFO",
                "fx": ["distortion", "lfo"],
                "params": {"distortion_gain": 3.0, "lfo_freq": 0.8, "lfo_depth": 0.4},
            },
        ]

        for chain in chains:
            print(f"\n🔗 {chain['name']}")
            print("-" * 20)
            self.apply_effects(sample_code, chain["fx"], chain["params"])
            print()

    def generate_fx_presets(self, output_file: str = "audio_fx_presets.json"):
        """Generate audio effects presets"""
        print("🎛️ Generating Audio Effects Presets")
        print("=" * 50)

        presets = {
            "vintage_sampler": {
                "description": "Classic 80s sampler vibes",
                "fx_chain": ["reverse", "reverb", "distortion"],
                "params": {
                    "reverb_taps": 4,
                    "reverb_decay": 0.7,
                    "distortion_gain": 2.0,
                    "distortion_clip": 0.8,
                },
            },
            "modern_daw": {
                "description": "Modern DAW processing",
                "fx_chain": ["delay", "chorus", "lfo"],
                "params": {
                    "delay_steps": 2,
                    "chorus_voices": 4,
                    "chorus_jitter": 0.02,
                    "lfo_freq": 0.3,
                    "lfo_depth": 0.2,
                },
            },
            "crunchy_loops": {
                "description": "Aggressive processing",
                "fx_chain": ["distortion", "gate", "swing"],
                "params": {
                    "distortion_gain": 4.0,
                    "distortion_clip": 0.5,
                    "gate_threshold": 0.3,
                    "swing_ratio": 0.7,
                },
            },
            "ambient_processing": {
                "description": "Smooth ambient effects",
                "fx_chain": ["reverb", "delay", "lfo"],
                "params": {
                    "reverb_taps": 6,
                    "reverb_decay": 0.8,
                    "delay_steps": 4,
                    "lfo_freq": 0.1,
                    "lfo_depth": 0.1,
                },
            },
            "rhythmic_groove": {
                "description": "Rhythmic processing",
                "fx_chain": ["swing", "gate", "chorus"],
                "params": {
                    "swing_ratio": 0.65,
                    "gate_threshold": 0.2,
                    "chorus_voices": 3,
                    "chorus_jitter": 0.04,
                },
            },
        }

        with open(output_file, "w") as f:
            json.dump(presets, f, indent=2)

        print(f"🎨 Generated {len(presets)} audio effects presets")
        print(f"💾 Saved to {output_file}")

        for name, preset in presets.items():
            print(f"\n🎵 {name.replace('_', ' ').title()}")
            print(f"   {preset['description']}")
            print(f"   Effects: {', '.join(preset['fx_chain'])}")

    def _get_fx_description(self, fx: str) -> str:
        """Get description for an audio effect"""
        descriptions = {
            "reverb": "Adds decaying echoes",
            "delay": "Offsets processing by steps",
            "reverse": "Iterates in reverse order",
            "chorus": "Adds multiple voices",
            "distortion": "Saturates/clips values",
            "lfo": "Modulates with sine wave",
            "swing": "Alternates timing patterns",
            "gate": "Skips low values",
        }
        return descriptions.get(fx, "Unknown effect")

    def load_preset(self, preset_file: str, preset_name: str) -> Optional[Dict]:
        """Load a preset from file"""
        try:
            with open(preset_file) as f:
                presets = json.load(f)
            return presets.get(preset_name)
        except Exception as e:
            print(f"❌ Error loading preset: {e}")
            return None


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Code Live - Audio Effects CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audio_fx_cli.py list
  python audio_fx_cli.py apply --fx "reverb,delay" --reverb-taps 3 --delay-steps 2
  python audio_fx_cli.py demo
  python audio_fx_cli.py presets
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List effects command
    subparsers.add_parser("list", help="List all available audio effects")

    # Apply effects command
    apply_parser = subparsers.add_parser("apply", help="Apply audio effects to code")
    apply_parser.add_argument(
        "--fx", required=True, help="Comma-separated list of effects"
    )
    apply_parser.add_argument("--code", help="Code to process (or read from stdin)")
    apply_parser.add_argument("--output", help="Output file")

    # Effect parameters
    apply_parser.add_argument("--reverb-taps", type=int, default=3, help="Reverb taps")
    apply_parser.add_argument(
        "--reverb-decay", type=float, default=0.6, help="Reverb decay"
    )
    apply_parser.add_argument("--delay-steps", type=int, default=3, help="Delay steps")
    apply_parser.add_argument(
        "--delay-extend-loop", action="store_true", help="Extend loop for delay"
    )
    apply_parser.add_argument(
        "--chorus-voices", type=int, default=3, help="Chorus voices"
    )
    apply_parser.add_argument(
        "--chorus-jitter", type=float, default=0.05, help="Chorus jitter"
    )
    apply_parser.add_argument(
        "--distortion-gain", type=float, default=2.5, help="Distortion gain"
    )
    apply_parser.add_argument(
        "--distortion-clip", type=float, default=1.0, help="Distortion clip"
    )
    apply_parser.add_argument("--lfo-target", default="param:alpha", help="LFO target")
    apply_parser.add_argument(
        "--lfo-freq", type=float, default=0.5, help="LFO frequency"
    )
    apply_parser.add_argument("--lfo-depth", type=float, default=0.3, help="LFO depth")
    apply_parser.add_argument(
        "--swing-ratio", type=float, default=0.6, help="Swing ratio"
    )
    apply_parser.add_argument(
        "--gate-threshold", type=float, default=0.1, help="Gate threshold"
    )

    # Demo command
    subparsers.add_parser("demo", help="Demonstrate audio effects")

    # Presets command
    presets_parser = subparsers.add_parser(
        "presets", help="Generate audio effects presets"
    )
    presets_parser.add_argument(
        "--output", default="audio_fx_presets.json", help="Output file"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = AudioFxCLI()

    if args.command == "list":
        cli.list_effects()
    elif args.command == "apply":
        # Get code from stdin or argument
        if args.code:
            code = args.code
        else:
            print("Enter code (end with Ctrl+D):")
            code = sys.stdin.read()

        # Parse effects
        fx_chain = [fx.strip() for fx in args.fx.split(",")]

        # Build parameters
        params = {
            "reverb_taps": args.reverb_taps,
            "reverb_decay": args.reverb_decay,
            "delay_steps": args.delay_steps,
            "delay_extend_loop": args.delay_extend_loop,
            "chorus_voices": args.chorus_voices,
            "chorus_jitter": args.chorus_jitter,
            "distortion_gain": args.distortion_gain,
            "distortion_clip": args.distortion_clip,
            "lfo_target": args.lfo_target,
            "lfo_freq": args.lfo_freq,
            "lfo_depth": args.lfo_depth,
            "swing_ratio": args.swing_ratio,
            "gate_threshold": args.gate_threshold,
        }

        cli.apply_effects(code, fx_chain, params, args.output)
    elif args.command == "demo":
        cli.demo_effects()
    elif args.command == "presets":
        cli.generate_fx_presets(args.output)


if __name__ == "__main__":
    main()
