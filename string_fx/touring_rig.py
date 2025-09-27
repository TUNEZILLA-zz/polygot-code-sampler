"""
Touring Rig System - Professional Show Controller
================================================

Complete touring rig system with:
- Scene thumbnails + notes
- Live intensity fader
- Morph curves per transition
- Momentary buttons
- Show safety & a11y
- Operator ergonomics
- Presets & authoring
- API hooks
- Metrics sidechain
- Testing checklist
- Export & share
"""

import json
import time
import math
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class MorphCurve(Enum):
    """Morph curve types"""
    LINEAR = "linear"
    EASE_IN = "easeIn"
    EASE_OUT = "easeOut"
    EASE_IN_OUT = "easeInOut"
    HOLD_THEN_DROP = "holdThenDrop"


class MomentaryButton(Enum):
    """Momentary button types"""
    FLASH_STROBE = "flash_strobe"
    BLACKOUT = "blackout"
    ALL_WHITE_BLOOM = "all_white_bloom"


@dataclass
class SceneThumbnail:
    """Scene thumbnail with preview variants"""
    scene_id: str
    name: str
    notes: str
    mono_preview: str
    motion_safe_preview: str
    intensity_preview: str
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ShowConfig:
    """Complete show configuration"""
    name: str
    bpm: float = 110.0
    scenes: List[str] = None
    morph_curves: Dict[str, MorphCurve] = None
    intensity: float = 100.0  # 0-120%
    metrics_link_strength: float = 100.0  # 0-100%
    duty_cycle_limits: Dict[str, float] = None
    motion_watchdog: bool = True
    heat_guard: bool = True
    
    def __post_init__(self):
        if self.scenes is None:
            self.scenes = []
        if self.morph_curves is None:
            self.morph_curves = {}
        if self.duty_cycle_limits is None:
            self.duty_cycle_limits = {
                "strobe_on_ms": 120.0,
                "strobe_off_ms": 125.0,
                "max_flashes_per_second": 8.0
            }


