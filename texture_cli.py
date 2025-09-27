#!/usr/bin/env python3
"""
🎨 Code Live - Texture CLI
==========================

Command-line interface for texture mode transformations.
Conceptual textures for code transformation aesthetics.
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from pcs.texture_mode import TextureEngine, TextureType, TextureParams


class TextureCLI:
    """CLI interface for texture transformations"""

    def __init__(self):
        self.engine = TextureEngine()

    def list_textures(self):
        """List all available texture types"""
        print("🎨 Code Live - Texture Mode")
        print("=" * 50)
        print("Available texture types:")
        print()

        descriptions = self.engine.get_texture_descriptions()
        for texture, description in descriptions.items():
            print(f"🎨 {texture.upper()}")
            print(f"   {description}")
            print()

    def apply_texture(
        self,
        code: str,
        texture_type: str,
        params: Dict[str, Any],
        output_file: Optional[str] = None,
    ):
        """Apply texture transformation to code"""
        print(f"🎨 Applying {texture_type} texture")
        print("=" * 50)

        # Create texture parameters
        texture_params = TextureParams(
            dense_nesting_level=params.get("dense_nesting_level", 3),
            dense_comprehensions=params.get("dense_comprehensions", True),
            sparse_minimal=params.get("sparse_minimal", True),
            sparse_flat=params.get("sparse_flat", True),
            smooth_vectorized=params.get("smooth_vectorized", True),
            smooth_interpolation=params.get("smooth_interpolation", True),
            grainy_jitter=params.get("grainy_jitter", 0.1),
            grainy_stepwise=params.get("grainy_stepwise", True),
            polyphonic_voices=params.get("polyphonic_voices", 3),
            polyphonic_harmony=params.get("polyphonic_harmony", True),
            minimal_lines=params.get("minimal_lines", 3),
            maximal_decorators=params.get("maximal_decorators", True),
            maximal_abstractions=params.get("maximal_abstractions", True),
            maximal_parallel=params.get("maximal_parallel", True),
            fractal_depth=params.get("fractal_depth", 3),
            fractal_branches=params.get("fractal_branches", 2),
        )

        print("✅ Texture parameters validated")

        # Apply texture
        try:
            result_code = self.engine.apply_texture(
                code, TextureType(texture_type), texture_params
            )

            print("\nOriginal code:")
            print("-" * 30)
            print(code)

            print("\nTextured code:")
            print("-" * 30)
            print(result_code)

            # Save to file if specified
            if output_file:
                with open(output_file, "w") as f:
                    f.write(result_code)
                print(f"\n💾 Saved to {output_file}")

            # Show texture details
            print(f"\n🎨 Texture Details:")
            print(f"   Type: {texture_type}")
            print(
                f"   Description: {self.engine.get_texture_descriptions().get(texture_type, 'Unknown')}"
            )

            # Show visual effects
            visual_effects = self.engine.get_texture_visual_effects(
                TextureType(texture_type)
            )
            print(
                f"   Visual: {visual_effects.get('particle_behavior', 'unknown')} ({visual_effects.get('color', 'unknown')})"
            )

        except Exception as e:
            print(f"❌ Error applying texture: {e}")

    def demo_textures(self):
        """Demonstrate texture transformations"""
        print("🎨 Code Live - Texture Mode Demo")
        print("=" * 50)

        # Sample code
        sample_code = """
for i in range(8):
    process(i)
