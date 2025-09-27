#!/usr/bin/env python3
"""
🥧 Code Live - Pi Mode CLI
==========================

Command-line interface for π (pi) mode transformations.
Mathematical playground with π references, circular waveforms, and Pi Day easter eggs!
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from pcs.pi_mode import PiModeEngine, PiModeParams, PiModeType


class PiModeCLI:
    """CLI interface for π mode transformations"""
    
    def __init__(self):
        self.engine = PiModeEngine()
    
    def list_pi_modes(self):
        """List all available π mode transformations"""
        print("🥧 Code Live - Pi Mode Transformations")
        print("=" * 50)
        print("Available π mode transformations:")
        print()
        
        pi_modes_info = {
            "pi_loop": {
                "description": "Loop lengths as π multiples (π × 100 = 314 iterations)",
                "params": ["pi_multiplier"],
                "example": "--pi-mode pi_loop --pi-multiplier 100"
            },
            "waveform": {
                "description": "π-based sine/cosine modulation with phase relationships",
                "params": ["waveform_freq"],
                "example": "--pi-mode waveform --waveform-freq 1.0"
            },
            "fractal": {
                "description": "π-based fractal patterns with mathematical recursion",
                "params": ["fractal_depth"],
                "example": "--pi-mode fractal --fractal-depth 3"
            },
            "circular": {
                "description": "Circular/spiral transformations with π coordinates",
                "params": ["circular_radius"],
                "example": "--pi-mode circular --circular-radius 1.0"
            },
            "constants": {
                "description": "Insert mathematical constants (π, τ, e, φ, γ)",
                "params": ["constants_mode"],
                "example": "--pi-mode constants"
            },
            "easter_egg": {
                "description": "Pi Day easter eggs and mathematical fun",
                "params": ["easter_egg_mode"],
                "example": "--pi-mode easter_egg"
            }
        }
        
        for mode, info in pi_modes_info.items():
            print(f"🥧 {mode.upper()}")
            print(f"   {info['description']}")
            if info['params']:
                print(f"   Parameters: {', '.join(info['params'])}")
            print(f"   Example: {info['example']}")
            print()
    
    def apply_pi_mode(
        self,
        code: str,
        pi_modes: List[str],
        params: Dict[str, Any],
        output_file: Optional[str] = None,
    ):
        """Apply π mode transformations to code"""
        print(f"🥧 Applying π Mode: {', '.join(pi_modes)}")
        print("=" * 50)
        
        # Create π mode parameters
        pi_params = PiModeParams(
            pi_multiplier=params.get("pi_multiplier", 100.0),
            waveform_freq=params.get("waveform_freq", 1.0),
            fractal_depth=params.get("fractal_depth", 3),
            circular_radius=params.get("circular_radius", 1.0),
            constants_mode=params.get("constants_mode", True),
            easter_egg_mode=params.get("easter_egg_mode", True)
        )
        
        print("✅ π Mode parameters validated")
        
        # Apply π mode
        try:
            result_code = self.engine.apply_pi_mode(code, pi_params)
            
            print("\nOriginal code:")
            print("-" * 30)
            print(code)
            
            print("\nπ Mode code:")
            print("-" * 30)
            print(result_code)
            
            # Save to file if specified
            if output_file:
                with open(output_file, "w") as f:
                    f.write(result_code)
                print(f"\n💾 Saved to {output_file}")
            
            # Show π mode details
            print("\n🥧 π Mode Details:")
            for mode in pi_modes:
                print(f"   - {mode}: {self._get_pi_mode_description(mode)}")
            
            # Show mathematical constants
            print("\n🧮 Mathematical Constants:")
            constants = self.engine.get_pi_constants()
            for name, value in constants.items():
                print(f"   {name} = {value:.10f}")
            
        except Exception as e:
            print(f"❌ Error applying π mode: {e}")
    
    def demo_pi_modes(self):
        """Demonstrate π mode transformations"""
        print("🥧 Code Live - π Mode Demo")
        print("=" * 50)
        
        # Sample code
        sample_code = """
for i in range(8):
    process(i)