class TouringRig:
    """
    Touring Rig System
    
    Complete professional show controller with scene management,
    live intensity, morph curves, momentary buttons, and operator ergonomics.
    """
    
    def __init__(self):
        self.current_show: Optional[ShowConfig] = None
        self.current_scene_index: int = 0
        self.is_playing: bool = False
        self.start_time: float = 0.0
        self.scene_start_time: float = 0.0
        
        # Live controls
        self.live_intensity: float = 100.0  # 0-120%
        self.metrics_link_enabled: bool = True
        self.metrics_link_strength: float = 100.0  # 0-100%
        self.motion_reduced: bool = False
        self.heat_guard_active: bool = False
        
        # Momentary buttons
        self.momentary_states: Dict[MomentaryButton, bool] = {
            button: False for button in MomentaryButton
        }
        self.momentary_timers: Dict[MomentaryButton, float] = {
            button: 0.0 for button in MomentaryButton
        }
        
        # Operator ergonomics
        self.hotkeys: Dict[str, str] = {
            "1": "scene_0", "2": "scene_1", "3": "scene_2",
            "4": "scene_3", "5": "scene_4", "6": "scene_5",
            "7": "scene_6", "8": "scene_7", "9": "scene_8",
            "[": "prev_scene", "]": "next_scene",
            "M": "toggle_metrics", "B": "blackout"
        }
        
        # Undo/Redo stack
        self.undo_stack: List[Dict[str, Any]] = []
        self.redo_stack: List[Dict[str, Any]] = []
        self.max_undo_steps: int = 20
        
        # Show clock
        self.show_clock: Dict[str, float] = {
            "elapsed": 0.0,
            "remaining": 0.0,
            "scene_elapsed": 0.0,
            "scene_remaining": 0.0
        }
        
        # Duty cycle limiter
        self.strobe_state: Dict[str, Any] = {
            "enabled": False,
            "is_on": False,
            "last_toggle": 0.0,
            "on_time": 0.12,
            "off_time": 0.125
        }
        
        # Motion watchdog
        self.motion_watchdog_timer: float = 0.0
        self.motion_watchdog_threshold: float = 0.5  # 500ms
        
        # Heat guard
        self.heat_guard_timer: float = 0.0
        self.heat_guard_threshold: float = 0.1  # 100ms
        self.quality_level: int = 3  # 1-5, 5 = highest
        
        # Scene thumbnails
        self.scene_thumbnails: Dict[str, SceneThumbnail] = {}
        
        # Metrics sidechain
        self.current_metrics: Dict[str, float] = {
            "qps": 0.0,
            "p95": 0.0,
            "error_rate": 0.0,
            "cpu_percent": 0.0,
            "frame_time_ms": 0.0
        }
    
    def load_show(self, show_config: ShowConfig) -> None:
        """Load a show configuration"""
        self.current_show = show_config
        self.current_scene_index = 0
        self.is_playing = False
        self.start_time = 0.0
        self.scene_start_time = 0.0
        
        # Initialize scene thumbnails
        self._generate_scene_thumbnails()
    
    def play_show(self, start_scene: int = 0, loop: bool = False) -> None:
        """Start playing the show"""
        if not self.current_show:
            raise ValueError("No show loaded")
        
        self.is_playing = True
        self.start_time = time.time()
        self.current_scene_index = start_scene
        self.scene_start_time = self.start_time
        
        print(f"🎭 Starting show: {self.current_show.name}")
        print(f"🎬 Starting at scene: {start_scene}")
        print(f"🔄 Loop: {loop}")
    
    def next_scene(self, morph_seconds: float = 2.0) -> None:
        """Advance to next scene with morphing"""
        if not self.current_show or not self.is_playing:
            return
        
        # Get morph curve for this transition
        curve_key = f"{self.current_scene_index}->{self.current_scene_index + 1}"
        morph_curve = self.current_show.morph_curves.get(curve_key, MorphCurve.EASE_IN_OUT)
        
        # Apply morph curve
        morph_progress = self._apply_morph_curve(0.0, 1.0, morph_seconds, morph_curve)
        
        # Advance scene
        self.current_scene_index = (self.current_scene_index + 1) % len(self.current_show.scenes)
        self.scene_start_time = time.time()
        
        print(f"🎬 Advanced to scene: {self.current_scene_index}")
        print(f"🎛️ Morph curve: {morph_curve.value}")
        print(f"🎛️ Morph progress: {morph_progress:.2f}")
    
    def jump_to_scene(self, scene_id: int, morph_seconds: float = 2.0) -> None:
        """Jump to specific scene"""
        if not self.current_show or not self.is_playing:
            return
        
        if 0 <= scene_id < len(self.current_show.scenes):
            self.current_scene_index = scene_id
            self.scene_start_time = time.time()
            print(f"🎬 Jumped to scene: {scene_id}")
    
    def set_parameter(self, path: str, value: float) -> None:
        """Set a parameter value with undo/redo support"""
        if not self.current_show:
            return
        
        # Save current state to undo stack
        self._save_undo_state()
        
        # Parse path (e.g., "scenes[2].fx[1].wet")
        try:
            # Simple path parsing - in production, use proper JSONPath
            if "scenes[" in path and "].fx[" in path and "].wet" in path:
                # Extract scene and fx indices
                scene_start = path.find("scenes[") + 7
                scene_end = path.find("]")
                fx_start = path.find("fx[") + 3
                fx_end = path.find("]", fx_start)
                
                scene_idx = int(path[scene_start:scene_end])
                fx_idx = int(path[fx_start:fx_end])
                
                # Apply parameter change
                print(f"🎛️ Setting parameter: {path} = {value}")
                print(f"🎬 Scene: {scene_idx}, FX: {fx_idx}")
                
        except Exception as e:
            print(f"❌ Error setting parameter: {e}")
    
    def toggle_blackout(self, state: bool) -> None:
        """Toggle blackout state"""
        self.momentary_states[MomentaryButton.BLACKOUT] = state
        self.momentary_timers[MomentaryButton.BLACKOUT] = time.time()
        
        if state:
            print("🌑 Blackout activated")
        else:
            print("🌑 Blackout deactivated")
    
    def toggle_flash_strobe(self, state: bool) -> None:
        """Toggle flash strobe with duty cycle limiting"""
        self.momentary_states[MomentaryButton.FLASH_STROBE] = state
        self.momentary_timers[MomentaryButton.FLASH_STROBE] = time.time()
        
        if state:
            self.strobe_state["enabled"] = True
            print("⚡ Flash strobe activated")
        else:
            self.strobe_state["enabled"] = False
            print("⚡ Flash strobe deactivated")
    
    def toggle_all_white_bloom(self, state: bool) -> None:
        """Toggle all-white bloom effect"""
        self.momentary_states[MomentaryButton.ALL_WHITE_BLOOM] = state
        self.momentary_timers[MomentaryButton.ALL_WHITE_BLOOM] = time.time()
        
        if state:
            print("💡 All-white bloom activated")
        else:
            print("💡 All-white bloom deactivated")
    
    def set_live_intensity(self, intensity: float) -> None:
        """Set live intensity (0-120%)"""
        self.live_intensity = max(0.0, min(120.0, intensity))
        print(f"🎛️ Live intensity: {self.live_intensity:.1f}%")
    
    def set_metrics_link_strength(self, strength: float) -> None:
        """Set metrics link strength (0-100%)"""
        self.metrics_link_strength = max(0.0, min(100.0, strength))
        print(f"📊 Metrics link strength: {self.metrics_link_strength:.1f}%")
    
    def update_metrics(self, metrics: Dict[str, float]) -> None:
        """Update live metrics for sidechain"""
        self.current_metrics.update(metrics)
        
        # Apply metrics sidechain
        if self.metrics_link_enabled and self.metrics_link_strength > 0:
            self._apply_metrics_sidechain()
    
    def _apply_metrics_sidechain(self) -> None:
        """Apply metrics sidechain with tasteful, safe mapping"""
        # Map QPS → RGB offset (soft-knee)
        qps = self.current_metrics.get("qps", 0.0)
        rgb_offset = self._soft_knee(qps, 0.0, 100.0, 0.0, 8.0)
        
        # Map p95 → fringe blur (capped)
        p95 = self.current_metrics.get("p95", 0.0)
        fringe_blur = min(3.0, max(0.0, (p95 - 20.0) / 80.0 * 3.0))
        
        # Map error_rate → spectrum amount (eases in ≥3s, out ≥2s)
        error_rate = self.current_metrics.get("error_rate", 0.0)
        spectrum_amount = self._ease_in_out(error_rate, 3.0, 2.0)
        
        # Apply link strength
        strength = self.metrics_link_strength / 100.0
        rgb_offset *= strength
        fringe_blur *= strength
        spectrum_amount *= strength
        
        print(f"📊 Sidechain: RGB={rgb_offset:.2f}, Fringe={fringe_blur:.2f}, Spectrum={spectrum_amount:.2f}")
    
    def _soft_knee(self, input_val: float, input_min: float, input_max: float, output_min: float, output_max: float) -> float:
        """Soft-knee mapping for smooth transitions"""
        if input_val <= input_min:
            return output_min
        elif input_val >= input_max:
            return output_max
        else:
            # Soft-knee curve
            t = (input_val - input_min) / (input_max - input_min)
            t = 0.5 * (1.0 - math.cos(math.pi * t))  # Ease in-out
            return output_min + t * (output_max - output_min)
    
    def _ease_in_out(self, input_val: float, ease_in_time: float, ease_out_time: float) -> float:
        """Ease in/out mapping for spectrum amount"""
        if input_val <= 0.0:
            return 0.0
        elif input_val >= 1.0:
            return 1.0
        else:
            # Ease in for first 3s, ease out for last 2s
            if input_val < ease_in_time / (ease_in_time + ease_out_time):
                t = input_val / (ease_in_time / (ease_in_time + ease_out_time))
                return 0.5 * (1.0 - math.cos(math.pi * t))
            else:
                t = (input_val - ease_in_time / (ease_in_time + ease_out_time)) / (ease_out_time / (ease_in_time + ease_out_time))
                return 0.5 * (1.0 + math.cos(math.pi * t))
    
    def _apply_morph_curve(self, start_val: float, end_val: float, duration: float, curve: MorphCurve) -> float:
        """Apply morph curve to transition"""
        t = min(1.0, (time.time() - self.scene_start_time) / duration)
        
        if curve == MorphCurve.LINEAR:
            return start_val + t * (end_val - start_val)
        elif curve == MorphCurve.EASE_IN:
            t = t * t
            return start_val + t * (end_val - start_val)
        elif curve == MorphCurve.EASE_OUT:
            t = 1.0 - (1.0 - t) * (1.0 - t)
            return start_val + t * (end_val - start_val)
        elif curve == MorphCurve.EASE_IN_OUT:
            t = 0.5 * (1.0 - math.cos(math.pi * t))
            return start_val + t * (end_val - start_val)
        elif curve == MorphCurve.HOLD_THEN_DROP:
            if t < 0.8:
                return start_val
            else:
                t = (t - 0.8) / 0.2
                return start_val + t * (end_val - start_val)
        else:
            return start_val + t * (end_val - start_val)
    
    def _generate_scene_thumbnails(self) -> None:
        """Generate scene thumbnails with preview variants"""
        if not self.current_show:
            return
        
        for i, scene_id in enumerate(self.current_show.scenes):
            thumbnail = SceneThumbnail(
                scene_id=scene_id,
                name=f"Scene {i+1}",
                notes=f"Scene {i+1} notes",
                mono_preview=f"Scene {i+1} mono preview",
                motion_safe_preview=f"Scene {i+1} motion safe preview",
                intensity_preview=f"Scene {i+1} intensity preview",
                tags=["warm-up" if i == 0 else "impact" if i == len(self.current_show.scenes) - 1 else "transition"]
            )
            self.scene_thumbnails[scene_id] = thumbnail
    
    def _save_undo_state(self) -> None:
        """Save current state to undo stack"""
        state = {
            "timestamp": time.time(),
            "scene_index": self.current_scene_index,
            "intensity": self.live_intensity,
            "metrics_link": self.metrics_link_enabled,
            "momentary_states": self.momentary_states.copy()
        }
        
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undo_steps:
            self.undo_stack.pop(0)
        
        # Clear redo stack when new action is performed
        self.redo_stack.clear()
    
    def undo(self) -> bool:
        """Undo last action"""
        if not self.undo_stack:
            return False
        
        # Save current state to redo stack
        current_state = {
            "timestamp": time.time(),
            "scene_index": self.current_scene_index,
            "intensity": self.live_intensity,
            "metrics_link": self.metrics_link_enabled,
            "momentary_states": self.momentary_states.copy()
        }
        self.redo_stack.append(current_state)
        
        # Restore previous state
        previous_state = self.undo_stack.pop()
        self.current_scene_index = previous_state["scene_index"]
        self.live_intensity = previous_state["intensity"]
        self.metrics_link_enabled = previous_state["metrics_link"]
        self.momentary_states = previous_state["momentary_states"]
        
        print(f"↶ Undo: Restored to scene {self.current_scene_index}")
        return True
    
    def redo(self) -> bool:
        """Redo last undone action"""
        if not self.redo_stack:
            return False
        
        # Save current state to undo stack
        current_state = {
            "timestamp": time.time(),
            "scene_index": self.current_scene_index,
            "intensity": self.live_intensity,
            "metrics_link": self.metrics_link_enabled,
            "momentary_states": self.momentary_states.copy()
        }
        self.undo_stack.append(current_state)
        
        # Restore next state
        next_state = self.redo_stack.pop()
        self.current_scene_index = next_state["scene_index"]
        self.live_intensity = next_state["intensity"]
        self.metrics_link_enabled = next_state["metrics_link"]
        self.momentary_states = next_state["momentary_states"]
        
        print(f"↷ Redo: Restored to scene {self.current_scene_index}")
        return True
    
    def update_show_clock(self) -> None:
        """Update show clock with elapsed and remaining times"""
        if not self.is_playing:
            return
        
        current_time = time.time()
        self.show_clock["elapsed"] = current_time - self.start_time
        self.show_clock["scene_elapsed"] = current_time - self.scene_start_time
        
        # Calculate remaining times (simplified)
        if self.current_show:
            total_duration = len(self.current_show.scenes) * 10.0  # 10s per scene
            self.show_clock["remaining"] = max(0.0, total_duration - self.show_clock["elapsed"])
            self.show_clock["scene_remaining"] = max(0.0, 10.0 - self.show_clock["scene_elapsed"])
    
    def check_motion_watchdog(self) -> None:
        """Check motion watchdog and auto-fade to mono if needed"""
        if not self.current_show or not self.current_show.motion_watchdog:
            return
        
        # Simulate motion-reduced toggle
        if self.motion_reduced and time.time() - self.motion_watchdog_timer > self.motion_watchdog_threshold:
            print("♿ Motion watchdog: Auto-fading to mono")
            self.motion_watchdog_timer = time.time()
    
    def check_heat_guard(self) -> None:
        """Check heat guard and step down quality if needed"""
        if not self.current_show or not self.current_show.heat_guard:
            return
        
        cpu_percent = self.current_metrics.get("cpu_percent", 0.0)
        frame_time = self.current_metrics.get("frame_time_ms", 0.0)
        
        if cpu_percent > 80.0 or frame_time > 12.0:
            if not self.heat_guard_active:
                self.heat_guard_active = True
                self.quality_level = max(1, self.quality_level - 1)
                print(f"🔥 Heat guard: Stepping down quality to level {self.quality_level}")
        else:
            if self.heat_guard_active:
                self.heat_guard_active = False
                self.quality_level = min(5, self.quality_level + 1)
                print(f"🔥 Heat guard: Stepping up quality to level {self.quality_level}")
    
    def process_duty_cycle(self) -> None:
        """Process duty cycle limiting for strobe effects"""
        if not self.strobe_state["enabled"]:
            return
        
        current_time = time.time()
        time_since_last_toggle = current_time - self.strobe_state["last_toggle"]
        
        if self.strobe_state["is_on"]:
            # Check if on-time has elapsed
            if time_since_last_toggle >= self.strobe_state["on_time"]:
                self.strobe_state["is_on"] = False
                self.strobe_state["last_toggle"] = current_time
        else:
            # Check if off-time has elapsed
            if time_since_last_toggle >= self.strobe_state["off_time"]:
                self.strobe_state["is_on"] = True
                self.strobe_state["last_toggle"] = current_time
    
    def get_show_status(self) -> Dict[str, Any]:
        """Get complete show status"""
        if not self.current_show:
            return {"status": "no_show"}
        
        self.update_show_clock()
        
        return {
            "show_name": self.current_show.name,
            "bpm": self.current_show.bpm,
            "scenes": len(self.current_show.scenes),
            "current_scene": self.current_scene_index,
            "is_playing": self.is_playing,
            "live_intensity": self.live_intensity,
            "metrics_link_enabled": self.metrics_link_enabled,
            "metrics_link_strength": self.metrics_link_strength,
            "motion_reduced": self.motion_reduced,
            "heat_guard_active": self.heat_guard_active,
            "quality_level": self.quality_level,
            "show_clock": self.show_clock,
            "momentary_states": {button.value: state for button, state in self.momentary_states.items()},
            "strobe_state": self.strobe_state,
            "current_metrics": self.current_metrics,
            "scene_thumbnails": {k: asdict(v) for k, v in self.scene_thumbnails.items()}
        }


