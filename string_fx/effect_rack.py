"""
Soundtoys-style Effect Rack for Text FX
========================================

A modular FX chain system where effects can be stacked, reordered, and mixed
just like professional audio plugins in Soundtoys Effect Rack.

Features:
- Drag & drop effect ordering
- Wet/Dry mix controls
- Bypass switches
- Effect stacking
- Real-time preview
- Preset management
"""

import json
import random
import math
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class EffectSlot(Enum):
    """Effect slot positions in the rack"""

    SLOT_1 = "slot_1"
    SLOT_2 = "slot_2"
    SLOT_3 = "slot_3"
    SLOT_4 = "slot_4"
    SLOT_5 = "slot_5"
    SLOT_6 = "slot_6"
    SLOT_7 = "slot_7"
    SLOT_8 = "slot_8"


@dataclass
class EffectSlotConfig:
    """Configuration for a single effect slot"""

    effect_name: str
    enabled: bool = True
    wet_dry_mix: float = 1.0  # 0.0 = dry, 1.0 = wet
    parameters: Dict[str, Any] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


@dataclass
class EffectRackConfig:
    """Complete effect rack configuration"""

    slots: Dict[EffectSlot, EffectSlotConfig]
    global_mix: float = 1.0
    global_bypass: bool = False
    name: str = "Untitled Rack"

    def __post_init__(self):
        if self.slots is None:
            self.slots = {}


