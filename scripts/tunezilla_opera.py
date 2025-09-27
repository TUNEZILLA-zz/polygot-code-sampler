#!/usr/bin/env python3
"""
🎭 TuneZilla Opera - Brand-Integrated Code Opera
===============================================

TuneZilla-specific Code Opera with brand elements:
- Opera Mask Mode (glitching masks for each voice)
- Crow & Lizard Chorus (percussive layers)
- Gold & Emerald Stage (visual themes)
- Glitch Libretto (poetry fragments as comments)
- Performance Mode (live gesture control)
"""

import os
import json
import time
import random
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TuneZillaVoice(Enum):
    """TuneZilla-specific voice types with brand elements"""

    PYTHON_TENOR = "python_tenor"  # Smooth, emerald-masked
    RUST_BASS = "rust_bass"  # Dense, gold-masked
    JULIA_SOPRANO = "julia_soprano"  # Fractal, crow-masked
    TYPESCRIPT_ALTO = "typescript_alto"  # Polyphonic, lizard-masked
    GO_BARITONE = "go_baritone"  # Sparse, emerald-masked
    CSHARP_BASS = "csharp_bass"  # Maximal, gold-masked
    SQL_FOUNDATION = "sql_foundation"  # Minimal, crow-masked


@dataclass
class TuneZillaMask:
    """TuneZilla mask configuration for each voice"""

    mask_type: str  # "emerald", "gold", "crow", "lizard"
    glitch_pattern: str  # "fractal", "wave", "pulse", "storm"
    color_primary: str  # Primary mask color
    color_secondary: str  # Secondary mask color
    animation_speed: float  # Mask animation speed


@dataclass
class TuneZillaVoiceConfig:
    """TuneZilla voice configuration with brand elements"""

    voice_type: TuneZillaVoice
    texture: str
    fx_chain: List[str]
    tempo: float
    volume: float
    harmony_note: str
    visual_color: str
    particle_behavior: str
    mask: TuneZillaMask
    glitch_libretto: List[str]  # Poetry fragments for comments
    crow_layers: int  # Number of crow percussive layers
    lizard_clones: int  # Number of lizard fractal formations


