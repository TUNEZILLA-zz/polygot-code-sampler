#!/usr/bin/env python3
"""
Micro canary benchmark for fast regression detection.
Tests one tiny IR per backend with best-of-k (k=5) and gates on +10% policy threshold.
"""

import json
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from pcs.core import IRComp, PyToIR
from pcs.renderer_api import render


def benchmark_backend(backend: str, ir: IRComp, k: int = 5) -> tuple[float, float]:
    """Benchmark a single backend with best-of-k timing."""
    times = []

    for _ in range(k):
        start = time.perf_counter()
        render(backend, ir)
        end = time.perf_counter()
        times.append(end - start)

    # Return mean and std
    mean_time = sum(times) / len(times)
    std_time = (sum((t - mean_time) ** 2 for t in times) / len(times)) ** 0.5
    return mean_time, std_time


def load_baseline() -> dict[str, float]:
    """Load baseline performance from canary_baseline.json."""
    baseline_file = Path("bench/canary_baseline.json")
    if baseline_file.exists():
        with open(baseline_file) as f:
            return json.load(f)
    return {}


def save_baseline(results: dict[str, float]) -> None:
    """Save current results as new baseline."""
    baseline_file = Path("bench/canary_baseline.json")
    baseline_file.parent.mkdir(exist_ok=True)

    with open(baseline_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"💾 Saved baseline to {baseline_file}")


def check_regression(current: float, baseline: float, threshold: float = 0.10) -> bool:
    """Check if current performance exceeds threshold above baseline."""
    if baseline == 0:
        return False  # No baseline to compare against

    regression_ratio = (current - baseline) / baseline
    return regression_ratio > threshold


def main():
    """Run micro canary benchmark."""
    print("🚀 PCS Micro Canary Benchmark")
    print("=" * 40)

    # Simple test case
    parser = PyToIR()
    ir = parser.parse("[x**2 for x in range(1, 100)]")

    # Backends to test
    backends = ["rust", "ts", "go", "csharp", "julia", "sql"]

    # Load baseline
    baseline = load_baseline()

    # Run benchmarks
    results = {}
    regressions = []

    for backend in backends:
        print(f"🧪 Benchmarking {backend}...")
        mean_time, std_time = benchmark_backend(backend, ir)
        results[backend] = mean_time

        print(f"   Mean: {mean_time:.6f}s (±{std_time:.6f}s)")

        # Check for regression
        if backend in baseline:
            if check_regression(mean_time, baseline[backend]):
                regression_pct = (
                    (mean_time - baseline[backend]) / baseline[backend]
                ) * 100
                regressions.append(f"{backend}: +{regression_pct:.1f}%")
                print(f"   ⚠️  REGRESSION: +{regression_pct:.1f}%")
            else:
                print("   ✅ Within threshold")
        else:
            print("   📊 New baseline")

    # Summary
    print("\n📊 Canary Results Summary")
    print("=" * 30)

    if regressions:
        print("❌ Performance regressions detected:")
        for reg in regressions:
            print(f"   {reg}")

        print(f"\n🚨 Canary failed: {len(regressions)} regressions")
        return 1
    else:
        print("✅ All backends within performance threshold")

        # Update baseline if no regressions
        save_baseline(results)
        print("💾 Updated baseline with current results")
        return 0


if __name__ == "__main__":
    sys.exit(main())
