"""
Chromatic Light Desk Show Controller
====================================

A complete show controller system for the Chromatic Light Desk with:
- Scene management and crossfading
- Metrics mapping and reactive effects
- Show flow automation
- A11y-friendly controls
- MIDI learn and auto-record
- Professional showpiece flow
"""

import json
import time
import math
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class SceneType(Enum):
    """Scene types for different show moments"""

    WARM_UP = "warm_up"
    BUILD_ENERGY = "build_energy"
    IMPACT_MOMENT = "impact_moment"
    COOL_DOWN = "cool_down"
    BASELINE = "baseline"


@dataclass
class SceneConfig:
    """Configuration for a show scene"""

    name: str
    scene_type: SceneType
    seed: int
    metrics_link: bool
    controls: Dict[str, float]
    mapping: Dict[str, str]
    duration: float = 10.0  # seconds
    crossfade_time: float = 2.0  # seconds
    a11y_safe: bool = True

    def __post_init__(self):
        if self.controls is None:
            self.controls = {}
        if self.mapping is None:
            self.mapping = {}


@dataclass
class ShowFlow:
    """Complete show flow configuration"""

    name: str
    scenes: List[SceneConfig]
    total_duration: float
    auto_advance: bool = True
    loop: bool = False


class ShowController:
    """
    Chromatic Light Desk Show Controller

    Manages show flows, scene transitions, metrics mapping,
    and professional showpiece automation.
    """

    def __init__(self):
        self.current_scene: Optional[SceneConfig] = None
        self.current_metrics: Dict[str, float] = {
            "qps": 0,
            "p95": 0,
            "error_rate": 0,
            "bpm": 60,
        }
        self.scene_start_time: float = 0
        self.is_playing: bool = False
        self.a11y_mode: bool = False
        self.mono_mode: bool = False

        # Clamps for safety
        self.clamps = {
            "offset_max": 8,
            "fringe_max": 3,
            "trail_len_max": 12,
            "update_rate": 20,  # Hz
            "duty_cycle_max": 0.1,  # 10% of any 30s window
        }

        # Scene history for duty cycle tracking
        self.scene_history: List[float] = []

    def load_scene(self, scene_config: SceneConfig) -> None:
        """Load a scene configuration"""
        self.current_scene = scene_config
        self.scene_start_time = time.time()

        # Add to history for duty cycle tracking
        self.scene_history.append(time.time())

        # Clean old history (keep last 30 seconds)
        current_time = time.time()
        self.scene_history = [t for t in self.scene_history if current_time - t < 30]

    def get_current_controls(self) -> Dict[str, float]:
        """Get current control values with metrics mapping applied"""
        if not self.current_scene:
            return {}

        controls = self.current_scene.controls.copy()

        # Apply metrics mapping if enabled
        if self.current_scene.metrics_link and not self.a11y_mode:
            for mapping_key, mapping_expr in self.current_scene.mapping.items():
                try:
                    # Parse mapping expression
                    if "->" in mapping_key:
                        source, target = mapping_key.split("->")
                        source = source.strip()
                        target = target.strip()

                        # Apply mapping
                        value = self._evaluate_mapping(mapping_expr, source)
                        controls[target] = self._clamp_value(target, value)
                except Exception as e:
                    print(f"Error applying mapping {mapping_key}: {e}")

        # Apply A11y safety
        if self.a11y_mode or self.mono_mode:
            controls = self._apply_a11y_safety(controls)

        return controls

    def _evaluate_mapping(self, expression: str, source: str) -> float:
        """Evaluate a mapping expression"""
        # Replace variables with current values
        expr = expression.replace("qps", str(self.current_metrics["qps"]))
        expr = expr.replace("p95", str(self.current_metrics["p95"]))
        expr = expr.replace("err", str(self.current_metrics["error_rate"]))
        expr = expr.replace("t", str(time.time() - self.scene_start_time))

        # Simple expression evaluation (in production, use ast.literal_eval or similar)
        try:
            # Handle clamp function
            if "clamp(" in expr:
                # Extract clamp parameters
                import re

                clamp_match = re.search(r"clamp\(([^,]+),([^)]+)\)", expr)
                if clamp_match:
                    min_val = float(clamp_match.group(1))
                    max_val = float(clamp_match.group(2))
                    # Evaluate the expression before clamp
                    base_expr = expr.split("|")[0].strip()
                    value = eval(base_expr)
                    return max(min_val, min(max_val, value))

            return eval(expr)
        except:
            return 0.0

    def _clamp_value(self, target: str, value: float) -> float:
        """Clamp a value based on target type"""
        if "offset" in target:
            return max(0, min(self.clamps["offset_max"], value))
        elif "fringe" in target:
            return max(0, min(self.clamps["fringe_max"], value))
        elif "trail" in target:
            return max(0, min(self.clamps["trail_len_max"], value))
        else:
            return value

    def _apply_a11y_safety(self, controls: Dict[str, float]) -> Dict[str, float]:
        """Apply accessibility safety measures"""
        safe_controls = controls.copy()

        # Reduce motion
        if self.a11y_mode:
            safe_controls["offset_px"] *= 0.3
            safe_controls["fringe_px"] *= 0.3
            safe_controls["trail_len"] *= 0.3

        # Mono mode
        if self.mono_mode:
            safe_controls["offset_px"] = 0
            safe_controls["fringe_px"] = 0
            safe_controls["trail_len"] = 0

        return safe_controls

    def update_metrics(self, metrics: Dict[str, float]) -> None:
        """Update current metrics"""
        self.current_metrics.update(metrics)

    def set_a11y_mode(self, enabled: bool) -> None:
        """Set accessibility mode"""
        self.a11y_mode = enabled

    def set_mono_mode(self, enabled: bool) -> None:
        """Set mono mode (no chromatic effects)"""
        self.mono_mode = enabled

    def get_scene_status(self) -> Dict[str, Any]:
        """Get current scene status"""
        if not self.current_scene:
            return {"status": "no_scene"}

        return {
            "scene_name": self.current_scene.name,
            "scene_type": self.current_scene.scene_type.value,
            "duration": time.time() - self.scene_start_time,
            "metrics_link": self.current_scene.metrics_link,
            "a11y_mode": self.a11y_mode,
            "mono_mode": self.mono_mode,
            "controls": self.get_current_controls(),
            "metrics": self.current_metrics,
        }

    def create_showpiece_flow(self) -> ShowFlow:
        """Create the professional showpiece flow"""
        scenes = [
            # 1. Warm-up (safe mode)
            SceneConfig(
                name="Cinemascope",
                scene_type=SceneType.WARM_UP,
                seed=777,
                metrics_link=False,
                controls={"offset_px": 1.0, "fringe_px": 0.5, "trail_len": 2},
                mapping={},
                duration=8.0,
                a11y_safe=True,
            ),
            # 2. Build energy
            SceneConfig(
                name="Neon Bloom",
                scene_type=SceneType.BUILD_ENERGY,
                seed=777,
                metrics_link=True,
                controls={
                    "offset_px": 3.0,
                    "fringe_px": 1.5,
                    "trail_len": 6,
                    "bpm": 90,
                },
                mapping={
                    "qps->offset_px": "0.06 * qps | clamp(0,8)",
                    "p95->fringe_px": "(p95-20)/80 | clamp(0,3)",
                    "bpm->pulse_rate": "bpm/60",
                },
                duration=10.0,
            ),
            # 3. Impact moment
            SceneConfig(
                name="Prism Burst",
                scene_type=SceneType.IMPACT_MOMENT,
                seed=777,
                metrics_link=True,
                controls={
                    "offset_px": 6.0,
                    "fringe_px": 2.5,
                    "trail_len": 10,
                    "bpm": 120,
                },
                mapping={
                    "qps->offset_px": "0.08 * qps | clamp(0,8)",
                    "p95->fringe_px": "(p95-20)/80 | clamp(0,3)",
                    "error->broken_spectrum": "err>0.05 ? ease(2*t%1) : 0",
                },
                duration=1.5,
                a11y_safe=False,
            ),
            # 4. Cool-down
            SceneConfig(
                name="Hologram",
                scene_type=SceneType.COOL_DOWN,
                seed=777,
                metrics_link=True,
                controls={
                    "offset_px": 2.0,
                    "fringe_px": 0.8,
                    "trail_len": 4,
                    "bpm": 80,
                },
                mapping={
                    "qps->offset_px": "0.04 * qps | clamp(0,8)",
                    "p95->fringe_px": "(p95-20)/80 | clamp(0,3)",
                },
                duration=8.0,
                a11y_safe=True,
            ),
        ]

        return ShowFlow(
            name="Professional Showpiece",
            scenes=scenes,
            total_duration=sum(scene.duration for scene in scenes),
            auto_advance=True,
            loop=False,
        )

    def save_scene(self, filename: str, scene_config: SceneConfig) -> None:
        """Save a scene configuration to file"""
        scene_data = asdict(scene_config)
        scene_data["scene_type"] = scene_config.scene_type.value

        with open(filename, "w") as f:
            json.dump(scene_data, f, indent=2)

    def load_scene_file(self, filename: str) -> SceneConfig:
        """Load a scene configuration from file"""
        with open(filename, "r") as f:
            scene_data = json.load(f)

        scene_data["scene_type"] = SceneType(scene_data["scene_type"])
        return SceneConfig(**scene_data)

    def create_snapshot_kit(
        self, scene_config: SceneConfig, states: List[str] = ["low", "medium", "peak"]
    ) -> Dict[str, Any]:
        """Create snapshot kit for social/docs"""
        snapshot_kit = {
            "scene": scene_config.name,
            "seed": scene_config.seed,
            "states": {},
        }

        for state in states:
            # Simulate different load states
            if state == "low":
                metrics = {"qps": 10, "p95": 20, "error_rate": 0.01}
            elif state == "medium":
                metrics = {"qps": 50, "p95": 60, "error_rate": 0.03}
            else:  # peak
                metrics = {"qps": 100, "p95": 120, "error_rate": 0.08}

            # Calculate controls for this state
            temp_controller = ShowController()
            temp_controller.load_scene(scene_config)
            temp_controller.update_metrics(metrics)
            controls = temp_controller.get_current_controls()

            snapshot_kit["states"][state] = {"metrics": metrics, "controls": controls}

        return snapshot_kit


