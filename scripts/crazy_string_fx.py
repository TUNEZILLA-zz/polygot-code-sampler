#!/usr/bin/env python3
"""
🎭 Crazy String FX - Mind-Bending String Effects
===============================================

Crazy string effects for Code Live:
- Stretch, Echo, Pitch Shift, Reverb
- Rainbow Gradient, Glitch Colors, Neon FX
- Invert FX, Stutter, Waveform, Cluster
- Random Insert, Scramble, ASCII Melt
"""

import random
import math
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class StringFXType(Enum):
    """Types of crazy string effects"""
    STRETCH = "stretch"
    ECHO = "echo"
    PITCH_SHIFT = "pitch_shift"
    REVERB = "reverb"
    RAINBOW_GRADIENT = "rainbow_gradient"
    GLITCH_COLORS = "glitch_colors"
    NEON_FX = "neon_fx"
    INVERT_FX = "invert_fx"
    STUTTER = "stutter"
    WAVEFORM = "waveform"
    CLUSTER = "cluster"
    RANDOM_INSERT = "random_insert"
    SCRAMBLE = "scramble"
    ASCII_MELT = "ascii_melt"


@dataclass
class StringFXParams:
    """Parameters for string effects"""
    intensity: float = 1.0
    speed: float = 1.0
    color_shift: float = 0.0
    glitch_factor: float = 0.5
    echo_delay: float = 0.3
    reverb_decay: float = 0.6
    stutter_rate: float = 0.2
    cluster_size: int = 3
    scramble_factor: float = 0.7
    melt_speed: float = 1.0


