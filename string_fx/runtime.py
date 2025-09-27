#!/usr/bin/env python3
"""
🎭 String FX Runtime - Declarative Effect Chain Engine
====================================================

FX graph runtime for chainable string effects:
- Declarative effect chains (JSON)
- Deterministic seeded chaos
- Intensity knob (one slider to rule them all)
- Safe output modes (raw/ansi/html)
- Performance guardrails
- MIDI/hotkey integration
"""

import random
import math
import time
from typing import Callable, Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class OutputMode(Enum):
    """Output modes for string effects"""
    RAW = "raw"      # No color/escapes
    ANSI = "ansi"    # Console color
    HTML = "html"    # HTML span tags


@dataclass
class FXConfig:
    """Configuration for string effects"""
    intensity: float = 0.75
    seed: Optional[int] = None
    mode: OutputMode = OutputMode.ANSI
    max_length: int = 8000
    budget_ms: int = 100


# Global FX Registry
FX_REGISTRY: Dict[str, Callable[[str, Dict[str, Any]], str]] = {}


def fx(name: str):
    """Decorator to register string effects"""
    def _wrap(fn):
        FX_REGISTRY[name] = fn
        return fn
    return _wrap


def apply_chain(text: str, chain: List[Dict[str, Any]], config: FXConfig = None) -> str:
    """Apply a chain of string effects"""
    if config is None:
        config = FXConfig()
    
    # Set seed for deterministic effects
    if config.seed is not None:
        random.seed(config.seed)
    
    # Start timing
    start_time = time.time()
    result = text
    
    for step in chain:
        # Check budget
        if time.time() - start_time > config.budget_ms / 1000:
            result += "...[truncated - budget exceeded]"
            break
        
        name = step["name"]
        params = step.get("params", {})
        
        # Apply intensity scaling
        if "intensity" in params:
            params["intensity"] = params["intensity"] * config.intensity
        else:
            params["intensity"] = config.intensity
        
        # Apply effect
        if name in FX_REGISTRY:
            result = FX_REGISTRY[name](result, params)
        else:
            result += f"[FX_ERROR: {name} not found]"
        
        # Check length limit
        if len(result) > config.max_length:
            result = result[:config.max_length] + "...[truncated]"
            break
    
    return result


# ============================================================================
# STRING EFFECTS REGISTRY
# ============================================================================

@fx("rainbow_gradient")
def rainbow_gradient(text: str, params: Dict[str, Any]) -> str:
    """Rainbow gradient effect"""
    intensity = params.get("intensity", 0.75)
    color_shift = params.get("color_shift", 0.0)
    
    colors = [
        "#ff0000", "#ff8000", "#ffff00", "#80ff00", 
        "#00ff00", "#00ff80", "#00ffff", "#0080ff",
        "#0000ff", "#8000ff", "#ff00ff", "#ff0080"
    ]
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        color_index = int((i + color_shift * 10) % len(colors))
        color = colors[color_index]
        
        if params.get("mode") == "html":
            result += f'<span style="color: {color}">{char}</span>'
        elif params.get("mode") == "ansi":
            ansi_color = _hex_to_ansi(color)
            result += f'\033[{ansi_color}m{char}\033[0m'
        else:
            result += char
    
    return result


@fx("neon_fx")
def neon_fx(text: str, params: Dict[str, Any]) -> str:
    """Neon effect with glow"""
    intensity = params.get("intensity", 0.75)
    glow = params.get("glow", 1.0) * intensity
    
    neon_colors = [
        "#ff00ff", "#00ffff", "#ffff00", "#ff0080",
        "#8000ff", "#00ff80", "#ff8000", "#0080ff"
    ]
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        color = neon_colors[i % len(neon_colors)]
        
        if params.get("mode") == "html":
            glow_px = int(glow * 10)
            result += f'<span style="color: {color}; text-shadow: 0 0 {glow_px}px {color}">{char}</span>'
        elif params.get("mode") == "ansi":
            ansi_color = _hex_to_ansi(color)
            result += f'\033[{ansi_color}m{char}\033[0m'
        else:
            result += char
    
    return result


