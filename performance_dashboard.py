#!/usr/bin/env python3
"""
Performance Dashboard for Polyglot Code Sampler

This script analyzes performance trends over time and generates
insights about performance regressions and improvements.
"""

import argparse
import json
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class PerformanceDashboard:
    """Performance trend analysis and dashboard generation"""

    def __init__(self, data_dir: str = "performance_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def load_benchmark_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Load benchmark data from a JSON file"""
        try:
            with open(file_path) as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return None

    def extract_metrics(self, benchmark_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract key performance metrics from benchmark data"""
        metrics = {}

        # Parsing metrics
        parsing = benchmark_data.get("parsing", {})
        metrics["parse_time_ms"] = parsing.get("avg_parse_time_ms", 0)
        metrics["infer_time_ms"] = parsing.get("avg_infer_time_ms", 0)

        # Generation metrics
        rust_gen = benchmark_data.get("rust_generation", {})
        metrics["rust_gen_time_ms"] = rust_gen.get("avg_generation_time_ms", 0)
        metrics["rust_parallel_time_ms"] = rust_gen.get(
            "avg_parallel_generation_time_ms", 0
        )

        ts_gen = benchmark_data.get("typescript_generation", {})
        metrics["ts_gen_time_ms"] = ts_gen.get("avg_generation_time_ms", 0)

        # Execution metrics (if available)
        rust_exec = benchmark_data.get("rust_execution", {})
        if "avg_compilation_time_ms" in rust_exec:
            metrics["rust_compile_time_ms"] = rust_exec["avg_compilation_time_ms"]
            metrics["rust_exec_time_ms"] = rust_exec["avg_execution_time_ms"]

        ts_exec = benchmark_data.get("typescript_execution", {})
        if "avg_execution_time_ms" in ts_exec:
            metrics["ts_exec_time_ms"] = ts_exec["avg_execution_time_ms"]

        return metrics

    def analyze_trends(self, metrics_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(metrics_history) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 data points for trend analysis",
            }

        # Sort by timestamp
        metrics_history.sort(key=lambda x: x.get("timestamp", ""))

        trends = {}

        # Analyze each metric
        metric_names = [
            "parse_time_ms",
            "infer_time_ms",
            "rust_gen_time_ms",
            "rust_parallel_time_ms",
            "ts_gen_time_ms",
        ]

        for metric in metric_names:
            values = [
                m["metrics"].get(metric, 0)
                for m in metrics_history
                if m["metrics"].get(metric, 0) > 0
            ]

            if len(values) < 2:
                continue

            # Calculate trend
            first_half = values[: len(values) // 2]
            second_half = values[len(values) // 2 :]

            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)

            if first_avg > 0:
                change_percent = ((second_avg - first_avg) / first_avg) * 100
            else:
                change_percent = 0

            # Determine trend direction
            if abs(change_percent) < 5:
                trend_direction = "stable"
            elif change_percent > 0:
                trend_direction = "regression"
            else:
                trend_direction = "improvement"

            trends[metric] = {
                "current_avg": second_avg,
                "historical_avg": first_avg,
                "change_percent": change_percent,
                "trend": trend_direction,
                "data_points": len(values),
                "latest_value": values[-1] if values else 0,
            }

        return trends

    def detect_regressions(self, trends: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect significant performance regressions"""
        regressions = []

        for metric, data in trends.items():
            if isinstance(data, dict) and data.get("trend") == "regression":
                change_percent = data.get("change_percent", 0)
                if change_percent > 10:  # Significant regression threshold
                    regressions.append(
                        {
                            "metric": metric,
                            "change_percent": change_percent,
                            "current_avg": data.get("current_avg", 0),
                            "historical_avg": data.get("historical_avg", 0),
                            "severity": "high" if change_percent > 25 else "medium",
                        }
                    )

        return regressions

    def generate_dashboard(self, metrics_history: List[Dict[str, Any]]) -> str:
        """Generate a performance dashboard report"""
        trends = self.analyze_trends(metrics_history)
        regressions = self.detect_regressions(trends)

        dashboard = f"""# 📊 Performance Dashboard

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Data Points:** {len(metrics_history)}
**Analysis Period:** {metrics_history[0].get('timestamp', 'Unknown')} to {metrics_history[-1].get('timestamp', 'Unknown')}

## 🎯 Current Performance

"""

        # Current performance summary
        if metrics_history:
            latest = metrics_history[-1]["metrics"]
            dashboard += f"""### Latest Benchmarks
- **Parse Time:** {latest.get('parse_time_ms', 0):.3f} ms
- **Type Inference:** {latest.get('infer_time_ms', 0):.3f} ms
- **Rust Generation:** {latest.get('rust_gen_time_ms', 0):.3f} ms (seq), {latest.get('rust_parallel_time_ms', 0):.3f} ms (par)
- **TypeScript Generation:** {latest.get('ts_gen_time_ms', 0):.3f} ms

"""

        # Performance trends
        dashboard += "## 📈 Performance Trends\n\n"

        if isinstance(trends, dict) and "status" not in trends:
            for metric, data in trends.items():
                if isinstance(data, dict):
                    trend_emoji = {
                        "improvement": "📈",
                        "regression": "📉",
                        "stable": "➡️",
                    }.get(data["trend"], "❓")

                    dashboard += f"""### {metric.replace('_', ' ').title()}
- **Trend:** {trend_emoji} {data['trend'].title()}
- **Change:** {data['change_percent']:+.1f}%
- **Current:** {data['current_avg']:.3f} ms
- **Historical:** {data['historical_avg']:.3f} ms
- **Data Points:** {data['data_points']}

"""
        else:
            dashboard += f"*{trends.get('message', 'Unable to analyze trends')}*\n\n"

        # Performance regressions
        if regressions:
            dashboard += "## 🚨 Performance Regressions\n\n"
            dashboard += "**Significant performance regressions detected:**\n\n"

            for reg in regressions:
                severity_emoji = {"high": "🔴", "medium": "🟡"}.get(
                    reg["severity"], "⚪"
                )
                dashboard += f"""### {severity_emoji} {reg['metric'].replace('_', ' ').title()}
- **Severity:** {reg['severity'].title()}
- **Regression:** {reg['change_percent']:+.1f}%
- **Current:** {reg['current_avg']:.3f} ms
- **Historical:** {reg['historical_avg']:.3f} ms

"""
        else:
            dashboard += "## ✅ No Significant Regressions\n\n"
            dashboard += "No significant performance regressions detected in the analyzed period.\n\n"

        # Recommendations
        dashboard += "## 💡 Recommendations\n\n"

        if regressions:
            dashboard += "### Performance Issues\n"
            for reg in regressions:
                if reg["severity"] == "high":
                    dashboard += f"- **{reg['metric']}**: Investigate recent changes that may have caused this {reg['change_percent']:.1f}% regression\n"
            dashboard += "\n"

        dashboard += """### General Recommendations
1. **Monitor Trends**: Continue tracking performance metrics over time
2. **Regression Testing**: Add performance regression tests for critical paths
3. **Optimization**: Focus on areas showing consistent regressions
4. **Documentation**: Document performance characteristics of major changes

---
*Dashboard generated by Polyglot Code Sampler Performance Dashboard*
"""

        return dashboard

    def save_dashboard(
        self, dashboard: str, filename: str = "performance_dashboard.md"
    ):
        """Save dashboard to file"""
        output_file = self.data_dir / filename
        output_file.write_text(dashboard)
        print(f"📊 Dashboard saved to {output_file}")

    def run_analysis(self, benchmark_files: List[str]) -> str:
        """Run complete performance analysis"""
        print("🔍 Loading benchmark data...")

        metrics_history = []
        for file_path in benchmark_files:
            data = self.load_benchmark_data(file_path)
            if data:
                metrics = self.extract_metrics(data)
                metrics_history.append(
                    {
                        "timestamp": data.get("timestamp", ""),
                        "commit_sha": data.get("commit_sha", ""),
                        "metrics": metrics,
                    }
                )

        if not metrics_history:
            return "❌ No valid benchmark data found"

        print(f"📈 Analyzing {len(metrics_history)} data points...")

        dashboard = self.generate_dashboard(metrics_history)
        self.save_dashboard(dashboard)

        return dashboard


def main():
    """Main dashboard runner"""
    parser = argparse.ArgumentParser(
        description="Performance Dashboard for Polyglot Code Sampler"
    )
    parser.add_argument(
        "--files", "-f", nargs="+", help="Benchmark JSON files to analyze"
    )
    parser.add_argument(
        "--data-dir",
        "-d",
        default="performance_data",
        help="Directory for performance data",
    )
    parser.add_argument("--output", "-o", help="Output dashboard file")
    parser.add_argument(
        "--print", action="store_true", help="Print dashboard to stdout"
    )

    args = parser.parse_args()

    dashboard = PerformanceDashboard(args.data_dir)

    # Default to current benchmark results if no files specified
    benchmark_files = args.files or ["benchmark_results.json"]

    result = dashboard.run_analysis(benchmark_files)

    if args.print:
        print(result)
    elif args.output:
        Path(args.output).write_text(result)
        print(f"📊 Dashboard saved to {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