class CrazyStringFX:
    """Crazy String FX Engine"""
    
    def __init__(self, seed: Optional[str] = None):
        self.seed = seed
        if seed:
            random.seed(seed)
        
        # Color palettes for effects
        self.rainbow_colors = [
            "#ff0000", "#ff8000", "#ffff00", "#80ff00", 
            "#00ff00", "#00ff80", "#00ffff", "#0080ff",
            "#0000ff", "#8000ff", "#ff00ff", "#ff0080"
        ]
        
        self.neon_colors = [
            "#ff00ff", "#00ffff", "#ffff00", "#ff0080",
            "#8000ff", "#00ff80", "#ff8000", "#0080ff"
        ]
        
        self.glitch_colors = [
            "#ff0000", "#00ff00", "#0000ff", "#ffff00",
            "#ff00ff", "#00ffff", "#ffffff", "#000000"
        ]
    
    def stretch_string(self, text: str, params: StringFXParams) -> str:
        """Stretch string with crazy spacing"""
        if not text:
            return text
        
        stretched = ""
        for i, char in enumerate(text):
            # Add variable spacing based on position and intensity
            spacing = int(params.intensity * (1 + math.sin(i * 0.5) * 0.5))
            stretched += char + " " * spacing
        
        return stretched
    
    def echo_string(self, text: str, params: StringFXParams) -> str:
        """Add echo effect to string"""
        if not text:
            return text
        
        echo_count = int(params.intensity * 3)
        echo_delay = int(params.echo_delay * 10)
        
        result = text
        for i in range(echo_count):
            # Add fading echo
            echo_text = text
            for j in range(echo_delay):
                echo_text = " " + echo_text
            
            # Fade the echo
            fade_factor = 1.0 - (i * 0.3)
            if fade_factor > 0:
                result += echo_text
        
        return result
    
    def pitch_shift_string(self, text: str, params: StringFXParams) -> str:
        """Pitch shift effect by changing character case and spacing"""
        if not text:
            return text
        
        shifted = ""
        for i, char in enumerate(text):
            # Create pitch shift effect
            pitch_factor = math.sin(i * params.speed * 0.5) * params.intensity
            
            if pitch_factor > 0.5:
                # High pitch - uppercase and tight spacing
                shifted += char.upper()
            elif pitch_factor < -0.5:
                # Low pitch - lowercase and wide spacing
                shifted += char.lower() + " "
            else:
                # Normal pitch
                shifted += char
        
        return shifted
    
    def reverb_string(self, text: str, params: StringFXParams) -> str:
        """Add reverb effect with decaying repeats"""
        if not text:
            return text
        
        reverb_count = int(params.intensity * 4)
        reverb_text = text
        
        for i in range(reverb_count):
            # Add decaying reverb
            decay = params.reverb_decay ** (i + 1)
            if decay > 0.1:
                # Add reverb with spacing
                reverb_text += " " * (i + 1) + text
        
        return reverb_text
    
    def rainbow_gradient_string(self, text: str, params: StringFXParams) -> str:
        """Apply rainbow gradient effect"""
        if not text:
            return text
        
        colored = ""
        for i, char in enumerate(text):
            if char.isspace():
                colored += char
                continue
            
            # Calculate color index
            color_index = int((i + params.color_shift * 10) % len(self.rainbow_colors))
            color = self.rainbow_colors[color_index]
            
            # Apply color (using HTML-like tags for demonstration)
            colored += f"<span style='color: {color}'>{char}</span>"
        
        return colored
    
    def glitch_colors_string(self, text: str, params: StringFXParams) -> str:
        """Apply glitch color effects"""
        if not text:
            return text
        
        glitched = ""
        for i, char in enumerate(text):
            if char.isspace():
                glitched += char
                continue
            
            # Random glitch color
            if random.random() < params.glitch_factor:
                color = random.choice(self.glitch_colors)
                glitched += f"<span style='color: {color}'>{char}</span>"
            else:
                glitched += char
        
        return glitched
    
    def neon_fx_string(self, text: str, params: StringFXParams) -> str:
        """Apply neon effects"""
        if not text:
            return text
        
        neon = ""
        for i, char in enumerate(text):
            if char.isspace():
                neon += char
                continue
            
            # Neon color with glow effect
            color = self.neon_colors[i % len(self.neon_colors)]
            glow = int(params.intensity * 10)
            
            neon += f"<span style='color: {color}; text-shadow: 0 0 {glow}px {color}'>{char}</span>"
        
        return neon
    
    def invert_fx_string(self, text: str, params: StringFXParams) -> str:
        """Invert string with crazy effects"""
        if not text:
            return text
        
        # Invert the string
        inverted = text[::-1]
        
        # Add inversion effects
        if params.intensity > 0.5:
            # Double inversion
            inverted = inverted[::-1]
        
        return inverted
    
    def stutter_string(self, text: str, params: StringFXParams) -> str:
        """Add stutter effect"""
        if not text:
            return text
        
        stuttered = ""
        for i, char in enumerate(text):
            stuttered += char
            
            # Add stutter based on rate
            if random.random() < params.stutter_rate:
                stutter_count = int(params.intensity * 3)
                for _ in range(stutter_count):
                    stuttered += char
        
        return stuttered
    
    def waveform_string(self, text: str, params: StringFXParams) -> str:
        """Create waveform effect"""
        if not text:
            return text
        
        waveform = ""
        for i, char in enumerate(text):
            if char.isspace():
                waveform += char
                continue
            
            # Create waveform spacing
            wave_height = int(math.sin(i * params.speed * 0.3) * params.intensity * 5)
            spacing = " " * max(0, wave_height)
            
            waveform += spacing + char
        
        return waveform
    
    def cluster_string(self, text: str, params: StringFXParams) -> str:
        """Create cluster effect"""
        if not text:
            return text
        
        clustered = ""
        cluster_size = params.cluster_size
        
        for i in range(0, len(text), cluster_size):
            cluster = text[i:i + cluster_size]
            
            # Add cluster spacing
            if i > 0:
                clustered += " " * int(params.intensity * 3)
            
            clustered += cluster
        
        return clustered
    
    def random_insert_string(self, text: str, params: StringFXParams) -> str:
        """Insert random characters"""
        if not text:
            return text
        
        inserted = ""
        for char in text:
            inserted += char
            
            # Random insert based on intensity
            if random.random() < params.intensity * 0.3:
                random_char = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
                inserted += random_char
        
        return inserted
    
    def scramble_string(self, text: str, params: StringFXParams) -> str:
        """Scramble string with controlled randomness"""
        if not text:
            return text
        
        scrambled = list(text)
        
        # Scramble based on factor
        scramble_count = int(len(text) * params.scramble_factor * params.intensity)
        
        for _ in range(scramble_count):
            if len(scrambled) > 1:
                i, j = random.sample(range(len(scrambled)), 2)
                scrambled[i], scrambled[j] = scrambled[j], scrambled[i]
        
        return ''.join(scrambled)
    
    def ascii_melt_string(self, text: str, params: StringFXParams) -> str:
        """Create ASCII melt effect"""
        if not text:
            return text
        
        melted = ""
        for i, char in enumerate(text):
            if char.isspace():
                melted += char
                continue
            
            # Create melt effect
            melt_offset = int(math.sin(i * params.melt_speed) * params.intensity * 3)
            melted += " " * max(0, melt_offset) + char
        
        return melted
    
    def apply_fx(self, text: str, fx_type: StringFXType, params: StringFXParams) -> str:
        """Apply a specific string effect"""
        if not text:
            return text
        
        if fx_type == StringFXType.STRETCH:
            return self.stretch_string(text, params)
        elif fx_type == StringFXType.ECHO:
            return self.echo_string(text, params)
        elif fx_type == StringFXType.PITCH_SHIFT:
            return self.pitch_shift_string(text, params)
        elif fx_type == StringFXType.REVERB:
            return self.reverb_string(text, params)
        elif fx_type == StringFXType.RAINBOW_GRADIENT:
            return self.rainbow_gradient_string(text, params)
        elif fx_type == StringFXType.GLITCH_COLORS:
            return self.glitch_colors_string(text, params)
        elif fx_type == StringFXType.NEON_FX:
            return self.neon_fx_string(text, params)
        elif fx_type == StringFXType.INVERT_FX:
            return self.invert_fx_string(text, params)
        elif fx_type == StringFXType.STUTTER:
            return self.stutter_string(text, params)
        elif fx_type == StringFXType.WAVEFORM:
            return self.waveform_string(text, params)
        elif fx_type == StringFXType.CLUSTER:
            return self.cluster_string(text, params)
        elif fx_type == StringFXType.RANDOM_INSERT:
            return self.random_insert_string(text, params)
        elif fx_type == StringFXType.SCRAMBLE:
            return self.scramble_string(text, params)
        elif fx_type == StringFXType.ASCII_MELT:
            return self.ascii_melt_string(text, params)
        else:
            return text
    
    def apply_fx_chain(self, text: str, fx_chain: List[StringFXType], params: StringFXParams) -> str:
        """Apply a chain of string effects"""
        result = text
        for fx_type in fx_chain:
            result = self.apply_fx(result, fx_type, params)
        return result
    
    def create_fx_preset(self, name: str, fx_chain: List[StringFXType], params: StringFXParams) -> Dict[str, Any]:
        """Create a string FX preset"""
        return {
            "name": name,
            "fx_chain": [fx.value for fx in fx_chain],
            "params": {
                "intensity": params.intensity,
                "speed": params.speed,
                "color_shift": params.color_shift,
                "glitch_factor": params.glitch_factor,
                "echo_delay": params.echo_delay,
                "reverb_decay": params.reverb_decay,
                "stutter_rate": params.stutter_rate,
                "cluster_size": params.cluster_size,
                "scramble_factor": params.scramble_factor,
                "melt_speed": params.melt_speed
            }
        }
    
    def generate_fx_demo(self, text: str = "Code Live") -> Dict[str, str]:
        """Generate demo of all string effects"""
        demo = {}
        params = StringFXParams()
        
        for fx_type in StringFXType:
            try:
                result = self.apply_fx(text, fx_type, params)
                demo[fx_type.value] = result
            except Exception as e:
                demo[fx_type.value] = f"Error: {e}"
        
        return demo
    
    def create_fx_html(self, text: str, fx_chain: List[StringFXType], params: StringFXParams) -> str:
        """Create HTML visualization of string effects"""
        result = self.apply_fx_chain(text, fx_chain, params)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 Crazy String FX - {text}</title>
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
        
        .fx-container {{
            text-align: center;
            max-width: 800px;
        }}
        
        .fx-title {{
            font-size: 2rem;
            margin-bottom: 2rem;
            background: linear-gradient(45deg, #00ff88, #ffd700, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .fx-result {{
            font-size: 3rem;
            font-weight: bold;
            margin: 2rem 0;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff88;
            border-radius: 15px;
            animation: fxGlow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes fxGlow {{
            from {{ box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }}
            to {{ box-shadow: 0 0 40px rgba(255, 215, 0, 0.8); }}
        }}
        
        .fx-info {{
            margin-top: 2rem;
            font-size: 1rem;
            opacity: 0.8;
        }}
        
        .fx-chain {{
            margin: 1rem 0;
            font-size: 0.9rem;
        }}
        
        .fx-param {{
            margin: 0.5rem 0;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="fx-container">
        <h1 class="fx-title">🎭 Crazy String FX</h1>
        <div class="fx-result">{result}</div>
        <div class="fx-info">
            <div class="fx-chain">
                <strong>FX Chain:</strong> {' → '.join([fx.value for fx in fx_chain])}
            </div>
            <div class="fx-param">
                <strong>Intensity:</strong> {params.intensity} | 
                <strong>Speed:</strong> {params.speed} | 
                <strong>Glitch:</strong> {params.glitch_factor}
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html


def main():
    """Main entry point for Crazy String FX"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🎭 Crazy String FX - Mind-Bending String Effects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/crazy_string_fx.py --text "Hello World" --fx stretch,echo
  python scripts/crazy_string_fx.py --text "Code Live" --fx rainbow_gradient,neon_fx
  python scripts/crazy_string_fx.py --text "TuneZilla" --fx glitch_colors,stutter
        """,
    )
    
    parser.add_argument("--text", default="Code Live", help="Text to apply effects to")
    parser.add_argument("--fx", help="Comma-separated list of effects to apply")
    parser.add_argument("--intensity", type=float, default=1.0, help="Effect intensity")
    parser.add_argument("--speed", type=float, default=1.0, help="Effect speed")
    parser.add_argument("--glitch", type=float, default=0.5, help="Glitch factor")
    parser.add_argument("--output", help="Output HTML file")
    parser.add_argument("--seed", help="Random seed for reproducible effects")
    
    args = parser.parse_args()
    
    print("🎭 Crazy String FX - Mind-Bending String Effects")
    print("=" * 50)
    
    # Create FX engine
    fx_engine = CrazyStringFX(seed=args.seed)
    
    # Parse FX chain
    if args.fx:
        fx_chain = []
        for fx_name in args.fx.split(','):
            fx_name = fx_name.strip()
            try:
                fx_type = StringFXType(fx_name)
                fx_chain.append(fx_type)
            except ValueError:
                print(f"⚠️  Unknown effect: {fx_name}")
                continue
    else:
        # Default FX chain
        fx_chain = [StringFXType.RAINBOW_GRADIENT, StringFXType.NEON_FX]
    
    # Create parameters
    params = StringFXParams(
        intensity=args.intensity,
        speed=args.speed,
        glitch_factor=args.glitch
    )
    
    # Apply effects
    result = fx_engine.apply_fx_chain(args.text, fx_chain, params)
    
    print(f"📝 Original: {args.text}")
    print(f"🎭 Result: {result}")
    print(f"🔧 FX Chain: {' → '.join([fx.value for fx in fx_chain])}")
    print(f"⚙️  Parameters: intensity={params.intensity}, speed={params.speed}, glitch={params.glitch_factor}")
    
    # Create HTML output if requested
    if args.output:
        html = fx_engine.create_fx_html(args.text, fx_chain, params)
        with open(args.output, "w") as f:
            f.write(html)
        print(f"🌐 HTML output: {args.output}")
    
    # Generate demo of all effects
    if not args.fx:
        print("\n🎭 All String Effects Demo:")
        print("-" * 30)
        demo = fx_engine.generate_fx_demo(args.text)
        for fx_name, fx_result in demo.items():
            print(f"{fx_name:20}: {fx_result[:50]}{'...' if len(fx_result) > 50 else ''}")


if __name__ == "__main__":
    main()