class TuneZillaOpera:
    """TuneZilla Opera - Brand-integrated creative coding performance"""

    def __init__(self, output_dir: str = "out", seed: Optional[str] = None):
        self.output_dir = Path(output_dir)
        self.seed = seed
        self.setup_directories()
        self.voices = self._create_tunezilla_choir()

        # Set deterministic seed if provided
        if self.seed:
            self._set_deterministic_seed()

    def setup_directories(self):
        """Create TuneZilla Opera directory structure"""
        dirs = ["tunezilla_opera", "masks", "libretto", "performance", "visuals"]

        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)

        print(f"🎭 Created TuneZilla Opera directory structure in {self.output_dir}")

    def _set_deterministic_seed(self):
        """Set deterministic seed for reproducible runs"""
        if self.seed:
            random.seed(self.seed)

            # Write seed to file for reproducibility
            seed_file = self.output_dir / "tunezilla_opera" / "SEED.txt"
            with open(seed_file, "w") as f:
                f.write(self.seed)

            print(f"🎭 Set deterministic seed: {self.seed}")

    def _create_tunezilla_choir(self) -> Dict[str, TuneZillaVoiceConfig]:
        """Create the TuneZilla voice choir with brand elements"""
        return {
            "python_tenor": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.PYTHON_TENOR,
                texture="smooth",
                fx_chain=["chorus", "delay"],
                tempo=110.0,
                volume=0.8,
                harmony_note="E",
                visual_color="#00ff88",  # Emerald
                particle_behavior="flowing_arcs",
                mask=TuneZillaMask(
                    mask_type="emerald",
                    glitch_pattern="wave",
                    color_primary="#00ff88",
                    color_secondary="#00cc66",
                    animation_speed=1.0,
                ),
                glitch_libretto=[
                    "✦ fracture in the loop ✦",
                    "voices collide at 432hz",
                    "emerald fog rises",
                ],
                crow_layers=2,
                lizard_clones=1,
            ),
            "rust_bass": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.RUST_BASS,
                texture="dense",
                fx_chain=["reverb", "distortion"],
                tempo=120.0,
                volume=0.9,
                harmony_note="C",
                visual_color="#ffd700",  # Gold
                particle_behavior="cluster_clouds",
                mask=TuneZillaMask(
                    mask_type="gold",
                    glitch_pattern="storm",
                    color_primary="#ffd700",
                    color_secondary="#ffb700",
                    animation_speed=1.5,
                ),
                glitch_libretto=[
                    "✦ golden glitch storm ✦",
                    "rust bass + sql foundation",
                    "crows circle the stage",
                ],
                crow_layers=3,
                lizard_clones=2,
            ),
            "julia_soprano": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.JULIA_SOPRANO,
                texture="fractal",
                fx_chain=["lfo", "reverb"],
                tempo=140.0,
                volume=0.7,
                harmony_note="G",
                visual_color="#ff6b6b",  # Red
                particle_behavior="fractal_explosion",
                mask=TuneZillaMask(
                    mask_type="crow",
                    glitch_pattern="fractal",
                    color_primary="#ff6b6b",
                    color_secondary="#ff4444",
                    animation_speed=2.0,
                ),
                glitch_libretto=[
                    "✦ recursive explosion ✦",
                    "julia's soprano fragments",
                    "lizard clones multiply",
                ],
                crow_layers=4,
                lizard_clones=3,
            ),
            "typescript_alto": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.TYPESCRIPT_ALTO,
                texture="polyphonic",
                fx_chain=["chorus", "delay"],
                tempo=115.0,
                volume=0.8,
                harmony_note="A",
                visual_color="#8b5cf6",  # Purple
                particle_behavior="polyphonic_layers",
                mask=TuneZillaMask(
                    mask_type="lizard",
                    glitch_pattern="pulse",
                    color_primary="#8b5cf6",
                    color_secondary="#6b46c1",
                    animation_speed=1.2,
                ),
                glitch_libretto=[
                    "✦ polyphonic layers ✦",
                    "typescript weaves harmony",
                    "lizard clones dance",
                ],
                crow_layers=2,
                lizard_clones=4,
            ),
            "go_baritone": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.GO_BARITONE,
                texture="sparse",
                fx_chain=["reverb"],
                tempo=100.0,
                volume=0.6,
                harmony_note="D",
                visual_color="#00ff88",  # Emerald
                particle_behavior="isolated_points",
                mask=TuneZillaMask(
                    mask_type="emerald",
                    glitch_pattern="wave",
                    color_primary="#00ff88",
                    color_secondary="#00cc66",
                    animation_speed=0.8,
                ),
                glitch_libretto=[
                    "✦ sparse foundation ✦",
                    "go's steady rhythm",
                    "emerald pulses",
                ],
                crow_layers=1,
                lizard_clones=1,
            ),
            "csharp_bass": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.CSHARP_BASS,
                texture="maximal",
                fx_chain=["distortion", "reverb"],
                tempo=105.0,
                volume=0.7,
                harmony_note="F",
                visual_color="#ffd700",  # Gold
                particle_behavior="maximal_chaos",
                mask=TuneZillaMask(
                    mask_type="gold",
                    glitch_pattern="storm",
                    color_primary="#ffd700",
                    color_secondary="#ffb700",
                    animation_speed=1.8,
                ),
                glitch_libretto=[
                    "✦ maximal enterprise ✦",
                    "csharp's rich foundation",
                    "golden glitch storm",
                ],
                crow_layers=2,
                lizard_clones=2,
            ),
            "sql_foundation": TuneZillaVoiceConfig(
                voice_type=TuneZillaVoice.SQL_FOUNDATION,
                texture="minimal",
                fx_chain=["reverb"],
                tempo=90.0,
                volume=0.5,
                harmony_note="B",
                visual_color="#ff6b6b",  # Red
                particle_behavior="minimal_structure",
                mask=TuneZillaMask(
                    mask_type="crow",
                    glitch_pattern="pulse",
                    color_primary="#ff6b6b",
                    color_secondary="#ff4444",
                    animation_speed=0.5,
                ),
                glitch_libretto=[
                    "✦ minimal structure ✦",
                    "sql's harmonic foundation",
                    "crow's steady caw",
                ],
                crow_layers=1,
                lizard_clones=0,
            ),
        }

    def generate_voice_code(
        self, voice_name: str, voice_config: TuneZillaVoiceConfig
    ) -> str:
        """Generate code for a TuneZilla voice with brand elements"""
        # Add glitch libretto as comments
        libretto_comments = "\n".join(
            [f"# {line}" for line in voice_config.glitch_libretto]
        )

        # Generate voice-specific code based on texture
        if voice_config.texture == "smooth":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Smooth, flowing emerald tenor
    for i in range(16):
        process_smooth(i, voice_config.volume)
        if i % 4 == 0:
            crow_caw(i // 4)
        if i % 8 == 0:
            lizard_dance(i // 8)
"""
        elif voice_config.texture == "dense":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Dense, powerful gold bass
    for i in range(20):
        process_dense(i, voice_config.volume)
        for crow in range(voice_config.crow_layers):
            crow_caw(i, crow)
        for lizard in range(voice_config.lizard_clones):
            lizard_fractal(i, lizard)
"""
        elif voice_config.texture == "fractal":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Fractal, recursive crow soprano
    for i in range(12):
        process_fractal(i, voice_config.volume)
        for depth in range(3):
            fractal_explosion(i, depth)
        for crow in range(voice_config.crow_layers):
            crow_fractal(i, crow)
        for lizard in range(voice_config.lizard_clones):
            lizard_recursive(i, lizard)
"""
        elif voice_config.texture == "polyphonic":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Polyphonic, layered lizard alto
    for i in range(14):
        process_polyphonic(i, voice_config.volume)
        for voice in range(3):
            harmony_voice(i, voice)
        for lizard in range(voice_config.lizard_clones):
            lizard_polyphonic(i, lizard)
        for crow in range(voice_config.crow_layers):
            crow_harmony(i, crow)
"""
        elif voice_config.texture == "sparse":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Sparse, minimal emerald baritone
    for i in range(8):
        process_sparse(i, voice_config.volume)
        if i % 2 == 0:
            emerald_pulse(i)
        if i % 4 == 0:
            crow_minimal(i)
"""
        elif voice_config.texture == "maximal":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Maximal, chaotic gold bass
    for i in range(24):
        process_maximal(i, voice_config.volume)
        for layer in range(4):
            chaos_layer(i, layer)
        for crow in range(voice_config.crow_layers):
            crow_chaos(i, crow)
        for lizard in range(voice_config.lizard_clones):
            lizard_chaos(i, lizard)
"""
        elif voice_config.texture == "minimal":
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Minimal, structured crow foundation
    for i in range(6):
        process_minimal(i, voice_config.volume)
        crow_steady(i)
        if i % 3 == 0:
            foundation_pulse(i)
"""
        else:
            code = f"""
# {voice_config.voice_type.value.upper()} Voice - TuneZilla Opera
# {voice_config.mask.mask_type.title()} Mask - {voice_config.mask.glitch_pattern.title()} Pattern
# Crow Layers: {voice_config.crow_layers}, Lizard Clones: {voice_config.lizard_clones}

{libretto_comments}

def {voice_name}_voice():
    # Default TuneZilla voice
    for i in range(10):
        process_tunezilla(i, voice_config.volume)
"""

        return code.strip()

    def create_mask_visualization(
        self, voice_name: str, voice_config: TuneZillaVoiceConfig
    ) -> str:
        """Create HTML visualization for TuneZilla mask"""
        mask_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 {voice_name.upper()} - TuneZilla Mask</title>
    <style>
        body {{
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e);
            color: {voice_config.mask.color_primary};
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        .mask-container {{
            position: relative;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: radial-gradient(circle, {voice_config.mask.color_primary}, {voice_config.mask.color_secondary});
            animation: {voice_config.mask.glitch_pattern} {voice_config.mask.animation_speed}s ease-in-out infinite;
        }}
        
        @keyframes fractal {{
            0%, 100% {{ transform: scale(1) rotate(0deg); }}
            50% {{ transform: scale(1.2) rotate(180deg); }}
        }}
        
        @keyframes wave {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.1); opacity: 1; }}
        }}
        
        @keyframes storm {{
            0%, 100% {{ transform: scale(1) rotate(0deg); }}
            25% {{ transform: scale(1.1) rotate(90deg); }}
            50% {{ transform: scale(1.2) rotate(180deg); }}
            75% {{ transform: scale(1.1) rotate(270deg); }}
        }}
        
        .mask-title {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
            z-index: 10;
        }}
        
        .crow-layers {{
            position: absolute;
            top: 10%;
            right: 10%;
            width: 50px;
            height: 50px;
            background: {voice_config.mask.color_primary};
            border-radius: 50%;
            animation: crowFly 2s ease-in-out infinite;
        }}
        
        @keyframes crowFly {{
            0%, 100% {{ transform: translateY(0) rotate(0deg); }}
            50% {{ transform: translateY(-10px) rotate(5deg); }}
        }}
        
        .lizard-clones {{
            position: absolute;
            bottom: 10%;
            left: 10%;
            width: 40px;
            height: 40px;
            background: {voice_config.mask.color_secondary};
            border-radius: 20px;
            animation: lizardSplit 3s ease-in-out infinite;
        }}
        
        @keyframes lizardSplit {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2) rotate(45deg); }}
        }}
    </style>
</head>
<body>
    <div class="mask-container">
        <div class="mask-title">
            {voice_name.upper()}<br>
            <small>{voice_config.mask.mask_type.title()} Mask</small>
        </div>
        <div class="crow-layers"></div>
        <div class="lizard-clones"></div>
    </div>
</body>
</html>
"""
        return mask_html

    def run_tunezilla_opera(self):
        """Run the complete TuneZilla Opera performance"""
        print("\n🎭 TuneZilla Opera Performance")
        print("=" * 50)

        performance_data = {
            "timestamp": time.time(),
            "seed": self.seed,
            "voices": {},
            "masks": {},
            "libretto": {},
            "performance_notes": [],
        }

        # Generate code for each voice
        for voice_name, voice_config in self.voices.items():
            print(f"\n🎭 {voice_name.upper()} Voice:")
            print("-" * 30)

            # Generate voice code
            voice_code = self.generate_voice_code(voice_name, voice_config)

            # Save voice code
            voice_file = self.output_dir / "tunezilla_opera" / f"{voice_name}_voice.py"
            with open(voice_file, "w") as f:
                f.write(voice_code)

            # Create mask visualization
            mask_html = self.create_mask_visualization(voice_name, voice_config)
            mask_file = self.output_dir / "masks" / f"{voice_name}_mask.html"
            with open(mask_file, "w") as f:
                f.write(mask_html)

            # Store voice data
            performance_data["voices"][voice_name] = {
                "texture": voice_config.texture,
                "fx_chain": voice_config.fx_chain,
                "tempo": voice_config.tempo,
                "volume": voice_config.volume,
                "harmony_note": voice_config.harmony_note,
                "visual_color": voice_config.visual_color,
                "particle_behavior": voice_config.particle_behavior,
                "mask_type": voice_config.mask.mask_type,
                "glitch_pattern": voice_config.mask.glitch_pattern,
                "crow_layers": voice_config.crow_layers,
                "lizard_clones": voice_config.lizard_clones,
                "code_file": str(voice_file),
                "mask_file": str(mask_file),
            }

            # Store mask data
            performance_data["masks"][voice_name] = {
                "mask_type": voice_config.mask.mask_type,
                "glitch_pattern": voice_config.mask.glitch_pattern,
                "color_primary": voice_config.mask.color_primary,
                "color_secondary": voice_config.mask.color_secondary,
                "animation_speed": voice_config.mask.animation_speed,
            }

            # Store libretto data
            performance_data["libretto"][voice_name] = voice_config.glitch_libretto

            print(f"✅ {voice_name}: {voice_file}")
            print(f"   Texture: {voice_config.texture}")
            print(f"   FX: {', '.join(voice_config.fx_chain)}")
            print(f"   Tempo: {voice_config.tempo} BPM")
            print(f"   Harmony: {voice_config.harmony_note}")
            print(
                f"   Mask: {voice_config.mask.mask_type} ({voice_config.mask.glitch_pattern})"
            )
            print(f"   Crow Layers: {voice_config.crow_layers}")
            print(f"   Lizard Clones: {voice_config.lizard_clones}")

        # Create TuneZilla Opera visualization
        print(f"\n🎭 Creating TuneZilla Opera visualization...")
        opera_html = self.create_tunezilla_opera_visualization()
        opera_file = self.output_dir / "tunezilla_opera" / "tunezilla_opera.html"
        with open(opera_file, "w") as f:
            f.write(opera_html)

        print(f"✅ TuneZilla Opera visualization: {opera_file}")

        # Generate performance notes
        performance_notes = [
            "🎭 TuneZilla Opera Performance Notes:",
            "=" * 40,
            "",
            "Brand Elements:",
            "- Opera Mask Mode: Each voice wears a glitching mask",
            "- Crow & Lizard Chorus: Percussive layers and fractal formations",
            "- Gold & Emerald Stage: Visual themes matching TuneZilla brand",
            "- Glitch Libretto: Poetry fragments as code comments",
            "- Performance Mode: Live gesture control for particles",
            "",
            "Voice Choir:",
            "- Python Tenor: Smooth, emerald-masked, crow layers",
            "- Rust Bass: Dense, gold-masked, storm pattern",
            "- Julia Soprano: Fractal, crow-masked, recursive explosion",
            "- TypeScript Alto: Polyphonic, lizard-masked, pulse pattern",
            "- Go Baritone: Sparse, emerald-masked, wave pattern",
            "- C# Bass: Maximal, gold-masked, storm pattern",
            "- SQL Foundation: Minimal, crow-masked, pulse pattern",
            "",
            "Visual Effects:",
            "- Each voice has unique mask with glitch patterns",
            "- Crow layers provide percussive elements",
            "- Lizard clones create fractal formations",
            "- Gold and emerald color schemes",
            "- Real-time performance controls for live coding",
        ]

        # Save performance notes
        notes_file = self.output_dir / "performance" / "tunezilla_opera_notes.txt"
        with open(notes_file, "w") as f:
            f.write("\n".join(performance_notes))

        print(f"✅ Performance notes: {notes_file}")

        # Save performance data
        performance_data["opera_html"] = str(opera_file)
        performance_data["performance_notes"] = performance_notes

        with open(
            self.output_dir / "tunezilla_opera" / "tunezilla_opera_data.json", "w"
        ) as f:
            json.dump(performance_data, f, indent=2)

        print(f"\n🎭 TuneZilla Opera Performance Complete!")
        print(f"📁 Check {self.output_dir}/tunezilla_opera/ for all artifacts")
        print(f"🌐 Open {opera_file} to see the TuneZilla Opera visualization")

        return performance_data

    def create_tunezilla_opera_visualization(self) -> str:
        """Create HTML visualization for TuneZilla Opera"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 TuneZilla Opera - Visual Storyboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff88;
            font-family: 'Orbitron', monospace;
            overflow-x: hidden;
            min-height: 100vh;
        }}
        
        .poster-container {{
            position: relative;
            width: 100vw;
            min-height: 100vh;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 255, 136, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
                linear-gradient(45deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        }}
        
        .main-title {{
            position: relative;
            text-align: center;
            padding: 2rem 0;
            z-index: 10;
        }}
        
        .title-text {{
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00ff88, #ffd700, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
            animation: titleGlow 2s ease-in-out infinite alternate;
        }}
        
        @keyframes titleGlow {{
            from {{ text-shadow: 0 0 30px rgba(0, 255, 136, 0.5); }}
            to {{ text-shadow: 0 0 50px rgba(255, 215, 0, 0.8); }}
        }}
        
        .subtitle {{
            font-size: 1.5rem;
            color: #ffd700;
            margin-top: 1rem;
            font-family: 'Space Mono', monospace;
        }}
        
        .voices-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
            z-index: 10;
            position: relative;
        }}
        
        .voice-card {{
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid;
            border-radius: 15px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .voice-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        }}
        
        .voice-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }}
        
        .glitch-libretto {{
            font-family: 'Space Mono', monospace;
            color: #ff6b6b;
            font-size: 0.9rem;
            line-height: 1.4;
            margin: 1rem 0;
            animation: textGlitch 0.5s infinite;
        }}
        
        @keyframes textGlitch {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-1px); }}
            75% {{ transform: translateX(1px); }}
        }}
        
        .voice-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .detail-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            font-size: 0.8rem;
        }}
        
        .tunezilla-mask {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(0, 255, 136, 0.3), transparent);
            border-radius: 50%;
            animation: maskPulse 3s ease-in-out infinite;
            z-index: 5;
        }}
        
        @keyframes maskPulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.3; }}
            50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; }}
        }}
        
        .crow-flock {{
            position: absolute;
            top: 10%;
            right: 10%;
            width: 100px;
            height: 100px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M20,30 Q30,20 40,30 Q50,40 60,30 Q70,20 80,30" stroke="%2300ff88" stroke-width="2" fill="none"/><circle cx="25" cy="25" r="2" fill="%2300ff88"/><circle cx="35" cy="25" r="2" fill="%2300ff88"/><circle cx="45" cy="25" r="2" fill="%2300ff88"/><circle cx="55" cy="25" r="2" fill="%2300ff88"/><circle cx="65" cy="25" r="2" fill="%2300ff88"/><circle cx="75" cy="25" r="2" fill="%2300ff88"/></svg>') no-repeat center;
            animation: crowFly 4s ease-in-out infinite;
        }}
        
        @keyframes crowFly {{
            0%, 100% {{ transform: translateY(0) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(5deg); }}
        }}
        
        .emerald-fractals {{
            position: absolute;
            bottom: 10%;
            left: 10%;
            width: 150px;
            height: 150px;
            background: 
                conic-gradient(from 0deg, transparent, #00ff88, transparent, #00ff88, transparent);
            border-radius: 50%;
            animation: fractalSpin 6s linear infinite;
            opacity: 0.6;
        }}
        
        @keyframes fractalSpin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .gold-storm {{
            position: absolute;
            top: 20%;
            left: 20%;
            width: 100px;
            height: 100px;
            background: 
                radial-gradient(circle, #ffd700, transparent),
                conic-gradient(from 45deg, #ffd700, transparent, #ffd700, transparent);
            animation: goldPulse 2s ease-in-out infinite;
        }}
        
        @keyframes goldPulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.4; }}
            50% {{ transform: scale(1.5); opacity: 0.8; }}
        }}
        
        .dollar-signs {{
            position: absolute;
            top: 30%;
            right: 30%;
            font-size: 2rem;
            color: #ffd700;
            animation: dollarFloat 3s ease-in-out infinite;
        }}
        
        @keyframes dollarFloat {{
            0%, 100% {{ transform: translateY(0) rotate(0deg); }}
            50% {{ transform: translateY(-10px) rotate(10deg); }}
        }}
        
        .lizard-clones {{
            position: absolute;
            bottom: 20%;
            right: 20%;
            width: 80px;
            height: 80px;
            background: 
                linear-gradient(45deg, #00ff88, #ffd700),
                conic-gradient(from 0deg, #00ff88, transparent, #ffd700, transparent);
            border-radius: 20px;
            animation: lizardSplit 4s ease-in-out infinite;
        }}
        
        @keyframes lizardSplit {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.2) rotate(45deg); }}
        }}
        
        .performance-notes {{
            position: absolute;
            bottom: 2rem;
            right: 2rem;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 1rem;
            max-width: 300px;
            font-size: 0.8rem;
        }}
        
        .performance-notes h4 {{
            color: #ffd700;
            margin-bottom: 0.5rem;
        }}
        
        .performance-notes p {{
            margin: 0.25rem 0;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .title-text {{
                font-size: 2.5rem;
            }}
            
            .voices-container {{
                grid-template-columns: 1fr;
                padding: 1rem;
            }}
            
            .voice-card {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="poster-container">
        <!-- TuneZilla Elements -->
        <div class="tunezilla-mask"></div>
        <div class="crow-flock"></div>
        <div class="emerald-fractals"></div>
        <div class="gold-storm"></div>
        <div class="dollar-signs">$$$</div>
        <div class="lizard-clones"></div>
        
        <!-- Main Title -->
        <div class="main-title">
            <h1 class="title-text">🎭 THE TUNEZILLA OPERA</h1>
            <p class="subtitle">A Surreal Musical-Tech Performance</p>
        </div>
        
        <!-- Voices -->
        <div class="voices-container">
"""

        # Add voice cards
        for voice_name, voice_config in self.voices.items():
            html_content += f"""
            <div class="voice-card" style="border-color: {voice_config.visual_color};">
                <h2 class="voice-title" style="color: {voice_config.visual_color};">
                    {voice_name.upper()}
                </h2>
                <div class="glitch-libretto">
                    {'<br>'.join(voice_config.glitch_libretto)}
                </div>
                <div class="voice-details">
                    <div class="detail-item">
                        <strong>Texture:</strong><br>{voice_config.texture.title()}
                    </div>
                    <div class="detail-item">
                        <strong>FX:</strong><br>{', '.join(voice_config.fx_chain)}
                    </div>
                    <div class="detail-item">
                        <strong>Mask:</strong><br>{voice_config.mask.mask_type.title()}
                    </div>
                    <div class="detail-item">
                        <strong>Pattern:</strong><br>{voice_config.mask.glitch_pattern.title()}
                    </div>
                    <div class="detail-item">
                        <strong>Crows:</strong><br>{voice_config.crow_layers}
                    </div>
                    <div class="detail-item">
                        <strong>Lizards:</strong><br>{voice_config.lizard_clones}
                    </div>
                </div>
            </div>
"""

        html_content += """
        </div>
        
        <!-- Performance Notes -->
        <div class="performance-notes">
            <h4>🎭 Performance Mode</h4>
            <p>• TuneZilla conducts with gestures</p>
            <p>• Particles + code voices shift textures</p>
            <p>• Live projector in music video sets</p>
            <p>• Real-time BPM + key modulation</p>
        </div>
    </div>
    
    <script>
        // Add interactive effects
        document.addEventListener('mousemove', (e) => {
            const mask = document.querySelector('.tunezilla-mask');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            mask.style.transform = `translate(${-50 + x * 20}%, ${-50 + y * 20}%)`;
        });
        
        // Add keyboard controls for live performance
        document.addEventListener('keydown', (e) => {
            if (e.key === ' ') {
                // Spacebar triggers glitch effect
                document.body.style.animation = 'glitch 0.1s infinite';
                setTimeout(() => {
                    document.body.style.animation = '';
                }, 1000);
            }
        });
        
        // Add performance mode toggle
        let performanceMode = false;
        document.addEventListener('keydown', (e) => {
            if (e.key === 'p' || e.key === 'P') {
                performanceMode = !performanceMode;
                if (performanceMode) {
                    document.body.style.background = 'linear-gradient(45deg, #ff6b6b, #ffd700, #00ff88)';
                    console.log('🎭 Performance Mode Activated!');
                } else {
                    document.body.style.background = 'linear-gradient(45deg, #0a0a0a, #1a1a2e, #16213e)';
                    console.log('🎭 Performance Mode Deactivated');
                }
            }
        });
        
        console.log('🎭 The TuneZilla Opera - Visual Storyboard Loaded');
        console.log('🎭 Press SPACE for glitch effect, P for performance mode');
    </script>
</body>
</html>
"""

        return html_content


def main():
    """Main entry point for TuneZilla Opera"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🎭 TuneZilla Opera - Brand-Integrated Code Opera",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/tunezilla_opera.py
  python scripts/tunezilla_opera.py --output-dir out/tunezilla
        """,
    )

    parser.add_argument("--output-dir", default="out", help="Output directory")
    parser.add_argument("--seed", help="Deterministic seed for reproducible runs")

    args = parser.parse_args()

    print("🎭 TuneZilla Opera - Brand-Integrated Code Opera")
    print("=" * 50)
    print("TuneZilla-specific Code Opera with brand elements:")
    print("- Opera Mask Mode (glitching masks for each voice)")
    print("- Crow & Lizard Chorus (percussive layers)")
    print("- Gold & Emerald Stage (visual themes)")
    print("- Glitch Libretto (poetry fragments as comments)")
    print("- Performance Mode (live gesture control)")
    print()

    # Create TuneZilla Opera
    opera = TuneZillaOpera(output_dir=args.output_dir, seed=args.seed)

    # Run the performance
    performance_data = opera.run_tunezilla_opera()

    print("\n🎉 TuneZilla Opera Performance Complete!")
    print("🎭 Ready for the next creative coding session!")


if __name__ == "__main__":
    main()