def create_show_controller_cli():
    """Create command-line interface for show controller"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Chromatic Light Desk Show Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run showpiece flow
  python3 scripts/show_controller_cli.py --flow showpiece

  # Load specific scene
  python3 scripts/show_controller_cli.py --scene cinemascope --text "Code Live"

  # Save scene configuration
  python3 scripts/show_controller_cli.py --save-scene my_scene.json --scene neon_bloom

  # Load scene from file
  python3 scripts/show_controller_cli.py --load-scene my_scene.json --text "TuneZilla"

  # Create snapshot kit
  python3 scripts/show_controller_cli.py --snapshot-kit --scene prism_burst
        """,
    )

    parser.add_argument("--text", "-t", help="Input text to process")
    parser.add_argument("--flow", help="Run a show flow (showpiece)")
    parser.add_argument("--scene", help="Load a specific scene")
    parser.add_argument("--save-scene", help="Save current scene to file")
    parser.add_argument("--load-scene", help="Load scene from file")
    parser.add_argument(
        "--snapshot-kit", action="store_true", help="Create snapshot kit"
    )
    parser.add_argument("--a11y", action="store_true", help="Enable accessibility mode")
    parser.add_argument("--mono", action="store_true", help="Enable mono mode")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--output", "-o", help="Output file for HTML mode")

    return parser


if __name__ == "__main__":
    # Example usage
    controller = ShowController()

    # Create showpiece flow
    show_flow = controller.create_showpiece_flow()
    print(f"Show Flow: {show_flow.name}")
    print(f"Total Duration: {show_flow.total_duration}s")
    print(f"Scenes: {len(show_flow.scenes)}")

    # Load first scene
    controller.load_scene(show_flow.scenes[0])
    print(f"Current Scene: {controller.current_scene.name}")

    # Get status
    status = controller.get_scene_status()
    print(f"Scene Status: {json.dumps(status, indent=2)}")