@fx("glitch_colors")
def glitch_colors(text: str, params: Dict[str, Any]) -> str:
    """Glitch color effects"""
    intensity = params.get("intensity", 0.75)
    glitch_factor = params.get("glitch_factor", 0.5) * intensity
    
    glitch_colors = [
        "#ff0000", "#00ff00", "#0000ff", "#ffff00",
        "#ff00ff", "#00ffff", "#ffffff", "#000000"
    ]
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        if random.random() < glitch_factor:
            color = random.choice(glitch_colors)
            
            if params.get("mode") == "html":
                result += f'<span style="color: {color}">{char}</span>'
            elif params.get("mode") == "ansi":
                ansi_color = _hex_to_ansi(color)
                result += f'\033[{ansi_color}m{char}\033[0m'
            else:
                result += char
        else:
            result += char
    
    return result


@fx("stutter")
def stutter(text: str, params: Dict[str, Any]) -> str:
    """Stutter effect"""
    intensity = params.get("intensity", 0.75)
    rate = params.get("rate", 0.2) * intensity
    
    result = ""
    for char in text:
        result += char
        if random.random() < rate:
            stutter_count = int(intensity * 3)
            for _ in range(stutter_count):
                result += char
    
    return result


@fx("scramble")
def scramble(text: str, params: Dict[str, Any]) -> str:
    """Scramble string with controlled randomness"""
    intensity = params.get("intensity", 0.75)
    scramble_factor = params.get("scramble_factor", 0.7) * intensity
    
    scrambled = list(text)
    scramble_count = int(len(text) * scramble_factor)
    
    for _ in range(scramble_count):
        if len(scrambled) > 1:
            i, j = random.sample(range(len(scrambled)), 2)
            scrambled[i], scrambled[j] = scrambled[j], scrambled[i]
    
    return ''.join(scrambled)


@fx("echo")
def echo(text: str, params: Dict[str, Any]) -> str:
    """Echo effect"""
    intensity = params.get("intensity", 0.75)
    taps = params.get("taps", 2)
    decay = params.get("decay", 0.6)
    
    result = text
    for i in range(int(taps * intensity)):
        echo_text = text
        for j in range(i + 1):
            echo_text = " " + echo_text
        
        fade = decay ** (i + 1)
        if fade > 0.1:
            result += echo_text
    
    return result


@fx("reverb")
def reverb(text: str, params: Dict[str, Any]) -> str:
    """Reverb effect"""
    intensity = params.get("intensity", 0.75)
    taps = params.get("taps", 3)
    decay = params.get("decay", 0.6)
    
    result = text
    for i in range(int(taps * intensity)):
        reverb_text = text
        for j in range(i + 1):
            reverb_text = " " + reverb_text
        
        fade = decay ** (i + 1)
        if fade > 0.1:
            result += reverb_text
    
    return result


@fx("ascii_melt")
def ascii_melt(text: str, params: Dict[str, Any]) -> str:
    """ASCII melt effect"""
    intensity = params.get("intensity", 0.75)
    melt_speed = params.get("melt_speed", 1.0) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        melt_offset = int(math.sin(i * melt_speed) * intensity * 3)
        result += " " * max(0, melt_offset) + char
    
    return result


@fx("waveform")
def waveform(text: str, params: Dict[str, Any]) -> str:
    """Waveform effect"""
    intensity = params.get("intensity", 0.75)
    speed = params.get("speed", 1.0) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        wave_height = int(math.sin(i * speed * 0.3) * intensity * 5)
        spacing = " " * max(0, wave_height)
        result += spacing + char
    
    return result


@fx("cluster")
def cluster(text: str, params: Dict[str, Any]) -> str:
    """Cluster effect"""
    intensity = params.get("intensity", 0.75)
    cluster_size = params.get("cluster_size", 3)
    
    result = ""
    for i in range(0, len(text), cluster_size):
        cluster = text[i:i + cluster_size]
        if i > 0:
            result += " " * int(intensity * 3)
        result += cluster
    
    return result


@fx("random_insert")
def random_insert(text: str, params: Dict[str, Any]) -> str:
    """Random character insertion"""
    intensity = params.get("intensity", 0.75)
    insert_chars = params.get("insert_chars", "!@#$%^&*()_+-=[]{}|;:,.<>?")
    rate = params.get("rate", 0.1) * intensity
    
    result = ""
    for char in text:
        result += char
        if random.random() < rate:
            random_char = random.choice(insert_chars)
            result += random_char
    
    return result