class EffectRack:
    """
    Soundtoys-style Effect Rack for Text FX

    Allows stacking, reordering, and mixing effects just like professional
    audio plugins in Soundtoys Effect Rack.
    """

    def __init__(self, config: Optional[EffectRackConfig] = None):
        self.config = config or EffectRackConfig(slots={})
        self.effect_registry = {}
        self._register_builtin_effects()

    def _register_builtin_effects(self):
        """Register all available effects"""
        from .runtime import FX_REGISTRY

        for effect_name, effect_func in FX_REGISTRY.items():
            self.effect_registry[effect_name] = effect_func

    def add_effect(
        self,
        slot: EffectSlot,
        effect_name: str,
        enabled: bool = True,
        wet_dry_mix: float = 1.0,
        parameters: Dict[str, Any] = None,
    ) -> None:
        """Add an effect to a specific slot"""
        if effect_name not in self.effect_registry:
            raise ValueError(f"Effect '{effect_name}' not found in registry")

        if parameters is None:
            parameters = {}

        self.config.slots[slot] = EffectSlotConfig(
            effect_name=effect_name,
            enabled=enabled,
            wet_dry_mix=wet_dry_mix,
            parameters=parameters,
        )

    def remove_effect(self, slot: EffectSlot) -> None:
        """Remove an effect from a slot"""
        if slot in self.config.slots:
            del self.config.slots[slot]

    def reorder_effects(self, new_order: List[EffectSlot]) -> None:
        """Reorder effects in the rack"""
        if len(new_order) != len(self.config.slots):
            raise ValueError("New order must contain all slots")

        # Create new slots dict with reordered effects
        new_slots = {}
        for i, slot in enumerate(new_order):
            if slot in self.config.slots:
                new_slots[slot] = self.config.slots[slot]

        self.config.slots = new_slots

    def bypass_effect(self, slot: EffectSlot, bypass: bool) -> None:
        """Bypass or enable an effect"""
        if slot in self.config.slots:
            self.config.slots[slot].enabled = not bypass

    def set_wet_dry_mix(self, slot: EffectSlot, mix: float) -> None:
        """Set wet/dry mix for an effect (0.0 = dry, 1.0 = wet)"""
        if slot in self.config.slots:
            self.config.slots[slot].wet_dry_mix = max(0.0, min(1.0, mix))

    def set_effect_parameters(
        self, slot: EffectSlot, parameters: Dict[str, Any]
    ) -> None:
        """Set parameters for an effect"""
        if slot in self.config.slots:
            self.config.slots[slot].parameters.update(parameters)

    def process_text(
        self, text: str, mode: str = "raw", seed: Optional[int] = None
    ) -> str:
        """Process text through the entire effect rack"""
        if self.config.global_bypass:
            return text

        if seed is not None:
            random.seed(seed)

        result = text

        # Process through each enabled slot in order
        for slot in EffectSlot:
            if slot not in self.config.slots:
                continue

            slot_config = self.config.slots[slot]
            if not slot_config.enabled:
                continue

            # Get the effect function
            effect_func = self.effect_registry.get(slot_config.effect_name)
            if not effect_func:
                continue

            # Prepare parameters
            params = slot_config.parameters.copy()
            params["mode"] = mode
            params["intensity"] = slot_config.wet_dry_mix

            # Apply the effect
            try:
                processed = effect_func(result, params)

                # Mix with original (wet/dry)
                if slot_config.wet_dry_mix < 1.0:
                    # Mix processed with original
                    result = self._mix_text(result, processed, slot_config.wet_dry_mix)
                else:
                    result = processed

            except Exception as e:
                print(f"Error applying effect {slot_config.effect_name}: {e}")
                continue

        # Apply global mix
        if self.config.global_mix < 1.0:
            result = self._mix_text(text, result, self.config.global_mix)

        return result

    def _mix_text(self, dry: str, wet: str, mix: float) -> str:
        """Mix dry and wet text based on mix ratio"""
        if mix <= 0.0:
            return dry
        elif mix >= 1.0:
            return wet

        # For text mixing, we'll use a simple approach
        # In a real implementation, this could be more sophisticated
        if len(dry) == len(wet):
            # Character-by-character mixing
            result = ""
            for i in range(len(dry)):
                if random.random() < mix:
                    result += wet[i] if i < len(wet) else dry[i]
                else:
                    result += dry[i] if i < len(dry) else wet[i]
            return result
        else:
            # Different lengths - use mix ratio to choose
            return wet if random.random() < mix else dry

    def get_rack_status(self) -> Dict[str, Any]:
        """Get current rack status for display"""
        status = {
            "name": self.config.name,
            "global_bypass": self.config.global_bypass,
            "global_mix": self.config.global_mix,
            "slots": {},
        }

        for slot in EffectSlot:
            if slot in self.config.slots:
                slot_config = self.config.slots[slot]
                status["slots"][slot.value] = {
                    "effect_name": slot_config.effect_name,
                    "enabled": slot_config.enabled,
                    "wet_dry_mix": slot_config.wet_dry_mix,
                    "parameters": slot_config.parameters,
                }
            else:
                status["slots"][slot.value] = None

        return status

    def save_preset(self, filename: str) -> None:
        """Save rack configuration to file"""
        preset_data = {
            "name": self.config.name,
            "global_mix": self.config.global_mix,
            "global_bypass": self.config.global_bypass,
            "slots": {},
        }

        for slot, config in self.config.slots.items():
            preset_data["slots"][slot.value] = asdict(config)

        with open(filename, "w") as f:
            json.dump(preset_data, f, indent=2)

    def load_preset(self, filename: str) -> None:
        """Load rack configuration from file"""
        with open(filename, "r") as f:
            preset_data = json.load(f)

        self.config.name = preset_data.get("name", "Untitled Rack")
        self.config.global_mix = preset_data.get("global_mix", 1.0)
        self.config.global_bypass = preset_data.get("global_bypass", False)

        self.config.slots = {}
        for slot_name, slot_data in preset_data.get("slots", {}).items():
            if slot_data:
                slot = EffectSlot(slot_name)
                self.config.slots[slot] = EffectSlotConfig(
                    effect_name=slot_data["effect_name"],
                    enabled=slot_data["enabled"],
                    wet_dry_mix=slot_data["wet_dry_mix"],
                    parameters=slot_data["parameters"],
                )

    def create_soundtoys_presets(self) -> Dict[str, EffectRackConfig]:
        """Create Soundtoys-inspired preset configurations"""
        presets = {}

        # Decapitator (Distortion)
        decapitator = EffectRackConfig(
            name="Decapitator",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig(
                    "distortion", True, 0.8, {"drive": 0.7}
                ),
                EffectSlot.SLOT_2: EffectSlotConfig(
                    "neon_fx", True, 0.6, {"glow": 1.5}
                ),
                EffectSlot.SLOT_3: EffectSlotConfig(
                    "glitch_colors", True, 0.4, {"glitch_factor": 0.6}
                ),
            },
        )
        presets["decapitator"] = decapitator

        # Little Plate (Reverb)
        little_plate = EffectRackConfig(
            name="Little Plate",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig(
                    "reverb", True, 0.9, {"decay": 0.8}
                ),
                EffectSlot.SLOT_2: EffectSlotConfig(
                    "harmonics", True, 0.5, {"harmonic_count": 2}
                ),
                EffectSlot.SLOT_3: EffectSlotConfig(
                    "light", True, 0.3, {"type": "glow"}
                ),
            },
        )
        presets["little_plate"] = little_plate

        # EchoBoy (Delay)
        echo_boy = EffectRackConfig(
            name="EchoBoy",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig("echo", True, 0.8, {"delay": 0.5}),
                EffectSlot.SLOT_2: EffectSlotConfig(
                    "feedback", True, 0.6, {"feedback_length": 3}
                ),
                EffectSlot.SLOT_3: EffectSlotConfig(
                    "chromatic", True, 0.4, {"type": "rgb_offset"}
                ),
            },
        )
        presets["echo_boy"] = echo_boy

        # Crystallizer (Granular)
        crystallizer = EffectRackConfig(
            name="Crystallizer",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig(
                    "scramble", True, 0.9, {"scramble_factor": 0.7}
                ),
                EffectSlot.SLOT_2: EffectSlotConfig(
                    "cluster", True, 0.6, {"cluster_size": 0.5}
                ),
                EffectSlot.SLOT_3: EffectSlotConfig("rainbow_gradient", True, 0.8, {}),
            },
        )
        presets["crystallizer"] = crystallizer

        # Devil-Loc (Compressor)
        devil_loc = EffectRackConfig(
            name="Devil-Loc",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig(
                    "stutter", True, 0.7, {"stutter_rate": 0.6}
                ),
                EffectSlot.SLOT_2: EffectSlotConfig("invert_fx", True, 0.5, {}),
                EffectSlot.SLOT_3: EffectSlotConfig(
                    "light", True, 0.8, {"type": "strobe"}
                ),
            },
        )
        presets["devil_loc"] = devil_loc

        # MicroShift (Chorus)
        micro_shift = EffectRackConfig(
            name="MicroShift",
            slots={
                EffectSlot.SLOT_1: EffectSlotConfig(
                    "chorus", True, 0.8, {"chorus_depth": 0.6}
                ),
                EffectSlot.SLOT_2: EffectSlotConfig(
                    "vibrato", True, 0.5, {"vibrato_rate": 0.4}
                ),
                EffectSlot.SLOT_3: EffectSlotConfig(
                    "harmonics", True, 0.3, {"harmonic_count": 1}
                ),
            },
        )
        presets["micro_shift"] = micro_shift

        return presets


