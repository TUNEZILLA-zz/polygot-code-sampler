#!/usr/bin/env python3
"""
Lolcat FX for Strings - Visual Glitch FX Layer for Code/Text Output
Transforms boring text into sparkly stretched-out chaos like: Heeellooooo!!! 🌈💥✨
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FXPreset(Enum):
    PARTY_MODE = "party"
    GLITCH_CAT = "glitch"
    WAVE_RIDER = "wave"
    CLASSIC_LOLCAT = "classic"


@dataclass
class LolcatFXConfig:
    """Configuration for Lolcat FX processing"""

    # Core FX
    stretch: float = 0.3
    echo: float = 0.2
    pitch_shift: float = 0.4
    reverb: float = 0.25

    # Color FX
    rainbow: float = 0.6
    glitch_colors: float = 0.3
    neon: float = 0.4
    invert: float = 0.2

    # Spacing FX
    stutter: float = 0.25
    waveform: float = 0.35
    cluster: float = 0.2

    # Chaos FX
    random_insert: float = 0.3
    scramble: float = 0.15
    ascii_melt: float = 0.25


class LolcatFX:
    """Lolcat FX processor for transforming text into visual glitch chaos"""

    def __init__(self, config: Optional[LolcatFXConfig] = None):
        self.config = config or LolcatFXConfig()
        self.emojis = [
            "⚡️",
            "🔥",
            "💥",
            "✨",
            "🌈",
            "🎉",
            "👾",
            "🐍",
            "💚",
            "💙",
            "💜",
            "💖",
            "💛",
            "💫",
            "🌟",
            "🎭",
            "🎪",
            "🎨",
            "🎵",
            "🎶",
        ]
        self.glitch_chars = [
            "̵",
            "̏",
            "͝",
            "͔",
            "̸",
            "͑",
            "̤",
            "͎",
            "̴",
            "̄",
            "̙",
            "̨",
            "̷",
            "̊",
            "̽",
            "̿",
            "̀",
            "́",
            "͂",
            "̓",
        ]
        self.rainbow_colors = [
            "🔴",
            "🟠",
            "🟡",
            "🟢",
            "🔵",
            "🟣",
            "🟤",
            "⚫",
            "⚪",
            "🟫",
        ]

    def process(self, text: str, preset: Optional[FXPreset] = None) -> str:
        """Process text through the Lolcat FX pipeline"""
        if not text:
            return text

        # Apply preset if specified
        if preset:
            self._apply_preset(preset)

        result = text

        # Apply Core FX
        if self.config.stretch > 0:
            result = self._apply_stretch(result)

        if self.config.echo > 0:
            result = self._apply_echo(result)

        if self.config.pitch_shift > 0:
            result = self._apply_pitch_shift(result)

        if self.config.reverb > 0:
            result = self._apply_reverb(result)

        # Apply Spacing FX
        if self.config.stutter > 0:
            result = self._apply_stutter(result)

        if self.config.waveform > 0:
            result = self._apply_waveform(result)

        if self.config.cluster > 0:
            result = self._apply_cluster(result)

        # Apply Chaos FX
        if self.config.random_insert > 0:
            result = self._apply_random_insert(result)

        if self.config.scramble > 0:
            result = self._apply_scramble(result)

        if self.config.ascii_melt > 0:
            result = self._apply_ascii_melt(result)

        return result

    def _apply_preset(self, preset: FXPreset) -> None:
        """Apply a preset configuration"""
        if preset == FXPreset.PARTY_MODE:
            self.config.stretch = 0.7
            self.config.echo = 0.6
            self.config.rainbow = 0.8
        elif preset == FXPreset.GLITCH_CAT:
            self.config.glitch_colors = 0.9
            self.config.ascii_melt = 0.7
            self.config.random_insert = 0.8
        elif preset == FXPreset.WAVE_RIDER:
            self.config.waveform = 0.8
            self.config.reverb = 0.6
            self.config.stutter = 0.5
        elif preset == FXPreset.CLASSIC_LOLCAT:
            self.config.pitch_shift = 0.7
            self.config.rainbow = 0.6
            self.config.stretch = 0.4

    def _apply_stretch(self, text: str) -> str:
        """Apply stretch effect - repeats letters"""
        if random.random() > self.config.stretch:
            return text

        return "".join(
            [char * (random.randint(2, 5) if char != " " else 1) for char in text]
        )

    def _apply_echo(self, text: str) -> str:
        """Apply echo effect - trailing spaces + exclamations"""
        if random.random() > self.config.echo:
            return text

        echo_count = random.randint(1, 3)
        echo_text = " !" * echo_count
        return text + echo_text

    def _apply_pitch_shift(self, text: str) -> str:
        """Apply pitch shift - random casing"""
        if random.random() > self.config.pitch_shift:
            return text

        return "".join(
            [char.upper() if random.random() < 0.5 else char.lower() for char in text]
        )

    def _apply_reverb(self, text: str) -> str:
        """Apply reverb - fade-out letters with spacing"""
        if random.random() > self.config.reverb:
            return text

        reverb_count = random.randint(1, 3)
        reverb_text = " o" * reverb_count
        return text + reverb_text

    def _apply_stutter(self, text: str) -> str:
        """Apply stutter - extra spaces between letters"""
        if random.random() > self.config.stutter:
            return text

        return "   ".join(text.split(""))

    def _apply_waveform(self, text: str) -> str:
        """Apply waveform - letters arranged in sine-wave pattern"""
        if random.random() > self.config.waveform:
            return text

        # Simple waveform effect - add some spacing
        return " ".join(text.split(""))

    def _apply_cluster(self, text: str) -> str:
        """Apply cluster - random bursts of duplicated letters"""
        if random.random() > self.config.cluster:
            return text

        result = []
        for char in text:
            if char != " " and random.random() < 0.3:
                result.append(char * random.randint(2, 4))
            else:
                result.append(char)
        return "".join(result)

    def _apply_random_insert(self, text: str) -> str:
        """Apply random insert - drops emojis, ASCII art, or symbols"""
        if random.random() > self.config.random_insert:
            return text

        result = []
        for char in text:
            result.append(char)
            if char != " " and random.random() < 0.3:
                result.append(random.choice(self.emojis))
        return "".join(result)

    def _apply_scramble(self, text: str) -> str:
        """Apply scramble - shuffles letters"""
        if random.random() > self.config.scramble:
            return text

        # Only scramble if the text is short enough
        if len(text) <= 10:
            return "".join(random.sample(text, len(text)))
        return text

    def _apply_ascii_melt(self, text: str) -> str:
        """Apply ASCII melt - overlays with unicode glitch blocks"""
        if random.random() > self.config.ascii_melt:
            return text

        result = []
        for char in text:
            result.append(char)
            if random.random() < 0.2:
                result.append(random.choice(self.glitch_chars))
        return "".join(result)

    def apply_rainbow_gradient(self, text: str) -> str:
        """Apply rainbow gradient - cycles letters through colors"""
        if self.config.rainbow <= 0:
            return text

        result = []
        for i, char in enumerate(text):
            if char != " ":
                color = self.rainbow_colors[i % len(self.rainbow_colors)]
                result.append(f"{color}{char}")
            else:
                result.append(char)
        return "".join(result)

    def apply_neon_effect(self, text: str) -> str:
        """Apply neon effect - bold + glow simulation"""
        if self.config.neon <= 0:
            return text

        return f"✨{text}✨"

    def apply_glitch_colors(self, text: str) -> str:
        """Apply glitch colors - random ANSI colors per character"""
        if self.config.glitch_colors <= 0:
            return text

        result = []
        for char in text:
            if char != " ":
                color = random.choice(self.rainbow_colors)
                result.append(f"{color}{char}")
            else:
                result.append(char)
        return "".join(result)


def lolcat_fx(text: str, preset: str = "classic", **kwargs) -> str:
    """
    Main function to apply Lolcat FX to text

    Args:
        text: Input text to transform
        preset: FX preset to apply ("party", "glitch", "wave", "classic")
        **kwargs: Additional FX parameters

    Returns:
        Transformed text with Lolcat FX applied
    """
    # Create config from kwargs
    config = LolcatFXConfig(**kwargs)

    # Create FX processor
    fx = LolcatFX(config)

    # Apply preset
    preset_enum = FXPreset(preset)

    # Process text
    result = fx.process(text, preset_enum)

    # Apply additional effects
    if config.rainbow > 0:
        result = fx.apply_rainbow_gradient(result)

    if config.neon > 0:
        result = fx.apply_neon_effect(result)

    if config.glitch_colors > 0:
        result = fx.apply_glitch_colors(result)

    return result


def demo_lolcat_fx():
    """Demo function showing Lolcat FX in action"""
    test_texts = [
        "hello",
        "Code Live",
        "Lolcat FX Rack",
        "Visual Glitch FX Layer",
        "Heeellooooo!!! 🌈💥✨",
    ]

    presets = ["party", "glitch", "wave", "classic"]

    print("🎛️ Lolcat FX Rack Demo")
    print("=" * 50)

    for text in test_texts:
        print(f"\nOriginal: {text}")
        print("-" * 30)

        for preset in presets:
            result = lolcat_fx(text, preset=preset)
            print(f"{preset.capitalize()}: {result}")

    print("\n🎉 Lolcat FX Rack Demo Complete!")


if __name__ == "__main__":
    demo_lolcat_fx()