@fx("invert_fx")
def invert_fx(text: str, params: Dict[str, Any]) -> str:
    """Invert string effect"""
    intensity = params.get("intensity", 0.75)
    
    if intensity > 0.5:
        return text[::-1]
    else:
        return text


@fx("stretch")
def stretch(text: str, params: Dict[str, Any]) -> str:
    """Stretch string with variable spacing"""
    intensity = params.get("intensity", 0.75)
    
    result = ""
    for i, char in enumerate(text):
        spacing = int(intensity * (1 + math.sin(i * 0.5) * 0.5))
        result += char + " " * spacing
    
    return result


@fx("tremolo")
def tremolo(text: str, params: Dict[str, Any]) -> str:
    """Tremolo effect - rapid visual oscillation"""
    intensity = params.get("intensity", 0.75)
    rate = params.get("rate", 5.0)  # tremolo rate (Hz-like)
    tremolo_type = params.get("type", "amplitude")  # amplitude, repetition, wave, color
    
    if tremolo_type == "amplitude":
        return _tremolo_amplitude(text, intensity, rate, params)
    elif tremolo_type == "repetition":
        return _tremolo_repetition(text, intensity, rate, params)
    elif tremolo_type == "wave":
        return _tremolo_wave(text, intensity, rate, params)
    elif tremolo_type == "color":
        return _tremolo_color(text, intensity, rate, params)
    else:
        return text


@fx("vibrato")
def vibrato(text: str, params: Dict[str, Any]) -> str:
    """Vibrato effect - pitch wobble with accent marks"""
    intensity = params.get("intensity", 0.75)
    rate = params.get("rate", 7.0)  # vibrato rate
    depth = params.get("depth", 0.5)  # vibrato depth
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate vibrato phase
        phase = (i * rate * 0.1) % (2 * math.pi)
        vibrato_strength = intensity * depth
        
        # Apply vibrato modulation
        if math.sin(phase) > vibrato_strength:
            # "Sharp" - add accent marks
            if params.get("mode") == "html":
                result += f'<span style="text-decoration: overline">{char}</span>'
            else:
                result += f'{char}͟'  # combining overline
        else:
            # "Flat" - add tildes
            if params.get("mode") == "html":
                result += f'<span style="text-decoration: underline">{char}</span>'
            else:
                result += f'{char}̴'  # combining tilde overlay
    
    return result


@fx("glissando")
def glissando(text: str, params: Dict[str, Any]) -> str:
    """Glissando effect - characters sliding into each other"""
    intensity = params.get("intensity", 0.75)
    slide_speed = params.get("slide_speed", 1.0) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate slide spacing
        slide_offset = int(math.sin(i * slide_speed * 0.3) * intensity * 3)
        spacing = "-" * max(1, slide_offset)
        result += char + spacing
    
    return result


@fx("arpeggio")
def arpeggio(text: str, params: Dict[str, Any]) -> str:
    """Arpeggio effect - spread letters like staggered notes"""
    intensity = params.get("intensity", 0.75)
    spread = params.get("spread", 2) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate arpeggio spacing
        arpeggio_offset = int(i * spread)
        spacing = " " * arpeggio_offset
        result += spacing + char + "\n"
    
    return result.strip()


@fx("harmonics")
def harmonics(text: str, params: Dict[str, Any]) -> str:
    """Harmonics effect - ghostly echo letters"""
    intensity = params.get("intensity", 0.75)
    harmonic_count = params.get("harmonic_count", 2) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Add harmonic echoes
        result += char
        for h in range(int(harmonic_count)):
            if params.get("mode") == "html":
                result += f'<span style="opacity: 0.3; font-size: 0.7em">{char}</span>'
            else:
                result += f'{char}ᴰ'  # combining superscript
    
    return result


@fx("palm_mute")
def palm_mute(text: str, params: Dict[str, Any]) -> str:
    """Palm mute effect - muted placeholders"""
    intensity = params.get("intensity", 0.75)
    mute_chars = params.get("mute_chars", "·x—")
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Apply palm mute
        if random.random() < intensity * 0.6:
            mute_char = random.choice(mute_chars)
            result += mute_char
        else:
            result += char
    
    return result