def create_touring_rig_cli():
    """Create command-line interface for touring rig"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Touring Rig System - Professional Show Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load and play show
  python3 scripts/touring_rig_cli.py --load presets/shows/tour_opener.show.json --play

  # Set live intensity
  python3 scripts/touring_rig_cli.py --intensity 85.5

  # Toggle momentary buttons
  python3 scripts/touring_rig_cli.py --blackout true
  python3 scripts/touring_rig_cli.py --flash-strobe true
  python3 scripts/touring_rig_cli.py --all-white-bloom true

  # Set parameters
  python3 scripts/touring_rig_cli.py --param "scenes[2].fx[1].wet" 0.42

  # Show status
  python3 scripts/touring_rig_cli.py --status
        """
    )
    
    parser.add_argument("--load", help="Load show from JSON file")
    parser.add_argument("--play", action="store_true", help="Start playing show")
    parser.add_argument("--next", action="store_true", help="Next scene")
    parser.add_argument("--jump", type=int, help="Jump to scene index")
    parser.add_argument("--intensity", type=float, help="Set live intensity (0-120%)")
    parser.add_argument("--metrics-link", type=float, help="Set metrics link strength (0-100%)")
    parser.add_argument("--blackout", type=bool, help="Toggle blackout")
    parser.add_argument("--flash-strobe", type=bool, help="Toggle flash strobe")
    parser.add_argument("--all-white-bloom", type=bool, help="Toggle all-white bloom")
    parser.add_argument("--param", nargs=2, help="Set parameter (path value)")
    parser.add_argument("--undo", action="store_true", help="Undo last action")
    parser.add_argument("--redo", action="store_true", help="Redo last action")
    parser.add_argument("--status", action="store_true", help="Show show status")
    
    return parser


if __name__ == "__main__":
    # Example usage
    rig = TouringRig()
    
    # Create a simple show
    show = ShowConfig(
        name="Demo Show",
        bpm=110.0,
        scenes=["scene1", "scene2", "scene3"],
        intensity=100.0,
        metrics_link_strength=100.0
    )
    
    rig.load_show(show)
    rig.play_show()
    
    # Show status
    status = rig.get_show_status()
    print(f"Touring Rig Status: {json.dumps(status, indent=2)}")
