#!/usr/bin/env python3
"""
Best-of-k Benchmarking

Runs each test k times and records the minimum (best) result.
Reduces noise without requiring long benchmark runs.
"""

import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any


def run_benchmark_k_times(test_func, k: int = 5) -> dict[str, Any]:
    """Run a benchmark function k times and return best result."""
    times = []

    for i in range(k):
        start_time = time.time_ns()
        try:
            result = test_func()
            end_time = time.time_ns()
            execution_time = end_time - start_time
            times.append(execution_time)
        except Exception as e:
            print(f"⚠️  Benchmark run {i+1} failed: {e}")
            continue

    if not times:
        raise RuntimeError("All benchmark runs failed")

    return {
        "mean_ns": min(times),  # Best (minimum) time
        "std_ns": statistics.stdev(times) if len(times) > 1 else 0,
        "reps": len(times),
        "k": k,
        "all_times": times,
    }


def benchmark_sum_even_squares(n: int = 1000000) -> int:
    """Benchmark: sum of even squares from 0 to n-1."""
    return sum(x * x for x in range(0, n) if x % 2 == 0)


def benchmark_dict_comprehension(n: int = 100000) -> dict[int, int]:
    """Benchmark: dictionary comprehension."""
    return {x: x * x for x in range(n) if x % 2 == 0}


def run_all_benchmarks(k: int = 5) -> list[dict[str, Any]]:
    """Run all benchmarks with best-of-k strategy."""
    results = []

    benchmarks = [
        ("sum_even_squares", benchmark_sum_even_squares, 1000000),
        ("dict_comprehension", benchmark_dict_comprehension, 100000),
    ]

    for test_name, test_func, n in benchmarks:
        print(f"🧪 Running {test_name} (k={k}, n={n})...")

        try:
            stats = run_benchmark_k_times(lambda: test_func(n), k)

            result = {
                "test": test_name,
                "n": n,
                "k": k,
                "mean_ns": stats["mean_ns"],
                "std_ns": stats["std_ns"],
                "reps": stats["reps"],
                "all_times": stats["all_times"],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "backend": "python_reference",
            }

            results.append(result)
            print(
                f"   ✅ Best time: {stats['mean_ns']:,.0f} ns (from {stats['reps']} runs)"
            )

        except Exception as e:
            print(f"   ❌ Failed: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Best-of-k benchmarking")
    parser.add_argument(
        "--k", type=int, default=5, help="Number of runs per test (default: 5)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("bench_best_of_k.json"),
        help="Output file for results",
    )

    args = parser.parse_args()

    print(f"🚀 Best-of-k Benchmarking (k={args.k})")
    print("=" * 50)

    results = run_all_benchmarks(args.k)

    # Save results
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Saved {len(results)} benchmark results to {args.output}")

    # Summary
    if results:
        best_times = [r["mean_ns"] for r in results]
        print("📊 Summary:")
        print(f"   Tests: {len(results)}")
        print(f"   Best time: {min(best_times):,.0f} ns")
        print(f"   Worst time: {max(best_times):,.0f} ns")
        print(f"   Average: {statistics.mean(best_times):,.0f} ns")


if __name__ == "__main__":
    main()