@fx("double_stops")
def double_stops(text: str, params: Dict[str, Any]) -> str:
    """Double stops effect - duplicate letters in parallel"""
    intensity = params.get("intensity", 0.75)
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Add parallel harmony
        if random.random() < intensity * 0.7:
            if params.get("mode") == "html":
                result += f'<span style="position: relative; top: -2px">{char}</span>'
            else:
                result += f'{char} {char}'
        else:
            result += char
    
    return result


@fx("string_bends")
def string_bends(text: str, params: Dict[str, Any]) -> str:
    """String bends effect - warp characters up/down"""
    intensity = params.get("intensity", 0.75)
    bend_strength = params.get("bend_strength", 0.5) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate bend offset
        bend_offset = int(math.sin(i * 0.5) * bend_strength * 3)
        
        if params.get("mode") == "html":
            result += f'<span style="position: relative; top: {bend_offset}px">{char}</span>'
        else:
            result += f'{char}͡'  # combining double breve
    
    return result


@fx("trill")
def trill(text: str, params: Dict[str, Any]) -> str:
    """Trill effect - rapid alternation between characters"""
    intensity = params.get("intensity", 0.75)
    trill_chars = params.get("trill_chars", "AB")
    trill_rate = params.get("trill_rate", 0.3) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Apply trill
        if random.random() < trill_rate:
            trill_char = random.choice(trill_chars)
            result += f'{char}{trill_char}'
        else:
            result += char
    
    return result


@fx("pizzicato")
def pizzicato(text: str, params: Dict[str, Any]) -> str:
    """Pizzicato effect - sharp staccato accents"""
    intensity = params.get("intensity", 0.75)
    accent_chars = params.get("accent_chars", "!?.")
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Add pizzicato accents
        if random.random() < intensity * 0.5:
            accent = random.choice(accent_chars)
            result += f'{char}{accent}'
        else:
            result += char
    
    return result


@fx("feedback")
def feedback(text: str, params: Dict[str, Any]) -> str:
    """Feedback effect - letters ring out and trail"""
    intensity = params.get("intensity", 0.75)
    feedback_length = params.get("feedback_length", 5) * intensity
    
    result = ""
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Add feedback trail
        result += char
        for f in range(int(feedback_length)):
            if params.get("mode") == "html":
                result += f'<span style="opacity: {0.8 - f * 0.1}">{char}</span>'
            else:
                result += f'{char}~'
    
    return result


def _tremolo_amplitude(text: str, intensity: float, rate: float, params: Dict[str, Any]) -> str:
    """Amplitude tremolo - volume-like pulses"""
    result = ""
    
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate tremolo phase
        phase = (i * rate * 0.1) % (2 * math.pi)
        tremolo_depth = intensity * 0.5
        
        # Apply tremolo modulation
        if math.sin(phase) > tremolo_depth:
            # "Loud" - normal character
            result += char
        else:
            # "Quiet" - ghosted character
            if params.get("mode") == "html":
                result += f'<span style="opacity: 0.3">{char}</span>'
            elif params.get("mode") == "ansi":
                result += f'\033[2m{char}\033[0m'  # dim
            else:
                result += char
    
    return result


def _tremolo_repetition(text: str, intensity: float, rate: float, params: Dict[str, Any]) -> str:
    """Repetition tremolo - character stutter like tremolo picking"""
    result = ""
    
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate tremolo phase
        phase = (i * rate * 0.1) % (2 * math.pi)
        tremolo_strength = intensity * 0.8
        
        # Apply repetition based on tremolo
        if math.sin(phase) > tremolo_strength:
            # Single character
            result += char
        else:
            # Repeated characters (tremolo picking effect)
            repeat_count = int(intensity * 3) + 1
            result += char * repeat_count
    
    return result


def _tremolo_wave(text: str, intensity: float, rate: float, params: Dict[str, Any]) -> str:
    """Wave tremolo - sinusoidal horizontal shift"""
    result = ""
    
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate wave offset
        phase = (i * rate * 0.1) % (2 * math.pi)
        wave_offset = int(math.sin(phase) * intensity * 5)
        
        # Apply wave spacing
        spacing = " " * max(0, wave_offset)
        result += spacing + char
    
    return result


