#!/usr/bin/env python3
"""
🎭 String FX Presets - Crazy String Effect Presets
=================================================

Predefined crazy string effect presets for Code Live:
- Glitch Mode, Neon Rave, Rainbow Wave
- ASCII Art, Cyberpunk, Retro Synth
- TuneZilla Mode, Code Opera, Performance Art
"""

from crazy_string_fx import CrazyStringFX, StringFXType, StringFXParams
from typing import Dict, List, Any


class StringFXPresets:
    """String FX Presets for different creative modes"""
    
    def __init__(self):
        self.presets = self._create_presets()
    
    def _create_presets(self) -> Dict[str, Dict[str, Any]]:
        """Create string FX presets"""
        return {
            "glitch_mode": {
                "name": "Glitch Mode",
                "description": "Chaotic glitch effects with random colors",
                "fx_chain": [StringFXType.GLITCH_COLORS, StringFXType.STUTTER, StringFXType.SCRAMBLE],
                "params": StringFXParams(
                    intensity=1.5,
                    speed=2.0,
                    glitch_factor=0.8,
                    stutter_rate=0.3,
                    scramble_factor=0.6
                )
            },
            "neon_rave": {
                "name": "Neon Rave",
                "description": "Bright neon effects with glow",
                "fx_chain": [StringFXType.NEON_FX, StringFXType.RAINBOW_GRADIENT, StringFXType.ECHO],
                "params": StringFXParams(
                    intensity=2.0,
                    speed=1.5,
                    color_shift=0.5,
                    echo_delay=0.2
                )
            },
            "rainbow_wave": {
                "name": "Rainbow Wave",
                "description": "Smooth rainbow gradient with waveform",
                "fx_chain": [StringFXType.RAINBOW_GRADIENT, StringFXType.WAVEFORM, StringFXType.STRETCH],
                "params": StringFXParams(
                    intensity=1.2,
                    speed=0.8,
                    color_shift=0.3
                )
            },
            "ascii_art": {
                "name": "ASCII Art",
                "description": "ASCII art effects with melt",
                "fx_chain": [StringFXType.ASCII_MELT, StringFXType.CLUSTER, StringFXType.RANDOM_INSERT],
                "params": StringFXParams(
                    intensity=1.0,
                    melt_speed=1.5,
                    cluster_size=4,
                    scramble_factor=0.3
                )
            },
            "cyberpunk": {
                "name": "Cyberpunk",
                "description": "Cyberpunk aesthetic with glitch",
                "fx_chain": [StringFXType.GLITCH_COLORS, StringFXType.NEON_FX, StringFXType.STUTTER],
                "params": StringFXParams(
                    intensity=1.8,
                    speed=2.5,
                    glitch_factor=0.9,
                    stutter_rate=0.4
                )
            },
            "retro_synth": {
                "name": "Retro Synth",
                "description": "Retro synthesizer effects",
                "fx_chain": [StringFXType.PITCH_SHIFT, StringFXType.ECHO, StringFXType.REVERB],
                "params": StringFXParams(
                    intensity=1.3,
                    speed=1.2,
                    echo_delay=0.4,
                    reverb_decay=0.7
                )
            },
            "tunezilla_mode": {
                "name": "TuneZilla Mode",
                "description": "TuneZilla brand effects with gold/emerald",
                "fx_chain": [StringFXType.RAINBOW_GRADIENT, StringFXType.NEON_FX, StringFXType.WAVEFORM],
                "params": StringFXParams(
                    intensity=1.6,
                    speed=1.8,
                    color_shift=0.7,
                    glitch_factor=0.4
                )
            },
            "code_opera": {
                "name": "Code Opera",
                "description": "Operatic string effects with harmony",
                "fx_chain": [StringFXType.ECHO, StringFXType.REVERB, StringFXType.PITCH_SHIFT],
                "params": StringFXParams(
                    intensity=1.4,
                    speed=0.9,
                    echo_delay=0.5,
                    reverb_decay=0.8
                )
            },
            "performance_art": {
                "name": "Performance Art",
                "description": "Live performance string effects",
                "fx_chain": [StringFXType.STUTTER, StringFXType.GLITCH_COLORS, StringFXType.SCRAMBLE],
                "params": StringFXParams(
                    intensity=2.2,
                    speed=3.0,
                    stutter_rate=0.5,
                    glitch_factor=0.7,
                    scramble_factor=0.8
                )
            },
            "lolcat_mode": {
                "name": "Lolcat Mode",
                "description": "Lolcat-style string effects",
                "fx_chain": [StringFXType.RAINBOW_GRADIENT, StringFXType.STRETCH, StringFXType.RANDOM_INSERT],
                "params": StringFXParams(
                    intensity=1.1,
                    speed=0.7,
                    color_shift=0.2,
                    scramble_factor=0.2
                )
            },
            "fractal_madness": {
                "name": "Fractal Madness",
                "description": "Fractal-inspired string effects",
                "fx_chain": [StringFXType.WAVEFORM, StringFXType.CLUSTER, StringFXType.ASCII_MELT],
                "params": StringFXParams(
                    intensity=1.7,
                    speed=1.3,
                    cluster_size=3,
                    melt_speed=2.0
                )
            },
            "chaos_mode": {
                "name": "Chaos Mode",
                "description": "Maximum chaos string effects",
                "fx_chain": [StringFXType.SCRAMBLE, StringFXType.GLITCH_COLORS, StringFXType.STUTTER, StringFXType.RANDOM_INSERT],
                "params": StringFXParams(
                    intensity=3.0,
                    speed=2.8,
                    glitch_factor=1.0,
                    stutter_rate=0.6,
                    scramble_factor=0.9
                )
            }
        }
    
    def get_preset(self, name: str) -> Dict[str, Any]:
        """Get a specific preset"""
        return self.presets.get(name, {})
    
    def list_presets(self) -> List[str]:
        """List all available presets"""
        return list(self.presets.keys())
    
    def apply_preset(self, text: str, preset_name: str, seed: str = None) -> str:
        """Apply a preset to text"""
        preset = self.get_preset(preset_name)
        if not preset:
            return text
        
        fx_engine = CrazyStringFX(seed=seed)
        return fx_engine.apply_fx_chain(text, preset["fx_chain"], preset["params"])
    
    def create_preset_html(self, text: str, preset_name: str, seed: str = None) -> str:
        """Create HTML visualization for a preset"""
        preset = self.get_preset(preset_name)
        if not preset:
            return f"<html><body><h1>Preset '{preset_name}' not found</h1></body></html>"
        
        fx_engine = CrazyStringFX(seed=seed)
        result = fx_engine.apply_fx_chain(text, preset["fx_chain"], preset["params"])
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 {preset['name']} - {text}</title>
    <style>
        body {{
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
            color: #00ff88;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .preset-container {{
            text-align: center;
            max-width: 900px;
        }}
        
        .preset-title {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #00ff88, #ffd700, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .preset-description {{
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.8;
        }}
        
        .preset-result {{
            font-size: 4rem;
            font-weight: bold;
            margin: 2rem 0;
            padding: 3rem;
            background: rgba(0, 0, 0, 0.8);
            border: 3px solid #00ff88;
            border-radius: 20px;
            animation: presetGlow 3s ease-in-out infinite alternate;
        }}
        
        @keyframes presetGlow {{
            from {{ box-shadow: 0 0 30px rgba(0, 255, 136, 0.5); }}
            to {{ box-shadow: 0 0 60px rgba(255, 215, 0, 0.8); }}
        }}
        
        .preset-info {{
            margin-top: 2rem;
            font-size: 1rem;
            opacity: 0.8;
        }}
        
        .preset-chain {{
            margin: 1rem 0;
            font-size: 1rem;
        }}
        
        .preset-params {{
            margin: 1rem 0;
            font-size: 0.9rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}
        
        .param-item {{
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 8px;
            padding: 0.5rem;
        }}
        
        .param-label {{
            font-weight: bold;
            color: #ffd700;
        }}
        
        .param-value {{
            color: #00ff88;
        }}
    </style>
</head>
<body>
    <div class="preset-container">
        <h1 class="preset-title">🎭 {preset['name']}</h1>
        <p class="preset-description">{preset['description']}</p>
        <div class="preset-result">{result}</div>
        <div class="preset-info">
            <div class="preset-chain">
                <strong>FX Chain:</strong> {' → '.join([fx.value for fx in preset['fx_chain']])}
            </div>
            <div class="preset-params">
                <div class="param-item">
                    <div class="param-label">Intensity</div>
                    <div class="param-value">{preset['params'].intensity}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Speed</div>
                    <div class="param-value">{preset['params'].speed}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Glitch Factor</div>
                    <div class="param-value">{preset['params'].glitch_factor}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Stutter Rate</div>
                    <div class="param-value">{preset['params'].stutter_rate}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Scramble Factor</div>
                    <div class="param-value">{preset['params'].scramble_factor}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Echo Delay</div>
                    <div class="param-value">{preset['params'].echo_delay}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def create_preset_gallery(self, text: str = "Code Live") -> str:
        """Create a gallery of all presets"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 String FX Presets Gallery - {text}</title>
    <style>
        body {{
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
            color: #00ff88;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
        }}
        
        .gallery-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .gallery-title {{
            text-align: center;
            font-size: 3rem;
            margin-bottom: 2rem;
            background: linear-gradient(45deg, #00ff88, #ffd700, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .presets-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .preset-card {{
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff88;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .preset-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        }}
        
        .preset-name {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #ffd700;
        }}
        
        .preset-description {{
            font-size: 1rem;
            margin-bottom: 1.5rem;
            opacity: 0.8;
        }}
        
        .preset-result {{
            font-size: 2rem;
            font-weight: bold;
            margin: 1rem 0;
            padding: 1rem;
            background: rgba(0, 255, 136, 0.1);
            border-radius: 10px;
            border: 1px solid #00ff88;
        }}
        
        .preset-chain {{
            font-size: 0.9rem;
            margin: 1rem 0;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="gallery-container">
        <h1 class="gallery-title">🎭 String FX Presets Gallery</h1>
        <div class="presets-grid">
"""
        
        # Add preset cards
        for preset_name, preset in self.presets.items():
            result = self.apply_preset(text, preset_name)
            html += f"""
            <div class="preset-card">
                <div class="preset-name">{preset['name']}</div>
                <div class="preset-description">{preset['description']}</div>
                <div class="preset-result">{result}</div>
                <div class="preset-chain">
                    {' → '.join([fx.value for fx in preset['fx_chain']])}
                </div>
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        return html


def main():
    """Main entry point for String FX Presets"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🎭 String FX Presets - Crazy String Effect Presets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/string_fx_presets.py --text "Hello World" --preset glitch_mode
  python scripts/string_fx_presets.py --text "TuneZilla" --preset tunezilla_mode
  python scripts/string_fx_presets.py --text "Code Live" --gallery
        """,
    )
    
    parser.add_argument("--text", default="Code Live", help="Text to apply effects to")
    parser.add_argument("--preset", help="Preset to apply")
    parser.add_argument("--gallery", action="store_true", help="Create preset gallery")
    parser.add_argument("--output", help="Output HTML file")
    parser.add_argument("--seed", help="Random seed for reproducible effects")
    
    args = parser.parse_args()
    
    print("🎭 String FX Presets - Crazy String Effect Presets")
    print("=" * 50)
    
    # Create presets
    presets = StringFXPresets()
    
    if args.gallery:
        # Create gallery
        html = presets.create_preset_gallery(args.text)
        output_file = args.output or "out/string_fx_gallery.html"
        with open(output_file, "w") as f:
            f.write(html)
        print(f"🌐 Gallery created: {output_file}")
        print(f"📝 Text: {args.text}")
        print(f"🎭 Presets: {len(presets.list_presets())}")
    elif args.preset:
        # Apply specific preset
        result = presets.apply_preset(args.text, args.preset, args.seed)
        print(f"📝 Original: {args.text}")
        print(f"🎭 Result: {result}")
        print(f"🔧 Preset: {args.preset}")
        
        # Create HTML if requested
        if args.output:
            html = presets.create_preset_html(args.text, args.preset, args.seed)
            with open(args.output, "w") as f:
                f.write(html)
            print(f"🌐 HTML output: {args.output}")
    else:
        # List all presets
        print("🎭 Available Presets:")
        print("-" * 30)
        for preset_name in presets.list_presets():
            preset = presets.get_preset(preset_name)
            print(f"{preset_name:20}: {preset['name']} - {preset['description']}")


if __name__ == "__main__":
    main()
