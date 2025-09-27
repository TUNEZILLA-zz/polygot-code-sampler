#!/usr/bin/env python3
"""
🎭 Enhanced String FX CLI - FX Graph Runtime Integration
======================================================

Enhanced string effects with:
- FX graph runtime (declarative chains)
- Deterministic seeded chaos
- Intensity knob (one slider to rule them all)
- Safe output modes (raw/ansi/html)
- Performance guardrails
- MIDI/hotkey integration
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add the string_fx directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "string_fx"))

from runtime import (
    apply_chain, FXConfig, OutputMode, 
    create_preset, get_preset_pack, export_preset
)


def main():
    parser = argparse.ArgumentParser(
        description="🎭 Enhanced String FX - Mind-Bending String Effects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic effect chain
  python3 scripts/enhanced_string_fx.py --text "Code Live" --chain rainbow_gradient,neon_fx,stutter

  # With intensity and seed
  python3 scripts/enhanced_string_fx.py --text "TuneZilla" --chain glitch_colors,scramble --intensity 0.8 --seed 42

  # Use preset
  python3 scripts/enhanced_string_fx.py --text "Hello World" --preset neon_rave --intensity 0.9

  # Export as HTML
  python3 scripts/enhanced_string_fx.py --text "Test" --chain rainbow_gradient --mode html --output test.html

  # List all presets
  python3 scripts/enhanced_string_fx.py --list-presets
        """
    )
    
    parser.add_argument("--text", "-t", help="Input text to transform")
    parser.add_argument("--chain", "-c", help="Comma-separated effect chain (e.g., rainbow_gradient,neon_fx,stutter)")
    parser.add_argument("--preset", "-p", help="Use a predefined preset")
    parser.add_argument("--intensity", "-i", type=float, default=0.75, help="Intensity knob (0.0-1.0)")
    parser.add_argument("--seed", "-s", type=int, help="Seed for deterministic effects")
    parser.add_argument("--mode", "-m", choices=["raw", "ansi", "html"], default="ansi", help="Output mode")
    parser.add_argument("--max-length", type=int, default=8000, help="Maximum output length")
    parser.add_argument("--budget-ms", type=int, default=100, help="Processing budget in milliseconds")
    parser.add_argument("--output", "-o", help="Output file (for HTML mode)")
    parser.add_argument("--list-presets", action="store_true", help="List all available presets")
    parser.add_argument("--export-preset", help="Export current chain as preset JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.list_presets:
        list_presets()
        return
    
    # Check if text is required for other operations
    if not args.text and (args.chain or args.preset):
        print("❌ Must specify --text for effect operations")
        return
    
    # Create FX config
    config = FXConfig(
        intensity=args.intensity,
        seed=args.seed,
        mode=OutputMode(args.mode),
        max_length=args.max_length,
        budget_ms=args.budget_ms
    )
    
    # Get effect chain
    if args.preset:
        chain = get_preset_chain(args.preset)
        if chain is None:
            print(f"❌ Preset '{args.preset}' not found")
            return
    elif args.chain:
        chain = parse_chain(args.chain)
    else:
        print("❌ Must specify either --chain or --preset")
        return
    
    if args.verbose:
        print(f"🎭 Enhanced String FX - Mind-Bending String Effects")
        print(f"==================================================")
        print(f"📝 Text: {args.text}")
        print(f"🔧 Chain: {[step['name'] for step in chain]}")
        print(f"⚙️  Intensity: {args.intensity}")
        if args.seed:
            print(f"🎲 Seed: {args.seed}")
        print(f"📱 Mode: {args.mode}")
        print()
    
    # Apply effects
    try:
        result = apply_chain(args.text, chain, config)
        
        if args.output and args.mode == "html":
            # Create HTML output
            html_content = create_html_output(result, args.text, chain, config)
            with open(args.output, 'w') as f:
                f.write(html_content)
            print(f"🌐 HTML output saved to: {args.output}")
        else:
            print(result)
        
        if args.export_preset:
            # Export preset
            preset_data = create_preset(
                args.export_preset,
                chain,
                f"Custom preset: {args.export_preset}"
            )
            export_data = export_preset(preset_data, args.seed)
            
            with open(f"{args.export_preset}.json", 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"💾 Preset exported to: {args.export_preset}.json")
        
        if args.verbose:
            print(f"🎭 Enhanced String FX complete!")
            
    except Exception as e:
        print(f"❌ Error applying effects: {e}")
        sys.exit(1)


def list_presets():
    """List all available presets"""
    print("🎭 Available String FX Presets")
    print("===============================")
    
    presets = get_preset_pack()
    for name, preset in presets.items():
        print(f"📦 {name}")
        print(f"   Description: {preset['description']}")
        print(f"   Chain: {' → '.join([step['name'] for step in preset['chain']])}")
        print()


def get_preset_chain(preset_name: str):
    """Get chain for a preset"""
    presets = get_preset_pack()
    if preset_name in presets:
        return presets[preset_name]["chain"]
    return None


def parse_chain(chain_str: str):
    """Parse effect chain string"""
    chain = []
    effects = [e.strip() for e in chain_str.split(',')]
    
    for effect in effects:
        if ':' in effect:
            # Effect with parameters
            name, params_str = effect.split(':', 1)
            params = {}
            for param in params_str.split(','):
                if '=' in param:
                    key, value = param.split('=', 1)
                    try:
                        # Try to parse as number
                        if '.' in value:
                            params[key] = float(value)
                        else:
                            params[key] = int(value)
                    except ValueError:
                        # Keep as string
                        params[key] = value
            chain.append({"name": name, "params": params})
        else:
            # Simple effect
            chain.append({"name": effect, "params": {}})
    
    return chain


def create_html_output(result: str, original_text: str, chain: list, config: FXConfig) -> str:
    """Create HTML output with styling"""
    chain_str = " → ".join([step['name'] for step in chain])
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 String FX Output</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #000;
            color: #fff;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            color: #888;
            font-size: 1.2em;
        }}
        .output {{
            background: #111;
            border: 2px solid #333;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-size: 1.5em;
            line-height: 1.6;
            word-wrap: break-word;
        }}
        .info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .info-item {{
            background: #222;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #00ffff;
        }}
        .info-label {{
            color: #00ffff;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #fff;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        .copy-btn {{
            background: #00ffff;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin: 10px;
        }}
        .copy-btn:hover {{
            background: #00cccc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎭 String FX Output</h1>
            <p class="subtitle">Mind-Bending String Effects</p>
        </div>
        
        <div class="output">
            {result}
        </div>
        
        <div class="info">
            <div class="info-item">
                <div class="info-label">Original Text</div>
                <div class="info-value">{original_text}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Effect Chain</div>
                <div class="info-value">{chain_str}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Intensity</div>
                <div class="info-value">{config.intensity}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Seed</div>
                <div class="info-value">{config.seed or 'Random'}</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="copy-btn" onclick="copyToClipboard()">📋 Copy Output</button>
            <button class="copy-btn" onclick="copyAsMarkdown()">📝 Copy as Markdown</button>
        </div>
        
        <div class="footer">
            <p>Generated by Enhanced String FX Runtime</p>
            <p>Chain: {chain_str} | Intensity: {config.intensity} | Seed: {config.seed or 'Random'}</p>
        </div>
    </div>
    
    <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText(`{result}`).then(() => {{
                alert('Output copied to clipboard!');
            }});
        }}
        
        function copyAsMarkdown() {{
            const markdown = `# String FX Output\\n\\n**Original:** {original_text}\\n\\n**Result:**\\n\\n\`\`\`\\n{result}\\n\`\`\`\\n\\n**Chain:** {chain_str}\\n**Intensity:** {config.intensity}\\n**Seed:** {config.seed or 'Random'}`;
            navigator.clipboard.writeText(markdown).then(() => {{
                alert('Markdown copied to clipboard!');
            }});
        }}
    </script>
</body>
</html>
    """
    
    return html


if __name__ == "__main__":
    main()