def _tremolo_color(text: str, intensity: float, rate: float, params: Dict[str, Any]) -> str:
    """Color tremolo - rapid color cycling"""
    result = ""
    
    # Tremolo colors
    tremolo_colors = [
        "#ff0000", "#ff8000", "#ffff00", "#80ff00",
        "#00ff00", "#00ff80", "#00ffff", "#0080ff",
        "#0000ff", "#8000ff", "#ff00ff", "#ff0080"
    ]
    
    for i, char in enumerate(text):
        if char.isspace():
            result += char
            continue
        
        # Calculate tremolo phase
        phase = (i * rate * 0.1) % (2 * math.pi)
        tremolo_strength = intensity * 0.7
        
        # Apply color based on tremolo
        if math.sin(phase) > tremolo_strength:
            # Normal color
            if params.get("mode") == "html":
                result += f'<span style="color: #ffffff">{char}</span>'
            elif params.get("mode") == "ansi":
                result += f'\033[37m{char}\033[0m'  # white
            else:
                result += char
        else:
            # Tremolo color
            color_index = int((i + phase * 10) % len(tremolo_colors))
            color = tremolo_colors[color_index]
            
            if params.get("mode") == "html":
                result += f'<span style="color: {color}">{char}</span>'
            elif params.get("mode") == "ansi":
                ansi_color = _hex_to_ansi(color)
                result += f'\033[{ansi_color}m{char}\033[0m'
            else:
                result += char
    
    return result


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _hex_to_ansi(hex_color: str) -> str:
    """Convert hex color to ANSI color code"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Map to ANSI 256 color
    if r == g == b:
        # Grayscale
        return f"38;5;{232 + int(r / 32)}"
    else:
        # Color
        return f"38;2;{r};{g};{b}"


def create_preset(name: str, chain: List[Dict[str, Any]], description: str = "") -> Dict[str, Any]:
    """Create a string FX preset"""
    return {
        "name": name,
        "description": description,
        "chain": chain
    }


def load_preset(preset_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load a preset and return its chain"""
    return preset_data.get("chain", [])


