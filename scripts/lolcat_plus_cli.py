#!/usr/bin/env python3
"""
LOLcat++ CLI - Drop-in FX node for creative text transformation
"""
import argparse
import sys
import json
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus

PRESETS = {
    "classic": {
        "intensity": 0.5, "uwu": 0.3, "chaos": 0.15, 
        "emoji": 0.1, "nyan_trail": 0.2, "gradient_phase": 0.0
    },
    "uwu-rainbow": {
        "intensity": 0.8, "uwu": 0.6, "chaos": 0.25, 
        "emoji": 0.2, "nyan_trail": 0.45, "gradient_phase": 0.0
    },
    "studio-safe": {
        "intensity": 0.4, "uwu": 0.2, "chaos": 0.05, 
        "emoji": 0.03, "nyan_trail": 0.0, "mono": True, 
        "reduced_motion": True
    },
    "nyan-march": {
        "intensity": 0.6, "uwu": 0.4, "chaos": 0.1, 
        "emoji": 0.15, "nyan_trail": 0.5, "gradient_phase": 0.0
    },
    "prismatic-purr": {
        "intensity": 0.7, "uwu": 0.5, "chaos": 0.1, 
        "emoji": 0.18, "nyan_trail": 0.3, "gradient_phase": 0.0
    },
    # Micro-presets for stage performance
    "classic-lite": {
        "intensity": 0.5, "uwu": 0.28, "chaos": 0.15, 
        "emoji": 0.06, "nyan_trail": 0.12, "gradient_phase": 0.0
    },
    "stage-punch": {
        "intensity": 0.7, "uwu": 0.4, "chaos": 0.32, 
        "emoji": 0.16, "nyan_trail": 0.42, "gradient_phase": 0.0
    },
    "cat-walk": {
        "intensity": 0.4, "uwu": 0.18, "chaos": 0.04, 
        "emoji": 0.08, "nyan_trail": 0.28, "gradient_phase": 0.0
    }
}

def main():
    parser = argparse.ArgumentParser(description="LOLcat++ Text FX")
    parser.add_argument("--text", required=True, help="Input text to transform")
    parser.add_argument("--preset", help="Preset name (classic, uwu-rainbow, studio-safe, nyan-march, prismatic-purr)")
    parser.add_argument("--intensity", type=float, default=0.6, help="Overall intensity (0.0-1.0)")
    parser.add_argument("--uwu", type=float, default=0.4, help="UwU-ifier amount (0.0-1.0)")
    parser.add_argument("--chaos", type=float, default=0.2, help="Chaos case amount (0.0-1.0)")
    parser.add_argument("--emoji", type=float, default=0.15, help="Emoji density (0.0-1.0)")
    parser.add_argument("--nyan-trail", type=float, default=0.0, help="Nyan trail amount (0.0-1.0)")
    parser.add_argument("--gradient-phase", type=float, default=0.0, help="Gradient phase (0.0-1.0)")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed")
    parser.add_argument("--mono", action="store_true", help="Monochrome mode")
    parser.add_argument("--reduced-motion", action="store_true", help="Reduced motion mode")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--format", choices=["text", "ansi", "json"], default="ansi", help="Output format")
    
    args = parser.parse_args()
    
    # Apply preset if specified
    if args.preset:
        if args.preset not in PRESETS:
            print(f"Unknown preset: {args.preset}", file=sys.stderr)
            print(f"Available presets: {', '.join(PRESETS.keys())}", file=sys.stderr)
            sys.exit(1)
        
        preset = PRESETS[args.preset]
        # Override with command line args
        params = {
            "intensity": args.intensity,
            "uwu": args.uwu,
            "chaos": args.chaos,
            "emoji": args.emoji,
            "nyan_trail": args.nyan_trail,
            "gradient_phase": args.gradient_phase,
            "seed": args.seed,
            "mono": args.mono,
            "reduced_motion": args.reduced_motion
        }
        
        # Apply preset defaults for unspecified params
        for key, value in preset.items():
            if key not in params or params[key] is None:
                params[key] = value
    else:
        params = {
            "intensity": args.intensity,
            "uwu": args.uwu,
            "chaos": args.chaos,
            "emoji": args.emoji,
            "nyan_trail": args.nyan_trail,
            "gradient_phase": args.gradient_phase,
            "seed": args.seed,
            "mono": args.mono,
            "reduced_motion": args.reduced_motion
        }
    
    # Transform text
    result = lolcat_plus(args.text, **params)
    
    # Output
    if args.format == "text":
        output = result["text"]
    elif args.format == "ansi":
        output = result["ansi"]
    elif args.format == "json":
        output = json.dumps(result, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
