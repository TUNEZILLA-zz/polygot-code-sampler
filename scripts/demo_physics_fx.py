#!/usr/bin/env python3
"""
Code Live Physics FX - Interactive Demo
Demonstrate the physics FX system with real-time metrics simulation
"""

import math
import random
import time
from typing import Any


class PhysicsFXDemo:
    def __init__(self):
        self.running = False
        self.metrics = {
            "qps": 0,
            "p95": 0,
            "errorRate": 0,
            "fallbackRatio": 0,
            "perBackend": {
                "rust": 0.9,
                "ts": 0.8,
                "go": 0.7,
                "csharp": 0.6,
                "sql": 0.5,
                "julia": 0.4,
            },
        }

    def simulate_metrics(self, scenario: str, elapsed: float) -> dict[str, Any]:
        """Simulate realistic metrics for different scenarios"""
        base_time = time.time()

        if scenario == "load_sweep":
            # Sine wave pattern for QPS
            qps = 60 + 60 * (1 + math.sin(elapsed * 0.1)) / 2
            qps = max(0, min(120, qps))
            p95 = 40 + 10 * random.random()
            error_rate = 0.02 + 0.01 * random.random()
            fallback_ratio = 0.05 + 0.02 * random.random()

        elif scenario == "latency_spike":
            # Spike pattern for P95
            p95 = 40 + 180 * (0.5 + 0.5 * math.sin(elapsed * 0.2)) / 2
            p95 = max(40, min(220, p95))
            qps = 25 + 5 * random.random()
            error_rate = 0.05 + 0.1 * random.random()
            fallback_ratio = 0.1 + 0.05 * random.random()

        elif scenario == "error_burst":
            # Burst pattern for ErrorRate
            error_rate = 0.1 + 0.1 * (0.5 + 0.5 * math.sin(elapsed * 0.3)) / 2
            error_rate = max(0, min(0.2, error_rate))
            qps = 20 + 10 * random.random()
            p95 = 50 + 20 * random.random()
            fallback_ratio = 0.15 + 0.1 * random.random()

        elif scenario == "fallback_storm":
            # Storm pattern for FallbackRatio
            fallback_ratio = 0.1 + 0.2 * (0.5 + 0.5 * math.sin(elapsed * 0.4)) / 2
            fallback_ratio = max(0, min(0.3, fallback_ratio))
            qps = 15 + 5 * random.random()
            p95 = 60 + 30 * random.random()
            error_rate = 0.2 + 0.1 * random.random()

        else:  # chaos_mode
            # Random everything
            qps = 10 + 40 * random.random()
            p95 = 30 + 200 * random.random()
            error_rate = 0.05 + 0.4 * random.random()
            fallback_ratio = 0.1 + 0.3 * random.random()

        return {
            "qps": qps,
            "p95": p95,
            "errorRate": error_rate,
            "fallbackRatio": fallback_ratio,
            "perBackend": {
                "rust": 0.9 + 0.1 * random.random(),
                "ts": 0.8 + 0.1 * random.random(),
                "go": 0.7 + 0.1 * random.random(),
                "csharp": 0.6 + 0.1 * random.random(),
                "sql": 0.5 + 0.1 * random.random(),
                "julia": 0.4 + 0.1 * random.random(),
            },
        }

    def calculate_physics_params(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Calculate physics parameters from metrics"""
        # Particle count based on QPS
        particle_count = int(80 * metrics["qps"])

        # Damping based on P95 latency
        damping = min(0.25, metrics["p95"] / 300.0)

        # Turbulence based on error rate
        turbulence = metrics["errorRate"] * 10.0

        # Wind strength based on fallback ratio
        wind_strength = metrics["fallbackRatio"] * 5.0

        # Motion heaviness based on P95
        motion_heaviness = "HEAVY" if metrics["p95"] > 150 else "NORMAL"

        # Boids organization based on error rate
        boids_organization = (
            "DISORGANIZED" if metrics["errorRate"] > 0.15 else "ORGANIZED"
        )

        # Warning tint based on fallback ratio
        warning_tint = "ACTIVE" if metrics["fallbackRatio"] > 0.15 else "INACTIVE"

        # Legend notice based on fallback ratio
        legend_notice = "SHOWING" if metrics["fallbackRatio"] > 0.2 else "HIDDEN"

        return {
            "particle_count": particle_count,
            "damping": damping,
            "turbulence": turbulence,
            "wind_strength": wind_strength,
            "motion_heaviness": motion_heaviness,
            "boids_organization": boids_organization,
            "warning_tint": warning_tint,
            "legend_notice": legend_notice,
        }

    def run_scenario(self, scenario: str, duration: int = 20):
        """Run a specific scenario"""
        print(f"\n🎛️ Starting {scenario.replace('_', ' ').title()} scenario...")
        print("=" * 60)

        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time

            # Get metrics for this scenario
            metrics = self.simulate_metrics(scenario, elapsed)

            # Calculate physics parameters
            physics_params = self.calculate_physics_params(metrics)

            # Display current state
            print(
                f"⏱️  {elapsed:5.1f}s | "
                f"QPS: {metrics['qps']:6.1f} | "
                f"P95: {metrics['p95']:6.1f}ms | "
                f"Error: {metrics['errorRate']:5.3f} | "
                f"Fallback: {metrics['fallbackRatio']:5.3f}"
            )

            print(
                f"    🌊 Particles: {physics_params['particle_count']:4d} | "
                f"Damping: {physics_params['damping']:5.3f} | "
                f"Turbulence: {physics_params['turbulence']:4.1f} | "
                f"Wind: {physics_params['wind_strength']:4.1f}"
            )

            print(
                f"    🎭 Motion: {physics_params['motion_heaviness']:6s} | "
                f"Boids: {physics_params['boids_organization']:12s} | "
                f"Warning: {physics_params['warning_tint']:6s} | "
                f"Legend: {physics_params['legend_notice']:7s}"
            )

            print()
            time.sleep(0.5)

        print(f"✅ {scenario.replace('_', ' ').title()} scenario completed!")

    def run_all_scenarios(self):
        """Run all demo scenarios"""
        print("🎛️ CODE LIVE PHYSICS FX - INTERACTIVE DEMO")
        print("=" * 60)
        print("Demonstrating physics-driven visual effects based on real-time metrics")
        print("=" * 60)

        scenarios = [
            ("load_sweep", 15, "QPS 0→120→0 (particle birth/decay)"),
            ("latency_spike", 12, "P95 40→220ms (motion heaviness)"),
            ("error_burst", 10, "ErrorRate 0→0.2 (turbulence + opacity)"),
            ("fallback_storm", 8, "FallbackRatio > 0.15 (warning tint)"),
            ("chaos_mode", 15, "Random everything (system resilience)"),
        ]

        for scenario, duration, description in scenarios:
            print(f"\n🎯 {description}")
            self.run_scenario(scenario, duration)
            time.sleep(1)

        print("\n🎉 All scenarios completed!")
        print("🎛️ Physics FX System Status: PRODUCTION READY!")

    def interactive_mode(self):
        """Interactive mode for real-time physics FX control"""
        print("\n🎛️ INTERACTIVE PHYSICS FX MODE")
        print("=" * 40)
        print("Press Enter to update metrics, 'q' to quit")

        while True:
            user_input = input(
                "\nPress Enter to generate new metrics (or 'q' to quit): "
            )
            if user_input.lower() == "q":
                break

            # Generate random metrics
            metrics = self.simulate_metrics("chaos_mode", time.time())
            physics_params = self.calculate_physics_params(metrics)

            print("\n📊 Current Metrics:")
            print(
                f"   QPS: {metrics['qps']:6.1f} | P95: {metrics['p95']:6.1f}ms | "
                f"Error: {metrics['errorRate']:5.3f} | Fallback: {metrics['fallbackRatio']:5.3f}"
            )

            print("\n🌊 Physics Parameters:")
            print(
                f"   Particles: {physics_params['particle_count']:4d} | "
                f"Damping: {physics_params['damping']:5.3f} | "
                f"Turbulence: {physics_params['turbulence']:4.1f} | "
                f"Wind: {physics_params['wind_strength']:4.1f}"
            )

            print("\n🎭 Visual Effects:")
            print(
                f"   Motion: {physics_params['motion_heaviness']:6s} | "
                f"Boids: {physics_params['boids_organization']:12s} | "
                f"Warning: {physics_params['warning_tint']:6s} | "
                f"Legend: {physics_params['legend_notice']:7s}"
            )

        print("\n👋 Interactive mode ended!")


def main():
    """Main function"""
    demo = PhysicsFXDemo()

    print("🎛️ CODE LIVE PHYSICS FX - DEMO MODE")
    print("=" * 50)
    print("1. Run all scenarios")
    print("2. Interactive mode")
    print("3. Exit")

    while True:
        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            demo.run_all_scenarios()
            break
        elif choice == "2":
            demo.interactive_mode()
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
