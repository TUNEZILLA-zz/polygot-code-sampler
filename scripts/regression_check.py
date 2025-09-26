#!/usr/bin/env python3
"""
Performance Regression Checker

Compares current benchmark results against rolling medians and alerts on regressions.
Designed to be run in CI/CD pipelines to catch performance regressions early.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from statistics import median
import os

# Import policy loader
try:
    from policy_loader import load_policy, get_regression_threshold, get_grace_period
except ImportError:
    # Fallback if policy_loader not available
    def load_policy():
        return None
    def get_regression_threshold(backend, policy):
        return 0.10
    def get_grace_period(policy):
        return 3

def load_benchmark_data(file_path: Path) -> List[Dict[str, Any]]:
    """Load benchmark data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("benchmarks.json must be a JSON array")
        return data
    except Exception as e:
        print(f"❌ Error loading benchmark data: {e}", file=sys.stderr)
        sys.exit(1)

def filter_recent_data(data: List[Dict[str, Any]], days: int = 7) -> List[Dict[str, Any]]:
    """Filter data to last N days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    filtered = []
    for record in data:
        try:
            # Parse timestamp (handle both ISO format and simple date)
            timestamp_str = record.get('timestamp', '')
            if 'T' in timestamp_str:
                record_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                record_date = datetime.fromisoformat(timestamp_str)
            
            if record_date >= cutoff_date:
                filtered.append(record)
        except (ValueError, TypeError):
            continue
    
    return filtered

def group_by_backend_test_mode(data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group data by (backend, test, mode) combination."""
    groups = {}
    
    for record in data:
        backend = record.get('backend', 'unknown')
        test = record.get('test', 'unknown')
        mode = record.get('mode', 'unknown')
        key = f"{backend}:{test}:{mode}"
        
        if key not in groups:
            groups[key] = []
        groups[key].append(record)
    
    return groups

def calculate_rolling_median(records: List[Dict[str, Any]], current_record: Dict[str, Any]) -> Optional[float]:
    """Calculate rolling median excluding the current record."""
    if len(records) < 2:
        return None
    
    # Sort by timestamp
    sorted_records = sorted(records, key=lambda x: x.get('timestamp', ''))
    
    # Get performance values (exclude current record)
    values = []
    for record in sorted_records:
        if record.get('timestamp') != current_record.get('timestamp'):
            mean_ns = record.get('mean_ns')
            if mean_ns is not None:
                values.append(mean_ns)
    
    if len(values) < 2:
        return None
    
    return median(values)

def parse_thresholds(threshold_str: str) -> Dict[str, float]:
    """Parse per-backend thresholds from string like '+12%:julia,+8%:rust,+15%:go'"""
    thresholds = {}
    if not threshold_str:
        return thresholds
    
    for part in threshold_str.split(','):
        if ':' in part:
            threshold_part, backend = part.split(':', 1)
            # Remove + and % signs, convert to decimal
            threshold_val = float(threshold_part.replace('+', '').replace('%', '')) / 100.0
            thresholds[backend.strip()] = threshold_val
    
    return thresholds

def check_regressions(data: List[Dict[str, Any]], threshold: float = 0.10, 
                     per_backend_thresholds: Dict[str, float] = None,
                     grace_period_days: int = 3) -> List[Dict[str, Any]]:
    """Check for performance regressions."""
    recent_data = filter_recent_data(data, days=7)
    groups = group_by_backend_test_mode(recent_data)
    
    regressions = []
    
    for key, records in groups.items():
        if len(records) < 2:
            continue
        
        backend, test, mode = key.split(':')
        
        # Grace period: skip if test doesn't have enough history
        if len(records) < grace_period_days:
            continue
        
        # Get the most recent record
        latest_record = max(records, key=lambda x: x.get('timestamp', ''))
        current_perf = latest_record.get('mean_ns')
        
        if current_perf is None:
            continue
        
        # Calculate rolling median
        rolling_median = calculate_rolling_median(records, latest_record)
        
        if rolling_median is None:
            continue
        
        # Use per-backend threshold or fallback to default
        backend_threshold = threshold
        if per_backend_thresholds and backend in per_backend_thresholds:
            backend_threshold = per_backend_thresholds[backend]
        
        # Check for regression
        regression_ratio = (current_perf - rolling_median) / rolling_median
        
        if regression_ratio > backend_threshold:
            regressions.append({
                'key': key,
                'current_perf': current_perf,
                'rolling_median': rolling_median,
                'regression_ratio': regression_ratio,
                'regression_pct': regression_ratio * 100,
                'record': latest_record
            })
    
    return regressions

def format_regression_report(regressions: List[Dict[str, Any]]) -> str:
    """Format regression report for display."""
    if not regressions:
        return "✅ No performance regressions detected"
    
    report = ["🚨 Performance Regressions Detected:", ""]
    
    for reg in regressions:
        backend, test, mode = reg['key'].split(':')
        report.append(f"**{backend}** ({test}, {mode}):")
        report.append(f"  Current: {reg['current_perf']:,.0f} ns")
        report.append(f"  Rolling Median: {reg['rolling_median']:,.0f} ns")
        report.append(f"  Regression: +{reg['regression_pct']:.1f}%")
        report.append(f"  Commit: {reg['record'].get('commit', 'unknown')[:7]}")
        report.append("")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Check for performance regressions")
    parser.add_argument("--input", "-i", type=Path, default=Path("site/benchmarks.json"),
                       help="Path to benchmarks.json file")
    parser.add_argument("--threshold", "-t", type=float, default=0.10,
                       help="Default regression threshold (default: 0.10 = 10%)")
    parser.add_argument("--per-backend-thresholds", type=str, default="",
                       help="Per-backend thresholds like '+12%:julia,+8%:rust,+15%:go'")
    parser.add_argument("--grace-period", type=int, default=3,
                       help="Grace period in days for new tests (default: 3)")
    parser.add_argument("--fail-on-regression", action="store_true",
                       help="Exit with non-zero code if regressions found")
    parser.add_argument("--github-comment", action="store_true",
                       help="Format output for GitHub PR comment")
    
    args = parser.parse_args()
    
    # Load data
    data = load_benchmark_data(args.input)
    
    if not data:
        print("⚠️  No benchmark data found", file=sys.stderr)
        sys.exit(0)
    
    # Parse per-backend thresholds
    per_backend_thresholds = parse_thresholds(args.per_backend_thresholds)
    
    # Check for regressions
    regressions = check_regressions(data, threshold=args.threshold, 
                                  per_backend_thresholds=per_backend_thresholds,
                                  grace_period_days=args.grace_period)
    
    # Generate report
    report = format_regression_report(regressions)
    
    if args.github_comment:
        print("## 📊 Performance Regression Check")
        print("")
        print(report)
        print("")
        print("---")
        print("*Automated performance regression detection*")
    else:
        print(report)
    
    # Exit with error code if regressions found and requested
    if regressions and args.fail_on_regression:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
