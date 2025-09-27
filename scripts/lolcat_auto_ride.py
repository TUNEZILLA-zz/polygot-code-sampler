#!/usr/bin/env python3
"""
LOLcat++ Auto-Ride Macro (Sidechain Lite) - Breathe the show every 8 bars
"""
import time
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus


class LOLcatAutoRide:
    def __init__(self):
        self.bpm = 120  # Default BPM
        self.bar_duration = 60.0 / self.bpm * 4  # 4 beats per bar
        self.eight_bars_duration = self.bar_duration * 8  # 8 bars
        self.last_ride_time = 0

        # Auto-ride parameters
        self.gradient_phase_nudge = 0.05  # ±0.05
        self.uwu_nudge = 0.02  # ±0.02
        self.intensity_nudge = 0.03  # ±0.03

        # Clamps
        self.gradient_phase_min = 0.0
        self.gradient_phase_max = 1.0
        self.uwu_min = 0.0
        self.uwu_max = 1.0
        self.intensity_min = 0.1
        self.intensity_max = 1.0

        # Current parameters
        self.gradient_phase = 0.0
        self.uwu = 0.3
        self.intensity = 0.5
        self.chaos = 0.15
        self.emoji = 0.1
        self.trail = 0.2

        # Ride direction (alternates)
        self.ride_direction = 1

    def set_bpm(self, bpm):
        """Set BPM and recalculate durations"""
        self.bpm = bpm
        self.bar_duration = 60.0 / bpm * 4
        self.eight_bars_duration = self.bar_duration * 8
        print(f"😺 BPM set to {bpm}, 8 bars = {self.eight_bars_duration:.1f}s")

    def should_ride(self):
        """Check if it's time for an auto-ride"""
        current_time = time.time()
        if current_time - self.last_ride_time >= self.eight_bars_duration:
            self.last_ride_time = current_time
            return True
        return False

    def auto_ride(self):
        """Perform auto-ride nudge"""
        if not self.should_ride():
            return

        # Nudge gradient_phase
        self.gradient_phase += self.gradient_phase_nudge * self.ride_direction
        self.gradient_phase = max(
            self.gradient_phase_min, min(self.gradient_phase_max, self.gradient_phase)
        )

        # Nudge uwu
        self.uwu += self.uwu_nudge * self.ride_direction
        self.uwu = max(self.uwu_min, min(self.uwu_max, self.uwu))

        # Nudge intensity
        self.intensity += self.intensity_nudge * self.ride_direction
        self.intensity = max(
            self.intensity_min, min(self.intensity_max, self.intensity)
        )

        # Alternate direction for next ride
        self.ride_direction *= -1

        print(
            f"😺 Auto-ride: phase={self.gradient_phase:.2f}, uwu={self.uwu:.2f}, intensity={self.intensity:.2f}"
        )

    def get_current_params(self):
        """Get current parameters"""
        return {
            "intensity": self.intensity,
            "uwu": self.uwu,
            "chaos": self.chaos,
            "emoji": self.emoji,
            "nyan_trail": self.trail,
            "gradient_phase": self.gradient_phase,
        }

    def transform_text(self, text, seed=1337):
        """Transform text with current parameters"""
        params = self.get_current_params()
        return lolcat_plus(text, seed=seed, **params)

    def demo_auto_ride(self, text="Auto-Ride Demo", duration=30):
        """Demo auto-ride system"""
        print("😺 Starting LOLcat++ Auto-Ride Demo...")
        print(f"BPM: {self.bpm}, 8 bars: {self.eight_bars_duration:.1f}s")
        print("Press Ctrl+C to stop")

        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Check for auto-ride
                self.auto_ride()

                # Transform text
                result = self.transform_text(text)

                # Show status
                elapsed = time.time() - start_time
                next_ride = self.eight_bars_duration - (
                    elapsed % self.eight_bars_duration
                )
                print(
                    f"\r😺 {elapsed:.1f}s | Next ride in {next_ride:.1f}s | {result['text']}",
                    end="",
                )

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n😺 Auto-ride demo stopped")

    def test_ride_timing(self, bpm=120):
        """Test ride timing for different BPMs"""
        print("😺 Testing Auto-Ride Timing...")

        test_bpms = [60, 90, 120, 140, 160]

        for test_bpm in test_bpms:
            self.set_bpm(test_bpm)
            print(f"   BPM {test_bpm}: 8 bars = {self.eight_bars_duration:.1f}s")

    def simulate_show_breathing(self, text="Show Breathing", duration=60):
        """Simulate show breathing with auto-ride"""
        print("😺 Simulating Show Breathing...")
        print("Auto-ride will nudge parameters every 8 bars")

        try:
            start_time = time.time()
            ride_count = 0

            while time.time() - start_time < duration:
                if self.should_ride():
                    ride_count += 1
                    self.auto_ride()

                    # Show transformation
                    result = self.transform_text(text)
                    print(f"😺 Ride #{ride_count}: {result['text']}")

                time.sleep(0.1)

        except KeyboardInterrupt:
            print(f"\n😺 Show breathing stopped after {ride_count} rides")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LOLcat++ Auto-Ride Macro")
    parser.add_argument("--demo", action="store_true", help="Run auto-ride demo")
    parser.add_argument(
        "--breathing", action="store_true", help="Simulate show breathing"
    )
    parser.add_argument("--test-timing", action="store_true", help="Test ride timing")
    parser.add_argument("--bpm", type=int, default=120, help="BPM for timing")
    parser.add_argument("--text", default="Auto-ride test", help="Text to transform")
    parser.add_argument(
        "--duration", type=int, default=30, help="Demo duration in seconds"
    )

    args = parser.parse_args()

    auto_ride = LOLcatAutoRide()
    auto_ride.set_bpm(args.bpm)

    if args.demo:
        auto_ride.demo_auto_ride(args.text, args.duration)
    elif args.breathing:
        auto_ride.simulate_show_breathing(args.text, args.duration)
    elif args.test_timing:
        auto_ride.test_ride_timing()
    else:
        # Single auto-ride test
        auto_ride.auto_ride()
        result = auto_ride.transform_text(args.text)
        print(f"😺 Auto-ride result: {result['text']}")


if __name__ == "__main__":
    main()
