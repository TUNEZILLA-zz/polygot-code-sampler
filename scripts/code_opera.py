#!/usr/bin/env python3
"""
🎭 Code Live - Code Opera
========================

Each backend (Rust, Python, Julia, etc.) is a "voice" in a choir.
Orchestrate textures + FX like vocal harmonies.
Visuals: particle swarms "singing" in sync with code loops.
"""

import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class VoiceType(Enum):
    """Voice types for the code opera choir"""
    RUST = "rust"  # Deep, powerful bass voice
    PYTHON = "python"  # Smooth, expressive tenor
    JULIA = "julia"  # Mathematical, precise soprano
    TYPESCRIPT = "typescript"  # Modern, versatile alto
    GO = "go"  # Steady, reliable baritone
    CSHARP = "csharp"  # Rich, enterprise bass
    SQL = "sql"  # Structured, harmonic foundation


@dataclass
class VoiceConfig:
    """Configuration for a voice in the code opera"""
    voice_type: VoiceType
    texture: str
    fx_chain: List[str]
    tempo: float  # BPM for this voice
    volume: float  # 0.0 to 1.0
    harmony_note: str  # Musical note for harmony
    visual_color: str  # Color for particle effects
    particle_behavior: str  # How particles move for this voice


class CodeOpera:
    """Code Opera - Multi-voice creative coding performance"""
    
    def __init__(self, output_dir: str = "out"):
        self.output_dir = Path(output_dir)
        self.setup_directories()
        self.voices = self._create_voice_choir()
    
    def setup_directories(self):
        """Create output directory structure for code opera"""
        dirs = ["opera", "voices", "harmony", "visuals", "performance"]
        
        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        print(f"🎭 Created Code Opera directory structure in {self.output_dir}")
    
    def _create_voice_choir(self) -> Dict[str, VoiceConfig]:
        """Create the voice choir configuration"""
        return {
            "rust": VoiceConfig(
                voice_type=VoiceType.RUST,
                texture="dense",
                fx_chain=["reverb", "distortion"],
                tempo=120.0,
                volume=0.8,
                harmony_note="C",
                visual_color="#dc2626",  # Red
                particle_behavior="powerful_bass"
            ),
            "python": VoiceConfig(
                voice_type=VoiceType.PYTHON,
                texture="smooth",
                fx_chain=["chorus", "delay"],
                tempo=110.0,
                volume=0.9,
                harmony_note="E",
                visual_color="#059669",  # Green
                particle_behavior="flowing_tenor"
            ),
            "julia": VoiceConfig(
                voice_type=VoiceType.JULIA,
                texture="fractal",
                fx_chain=["lfo", "reverb"],
                tempo=140.0,
                volume=0.7,
                harmony_note="G",
                visual_color="#7c3aed",  # Purple
                particle_behavior="mathematical_soprano"
            ),
            "typescript": VoiceConfig(
                voice_type=VoiceType.TYPESCRIPT,
                texture="polyphonic",
                fx_chain=["chorus", "delay"],
                tempo=115.0,
                volume=0.8,
                harmony_note="A",
                visual_color="#2563eb",  # Blue
                particle_behavior="versatile_alto"
            ),
            "go": VoiceConfig(
                voice_type=VoiceType.GO,
                texture="sparse",
                fx_chain=["reverb"],
                tempo=100.0,
                volume=0.6,
                harmony_note="D",
                visual_color="#0891b2",  # Cyan
                particle_behavior="steady_baritone"
            ),
            "csharp": VoiceConfig(
                voice_type=VoiceType.CSHARP,
                texture="maximal",
                fx_chain=["distortion", "reverb"],
                tempo=105.0,
                volume=0.7,
                harmony_note="F",
                visual_color="#be185d",  # Pink
                particle_behavior="enterprise_bass"
            ),
            "sql": VoiceConfig(
                voice_type=VoiceType.SQL,
                texture="minimal",
                fx_chain=["reverb"],
                tempo=90.0,
                volume=0.5,
                harmony_note="B",
                visual_color="#f59e0b",  # Amber
                particle_behavior="harmonic_foundation"
            )
        }
    
    def generate_voice_code(self, voice_name: str, voice_config: VoiceConfig) -> str:
        """Generate code for a specific voice"""
        print(f"🎭 Generating {voice_name} voice...")
        
        # Base code for this voice
        base_code = f"for i in range(16): process_{voice_name}(i)"
        
        try:
            # Apply texture transformation
            cmd = [
                "python3", "texture_cli.py", "apply",
                "--texture", voice_config.texture,
                "--code", base_code
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                # Extract the transformed code
                lines = result.stdout.split('\n')
                code_start = False
                transformed_code = []
                
                for line in lines:
                    if "Textured code:" in line:
                        code_start = True
                        continue
                    if code_start and line.strip() and not line.startswith("🎨"):
                        transformed_code.append(line)
                
                return '\n'.join(transformed_code)
            else:
                print(f"❌ {voice_name} voice failed: {result.stderr}")
                return base_code
                
        except Exception as e:
            print(f"❌ {voice_name} voice error: {e}")
            return base_code
    
    def create_harmony_visualization(self) -> str:
        """Create HTML visualization of the code opera harmony"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 Code Opera - Voice Harmony</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(45deg, #0f172a, #1e293b);
            color: #e2e8f0;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .opera-stage {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .title {{
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 40px;
            background: linear-gradient(45deg, #4b6cff, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .voice-choir {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        
        .voice-card {{
            background: rgba(75, 108, 255, 0.1);
            border: 2px solid #4b6cff;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }}
        
        .voice-name {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .voice-details {{
            margin: 10px 0;
        }}
        
        .particle-demo {{
            width: 100%;
            height: 100px;
            background: #0f172a;
            border: 1px solid #4b6cff;
            border-radius: 10px;
            margin: 10px 0;
            position: relative;
            overflow: hidden;
        }}
        
        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0) scale(1); opacity: 0.6; }}
            50% {{ transform: translateY(-20px) scale(1.2); opacity: 1.0; }}
        }}
        
        .harmony-visual {{
            width: 100%;
            height: 200px;
            background: linear-gradient(45deg, #0f172a, #1e293b);
            border: 2px solid #4b6cff;
            border-radius: 10px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }}
        
        .harmony-wave {{
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #4b6cff, #2dd4bf);
            transform: translateY(-50%);
            animation: harmony-pulse 2s ease-in-out infinite;
        }}
        
        @keyframes harmony-pulse {{
            0%, 100% {{ transform: translateY(-50%) scaleX(1); opacity: 0.8; }}
            50% {{ transform: translateY(-50%) scaleX(1.1); opacity: 1.0; }}
        }}
        
        .performance-controls {{
            text-align: center;
            margin: 40px 0;
        }}
        
        button {{
            background: linear-gradient(45deg, #4b6cff, #2dd4bf);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            margin: 10px;
            transition: all 0.3s ease;
        }}
        
        button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(75, 108, 255, 0.4);
        }}
    </style>
</head>
<body>
    <div class="opera-stage">
        <h1 class="title">🎭 Code Opera - Voice Harmony</h1>
        <p style="text-align: center; font-size: 1.2em; margin-bottom: 40px;">
            Each backend is a "voice" in a choir. Orchestrate textures + FX like vocal harmonies.
        </p>
        
        <div class="voice-choir">
"""
        
        # Add voice cards
        for voice_name, voice_config in self.voices.items():
            html_content += f"""
            <div class="voice-card">
                <div class="voice-name">{voice_name.upper()}</div>
                <div class="voice-details">
                    <strong>Texture:</strong> {voice_config.texture}<br>
                    <strong>FX Chain:</strong> {', '.join(voice_config.fx_chain)}<br>
                    <strong>Tempo:</strong> {voice_config.tempo} BPM<br>
                    <strong>Volume:</strong> {voice_config.volume}<br>
                    <strong>Harmony Note:</strong> {voice_config.harmony_note}
                </div>
                <div class="particle-demo" style="border-color: {voice_config.visual_color};">
                    <div class="particle" style="background: {voice_config.visual_color}; left: 20%; animation-delay: 0s;"></div>
                    <div class="particle" style="background: {voice_config.visual_color}; left: 40%; animation-delay: 0.5s;"></div>
                    <div class="particle" style="background: {voice_config.visual_color}; left: 60%; animation-delay: 1s;"></div>
                    <div class="particle" style="background: {voice_config.visual_color}; left: 80%; animation-delay: 1.5s;"></div>
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="harmony-visual">
            <div class="harmony-wave"></div>
        </div>
        
        <div class="performance-controls">
            <button onclick="startOpera()">🎭 Start Code Opera</button>
            <button onclick="stopOpera()">⏹️ Stop Performance</button>
            <button onclick="toggleHarmony()">🎵 Toggle Harmony</button>
        </div>
    </div>
    
    <script>
        let operaActive = false;
        let harmonyActive = false;
        
        function startOpera() {
            operaActive = true;
            console.log('🎭 Code Opera started!');
            // Add particle animation logic here
        }
        
        function stopOpera() {
            operaActive = false;
            console.log('⏹️ Code Opera stopped');
        }
        
        function toggleHarmony() {
            harmonyActive = !harmonyActive;
            console.log('🎵 Harmony:', harmonyActive ? 'ON' : 'OFF');
        }
    </script>
</body>
</html>
"""
        
        return html_content
    
    def run_code_opera(self):
        """Run the complete code opera performance"""
        print("\n🎭 Code Opera Performance")
        print("=" * 50)
        
        performance_data = {
            "timestamp": time.time(),
            "voices": {},
            "harmony": {},
            "performance_notes": []
        }
        
        # Generate code for each voice
        for voice_name, voice_config in self.voices.items():
            print(f"\n🎭 {voice_name.upper()} Voice:")
            print("-" * 30)
            
            # Generate voice code
            voice_code = self.generate_voice_code(voice_name, voice_config)
            
            # Save voice code
            voice_file = self.output_dir / "voices" / f"{voice_name}_voice.py"
            with open(voice_file, "w") as f:
                f.write(f"# {voice_name.upper()} Voice - {voice_config.texture} texture\n")
                f.write(f"# FX Chain: {', '.join(voice_config.fx_chain)}\n")
                f.write(f"# Tempo: {voice_config.tempo} BPM\n")
                f.write(f"# Harmony Note: {voice_config.harmony_note}\n\n")
                f.write(voice_code)
            
            # Store voice data
            performance_data["voices"][voice_name] = {
                "texture": voice_config.texture,
                "fx_chain": voice_config.fx_chain,
                "tempo": voice_config.tempo,
                "volume": voice_config.volume,
                "harmony_note": voice_config.harmony_note,
                "visual_color": voice_config.visual_color,
                "particle_behavior": voice_config.particle_behavior,
                "code_file": str(voice_file)
            }
            
            print(f"✅ {voice_name}: {voice_file}")
            print(f"   Texture: {voice_config.texture}")
            print(f"   FX: {', '.join(voice_config.fx_chain)}")
            print(f"   Tempo: {voice_config.tempo} BPM")
            print(f"   Harmony: {voice_config.harmony_note}")
        
        # Create harmony visualization
        print(f"\n🎭 Creating harmony visualization...")
        harmony_html = self.create_harmony_visualization()
        harmony_file = self.output_dir / "opera" / "code_opera_harmony.html"
        with open(harmony_file, "w") as f:
            f.write(harmony_html)
        
        print(f"✅ Harmony visualization: {harmony_file}")
        
        # Generate performance notes
        performance_notes = [
            "🎭 Code Opera Performance Notes:",
            "=" * 40,
            "",
            "Voice Choir:",
            "- Rust: Deep, powerful bass (dense texture, reverb+distortion)",
            "- Python: Smooth, expressive tenor (smooth texture, chorus+delay)",
            "- Julia: Mathematical, precise soprano (fractal texture, lfo+reverb)",
            "- TypeScript: Modern, versatile alto (polyphonic texture, chorus+delay)",
            "- Go: Steady, reliable baritone (sparse texture, reverb)",
            "- C#: Rich, enterprise bass (maximal texture, distortion+reverb)",
            "- SQL: Structured, harmonic foundation (minimal texture, reverb)",
            "",
            "Harmony Structure:",
            "- C (Rust) - Root note, powerful foundation",
            "- E (Python) - Major third, smooth expression",
            "- G (Julia) - Perfect fifth, mathematical precision",
            "- A (TypeScript) - Major sixth, modern versatility",
            "- D (Go) - Perfect fourth, steady reliability",
            "- F (C#) - Major second, enterprise richness",
            "- B (SQL) - Major seventh, harmonic foundation",
            "",
            "Visual Effects:",
            "- Each voice has unique particle behavior and color",
            "- Particles 'sing' in sync with code loops",
            "- Harmony visualization shows combined effects",
            "- Real-time performance controls for live coding"
        ]
        
        # Save performance notes
        notes_file = self.output_dir / "performance" / "code_opera_notes.txt"
        with open(notes_file, "w") as f:
            f.write('\n'.join(performance_notes))
        
        print(f"✅ Performance notes: {notes_file}")
        
        # Save performance data
        performance_data["harmony"]["html_file"] = str(harmony_file)
        performance_data["harmony"]["notes_file"] = str(notes_file)
        performance_data["performance_notes"] = performance_notes
        
        with open(self.output_dir / "opera" / "code_opera_data.json", "w") as f:
            json.dump(performance_data, f, indent=2)
        
        print(f"\n🎭 Code Opera Performance Complete!")
        print(f"📁 Check {self.output_dir}/opera/ for all artifacts")
        print(f"🌐 Open {harmony_file} to see the harmony visualization")
        
        return performance_data


def main():
    """Main entry point for Code Opera"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🎭 Code Live - Code Opera",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/code_opera.py
  python scripts/code_opera.py --output-dir out/opera
        """,
    )
    
    parser.add_argument("--output-dir", default="out", help="Output directory")
    
    args = parser.parse_args()
    
    print("🎭 Code Live - Code Opera")
    print("=" * 50)
    print("Each backend is a 'voice' in a choir.")
    print("Orchestrate textures + FX like vocal harmonies.")
    print("Visuals: particle swarms 'singing' in sync with code loops.")
    print()
    
    # Create Code Opera
    opera = CodeOpera(output_dir=args.output_dir)
    
    # Run the performance
    performance_data = opera.run_code_opera()
    
    print("\n🎉 Code Opera Performance Complete!")
    print("🎭 Ready for the next creative coding session!")


if __name__ == "__main__":
    main()
