#!/usr/bin/env python3
"""
Cosmic Dust CLI - Infinite Space Vibe
====================================

Command-line interface for cosmic dust effects.
"""

import argparse
import sys
import json
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from string_fx.cosmic_dust import (
    CosmicDustEngine, 
    CosmicDustType, 
    CosmicDustParams,
    create_cosmic_dust_presets
)


def list_cosmic_dust_types():
    """List all cosmic dust types"""
    print("🌌 Cosmic Dust Types:")
    print("=" * 30)
    
    for dust_type in CosmicDustType:
        print(f"✨ {dust_type.value}")
    
    print("\n🎛️  Parameters:")
    print("  density: 0.0 to 1.0 (dust particle density)")
    print("  intensity: 0.0 to 1.0 (effect strength)")
    print("  spread: 0.0 to 1.0 (particle spread)")
    print("  fade_depth: 0.0 to 1.0 (fade intensity)")
    print("  spectrum_shimmer: 0.0 to 1.0 (RGB shimmer)")
    print("  polarity_shift: -1.0 to 1.0 (color polarity)")
    print("  saturation: 0.0 to 1.0 (color saturation)")
    print("  grid_size: 1 to 10 (grid spacing)")


def apply_cosmic_dust(text: str, dust_type: str, **kwargs):
    """Apply cosmic dust effect to text"""
    try:
        dust_type_enum = CosmicDustType(dust_type)
    except ValueError:
        print(f"❌ Error: Unknown dust type '{dust_type}'")
        print("Available types:", [t.value for t in CosmicDustType])
        return
    
    # Create parameters
    params = CosmicDustParams(
        density=kwargs.get('density', 0.3),
        intensity=kwargs.get('intensity', 0.7),
        spread=kwargs.get('spread', 0.5),
        fade_depth=kwargs.get('fade_depth', 0.8),
        spectrum_shimmer=kwargs.get('spectrum_shimmer', 0.6),
        polarity_shift=kwargs.get('polarity_shift', 0.0),
        saturation=kwargs.get('saturation', 0.8),
        grid_size=kwargs.get('grid_size', 3)
    )
    
    # Apply effect
    engine = CosmicDustEngine()
    result = engine.apply_cosmic_dust(text, dust_type_enum, params)
    
    print(f"🌌 {dust_type}: {result}")


def demo_cosmic_dust():
    """Demo cosmic dust effects"""
    test_texts = [
        "TuneZilla",
        "Rawtunez",
        "Code Live",
        "Cosmic Dust",
        "Infinite Space"
    ]
    
    print("🌌 COSMIC DUST FX - INFINITE SPACE VIBE")
    print("=" * 50)
    
    engine = CosmicDustEngine()
    
    for text in test_texts:
        print(f"\n📝 Original: {text}")
        
        # Test all dust types
        for dust_type in CosmicDustType:
            params = CosmicDustParams()
            result = engine.apply_cosmic_dust(text, dust_type, params)
            print(f"✨ {dust_type.value}: {result}")
        
        # Test spectrum dust
        params = CosmicDustParams(spectrum_shimmer=0.8, polarity_shift=0.3)
        spectrum_result = engine.apply_spectrum_dust(text, params)
        print(f"🌈 Spectrum: {spectrum_result}")
        
        # Test grid dust
        params = CosmicDustParams(grid_size=3, density=0.4)
        grid_result = engine.apply_grid_dust(text, params)
        print(f"🔲 Grid: {grid_result}")


def generate_presets():
    """Generate cosmic dust presets"""
    presets = create_cosmic_dust_presets()
    
    print("🌌 Cosmic Dust Presets:")
    print("=" * 30)
    
    for preset in presets:
        print(f"\n✨ {preset['name']}")
        print(f"   Type: {preset['type']}")
        print(f"   Params: {preset['params']}")
    
    # Save to JSON
    output_file = "out/cosmic_dust_presets.json"
    Path("out").mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(presets, f, indent=2)
    
    print(f"\n💾 Presets saved to: {output_file}")