"""
        
        print("Sample code:")
        print(sample_code.strip())
        print()
        
        # Demo individual π modes
        demos = [
            {
                "name": "π Loop Length",
                "modes": ["pi_loop"],
                "params": {"pi_multiplier": 100.0}
            },
            {
                "name": "π Waveform Modulation",
                "modes": ["waveform"],
                "params": {"waveform_freq": 1.0}
            },
            {
                "name": "π Fractal Patterns",
                "modes": ["fractal"],
                "params": {"fractal_depth": 3}
            },
            {
                "name": "π Circular Coordinates",
                "modes": ["circular"],
                "params": {"circular_radius": 1.0}
            },
            {
                "name": "π Mathematical Constants",
                "modes": ["constants"],
                "params": {"constants_mode": True}
            },
            {
                "name": "π Day Easter Eggs",
                "modes": ["easter_egg"],
                "params": {"easter_egg_mode": True}
            }
        ]
        
        for demo in demos:
            print(f"\n🥧 {demo['name']}")
            print("-" * 30)
            self.apply_pi_mode(sample_code, demo["modes"], demo["params"])
            print()
        
        # Demo π mode combinations
        print("\n🥧 π Mode Combinations")
        print("-" * 30)
        
        combinations = [
            {
                "name": "π Loop + Waveform",
                "modes": ["pi_loop", "waveform"],
                "params": {"pi_multiplier": 100.0, "waveform_freq": 1.0}
            },
            {
                "name": "π Fractal + Circular",
                "modes": ["fractal", "circular"],
                "params": {"fractal_depth": 3, "circular_radius": 1.0}
            },
            {
                "name": "π Constants + Easter Eggs",
                "modes": ["constants", "easter_egg"],
                "params": {"constants_mode": True, "easter_egg_mode": True}
            }
        ]
        
        for combo in combinations:
            print(f"\n🔗 {combo['name']}")
            print("-" * 20)
            self.apply_pi_mode(sample_code, combo["modes"], combo["params"])
            print()
    
    def generate_pi_art(self, output_file: str = "pi_mode_art.json"):
        """Generate π mode art data"""
        print("🥧 Generating π Mode Art Data")
        print("=" * 50)
        
        # Create π mode parameters
        pi_params = PiModeParams(
            pi_multiplier=100.0,
            waveform_freq=1.0,
            fractal_depth=3,
            circular_radius=1.0,
            constants_mode=True,
            easter_egg_mode=True
        )
        
        # Generate π art data
        pi_art = self.engine.generate_pi_art(pi_params)
        
        # Save π art data
        with open(output_file, "w") as f:
            json.dump(pi_art, f, indent=2)
        
        print(f"🎨 Generated π mode art data")
        print(f"💾 Saved to {output_file}")
        
        # Show π art details
        print("\n🥧 π Mode Art Details:")
        for key, value in pi_art["transformations"].items():
            print(f"   {key}: {value}")
        
        print("\n🧮 Mathematical Beauty:")
        for beauty in pi_art["mathematical_beauty"]:
            print(f"   - {beauty}")
    
    def _get_pi_mode_description(self, mode: str) -> str:
        """Get description for a π mode transformation"""
        descriptions = {
            "pi_loop": "Loop lengths as π multiples",
            "waveform": "π-based sine/cosine modulation",
            "fractal": "π-based fractal patterns",
            "circular": "Circular/spiral transformations",
            "constants": "Mathematical constants (π, τ, e, φ, γ)",
            "easter_egg": "Pi Day easter eggs and fun"
        }
        return descriptions.get(mode, "Unknown π mode")
    
    def show_pi_constants(self):
        """Show mathematical constants"""
        print("🥧 Mathematical Constants")
        print("=" * 50)
        
        constants = self.engine.get_pi_constants()
        for name, value in constants.items():
            print(f"{name} = {value:.10f}")
        
        print("\n🥧 Pi Day Fun Facts:")
        print("   - π ≈ 3.141592653589793...")
        print("   - τ = 2π ≈ 6.283185307179586...")
        print("   - e ≈ 2.718281828459045...")
        print("   - φ (Golden Ratio) ≈ 1.618033988749895...")
        print("   - γ (Euler-Mascheroni) ≈ 0.5772156649015329...")
        print("\n🥧 Happy Pi Day! π ≈ 3.14159...")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Code Live - π Mode CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pi_mode_cli.py list
  python pi_mode_cli.py apply --pi-mode "pi_loop,waveform" --pi-multiplier 100
  python pi_mode_cli.py demo
  python pi_mode_cli.py constants
  python pi_mode_cli.py art
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List π modes command
    subparsers.add_parser("list", help="List all available π mode transformations")
    
    # Apply π mode command
    apply_parser = subparsers.add_parser("apply", help="Apply π mode transformations to code")
    apply_parser.add_argument("--pi-mode", required=True, help="Comma-separated list of π modes")
    apply_parser.add_argument("--code", help="Code to process (or read from stdin)")
    apply_parser.add_argument("--output", help="Output file")
    
    # π mode parameters
    apply_parser.add_argument("--pi-multiplier", type=float, default=100.0, help="π multiplier for loop length")
    apply_parser.add_argument("--waveform-freq", type=float, default=1.0, help="Waveform frequency")
    apply_parser.add_argument("--fractal-depth", type=int, default=3, help="Fractal recursion depth")
    apply_parser.add_argument("--circular-radius", type=float, default=1.0, help="Circular radius")
    apply_parser.add_argument("--constants-mode", action="store_true", help="Enable mathematical constants")
    apply_parser.add_argument("--easter-egg-mode", action="store_true", help="Enable Pi Day easter eggs")
    
    # Demo command
    subparsers.add_parser("demo", help="Demonstrate π mode transformations")
    
    # Constants command
    subparsers.add_parser("constants", help="Show mathematical constants")
    
    # Art command
    art_parser = subparsers.add_parser("art", help="Generate π mode art data")
    art_parser.add_argument("--output", default="pi_mode_art.json", help="Output file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PiModeCLI()
    
    if args.command == "list":
        cli.list_pi_modes()
    elif args.command == "apply":
        # Get code from stdin or argument
        if args.code:
            code = args.code
        else:
            print("Enter code (end with Ctrl+D):")
            code = sys.stdin.read()
        
        # Parse π modes
        pi_modes = [mode.strip() for mode in args.pi_mode.split(",")]
        
        # Build parameters
        params = {
            "pi_multiplier": args.pi_multiplier,
            "waveform_freq": args.waveform_freq,
            "fractal_depth": args.fractal_depth,
            "circular_radius": args.circular_radius,
            "constants_mode": args.constants_mode,
            "easter_egg_mode": args.easter_egg_mode
        }
        
        cli.apply_pi_mode(code, pi_modes, params, args.output)
    elif args.command == "demo":
        cli.demo_pi_modes()
    elif args.command == "constants":
        cli.show_pi_constants()
    elif args.command == "art":
        cli.generate_pi_art(args.output)


if __name__ == "__main__":
    main()