def create_effect_rack_cli():
    """Create command-line interface for effect rack"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Soundtoys-style Effect Rack for Text FX"
    )
    parser.add_argument("--text", "-t", required=True, help="Input text to process")
    parser.add_argument("--preset", "-p", help="Load a preset configuration")
    parser.add_argument(
        "--mode",
        "-m",
        default="raw",
        choices=["raw", "ansi", "html"],
        help="Output mode",
    )
    parser.add_argument(
        "--seed", "-s", type=int, help="Random seed for deterministic results"
    )
    parser.add_argument("--save", help="Save current configuration to file")
    parser.add_argument("--load", help="Load configuration from file")
    parser.add_argument(
        "--list-presets", action="store_true", help="List available presets"
    )
    parser.add_argument(
        "--rack-status", action="store_true", help="Show current rack status"
    )

    return parser


if __name__ == "__main__":
    # Example usage
    rack = EffectRack()

    # Create a Soundtoys-inspired preset
    presets = rack.create_soundtoys_presets()

    # Load Decapitator preset
    rack.config = presets["decapitator"]

    # Process some text
    result = rack.process_text("Code Live", mode="raw", seed=42)
    print(f"Decapitator: {result}")

    # Show rack status
    status = rack.get_rack_status()
    print(f"Rack Status: {json.dumps(status, indent=2)}")