def export_preset(preset_data: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
    """Export preset with metadata"""
    export_data = preset_data.copy()
    if seed is not None:
        export_data["seed"] = seed
    export_data["exported_at"] = time.time()
    return export_data


# ============================================================================
# PRESET PACKS
# ============================================================================

def get_preset_pack() -> Dict[str, Dict[str, Any]]:
    """Get the default preset pack"""
    return {
        "neon_rave": create_preset(
            "Neon Rave",
            [
                {"name": "rainbow_gradient"},
                {"name": "neon_fx", "params": {"glow": 1.3}},
                {"name": "stutter", "params": {"rate": 0.2}}
            ],
            "Bright neon effects with glow and stutter"
        ),
        "tunezilla": create_preset(
            "TuneZilla Mode",
            [
                {"name": "glitch_colors", "params": {"glitch_factor": 0.8}},
                {"name": "scramble", "params": {"scramble_factor": 0.6}},
                {"name": "ascii_melt", "params": {"melt_speed": 0.5}}
            ],
            "TuneZilla brand effects with glitch and melt"
        ),
        "opera_cards": create_preset(
            "Opera Cards",
            [
                {"name": "echo", "params": {"taps": 2, "decay": 0.7}},
                {"name": "reverb", "params": {"taps": 3, "decay": 0.5}}
            ],
            "Operatic harmony effects with echo and reverb"
        ),
        "retro_synth": create_preset(
            "Retro Synth",
            [
                {"name": "invert_fx"},
                {"name": "cluster", "params": {"cluster_size": 2}},
                {"name": "waveform", "params": {"depth": 0.3}}
            ],
            "Retro synthesizer effects"
        ),
        "lolcat_max": create_preset(
            "Lolcat Max",
            [
                {"name": "rainbow_gradient"},
                {"name": "random_insert", "params": {"insert_chars": " 😹 ", "rate": 0.1}}
            ],
            "Lolcat-style effects with emoji insertion"
        ),
        "chaos_mode": create_preset(
            "Chaos Mode",
            [
                {"name": "scramble", "params": {"scramble_factor": 0.9}},
                {"name": "glitch_colors", "params": {"glitch_factor": 1.0}},
                {"name": "stutter", "params": {"rate": 0.6}},
                {"name": "random_insert", "params": {"rate": 0.3}}
            ],
            "Maximum chaos effects"
        ),
        "tremolo_rave": create_preset(
            "Tremolo Rave",
            [
                {"name": "tremolo", "params": {"type": "repetition", "rate": 8.0}},
                {"name": "stutter", "params": {"rate": 0.3}},
                {"name": "neon_fx", "params": {"glow": 1.5}}
            ],
            "Tremolo picking with neon glow"
        ),
        "tremolo_wave": create_preset(
            "Tremolo Wave",
            [
                {"name": "tremolo", "params": {"type": "wave", "rate": 6.0}},
                {"name": "tremolo", "params": {"type": "color", "rate": 4.0}}
            ],
            "Wave tremolo with color cycling"
        ),
        "tremolo_amplitude": create_preset(
            "Tremolo Amplitude",
            [
                {"name": "tremolo", "params": {"type": "amplitude", "rate": 10.0}},
                {"name": "echo", "params": {"taps": 2, "decay": 0.8}}
            ],
            "Volume-like tremolo with echo"
        ),
        "tremolo_glitch": create_preset(
            "Tremolo Glitch",
            [
                {"name": "tremolo", "params": {"type": "repetition", "rate": 12.0}},
                {"name": "glitch_colors", "params": {"glitch_factor": 0.8}},
                {"name": "scramble", "params": {"scramble_factor": 0.4}}
            ],
            "Tremolo with glitch effects"
        ),
        "string_orchestra": create_preset(
            "String Orchestra",
            [
                {"name": "vibrato", "params": {"rate": 6.0, "depth": 0.6}},
                {"name": "harmonics", "params": {"harmonic_count": 2}},
                {"name": "double_stops", "params": {"intensity": 0.5}}
            ],
            "Full string orchestra with vibrato, harmonics, and double stops"
        ),
        "violin_solo": create_preset(
            "Violin Solo",
            [
                {"name": "vibrato", "params": {"rate": 8.0, "depth": 0.8}},
                {"name": "glissando", "params": {"slide_speed": 1.2}},
                {"name": "harmonics", "params": {"harmonic_count": 1}}
            ],
            "Violin solo with vibrato, glissando, and harmonics"
        ),
        "guitar_lead": create_preset(
            "Guitar Lead",
            [
                {"name": "string_bends", "params": {"bend_strength": 0.7}},
                {"name": "vibrato", "params": {"rate": 7.0, "depth": 0.5}},
                {"name": "feedback", "params": {"feedback_length": 3}}
            ],
            "Guitar lead with string bends, vibrato, and feedback"
        ),
        "pizzicato_strings": create_preset(
            "Pizzicato Strings",
            [
                {"name": "pizzicato", "params": {"accent_chars": "!?."}},
                {"name": "palm_mute", "params": {"mute_chars": "·x—"}},
                {"name": "trill", "params": {"trill_chars": "AB", "trill_rate": 0.4}}
            ],
            "Pizzicato strings with palm mute and trill"
        ),
        "arpeggio_harp": create_preset(
            "Arpeggio Harp",
            [
                {"name": "arpeggio", "params": {"spread": 3}},
                {"name": "harmonics", "params": {"harmonic_count": 3}},
                {"name": "glissando", "params": {"slide_speed": 0.8}}
            ],
            "Harp-like arpeggio with harmonics and glissando"
        ),
        "feedback_sustain": create_preset(
            "Feedback Sustain",
            [
                {"name": "feedback", "params": {"feedback_length": 8}},
                {"name": "tremolo", "params": {"type": "amplitude", "rate": 4.0}},
                {"name": "harmonics", "params": {"harmonic_count": 2}}
            ],
            "Feedback sustain with tremolo and harmonics"
        )
    }


if __name__ == "__main__":
    # Test the runtime
    config = FXConfig(intensity=0.8, seed=42, mode=OutputMode.ANSI)
    
    chain = [
        {"name": "rainbow_gradient"},
        {"name": "neon_fx", "params": {"glow": 1.2}},
        {"name": "stutter", "params": {"rate": 0.3}}
    ]
    
    result = apply_chain("Code Live", chain, config)
    print(f"Result: {result}")
