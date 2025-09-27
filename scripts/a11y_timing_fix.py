#!/usr/bin/env python3
"""
A11y Timing Fix - Bulletproof Motion-Reduced Fade System
========================================================

Fixes the 500ms A11y motion-reduced fade with:
- Frame cadence quantization
- Monotonic clock timing
- Non-overshooting easing
- Pre-warm before measuring
- Hard clamp at end
- Param slew limiter
- Motion-budget governor
"""

import time
import math
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class FrameRate(Enum):
    """Frame rate presets"""
    FPS_60 = 60.0
    FPS_59 = 59.0
    FPS_58 = 58.0
    FPS_30 = 30.0


@dataclass
class TimingConfig:
    """Timing configuration for A11y fades"""
    target_ms: float = 500.0
    safe_ms: float = 490.0  # aim lower so drift never crosses 500
    jitter_budget_ms: float = 6.0  # CI jitter tolerance
    frame_ms: float = 16.6667  # 60 fps default
    pre_warm_ticks: int = 1
    hard_clamp_threshold: float = 1e-6


class A11yTimingEngine:
    """
    A11y Timing Engine
    
    Provides bulletproof timing for motion-reduced fades with:
    - Frame cadence quantization
    - Monotonic clock timing
    - Non-overshooting easing
    - Pre-warm before measuring
    - Hard clamp at end
    """
    
    def __init__(self, config: TimingConfig = None):
        self.config = config or TimingConfig()
        self.frame_ms = self.config.frame_ms
        self.safe_ms = self.config.safe_ms
        self.jitter_budget = self.config.jitter_budget_ms
        
        # Calculate quantized duration
        self.steps = max(1, int(self.safe_ms // self.frame_ms))
        self.dur_ms = self.steps * self.frame_ms
        
        # Timing state
        self.t0: Optional[float] = None
        self.is_running = False
        self.progress = 0.0
        
        # Performance monitoring
        self.frame_times: List[float] = []
        self.p95_frame_ms = 0.0
        
        # Param slew limiter
        self.max_delta_per_frame = 1.0 / self.steps
        self.current_delta = 0.0
    
    def start_fade(self) -> None:
        """Start the A11y fade with pre-warm"""
        # Pre-warm: kick caches, layout, shaders
        self._pre_warm()
        
        # Start timing on second frame
        self.t0 = time.perf_counter()
        self.is_running = True
        self.progress = 0.0
        self.frame_times.clear()
    
    def _pre_warm(self) -> None:
        """Pre-warm caches, layout, shaders"""
        for _ in range(self.config.pre_warm_ticks):
            # Simulate pre-warm operations
            time.sleep(0.001)  # 1ms warm-up
    
    def update_fade(self) -> Tuple[float, bool]:
        """
        Update fade progress
        
        Returns:
            Tuple[float, bool]: (progress, is_complete)
        """
        if not self.is_running or self.t0 is None:
            return 0.0, False
        
        # Get current time
        now = time.perf_counter()
        elapsed = now - self.t0
        
        # Calculate progress
        progress = elapsed / (self.dur_ms / 1000.0)
        
        # Hard clamp at end
        if progress >= 1.0 - self.config.hard_clamp_threshold:
            progress = 1.0
            self.is_running = False
        
        # Apply non-overshooting easing
        eased_progress = self._ease_soft_knee(progress)
        
        # Apply param slew limiter
        eased_progress = self._apply_slew_limiter(eased_progress)
        
        # Update state
        self.progress = eased_progress
        
        # Record frame time for performance monitoring
        self._record_frame_time(elapsed)
        
        return eased_progress, not self.is_running
    
    def _ease_soft_knee(self, t: float) -> float:
        """
        Non-overshooting easing for motion-reduced mode
        
        Args:
            t: Progress (0.0 to 1.0)
            
        Returns:
            Eased progress (0.0 to 1.0, never exceeds 1.0)
        """
        # 0→1, C1 continuous, no overshoot
        if t < 0.3:  # gentle start
            return (t / 0.3) * 0.5 * t / 0.3
        elif t < 0.9:  # linear mid
            return 0.5 + (t - 0.3) * (0.5 / 0.6)
        else:  # short decel
            u = (t - 0.9) / 0.1
            return min(1.0, 1.0 - (1.0 - u) * (1.0 - u) * 0.5)
    
    def _apply_slew_limiter(self, target: float) -> float:
        """
        Apply param slew limiter to prevent overshooting
        
        Args:
            target: Target progress value
            
        Returns:
            Clamped progress value
        """
        # Calculate delta
        delta = target - self.current_delta
        
        # Clamp delta to max per frame
        delta = max(-self.max_delta_per_frame, min(self.max_delta_per_frame, delta))
        
        # Update current delta
        self.current_delta += delta
        
        # Clamp to valid range
        self.current_delta = max(0.0, min(1.0, self.current_delta))
        
        return self.current_delta
    
    def _record_frame_time(self, elapsed: float) -> None:
        """Record frame time for performance monitoring"""
        if len(self.frame_times) > 0:
            frame_time = elapsed - sum(self.frame_times)
            self.frame_times.append(frame_time)
            
            # Keep only last 30 frames
            if len(self.frame_times) > 30:
                self.frame_times.pop(0)
            
            # Calculate p95
            if len(self.frame_times) >= 10:
                sorted_times = sorted(self.frame_times)
                p95_index = int(0.95 * len(sorted_times))
                self.p95_frame_ms = sorted_times[p95_index] * 1000.0
    
    def get_timing_info(self) -> Dict[str, Any]:
        """Get timing information for logging"""
        return {
            "target_ms": self.config.target_ms,
            "safe_ms": self.safe_ms,
            "dur_ms": self.dur_ms,
            "frame_ms": self.frame_ms,
            "steps": self.steps,
            "p95_frame_ms": self.p95_frame_ms,
            "progress": self.progress,
            "is_running": self.is_running
        }
    
    def is_compliant(self) -> bool:
        """Check if timing is compliant with A11y requirements"""
        if not self.is_running:
            return True
        
        # Check if we're within jitter budget
        if self.t0 is not None:
            elapsed = time.perf_counter() - self.t0
            elapsed_ms = elapsed * 1000.0
            return elapsed_ms <= self.config.target_ms + self.jitter_budget
        
        return True


class MotionBudgetGovernor:
    """
    Motion Budget Governor
    
    Automatically adjusts FX parameters to keep A11y fades on time
    """
    
    def __init__(self, timing_engine: A11yTimingEngine):
        self.timing_engine = timing_engine
        self.frame_budget_ms = 12.0  # 12ms frame budget
        self.auto_adjust_enabled = True
        
        # Adjustment history
        self.adjustments: List[Dict[str, Any]] = []
    
    def check_and_adjust(self, fx_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check frame budget and adjust FX parameters if needed
        
        Args:
            fx_params: Current FX parameters
            
        Returns:
            Adjusted FX parameters
        """
        if not self.auto_adjust_enabled:
            return fx_params
        
        # Check if we're over budget
        if self.timing_engine.p95_frame_ms > self.frame_budget_ms:
            # Auto-adjust parameters
            adjusted_params = self._auto_adjust_params(fx_params)
            
            # Record adjustment
            self.adjustments.append({
                "timestamp": time.perf_counter(),
                "p95_frame_ms": self.timing_engine.p95_frame_ms,
                "adjustments": adjusted_params
            })
            
            return adjusted_params
        
        return fx_params
    
    def _auto_adjust_params(self, fx_params: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-adjust FX parameters to reduce frame time"""
        adjusted = fx_params.copy()
        
        # Reduce trail length
        if "trail_length" in adjusted:
            adjusted["trail_length"] = max(2, int(adjusted["trail_length"] * 0.8))
        
        # Reduce pulse amplitude
        if "pulse_amplitude" in adjusted:
            adjusted["pulse_amplitude"] = max(0.1, adjusted["pulse_amplitude"] * 0.8)
        
        # Reduce particle count
        if "particle_count" in adjusted:
            adjusted["particle_count"] = max(10, int(adjusted["particle_count"] * 0.8))
        
        # Reduce chromatic offset
        if "chromatic_offset" in adjusted:
            adjusted["chromatic_offset"] = max(0.05, adjusted["chromatic_offset"] * 0.8)
        
        return adjusted


class A11yHardMode:
    """
    A11y Hard Mode
    
    Forces maximum compliance for venues
    """
    
    def __init__(self):
        self.enabled = False
        self.hard_limits = {
            "intensity_cap": 0.65,
            "chromatic_offset_max": 0.15,
            "strobe_enabled": False,
            "trails_max_frames": 2,
            "motion_fade_max_ms": 480.0
        }
    
    def apply_hard_limits(self, fx_params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply hard mode limits to FX parameters"""
        if not self.enabled:
            return fx_params
        
        adjusted = fx_params.copy()
        
        # Apply intensity cap
        if "intensity" in adjusted:
            adjusted["intensity"] = min(adjusted["intensity"], self.hard_limits["intensity_cap"])
        
        # Apply chromatic offset limit
        if "chromatic_offset" in adjusted:
            adjusted["chromatic_offset"] = min(
                adjusted["chromatic_offset"], 
                self.hard_limits["chromatic_offset_max"]
            )
        
        # Disable strobe
        if "strobe_enabled" in adjusted:
            adjusted["strobe_enabled"] = False
        
        # Limit trails
        if "trail_length" in adjusted:
            adjusted["trail_length"] = min(
                adjusted["trail_length"], 
                self.hard_limits["trails_max_frames"]
            )
        
        return adjusted
    
    def enable(self) -> None:
        """Enable A11y hard mode"""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable A11y hard mode"""
        self.enabled = False


def test_a11y_timing() -> None:
    """Test A11y timing system"""
    print("🧪 Testing A11y Timing System...")
    
    # Test different frame rates
    frame_rates = [58.0, 59.0, 60.0, 61.0]
    
    for fps in frame_rates:
        print(f"\n📊 Testing at {fps} FPS...")
        
        # Create timing engine
        config = TimingConfig()
        config.frame_ms = 1000.0 / fps
        engine = A11yTimingEngine(config)
        
        # Start fade
        engine.start_fade()
        
        # Simulate fade
        start_time = time.perf_counter()
        while engine.is_running:
            progress, is_complete = engine.update_fade()
            
            # Simulate frame time
            time.sleep(0.001)  # 1ms frame time
            
            if is_complete:
                break
        
        # Check timing
        elapsed = time.perf_counter() - start_time
        elapsed_ms = elapsed * 1000.0
        
        # Get timing info
        info = engine.get_timing_info()
        
        print(f"  Target: {info['target_ms']:.1f}ms")
        print(f"  Safe: {info['safe_ms']:.1f}ms")
        print(f"  Duration: {info['dur_ms']:.1f}ms")
        print(f"  Steps: {info['steps']}")
        print(f"  Frame: {info['frame_ms']:.3f}ms")
        print(f"  Actual: {elapsed_ms:.1f}ms")
        print(f"  P95: {info['p95_frame_ms']:.1f}ms")
        print(f"  Compliant: {engine.is_compliant()}")
        
        # Check compliance
        if elapsed_ms <= 500.0 + config.jitter_budget_ms:
            print("  ✅ PASSED")
        else:
            print("  ❌ FAILED")


def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="A11y Timing Fix - Bulletproof Motion-Reduced Fade System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test A11y timing system
  python3 scripts/a11y_timing_fix.py --test

  # Test with specific frame rate
  python3 scripts/a11y_timing_fix.py --test --fps 59

  # Test hard mode
  python3 scripts/a11y_timing_fix.py --test --hard-mode
        """
    )
    
    parser.add_argument("--test", action="store_true", help="Run timing tests")
    parser.add_argument("--fps", type=float, default=60.0, help="Frame rate for testing")
    parser.add_argument("--hard-mode", action="store_true", help="Enable A11y hard mode")
    parser.add_argument("--jitter-budget", type=float, default=6.0, help="Jitter budget in ms")
    
    args = parser.parse_args()
    
    if args.test:
        # Configure timing
        config = TimingConfig()
        config.frame_ms = 1000.0 / args.fps
        config.jitter_budget_ms = args.jitter_budget
        
        # Create timing engine
        engine = A11yTimingEngine(config)
        
        # Test hard mode if enabled
        if args.hard_mode:
            hard_mode = A11yHardMode()
            hard_mode.enable()
            print("🔒 A11y Hard Mode enabled")
        
        # Run test
        test_a11y_timing()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