"""

        print("Sample code:")
        print(sample_code.strip())
        print()

        # Demo individual textures
        demos = [
            {
                "name": "Dense Texture",
                "texture": "dense",
                "params": {"dense_nesting_level": 3, "dense_comprehensions": True},
            },
            {
                "name": "Sparse Texture",
                "texture": "sparse",
                "params": {"sparse_minimal": True, "sparse_flat": True},
            },
            {
                "name": "Smooth Texture",
                "texture": "smooth",
                "params": {"smooth_vectorized": True, "smooth_interpolation": True},
            },
            {
                "name": "Grainy Texture",
                "texture": "grainy",
                "params": {"grainy_jitter": 0.1, "grainy_stepwise": True},
            },
            {
                "name": "Polyphonic Texture",
                "texture": "polyphonic",
                "params": {"polyphonic_voices": 3, "polyphonic_harmony": True},
            },
            {
                "name": "Minimal Texture",
                "texture": "minimal",
                "params": {"minimal_lines": 3},
            },
            {
                "name": "Maximal Texture",
                "texture": "maximal",
                "params": {"maximal_decorators": True, "maximal_parallel": True},
            },
            {
                "name": "Fractal Texture",
                "texture": "fractal",
                "params": {"fractal_depth": 3, "fractal_branches": 2},
            },
        ]

        for demo in demos:
            print(f"\n🎨 {demo['name']}")
            print("-" * 30)
            self.apply_texture(sample_code, demo["texture"], demo["params"])
            print()

    def generate_texture_presets(self, output_file: str = "texture_presets.json"):
        """Generate texture presets"""
        print("🎨 Generating Texture Presets")
        print("=" * 50)

        presets = {
            "musical_dense": {
                "description": "Musical dense texture with harmonic relationships",
                "texture": "dense",
                "params": {"dense_nesting_level": 4, "dense_comprehensions": True},
            },
            "minimalist_sparse": {
                "description": "Minimalist sparse texture for clean aesthetics",
                "texture": "sparse",
                "params": {"sparse_minimal": True, "sparse_flat": True},
            },
            "smooth_vectorized": {
                "description": "Smooth vectorized texture for mathematical elegance",
                "texture": "smooth",
                "params": {"smooth_vectorized": True, "smooth_interpolation": True},
            },
            "grainy_organic": {
                "description": "Grainy organic texture for natural feel",
                "texture": "grainy",
                "params": {"grainy_jitter": 0.15, "grainy_stepwise": True},
            },
            "polyphonic_harmony": {
                "description": "Polyphonic harmony texture for musical complexity",
                "texture": "polyphonic",
                "params": {"polyphonic_voices": 4, "polyphonic_harmony": True},
            },
            "haiku_minimal": {
                "description": "Haiku minimal texture for poetic simplicity",
                "texture": "minimal",
                "params": {"minimal_lines": 2},
            },
            "maximal_abstraction": {
                "description": "Maximal abstraction texture for complex systems",
                "texture": "maximal",
                "params": {
                    "maximal_decorators": True,
                    "maximal_abstractions": True,
                    "maximal_parallel": True,
                },
            },
            "fractal_recursive": {
                "description": "Fractal recursive texture for self-similar patterns",
                "texture": "fractal",
                "params": {"fractal_depth": 4, "fractal_branches": 3},
            },
        }

        with open(output_file, "w") as f:
            json.dump(presets, f, indent=2)

        print(f"🎨 Generated {len(presets)} texture presets")
        print(f"💾 Saved to {output_file}")

        for name, preset in presets.items():
            print(f"\n🎨 {name.replace('_', ' ').title()}")
            print(f"   {preset['description']}")
            print(f"   Texture: {preset['texture']}")

    def show_visual_effects(self):
        """Show visual effects for all textures"""
        print("🎨 Texture Visual Effects")
        print("=" * 50)

        for texture_type in TextureType:
            effects = self.engine.get_texture_visual_effects(texture_type)
            print(f"\n🎨 {texture_type.value.upper()}")
            print(
                f"   Particle Behavior: {effects.get('particle_behavior', 'unknown')}"
            )
            print(f"   Movement: {effects.get('movement', 'unknown')}")
            print(f"   Density: {effects.get('density', 'unknown')}")
            print(f"   Color: {effects.get('color', 'unknown')}")

    def _get_texture_description(self, texture: str) -> str:
        """Get description for a texture type"""
        descriptions = self.engine.get_texture_descriptions()
        return descriptions.get(texture, "Unknown texture")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Code Live - Texture CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python texture_cli.py list
  python texture_cli.py apply --texture dense --dense-nesting-level 4
  python texture_cli.py demo
  python texture_cli.py presets
  python texture_cli.py visual-effects
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List textures command
    subparsers.add_parser("list", help="List all available texture types")

    # Apply texture command
    apply_parser = subparsers.add_parser(
        "apply", help="Apply texture transformation to code"
    )
    apply_parser.add_argument("--texture", required=True, help="Texture type to apply")
    apply_parser.add_argument("--code", help="Code to process (or read from stdin)")
    apply_parser.add_argument("--output", help="Output file")

    # Texture parameters
    apply_parser.add_argument(
        "--dense-nesting-level", type=int, default=3, help="Dense nesting level"
    )
    apply_parser.add_argument(
        "--dense-comprehensions", action="store_true", help="Use comprehensions"
    )
    apply_parser.add_argument(
        "--sparse-minimal", action="store_true", help="Keep minimal"
    )
    apply_parser.add_argument("--sparse-flat", action="store_true", help="Keep flat")
    apply_parser.add_argument(
        "--smooth-vectorized", action="store_true", help="Use vectorized ops"
    )
    apply_parser.add_argument(
        "--smooth-interpolation", action="store_true", help="Use interpolation"
    )
    apply_parser.add_argument(
        "--grainy-jitter", type=float, default=0.1, help="Grainy jitter amount"
    )
    apply_parser.add_argument(
        "--grainy-stepwise", action="store_true", help="Use stepwise processing"
    )
    apply_parser.add_argument(
        "--polyphonic-voices", type=int, default=3, help="Polyphonic voices"
    )
    apply_parser.add_argument(
        "--polyphonic-harmony", action="store_true", help="Add harmony"
    )
    apply_parser.add_argument(
        "--minimal-lines", type=int, default=3, help="Minimal lines"
    )
    apply_parser.add_argument(
        "--maximal-decorators", action="store_true", help="Add decorators"
    )
    apply_parser.add_argument(
        "--maximal-abstractions", action="store_true", help="Add abstractions"
    )
    apply_parser.add_argument(
        "--maximal-parallel", action="store_true", help="Add parallelization"
    )
    apply_parser.add_argument(
        "--fractal-depth", type=int, default=3, help="Fractal depth"
    )
    apply_parser.add_argument(
        "--fractal-branches", type=int, default=2, help="Fractal branches"
    )

    # Demo command
    subparsers.add_parser("demo", help="Demonstrate texture transformations")

    # Presets command
    presets_parser = subparsers.add_parser("presets", help="Generate texture presets")
    presets_parser.add_argument(
        "--output", default="texture_presets.json", help="Output file"
    )

    # Visual effects command
    subparsers.add_parser("visual-effects", help="Show visual effects for all textures")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = TextureCLI()

    if args.command == "list":
        cli.list_textures()
    elif args.command == "apply":
        # Get code from stdin or argument
        if args.code:
            code = args.code
        else:
            print("Enter code (end with Ctrl+D):")
            code = sys.stdin.read()

        # Build parameters
        params = {
            "dense_nesting_level": args.dense_nesting_level,
            "dense_comprehensions": args.dense_comprehensions,
            "sparse_minimal": args.sparse_minimal,
            "sparse_flat": args.sparse_flat,
            "smooth_vectorized": args.smooth_vectorized,
            "smooth_interpolation": args.smooth_interpolation,
            "grainy_jitter": args.grainy_jitter,
            "grainy_stepwise": args.grainy_stepwise,
            "polyphonic_voices": args.polyphonic_voices,
            "polyphonic_harmony": args.polyphonic_harmony,
            "minimal_lines": args.minimal_lines,
            "maximal_decorators": args.maximal_decorators,
            "maximal_abstractions": args.maximal_abstractions,
            "maximal_parallel": args.maximal_parallel,
            "fractal_depth": args.fractal_depth,
            "fractal_branches": args.fractal_branches,
        }

        cli.apply_texture(code, args.texture, params, args.output)
    elif args.command == "demo":
        cli.demo_textures()
    elif args.command == "presets":
        cli.generate_texture_presets(args.output)
    elif args.command == "visual-effects":
        cli.show_visual_effects()


if __name__ == "__main__":
    main()