def create_cosmic_dust_html():
    """Create HTML gallery for cosmic dust effects"""
    engine = CosmicDustEngine()
    
    test_texts = [
        "TuneZilla",
        "Rawtunez",
        "Code Live",
        "Cosmic Dust",
        "Infinite Space"
    ]
    
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cosmic Dust FX - Infinite Space Vibe</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0c0c0c, #1a1a2e, #16213e);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: #00ffff;
            text-shadow: 0 0 20px #00ffff;
            margin-bottom: 30px;
        }
        
        .effect-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .effect-card {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(0, 255, 255, 0.3);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .effect-title {
            color: #00ffff;
            font-size: 1.2em;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .text-example {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            line-height: 1.5;
        }
        
        .original {
            color: #ffffff;
        }
        
        .cosmic {
            color: #00ffff;
            text-shadow: 0 0 10px #00ffff;
        }
        
        .spectrum {
            background: linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #80ff00, #00ff00, #00ff80, #00ffff, #0080ff, #0000ff, #8000ff, #ff00ff, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .grid {
            color: #ffff00;
            text-shadow: 0 0 10px #ffff00;
        }
        
        .preset-info {
            background: rgba(0, 255, 255, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌌 Cosmic Dust FX - Infinite Space Vibe</h1>
        
        <div class="effect-grid">
"""
    
    # Add effect cards
    for dust_type in CosmicDustType:
        html_content += f"""
            <div class="effect-card">
                <div class="effect-title">✨ {dust_type.value.replace('_', ' ').title()}</div>
"""
        
        for text in test_texts:
            params = CosmicDustParams()
            result = engine.apply_cosmic_dust(text, dust_type, params)
            html_content += f"""
                <div class="text-example">
                    <div class="original">Original: {text}</div>
                    <div class="cosmic">Cosmic: {result}</div>
                </div>
"""
        
        html_content += """
            </div>
"""
    
    # Add spectrum and grid effects
    html_content += """
            <div class="effect-card">
                <div class="effect-title">🌈 Spectrum Dust</div>
"""
    
    for text in test_texts:
        params = CosmicDustParams(spectrum_shimmer=0.8, polarity_shift=0.3)
        spectrum_result = engine.apply_spectrum_dust(text, params)
        html_content += f"""
                <div class="text-example">
                    <div class="original">Original: {text}</div>
                    <div class="spectrum">Spectrum: {spectrum_result}</div>
                </div>
"""
    
    html_content += """
            </div>
            
            <div class="effect-card">
                <div class="effect-title">🔲 Grid Dust</div>
"""
    
    for text in test_texts:
        params = CosmicDustParams(grid_size=3, density=0.4)
        grid_result = engine.apply_grid_dust(text, params)
        html_content += f"""
                <div class="text-example">
                    <div class="original">Original: {text}</div>
                    <div class="grid">Grid: {grid_result}</div>
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="preset-info">
            <h3>🎛️ Cosmic Dust Parameters:</h3>
            <ul>
                <li><strong>density</strong>: 0.0 to 1.0 (dust particle density)</li>
                <li><strong>intensity</strong>: 0.0 to 1.0 (effect strength)</li>
                <li><strong>spread</strong>: 0.0 to 1.0 (particle spread)</li>
                <li><strong>fade_depth</strong>: 0.0 to 1.0 (fade intensity)</li>
                <li><strong>spectrum_shimmer</strong>: 0.0 to 1.0 (RGB shimmer)</li>
                <li><strong>polarity_shift</strong>: -1.0 to 1.0 (color polarity)</li>
                <li><strong>saturation</strong>: 0.0 to 1.0 (color saturation)</li>
                <li><strong>grid_size</strong>: 1 to 10 (grid spacing)</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML
    output_file = "out/cosmic_dust_gallery.html"
    Path("out").mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"🌌 HTML gallery created: {output_file}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Cosmic Dust FX - Infinite Space Vibe")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    subparsers.add_parser('list', help='List cosmic dust types and parameters')
    
    # Apply command
    apply_parser = subparsers.add_parser('apply', help='Apply cosmic dust effect to text')
    apply_parser.add_argument('text', help='Text to apply effect to')
    apply_parser.add_argument('--type', required=True, help='Dust type')
    apply_parser.add_argument('--density', type=float, default=0.3, help='Dust density (0.0-1.0)')
    apply_parser.add_argument('--intensity', type=float, default=0.7, help='Effect intensity (0.0-1.0)')
    apply_parser.add_argument('--spread', type=float, default=0.5, help='Particle spread (0.0-1.0)')
    apply_parser.add_argument('--fade-depth', type=float, default=0.8, help='Fade depth (0.0-1.0)')
    apply_parser.add_argument('--spectrum-shimmer', type=float, default=0.6, help='RGB shimmer (0.0-1.0)')
    apply_parser.add_argument('--polarity-shift', type=float, default=0.0, help='Polarity shift (-1.0 to 1.0)')
    apply_parser.add_argument('--saturation', type=float, default=0.8, help='Color saturation (0.0-1.0)')
    apply_parser.add_argument('--grid-size', type=int, default=3, help='Grid size (1-10)')
    
    # Demo command
    subparsers.add_parser('demo', help='Demo cosmic dust effects')
    
    # Presets command
    subparsers.add_parser('presets', help='Generate cosmic dust presets')
    
    # HTML command
    subparsers.add_parser('html', help='Create HTML gallery')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_cosmic_dust_types()
    elif args.command == 'apply':
        apply_cosmic_dust(
            args.text,
            args.type,
            density=args.density,
            intensity=args.intensity,
            spread=args.spread,
            fade_depth=args.fade_depth,
            spectrum_shimmer=args.spectrum_shimmer,
            polarity_shift=args.polarity_shift,
            saturation=args.saturation,
            grid_size=args.grid_size
        )
    elif args.command == 'demo':
        demo_cosmic_dust()
    elif args.command == 'presets':
        generate_presets()
    elif args.command == 'html':
        create_cosmic_dust_html()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
