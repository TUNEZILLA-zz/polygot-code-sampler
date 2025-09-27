"""
Cosmic Dust FX - Infinite Space Vibe
====================================

Cosmic dust as both a visual layer and textual FX family.
Ties perfectly into the light + chromatic + string FX universe.
"""

import random
import math
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class CosmicDustType(Enum):
    """Types of cosmic dust effects"""

    NEBULA = "nebula"
    METEOR_TRAIL = "meteor_trail"
    STARDUST_PULSE = "stardust_pulse"
    SUPERNOVA_BURST = "supernova_burst"
    BLACK_HOLE_FADE = "black_hole_fade"


@dataclass
class CosmicDustParams:
    """Parameters for cosmic dust effects"""

    density: float = 0.3  # 0.0 to 1.0
    intensity: float = 0.7  # 0.0 to 1.0
    spread: float = 0.5  # 0.0 to 1.0
    fade_depth: float = 0.8  # 0.0 to 1.0
    spectrum_shimmer: float = 0.6  # 0.0 to 1.0
    polarity_shift: float = 0.0  # -1.0 to 1.0
    saturation: float = 0.8  # 0.0 to 1.0
    grid_size: int = 3  # 1 to 10


class CosmicDustEngine:
    """Engine for cosmic dust effects"""

    def __init__(self):
        self.cosmic_chars = {
            "dots": ["·", "•", "✦", "✧", "⁂", "⁑", "✴", "✵", "✶", "✷"],
            "noise": ["░", "▓", "▒", "█", "▄", "▀", "▌", "▐", "▖", "▗"],
            "stars": ["★", "☆", "✩", "✪", "✫", "✬", "✭", "✮", "✯", "✰"],
            "sparkles": ["✨", "⭐", "🌟", "💫", "⚡", "🔥", "💥", "💢", "💣", "💤"],
            "space": ["🌌", "🌠", "🌅", "🌆", "🌇", "🌃", "🌄", "🌊", "🌋", "🌍"],
        }

        self.rgb_spectrum = [
            (255, 0, 0),  # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (127, 255, 0),  # Lime
            (0, 255, 0),  # Green
            (0, 255, 127),  # Spring Green
            (0, 255, 255),  # Cyan
            (0, 127, 255),  # Sky Blue
            (0, 0, 255),  # Blue
            (127, 0, 255),  # Purple
            (255, 0, 255),  # Magenta
            (255, 0, 127),  # Rose
        ]

    def apply_cosmic_dust(
        self, text: str, dust_type: CosmicDustType, params: CosmicDustParams
    ) -> str:
        """Apply cosmic dust effect to text"""
        if dust_type == CosmicDustType.NEBULA:
            return self._apply_nebula_dust(text, params)
        elif dust_type == CosmicDustType.METEOR_TRAIL:
            return self._apply_meteor_trail(text, params)
        elif dust_type == CosmicDustType.STARDUST_PULSE:
            return self._apply_stardust_pulse(text, params)
        elif dust_type == CosmicDustType.SUPERNOVA_BURST:
            return self._apply_supernova_burst(text, params)
        elif dust_type == CosmicDustType.BLACK_HOLE_FADE:
            return self._apply_black_hole_fade(text, params)
        else:
            return text

    def _apply_nebula_dust(self, text: str, params: CosmicDustParams) -> str:
        """Apply nebula dust - swirling, soft gradient particles"""
        result = []
        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add nebula dust particles
            if random.random() < params.density:
                # Swirling pattern
                angle = (i * 0.5) % (2 * math.pi)
                radius = params.spread * 3

                # Add multiple dust particles
                for j in range(int(params.intensity * 5)):
                    dust_char = random.choice(self.cosmic_chars["dots"])
                    # Position dust around character
                    offset = int(radius * math.sin(angle + j * 0.5))
                    if offset != 0:
                        result.append(" " * abs(offset) + dust_char)
                    else:
                        result.append(dust_char)

        return "".join(result)

    def _apply_meteor_trail(self, text: str, params: CosmicDustParams) -> str:
        """Apply meteor trail - streaked dust following characters"""
        result = []
        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add meteor trail
            if random.random() < params.density:
                trail_length = int(params.intensity * 8)
                for j in range(trail_length):
                    dust_char = random.choice(self.cosmic_chars["stars"])
                    # Fade trail intensity
                    fade = 1.0 - (j / trail_length) * params.fade_depth
                    if random.random() < fade:
                        result.append(dust_char)

        return "".join(result)

    def _apply_stardust_pulse(self, text: str, params: CosmicDustParams) -> str:
        """Apply stardust pulse - dust clusters that breathe in/out"""
        result = []
        pulse_phase = math.sin(params.intensity * math.pi)

        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add pulsing stardust
            if random.random() < params.density * (0.5 + 0.5 * pulse_phase):
                # Create dust cluster
                cluster_size = int(params.intensity * 6)
                for j in range(cluster_size):
                    dust_char = random.choice(self.cosmic_chars["sparkles"])
                    # Pulse effect
                    pulse_intensity = 0.5 + 0.5 * math.sin(i * 0.3 + j * 0.2)
                    if random.random() < pulse_intensity:
                        result.append(dust_char)

        return "".join(result)

    def _apply_supernova_burst(self, text: str, params: CosmicDustParams) -> str:
        """Apply supernova burst - sudden explosion of dust on impact moments"""
        result = []
        burst_threshold = 0.8

        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Check for burst moment
            if random.random() < params.density * burst_threshold:
                # Supernova explosion
                explosion_size = int(params.intensity * 12)
                for j in range(explosion_size):
                    dust_char = random.choice(self.cosmic_chars["sparkles"])
                    # Radial explosion pattern
                    angle = (j / explosion_size) * 2 * math.pi
                    radius = int(params.spread * 5)
                    offset = int(radius * math.cos(angle))
                    if offset != 0:
                        result.append(" " * abs(offset) + dust_char)
                    else:
                        result.append(dust_char)

        return "".join(result)

    def _apply_black_hole_fade(self, text: str, params: CosmicDustParams) -> str:
        """Apply black hole fade - dust pulled inward toward center"""
        result = []
        center = len(text) // 2

        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add black hole dust
            if random.random() < params.density:
                # Calculate distance from center
                distance = abs(i - center)
                max_distance = len(text) // 2

                # Dust gets pulled toward center
                pull_strength = 1.0 - (distance / max_distance) * params.fade_depth
                if random.random() < pull_strength:
                    dust_char = random.choice(self.cosmic_chars["space"])
                    # Position dust toward center
                    if i < center:
                        result.append(dust_char)
                    else:
                        result.append(" " + dust_char)

        return "".join(result)

    def apply_spectrum_dust(self, text: str, params: CosmicDustParams) -> str:
        """Apply spectrum dust with RGB shimmer"""
        result = []

        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add spectrum dust
            if random.random() < params.density:
                dust_char = random.choice(self.cosmic_chars["dots"])

                # RGB spectrum shimmer
                spectrum_index = int(
                    (i * params.spectrum_shimmer) % len(self.rgb_spectrum)
                )
                rgb = self.rgb_spectrum[spectrum_index]

                # Apply polarity shift
                if params.polarity_shift > 0:
                    # Positive polarity - bright colors
                    rgb = tuple(
                        min(255, int(c * (1 + params.polarity_shift))) for c in rgb
                    )
                elif params.polarity_shift < 0:
                    # Negative polarity - dark colors
                    rgb = tuple(
                        max(0, int(c * (1 + params.polarity_shift))) for c in rgb
                    )

                # Apply saturation
                if params.saturation < 1.0:
                    # Desaturate
                    gray = int(sum(rgb) / 3)
                    rgb = tuple(
                        int(c * params.saturation + gray * (1 - params.saturation))
                        for c in rgb
                    )

                # Add dust with RGB color
                result.append(
                    f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{dust_char}\033[0m"
                )

        return "".join(result)

    def apply_grid_dust(self, text: str, params: CosmicDustParams) -> str:
        """Apply grid-based cosmic dust"""
        result = []
        grid_size = params.grid_size

        for i, char in enumerate(text):
            # Add base character
            result.append(char)

            # Add grid dust
            if i % grid_size == 0 and random.random() < params.density:
                dust_char = random.choice(self.cosmic_chars["noise"])
                result.append(dust_char)

        return "".join(result)

    def create_cosmic_preset(
        self, name: str, dust_type: CosmicDustType, params: CosmicDustParams
    ) -> Dict[str, Any]:
        """Create a cosmic dust preset"""
        return {
            "name": name,
            "type": dust_type.value,
            "params": {
                "density": params.density,
                "intensity": params.intensity,
                "spread": params.spread,
                "fade_depth": params.fade_depth,
                "spectrum_shimmer": params.spectrum_shimmer,
                "polarity_shift": params.polarity_shift,
                "saturation": params.saturation,
                "grid_size": params.grid_size,
            },
        }


def create_cosmic_dust_presets() -> List[Dict[str, Any]]:
    """Create cosmic dust presets"""
    engine = CosmicDustEngine()

    presets = [
        # Nebula Dust
        engine.create_cosmic_preset(
            "Nebula Dust",
            CosmicDustType.NEBULA,
            CosmicDustParams(
                density=0.4,
                intensity=0.6,
                spread=0.7,
                fade_depth=0.8,
                spectrum_shimmer=0.5,
                polarity_shift=0.2,
                saturation=0.9,
                grid_size=4,
            ),
        ),
        # Meteor Trail
        engine.create_cosmic_preset(
            "Meteor Trail",
            CosmicDustType.METEOR_TRAIL,
            CosmicDustParams(
                density=0.3,
                intensity=0.8,
                spread=0.4,
                fade_depth=0.9,
                spectrum_shimmer=0.7,
                polarity_shift=0.0,
                saturation=0.8,
                grid_size=2,
            ),
        ),
        # Stardust Pulse
        engine.create_cosmic_preset(
            "Stardust Pulse",
            CosmicDustType.STARDUST_PULSE,
            CosmicDustParams(
                density=0.5,
                intensity=0.7,
                spread=0.6,
                fade_depth=0.6,
                spectrum_shimmer=0.8,
                polarity_shift=0.3,
                saturation=0.9,
                grid_size=3,
            ),
        ),
        # Supernova Burst
        engine.create_cosmic_preset(
            "Supernova Burst",
            CosmicDustType.SUPERNOVA_BURST,
            CosmicDustParams(
                density=0.2,
                intensity=0.9,
                spread=0.8,
                fade_depth=0.7,
                spectrum_shimmer=0.9,
                polarity_shift=0.5,
                saturation=1.0,
                grid_size=1,
            ),
        ),
        # Black Hole Fade
        engine.create_cosmic_preset(
            "Black Hole Fade",
            CosmicDustType.BLACK_HOLE_FADE,
            CosmicDustParams(
                density=0.6,
                intensity=0.5,
                spread=0.3,
                fade_depth=0.9,
                spectrum_shimmer=0.3,
                polarity_shift=-0.3,
                saturation=0.7,
                grid_size=5,
            ),
        ),
    ]

    return presets


def demo_cosmic_dust():
    """Demo cosmic dust effects"""
    engine = CosmicDustEngine()

    test_texts = ["TuneZilla", "Rawtunez", "Code Live", "Cosmic Dust", "Infinite Space"]

    dust_types = [
        CosmicDustType.NEBULA,
        CosmicDustType.METEOR_TRAIL,
        CosmicDustType.STARDUST_PULSE,
        CosmicDustType.SUPERNOVA_BURST,
        CosmicDustType.BLACK_HOLE_FADE,
    ]

    print("🌌 COSMIC DUST FX - INFINITE SPACE VIBE")
    print("=" * 50)

    for text in test_texts:
        print(f"\n📝 Original: {text}")

        for dust_type in dust_types:
            params = CosmicDustParams()
            result = engine.apply_cosmic_dust(text, dust_type, params)
            print(f"🌌 {dust_type.value}: {result}")

        # Spectrum dust
        params = CosmicDustParams(spectrum_shimmer=0.8, polarity_shift=0.3)
        spectrum_result = engine.apply_spectrum_dust(text, params)
        print(f"🌈 Spectrum: {spectrum_result}")

        # Grid dust
        params = CosmicDustParams(grid_size=3, density=0.4)
        grid_result = engine.apply_grid_dust(text, params)
        print(f"🔲 Grid: {grid_result}")


if __name__ == "__main__":
    demo_cosmic_dust()
