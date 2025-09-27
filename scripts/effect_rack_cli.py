#!/usr/bin/env python3
"""
Effect Rack CLI - Soundtoys-style Effect Rack for Text FX
=========================================================

Command-line interface for the modular FX chain system.
"""

import argparse
import json
import sys
import os

# Add the parent directory to the path so we can import the effect rack
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from string_fx.effect_rack import EffectRack, EffectSlot, EffectSlotConfig


def main():
    parser = argparse.ArgumentParser(
        description="Soundtoys-style Effect Rack for Text FX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process text with Decapitator preset
  python3 scripts/effect_rack_cli.py --text "Code Live" --preset decapitator

  # Process with custom effects
  python3 scripts/effect_rack_cli.py --text "TuneZilla" --effects distortion,neon_fx,glitch_colors

  # Save current configuration
  python3 scripts/effect_rack_cli.py --text "Rawtunez" --save my_rack.json

  # Load and process with saved configuration
  python3 scripts/effect_rack_cli.py --text "Code Live" --load my_rack.json

  # Show rack status
  python3 scripts/effect_rack_cli.py --rack-status
        """
    )
    
    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--preset", "-p", help="Load a preset configuration")
    parser.add_argument("--effects", "-e", help="Comma-separated list of effects to apply")
    parser.add_argument("--mode", "-m", default="raw", choices=["raw", "ansi", "html"], 
                       help="Output mode")
    parser.add_argument("--seed", "-s", type=int, help="Random seed for deterministic results")
    parser.add_argument("--save", help="Save current configuration to file")
    parser.add_argument("--load", help="Load configuration from file")
    parser.add_argument("--list-presets", action="store_true", help="List available presets")
    parser.add_argument("--rack-status", action="store_true", help="Show current rack status")
    parser.add_argument("--output", "-o", help="Output file for HTML mode")
    
    args = parser.parse_args()
    
    # Create effect rack
    rack = EffectRack()
    
    # Handle list presets
    if args.list_presets:
        presets = rack.create_soundtoys_presets()
        print("🎛️ Available Soundtoys-inspired Presets:")
        print("=" * 50)
        for name, config in presets.items():
            print(f"• {name}: {config.name}")
            for slot, slot_config in config.slots.items():
                print(f"  - {slot.value}: {slot_config.effect_name} (mix: {slot_config.wet_dry_mix})")
        return
    
    # Handle rack status
    if args.rack_status:
        status = rack.get_rack_status()
        print("🎛️ Effect Rack Status:")
        print("=" * 30)
        print(json.dumps(status, indent=2))
        return
    
    # Load preset if specified
    if args.preset:
        presets = rack.create_soundtoys_presets()
        if args.preset not in presets:
            print(f"❌ Preset '{args.preset}' not found. Available presets:")
            for name in presets.keys():
                print(f"  • {name}")
            return
        rack.config = presets[args.preset]
        print(f"🎛️ Loaded preset: {rack.config.name}")
    
    # Load configuration from file if specified
    if args.load:
        try:
            rack.load_preset(args.load)
            print(f"🎛️ Loaded configuration from: {args.load}")
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return
    
    # Apply effects if specified
    if args.effects:
        effect_names = [e.strip() for e in args.effects.split(",")]
        for i, effect_name in enumerate(effect_names):
            slot = list(EffectSlot)[i]
            rack.add_effect(slot, effect_name, enabled=True, wet_dry_mix=1.0)
        print(f"🎛️ Applied effects: {', '.join(effect_names)}")
    
    # Process text if provided
    if args.text:
        try:
            result = rack.process_text(args.text, mode=args.mode, seed=args.seed)
            
            if args.mode == "html" and args.output:
                # Create HTML output
                html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Effect Rack Output</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #fff;
            padding: 20px;
            text-align: center;
        }}
        .output {{
            font-size: 2rem;
            font-weight: bold;
            margin: 20px 0;
        }}
        .rack-info {{
            color: #888;
            font-size: 0.9rem;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>🎛️ Effect Rack Output</h1>
    <div class="output">{result}</div>
    <div class="rack-info">
        <p>Rack: {rack.config.name}</p>
        <p>Effects: {', '.join([config.effect_name for config in rack.config.slots.values()])}</p>
    </div>
</body>
</html>
                """
                with open(args.output, 'w') as f:
                    f.write(html_content)
                print(f"🌐 HTML output saved to: {args.output}")
            else:
                print(f"🎛️ Effect Rack Output: {result}")
                
        except Exception as e:
            print(f"❌ Error processing text: {e}")
            return
    
    # Save configuration if specified
    if args.save:
        try:
            rack.save_preset(args.save)
            print(f"🎛️ Configuration saved to: {args.save}")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return


if __name__ == "__main__":
    main()
