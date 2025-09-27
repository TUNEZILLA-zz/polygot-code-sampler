#!/usr/bin/env python3
"""
🎭 Code Opera - State Management
===============================

Conductor panel state management for Code Opera performance.
Handles BPM, key, and per-voice gain/FX controls.
"""

from pydantic import BaseModel
from typing import Dict, Optional
import json
from pathlib import Path


class FX(BaseModel):
    """Audio effects for a voice"""
    reverb: float = 0.2
    chorus: float = 0.0
    distortion: float = 0.0
    delay: float = 0.0
    lfo: float = 0.0


class Voice(BaseModel):
    """Individual voice configuration"""
    gain: float = 0.8
    fx: FX = FX()
    muted: bool = False
    solo: bool = False


class Conductor(BaseModel):
    """Conductor state for Code Opera"""
    bpm: int = 96
    key: str = "C"
    mode: str = "ionian"
    seed: Optional[str] = None
    act: int = 1  # Current act (I, II, III)
    
    voices: Dict[str, Voice] = {
        "rust": Voice(gain=0.8, fx=FX(reverb=0.3, distortion=0.2)),
        "python": Voice(gain=0.9, fx=FX(chorus=0.4, delay=0.3)),
        "julia": Voice(gain=0.7, fx=FX(lfo=0.5, reverb=0.2)),
        "typescript": Voice(gain=0.8, fx=FX(chorus=0.3, delay=0.2)),
        "go": Voice(gain=0.6, fx=FX(reverb=0.4)),
        "csharp": Voice(gain=0.7, fx=FX(distortion=0.3, reverb=0.2)),
        "sql": Voice(gain=0.5, fx=FX(reverb=0.3))
    }
    
    # Performance metrics
    p95_latency: float = 0.0  # Maps to dynamics (forte)
    error_rate: float = 0.0   # Maps to staccato (shorter motifs)
    qps: float = 0.0          # Maps to tempo bump
    
    def get_dynamics(self) -> str:
        """Get dynamics based on p95 latency"""
        if self.p95_latency > 200:
            return "fortissimo"
        elif self.p95_latency > 100:
            return "forte"
        elif self.p95_latency > 50:
            return "mezzo-forte"
        else:
            return "piano"
    
    def get_tempo_modifier(self) -> float:
        """Get tempo modifier based on QPS"""
        if self.qps > 100:
            return 1.2  # 20% faster
        elif self.qps > 50:
            return 1.1  # 10% faster
        else:
            return 1.0  # Normal tempo
    
    def get_motif_length(self) -> int:
        """Get motif length based on error rate"""
        if self.error_rate > 0.1:
            return 4  # Shorter, staccato
        elif self.error_rate > 0.05:
            return 8  # Medium
        else:
            return 16  # Long, legato


# Global state
state = Conductor()


def save_state(file_path: str = "out/opera/state.json"):
    """Save conductor state to file"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(state.dict(), f, indent=2)


def load_state(file_path: str = "out/opera/state.json") -> Conductor:
    """Load conductor state from file"""
    if Path(file_path).exists():
        with open(file_path, "r") as f:
            data = json.load(f)
            return Conductor(**data)
    return Conductor()


def update_state(update_data: dict) -> Conductor:
    """Update conductor state"""
    global state
    
    # Update top-level fields
    for key, value in update_data.items():
        if key == "voices":
            # Update voice configurations
            for voice_name, voice_data in value.items():
                if voice_name in state.voices:
                    if isinstance(voice_data, dict):
                        # Update individual voice fields
                        for field, field_value in voice_data.items():
                            if field == "fx" and isinstance(field_value, dict):
                                # Update FX fields
                                for fx_field, fx_value in field_value.items():
                                    setattr(state.voices[voice_name].fx, fx_field, fx_value)
                            else:
                                setattr(state.voices[voice_name], field, field_value)
        else:
            setattr(state, key, value)
    
    # Save updated state
    save_state()
    return state


def get_state() -> Conductor:
    """Get current conductor state"""
    return state


def set_seed(seed: str) -> None:
    """Set deterministic seed"""
    global state
    state.seed = seed
    
    # Write seed to file for reproducibility
    seed_file = Path("out/opera/SEED.txt")
    seed_file.parent.mkdir(parents=True, exist_ok=True)
    with open(seed_file, "w") as f:
        f.write(seed)
    
    save_state()


def get_seed() -> Optional[str]:
    """Get current seed"""
    return state.seed


def advance_act() -> int:
    """Advance to next act"""
    global state
    state.act = min(3, state.act + 1)
    
    # Key modulation in Act II (C -> G)
    if state.act == 2:
        state.key = "G"
    # Grand cadence in Act III
    elif state.act == 3:
        state.key = "C"  # Return to home key
    
    save_state()
    return state.act


def reset_performance() -> None:
    """Reset performance to Act I"""
    global state
    state.act = 1
    state.key = "C"
    state.p95_latency = 0.0
    state.error_rate = 0.0
    state.qps = 0.0
    save_state()


def update_metrics(p95_latency: float, error_rate: float, qps: float) -> None:
    """Update performance metrics"""
    global state
    state.p95_latency = p95_latency
    state.error_rate = error_rate
    state.qps = qps
    save_state()


if __name__ == "__main__":
    # Test the state management
    print("🎭 Code Opera State Management")
    print("=" * 50)
    
    # Create initial state
    initial_state = Conductor()
    print(f"Initial BPM: {initial_state.bpm}")
    print(f"Initial Key: {initial_state.key}")
    print(f"Voice count: {len(initial_state.voices)}")
    
    # Test state update
    update_data = {
        "bpm": 120,
        "key": "G",
        "voices": {
            "rust": {"gain": 0.9, "fx": {"reverb": 0.5}}
        }
    }
    
    updated_state = update_state(update_data)
    print(f"\nUpdated BPM: {updated_state.bpm}")
    print(f"Updated Key: {updated_state.key}")
    print(f"Rust gain: {updated_state.voices['rust'].gain}")
    print(f"Rust reverb: {updated_state.voices['rust'].fx.reverb}")
    
    # Test metrics
    update_metrics(150.0, 0.05, 75.0)
    print(f"\nDynamics: {updated_state.get_dynamics()}")
    print(f"Tempo modifier: {updated_state.get_tempo_modifier()}")
    print(f"Motif length: {updated_state.get_motif_length()}")
    
    print("\n✅ State management working!")
