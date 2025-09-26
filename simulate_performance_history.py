#!/usr/bin/env python3
"""
Simulate performance history for testing the performance dashboard

This script creates multiple benchmark results with simulated
performance variations to test trend analysis capabilities.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path


def create_simulated_benchmark(timestamp: str, base_metrics: dict, variation: float = 0.1) -> dict:
    """Create a simulated benchmark result with some variation"""

    def add_variation(value: float, variation: float) -> float:
        """Add random variation to a metric value"""
        if value == 0:
            return 0
        variation_amount = value * variation * (random.random() - 0.5) * 2
        return max(0, value + variation_amount)

    # Create variations of the base metrics
    simulated_metrics = {}
    for key, value in base_metrics.items():
        simulated_metrics[key] = add_variation(value, variation)

    return {
        "timestamp": timestamp,
        "mode": "quick",
        "parsing": {
            "total_cases": 2,
            "avg_parse_time_ms": simulated_metrics.get('parse_time_ms', 0.12),
            "avg_infer_time_ms": simulated_metrics.get('infer_time_ms', 0.07),
            "parse_times": [
                {
                    "case": "simple_squares",
                    "time_ms": simulated_metrics.get('parse_time_ms', 0.12) * 1.2,
                    "memory_mb": 0.05
                },
                {
                    "case": "dict_odds",
                    "time_ms": simulated_metrics.get('parse_time_ms', 0.12) * 0.8,
                    "memory_mb": 0.0
                }
            ],
            "type_inference_times": [
                {
                    "case": "simple_squares",
                    "time_ms": simulated_metrics.get('infer_time_ms', 0.07) * 1.1,
                    "memory_mb": 0.0
                },
                {
                    "case": "dict_odds",
                    "time_ms": simulated_metrics.get('infer_time_ms', 0.07) * 0.9,
                    "memory_mb": 0.0
                }
            ]
        },
        "rust_generation": {
            "total_cases": 2,
            "avg_generation_time_ms": simulated_metrics.get('rust_gen_time_ms', 0.062),
            "avg_parallel_generation_time_ms": simulated_metrics.get('rust_parallel_time_ms', 0.008),
            "generation_times": [
                {
                    "case": "simple_squares",
                    "time_ms": simulated_metrics.get('rust_gen_time_ms', 0.062) * 1.5,
                    "code_size_chars": 154
                },
                {
                    "case": "dict_odds",
                    "time_ms": simulated_metrics.get('rust_gen_time_ms', 0.062) * 0.5,
                    "code_size_chars": 223
                }
            ],
            "parallel_generation_times": [
                {
                    "case": "simple_squares",
                    "time_ms": simulated_metrics.get('rust_parallel_time_ms', 0.008) * 1.2,
                    "code_size_chars": 154
                },
                {
                    "case": "dict_odds",
                    "time_ms": simulated_metrics.get('rust_parallel_time_ms', 0.008) * 0.8,
                    "code_size_chars": 223
                }
            ]
        },
        "typescript_generation": {
            "total_cases": 2,
            "avg_generation_time_ms": simulated_metrics.get('ts_gen_time_ms', 0.008),
            "generation_times": [
                {
                    "case": "simple_squares",
                    "time_ms": simulated_metrics.get('ts_gen_time_ms', 0.008) * 0.8,
                    "code_size_chars": 192
                },
                {
                    "case": "dict_odds",
                    "time_ms": simulated_metrics.get('ts_gen_time_ms', 0.008) * 1.2,
                    "code_size_chars": 233
                }
            ]
        }
    }


def main():
    """Generate simulated performance history"""

    # Base metrics from our actual benchmark
    base_metrics = {
        'parse_time_ms': 0.120,
        'infer_time_ms': 0.070,
        'rust_gen_time_ms': 0.062,
        'rust_parallel_time_ms': 0.008,
        'ts_gen_time_ms': 0.008
    }

    # Create performance data directory
    data_dir = Path("performance_data")
    data_dir.mkdir(exist_ok=True)

    # Generate 10 days of simulated data
    print("🎭 Generating simulated performance history...")

    for i in range(10):
        # Create timestamp for each day
        date = datetime.now() - timedelta(days=9-i)
        timestamp = date.strftime("%Y-%m-%d %H:%M:%S")

        # Simulate some performance trends
        if i < 3:
            # Early days - slightly worse performance
            variation = 0.15
            trend_multiplier = 1.1
        elif i < 7:
            # Middle period - stable performance
            variation = 0.1
            trend_multiplier = 1.0
        else:
            # Recent days - improved performance
            variation = 0.08
            trend_multiplier = 0.9

        # Apply trend to base metrics
        trended_metrics = {}
        for key, value in base_metrics.items():
            trended_metrics[key] = value * trend_multiplier

        # Create simulated benchmark
        benchmark_data = create_simulated_benchmark(timestamp, trended_metrics, variation)

        # Save to file
        filename = data_dir / f"benchmark_history_{i:02d}.json"
        with open(filename, 'w') as f:
            json.dump(benchmark_data, f, indent=2)

        print(f"  📅 {timestamp}: Generated {filename}")

    print(f"\n✅ Generated {10} simulated benchmark files in {data_dir}/")
    print("\n🔍 Now you can test the performance dashboard:")
    print("   python3 performance_dashboard.py --files performance_data/benchmark_history_*.json --print")


if __name__ == "__main__":
    main()
