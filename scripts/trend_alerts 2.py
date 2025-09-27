#!/usr/bin/env python3
"""
Trend Alerts - Performance regression detection with GitHub PR comments
Compares today's performance vs rolling median and alerts on >10% slowdowns
"""

import json
import os
import pathlib
import statistics
import sys
from datetime import datetime, timedelta
from typing import Any, Optional

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS = ROOT / "bench" / "results"


def load_benchmark_data() -> list[dict[str, Any]]:
    """Load all benchmark results from NDJSON files"""
    all_data = []

    if not RESULTS.exists():
        print(f"❌ Results directory not found: {RESULTS}")
        return all_data

    for p in sorted(RESULTS.glob("*.ndjson")):
        try:
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        try:
                            data = json.loads(line)
                            if "error" not in data:  # Skip error results
                                all_data.append(data)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️ Error reading {p}: {e}")

    return all_data


def get_rolling_median(data: list[dict[str, Any]], days: int = 7) -> dict[str, float]:
    """Calculate rolling median performance for each backend/test/mode combination"""
    # Group by backend/test/mode
    groups = {}
    for row in data:
        key = (
            row.get("backend"),
            row.get("test"),
            row.get("mode"),
            row.get("parallel"),
        )
        if key not in groups:
            groups[key] = []
        groups[key].append(row)

    # Calculate rolling median for each group
    rolling_medians = {}
    cutoff_date = datetime.now() - timedelta(days=days)

    for key, rows in groups.items():
        # Filter to last N days
        recent_rows = []
        for row in rows:
            try:
                timestamp = datetime.fromisoformat(
                    row["timestamp"].replace("Z", "+00:00")
                )
                # Make cutoff_date timezone-aware for comparison
                cutoff_aware = cutoff_date.replace(tzinfo=timestamp.tzinfo)
                if timestamp >= cutoff_aware:
                    recent_rows.append(row["mean_ns"])
            except (ValueError, KeyError):
                continue

        if len(recent_rows) >= 3:  # Need at least 3 data points
            rolling_medians[key] = statistics.median(recent_rows)

    return rolling_medians


def detect_regressions(
    data: list[dict[str, Any]], threshold: float = 0.10
) -> list[dict[str, Any]]:
    """Detect performance regressions > threshold"""
    rolling_medians = get_rolling_median(data)
    regressions = []

    # Get today's results
    today = datetime.now().strftime("%Y-%m-%d")
    today_results = [row for row in data if row.get("timestamp", "").startswith(today)]

    for result in today_results:
        key = (
            result.get("backend"),
            result.get("test"),
            result.get("mode"),
            result.get("parallel"),
        )

        if key in rolling_medians:
            current_perf = result["mean_ns"]
            median_perf = rolling_medians[key]

            # Calculate slowdown percentage
            slowdown = (current_perf - median_perf) / median_perf

            if slowdown > threshold:
                regressions.append(
                    {
                        "backend": result.get("backend"),
                        "test": result.get("test"),
                        "mode": result.get("mode"),
                        "parallel": result.get("parallel"),
                        "current_ns": current_perf,
                        "median_ns": median_perf,
                        "slowdown_pct": slowdown * 100,
                        "commit": result.get("commit"),
                        "timestamp": result.get("timestamp"),
                    }
                )

    return regressions


def format_regression_comment(regressions: list[dict[str, Any]]) -> str:
    """Format regression alert as GitHub comment"""
    if not regressions:
        return "✅ **Performance Check**: No significant regressions detected!"

    comment = "🚨 **Performance Regression Alert**\n\n"
    comment += f"Detected {len(regressions)} performance regression(s) >10%:\n\n"

    for reg in regressions:
        comment += f"### {reg['backend']} - {reg['test']} ({reg['mode']}"
        if reg["parallel"]:
            comment += ", parallel"
        comment += ")\n"
        comment += f"- **Current**: {reg['current_ns']:,} ns\n"
        comment += f"- **7-day median**: {reg['median_ns']:,} ns\n"
        comment += f"- **Slowdown**: {reg['slowdown_pct']:.1f}%\n"
        comment += f"- **Commit**: `{reg['commit'][:8]}`\n\n"

    comment += "💡 **Recommendations**:\n"
    comment += "- Check recent changes that might affect performance\n"
    comment += "- Consider reverting if regression is significant\n"
    comment += "- Run local benchmarks to verify\n"
    comment += "- [View full dashboard](https://tunezilla-zz.github.io/polygot-code-sampler/)\n"

    return comment


def post_github_comment(comment: str, pr_number: Optional[int] = None) -> bool:
    """Post comment to GitHub PR (if in CI environment)"""
    if not pr_number and "GITHUB_EVENT_PATH" in os.environ:
        # Try to extract PR number from GitHub event
        try:
            with open(os.environ["GITHUB_EVENT_PATH"]) as f:
                event_data = json.load(f)
                pr_number = event_data.get("pull_request", {}).get("number")
        except Exception:
            pass

    if not pr_number:
        print("ℹ️ Not in PR context, skipping GitHub comment")
        return False

    # This would use GitHub API to post comment
    # For now, just print the comment
    print("📝 GitHub PR Comment:")
    print("=" * 50)
    print(comment)
    print("=" * 50)

    return True


def main():
    """Main trend alerts function"""
    print("🔍 PCS Trend Alerts - Performance Regression Detection")
    print("=" * 55)

    # Load benchmark data
    data = load_benchmark_data()
    if not data:
        print("❌ No benchmark data found")
        return 1

    print(f"📊 Loaded {len(data)} benchmark results")

    # Detect regressions
    regressions = detect_regressions(data, threshold=0.10)  # 10% threshold

    if regressions:
        print(f"🚨 Found {len(regressions)} performance regression(s)")
        for reg in regressions:
            print(
                f"   {reg['backend']} {reg['test']} ({reg['mode']}): {reg['slowdown_pct']:.1f}% slower"
            )
    else:
        print("✅ No significant regressions detected")

    # Format and post comment
    comment = format_regression_comment(regressions)

    # Try to post to GitHub PR
    pr_number = os.environ.get("PR_NUMBER")
    if pr_number:
        try:
            pr_number = int(pr_number)
        except ValueError:
            pr_number = None

    post_github_comment(comment, pr_number)

    # Exit with error code if regressions found
    if regressions:
        print("\n❌ Performance regressions detected! Exiting with code 1")
        return 1
    else:
        print("\n✅ Performance check passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
